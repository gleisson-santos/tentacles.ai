"""Teste completo em modo produção: 1 ciclo completo com publicação real no LinkedIn"""
import sys
sys.stdout.reconfigure(encoding="utf-8")

import auto_poster as ap

print("=" * 55)
print("   TESTE DE PRODUÇÃO - 1 ciclo completo")
print("   Groq AI + Stability AI + LinkedIn")
print("=" * 55)

ap.run_cycle()

print("\nTeste de produção concluído!")
