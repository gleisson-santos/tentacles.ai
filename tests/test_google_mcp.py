import sys
import os
import unittest
from unittest.mock import patch, MagicMock

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from mcp_servers.google_mcp import gmail_tools

class TestGmailTools(unittest.TestCase):
    
    @patch("mcp_servers.google_mcp.gmail_tools._service")
    def test_send_email_headers(self, mock_service):
        # Mock do serviço Gmail
        mock_svc = MagicMock()
        mock_service.return_value = mock_svc
        mock_svc.users().messages().send().execute.return_value = {"id": "123"}
        
        to = "test@example.com"
        subject = "Test Subject"
        body = "Test Body"
        
        result = gmail_tools.send_email(to, subject, body)
        
        # Verifica se o email foi enviado
        self.assertIn("ID: 123", result)
        
        # Verifica se as chamadas ao mock foram feitas
        args, kwargs = mock_svc.users().messages().send.call_args
        raw_msg = kwargs["body"]["raw"]
        import base64
        decoded_msg = base64.urlsafe_b64decode(raw_msg).decode()
        
        self.assertIn(f"To: {to}", decoded_msg)
        self.assertIn(f"Subject: {subject}", decoded_msg)
        # O corpo pode estar em base64 dependendo do MIME type
        import base64
        body_b64 = base64.b64encode(body.encode()).decode()
        self.assertTrue(body in decoded_msg or body_b64 in decoded_msg)

    @patch("mcp_servers.google_mcp.gmail_tools._service")
    def test_get_email_case_insensitive_headers(self, mock_service):
        # Mock do serviço Gmail
        mock_svc = MagicMock()
        mock_service.return_value = mock_svc
        
        mock_msg = {
            "payload": {
                "headers": [
                    {"name": "to", "value": "recipient@example.com"},
                    {"name": "SUBJECT", "value": "SHOUTING"},
                    {"name": "From", "value": "sender@example.com"},
                    {"name": "Date", "value": "Today"}
                ]
            },
            "snippet": "Snippet"
        }
        mock_svc.users().messages().get().execute.return_value = mock_msg
        
        with patch("mcp_servers.google_mcp.gmail_tools._decode_body", return_value="Body"):
            email = gmail_tools.get_email("123")
            
            self.assertEqual(email["to"], "recipient@example.com")
            self.assertEqual(email["subject"], "SHOUTING")
            self.assertEqual(email["from"], "sender@example.com")

if __name__ == "__main__":
    unittest.main()
