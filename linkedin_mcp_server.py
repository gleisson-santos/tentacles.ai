import json
import os
import tempfile
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlencode, urlparse, parse_qs

import httpx
import requests as req
from bs4 import BeautifulSoup
from mcp.server.fastmcp import FastMCP

CLIENT_ID = os.environ.get("LINKEDIN_CLIENT_ID", "")
CLIENT_SECRET = os.environ.get("LINKEDIN_CLIENT_SECRET", "")
REDIRECT_URI = os.environ.get("LINKEDIN_REDIRECT_URI", "http://localhost:3000/callback")
STABILITY_API_KEY = os.environ.get("STABILITY_API_KEY", "")
TOKEN_FILE = os.path.expanduser("~/.linkedin_mcp_token.json")

mcp = FastMCP("LinkedIn Poster")


# ── helpers ──────────────────────────────────────────────────────────────────

def _load_token() -> dict | None:
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE) as f:
            return json.load(f)
    return None


def _save_token(data: dict) -> None:
    with open(TOKEN_FILE, "w") as f:
        json.dump(data, f)


def _auth_headers(access_token: str) -> dict:
    return {
        "Authorization": "Bearer " + access_token,
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0",
    }


def _get_person_urn(access_token: str, client: httpx.Client) -> str:
    resp = client.get("https://api.linkedin.com/v2/userinfo",
                      headers=_auth_headers(access_token))
    resp.raise_for_status()
    return "urn:li:person:" + resp.json()["sub"]


# ── tools ─────────────────────────────────────────────────────────────────────

@mcp.tool()
def authenticate() -> str:
    """Abre o navegador para autenticar com o LinkedIn via OAuth2 e salva o token."""
    params = {
        "response_type": "code",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": "openid profile email w_member_social",
        "state": "linkedin_mcp_state",
    }
    auth_url = "https://www.linkedin.com/oauth/v2/authorization?" + urlencode(params)
    auth_code: list[str | None] = [None]

    class _Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            qs = parse_qs(urlparse(self.path).query)
            if "code" in qs:
                auth_code[0] = qs["code"][0]
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"<h1>Autenticado! Pode fechar esta janela.</h1>")

        def log_message(self, *_):
            pass

    webbrowser.open(auth_url)
    HTTPServer(("localhost", 3000), _Handler).handle_request()

    if not auth_code[0]:
        return "Falha: nenhum codigo de autorização recebido."

    with httpx.Client() as client:
        resp = client.post(
            "https://www.linkedin.com/oauth/v2/accessToken",
            data={
                "grant_type": "authorization_code",
                "code": auth_code[0],
                "redirect_uri": REDIRECT_URI,
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
            },
        )
        token_data = resp.json()

    if "access_token" not in token_data:
        return f"Erro ao obter token: {token_data}"

    _save_token(token_data)
    return "Autenticado com sucesso! Token salvo."


@mcp.tool()
def check_auth_status() -> str:
    """Verifica se você já está autenticado no LinkedIn."""
    token_data = _load_token()
    if not token_data:
        return "Não autenticado. Execute 'authenticate' para fazer login."
    with httpx.Client() as client:
        resp = client.get(
            "https://api.linkedin.com/v2/userinfo",
            headers={"Authorization": "Bearer " + token_data["access_token"]},
        )
    if resp.status_code == 200:
        info = resp.json()
        return f"Autenticado como: {info.get('name')} ({info.get('email')})"
    return f"Token inválido (status {resp.status_code}). Execute 'authenticate' novamente."


@mcp.tool()
def fetch_url_content(url: str) -> str:
    """
    Busca o conteúdo textual de uma URL (artigo, notícia, post).
    Retorna o texto extraído para análise e criação de post.

    Args:
        url: URL do artigo, notícia ou página a ser analisada.
    """
    try:
        with httpx.Client(follow_redirects=True, timeout=15) as client:
            resp = client.get(url, headers={"User-Agent": "Mozilla/5.0"})
            resp.raise_for_status()

        soup = BeautifulSoup(resp.text, "html.parser")

        for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
            tag.decompose()

        title = soup.title.string.strip() if soup.title else "Sem título"
        paragraphs = [p.get_text(" ", strip=True) for p in soup.find_all("p") if len(p.get_text(strip=True)) > 50]
        body = "\n\n".join(paragraphs[:30])

        return f"TÍTULO: {title}\n\nCONTEÚDO:\n{body[:8000]}"
    except Exception as e:
        return f"Erro ao buscar URL: {e}"


@mcp.tool()
def generate_image(prompt: str) -> str:
    """
    Gera uma imagem com Stability AI (Stable Image Core, $0.03/imagem).
    Retorna o caminho do arquivo gerado.

    Args:
        prompt: Descrição detalhada da imagem em inglês para melhor resultado.
    """
    if not STABILITY_API_KEY:
        return "STABILITY_API_KEY não configurada."

    try:
        response = req.post(
            "https://api.stability.ai/v2beta/stable-image/generate/core",
            headers={
                "authorization": f"Bearer {STABILITY_API_KEY}",
                "accept": "image/*",
            },
            files={"none": ""},
            data={
                "prompt": prompt,
                "output_format": "jpeg",
                "aspect_ratio": "1:1",
            },
            timeout=60,
        )

        if response.status_code != 200:
            return f"Erro Stability AI {response.status_code}: {response.text}"

        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg",
                                          dir=os.path.expanduser("~"))
        tmp.write(response.content)
        tmp.close()
        return f"Imagem gerada: {tmp.name}"
    except Exception as e:
        return f"Erro ao gerar imagem: {e}"


@mcp.tool()
def create_post(text: str, visibility: str = "PUBLIC") -> str:
    """
    Publica um post de texto no LinkedIn.

    Args:
        text: Conteúdo do post.
        visibility: 'PUBLIC' (padrão) ou 'CONNECTIONS'.
    """
    token_data = _load_token()
    if not token_data:
        return "Não autenticado. Execute 'authenticate' primeiro."

    access_token = token_data["access_token"]

    with httpx.Client() as client:
        person_urn = _get_person_urn(access_token, client)
        resp = client.post(
            "https://api.linkedin.com/v2/ugcPosts",
            headers=_auth_headers(access_token),
            json={
                "author": person_urn,
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {"text": text},
                        "shareMediaCategory": "NONE",
                    }
                },
                "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": visibility},
            },
        )

    if resp.status_code in (200, 201):
        return f"Post publicado! ID: {resp.headers.get('x-restli-id', 'N/A')}"
    return f"Erro {resp.status_code}: {resp.text}"


@mcp.tool()
def create_post_with_image(text: str, image_path: str, visibility: str = "PUBLIC") -> str:
    """
    Publica um post no LinkedIn com imagem.

    Args:
        text: Conteúdo do post.
        image_path: Caminho local da imagem (gerada pelo generate_image ou fornecida).
        visibility: 'PUBLIC' (padrão) ou 'CONNECTIONS'.
    """
    token_data = _load_token()
    if not token_data:
        return "Não autenticado. Execute 'authenticate' primeiro."

    if not os.path.exists(image_path):
        return f"Imagem não encontrada: {image_path}"

    access_token = token_data["access_token"]
    headers = _auth_headers(access_token)

    with httpx.Client() as client:
        person_urn = _get_person_urn(access_token, client)

        # 1. Registrar upload
        reg = client.post(
            "https://api.linkedin.com/v2/assets?action=registerUpload",
            headers=headers,
            json={
                "registerUploadRequest": {
                    "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
                    "owner": person_urn,
                    "serviceRelationships": [{
                        "relationshipType": "OWNER",
                        "identifier": "urn:li:userGeneratedContent",
                    }],
                }
            },
        )

        if reg.status_code != 200:
            return f"Erro ao registrar upload: {reg.status_code} - {reg.text}"

        reg_data = reg.json()
        upload_url = reg_data["value"]["uploadMechanism"][
            "com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest"
        ]["uploadUrl"]
        asset_urn = reg_data["value"]["asset"]

        # 2. Enviar imagem
        with open(image_path, "rb") as img_file:
            upload_resp = client.put(
                upload_url,
                content=img_file.read(),
                headers={"Authorization": "Bearer " + access_token,
                         "Content-Type": "image/jpeg"},
            )

        if upload_resp.status_code not in (200, 201):
            return f"Erro no upload da imagem: {upload_resp.status_code}"

        # 3. Criar post com imagem
        post_resp = client.post(
            "https://api.linkedin.com/v2/ugcPosts",
            headers=headers,
            json={
                "author": person_urn,
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {"text": text},
                        "shareMediaCategory": "IMAGE",
                        "media": [{
                            "status": "READY",
                            "description": {"text": text[:200]},
                            "media": asset_urn,
                            "title": {"text": text[:100]},
                        }],
                    }
                },
                "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": visibility},
            },
        )

    if post_resp.status_code in (200, 201):
        return f"Post com imagem publicado! ID: {post_resp.headers.get('x-restli-id', 'N/A')}"
    return f"Erro {post_resp.status_code}: {post_resp.text}"


if __name__ == "__main__":
    mcp.run()
