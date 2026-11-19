#!/usr/bin/env python3
"""Viabilidade da locação de andaimes tubulares — PEXUS (Severino + James).
Premissas no topo; rode para recalcular. Valores de compra: anúncios Mercado Livre/Loja do Mecânico (nov/2026)."""
# ---- composição de 1 torre de 6 m (painel 1,00 x 1,50 m) ----
TORRE = {  # item: (qtd, preço unitário R$)
    "Painel tubular 1,00 x 1,50 m": (8, 314.0),   # kit 4 peças R$ 1.256 (HGMAX/ML)
    "Diagonal 1,5 m":               (4, 76.0),    # R$ 75,77 Pix (HGMAX/ML)
    "Piso metálico 1,5 m":          (3, 343.0),   # R$ 343,42 Pix (HGMAX/ML)
    "Sapata regulável 45 cm":       (4, 65.0),    # R$ 64,99 (HGMAX/ML)
    "Guarda-corpo (par)":           (2, 120.0),   # ESTIMATIVA — cotar
}
EXTRAS_INICIAIS = 1200.0   # contrato padrão + placas/etiquetas, cintas de amarração, pintura/identificação, EPI extra (estimativa)
DIARIA_PECA = [0.60, 0.80] # R$/peça/dia — premissa (ref. distante: ORSE maio/2026 R$ 0,66/peça/dia)
OCUPACAO = [0.40, 0.60, 0.80]
IMPOSTO = 0.06             # premissa Simples — confirmar enquadramento de locação de bens móveis com contador
MANUT_MES = 0.01           # 1% do valor do estoque/mês: reposição, pintura, peças perdidas
USO_PROPRIO_MES = 1        # meses/ano em que a PEXUS usaria 1 torre nas próprias obras (aluguel evitado)

def br(v): return f"R$ {v:,.0f}".replace(",", ".")
pecas = sum(q for q, _ in TORRE.values()); valor_torre = sum(q * p for q, p in TORRE.values())
print(f"1 torre de 6 m: {pecas} peças, {br(valor_torre)}\n")
for n in (2, 4, 6):
    inv = n * valor_torre + EXTRAS_INICIAIS
    print(f"### {n} torres ({n*pecas} peças) — investimento {br(inv)}")
    print("| Diária/peça | Ocupação | Receita/mês | Impostos | Manutenção | Lucro/mês | Retorno do investimento |")
    print("|---|---|---|---|---|---|---|")
    for d in DIARIA_PECA:
        for o in OCUPACAO:
            rec = n * pecas * d * 30 * o
            lucro = rec - rec * IMPOSTO - n * valor_torre * MANUT_MES
            pb = f"{inv / lucro:.0f} meses" if lucro > 0 else "não se paga"
            print(f"| R$ {d:.2f} | {o:.0%} | {br(rec)} | {br(rec*IMPOSTO)} | {br(n*valor_torre*MANUT_MES)} | {br(lucro)} | {pb} |")
    print()
aluguel_torre_mes = pecas * 0.80 * 30
print(f"Uso próprio: cada mês que a PEXUS usa uma torre própria evita ~{br(aluguel_torre_mes)} de aluguel (a R$ 0,80/peça/dia).")
