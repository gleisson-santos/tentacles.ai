"""Teste das etapas 1 e 2: notícias + Groq AI (sem publicar no LinkedIn)"""
import sys
sys.stdout.reconfigure(encoding="utf-8")

import auto_poster as ap

print("=== TESTE - Etapa 1: Buscando notícias ===")
articles = ap.fetch_news()
print(f"Artigos coletados: {len(articles)}")

print()
print("=== TESTE - Etapa 2: Gerando post com Groq AI ===")
result = ap.analyze_and_write(articles)
print(f"Tópico : {result['topic']}")
print(f"Título : {result['title'][:80]}")
print()
print("--- POST GERADO ---")
print(result["post"])
print("--- FIM DO POST ---")
print(f"\nConceito visual: {result['image_concept']}")
print("\nTeste concluído com sucesso!")
