#!/usr/bin/env python3
"""Custo e preço sugerido do serviço de Proteção Anticorrosiva (maresia).

Método do James: preço = custo direto ÷ (1 − impostos − taxa − margem).
Todas as premissas estão no topo — ajuste e rode de novo.
"""
# ---------------- PREMISSAS (ajustar) ----------------
HORA_TECNICA = 100.0      # R$/h — valor da hora do Pedro (premissa, validar com James)
IMPOSTOS = 0.06           # 6% — Simples Nacional Anexo III (premissa p/ quando houver CNPJ)
MARGEM = 0.20             # 20% — margem configurada no aplicativo PEXUS (configCalc)
TAXA_CARTAO = 0.05        # 5% — só quando o cliente paga no cartão
CUSTO_KM = 1.00           # R$/km — Kicks 1.6 (combustível ~R$0,60 + desgaste ~R$0,40)
KM_VISITA = 30            # ida e volta média no Rio
ESTACIONAMENTO = 15.0
# preço médio de referência dos produtos (meio da faixa estimada — cotar!)
P = dict(serpentina=105.0, verniz=65.0, graxa=35.0, zinco=45.0, silicone=25.0, alcool=45.0)
CONSUMIVEIS = 8.0         # fita crepe, lixa, panos
DEPREC_KIT = 5.0          # respirador/filtro, escovas, pincéis por aparelho

FAIXAS = {  # latas de serpentina, fração verniz, graxa, zinco, silicone, horas (combo, avulso)
    "até 12.000":    (1, 1/8, 1/10, 1/3, 1/4, (1.00, 2.00)),
    "18.000–24.000": (2, 1/8, 1/10, 1/3, 1/4, (1.25, 2.50)),
    "30.000–36.000": (3, 1/6, 1/8, 1/2, 1/3, (1.50, 3.00)),
}
H_BASICA = {"até 12.000": (0.50, 1.50), "18.000–24.000": (0.50, 1.75), "30.000–36.000": (0.75, 2.00)}

def br(v): return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
def br0(v): return f"R$ {round(v / 5) * 5:,.0f}".replace(",", ".")

def materiais(f, completa):
    lat, ver, gra, zin, sil, _ = f
    m = ver * P["verniz"] + gra * P["graxa"] + zin * P["zinco"] + sil * P["silicone"] \
        + 0.05 * P["alcool"] + CONSUMIVEIS + DEPREC_KIT
    if completa: m += lat * P["serpentina"]
    return m

div = 1 - IMPOSTOS - MARGEM
desloc = KM_VISITA * CUSTO_KM + ESTACIONAMENTO
print(f"Divisor (PIX): 1 − {IMPOSTOS:.0%} − {MARGEM:.0%} = {div:.2f} | deslocamento avulso: {br(desloc)}\n")
for nivel, completa in (("COMPLETA (com revestimento da serpentina)", True), ("BÁSICA (sem revestimento da serpentina)", False)):
    print(f"### {nivel}\n")
    print("| Capacidade | Material | MO junto c/ limpeza | Custo junto | Preço junto (PIX) | MO avulso | Custo avulso | Preço avulso (PIX) |")
    print("|---|---|---|---|---|---|---|---|")
    for cap, f in FAIXAS.items():
        hc, ha = f[5] if completa else H_BASICA[cap]
        mat = materiais(f, completa)
        cj = mat + hc * HORA_TECNICA
        ca = mat + ha * HORA_TECNICA + desloc
        print(f"| {cap} | {br(mat)} | {hc:g} h = {br(hc*HORA_TECNICA)} | {br(cj)} | **{br0(cj/div)}** | {ha:g} h | {br(ca)} | **{br0(ca/div)}** |")
    print()
print(f"Cartão: dividir por {div - TAXA_CARTAO:.2f} em vez de {div:.2f} (≈ +{(div/(div-TAXA_CARTAO)-1):.0%}).")
print("Avulso com 2+ aparelhos no mesmo endereço: deslocamento entra uma vez só.")
