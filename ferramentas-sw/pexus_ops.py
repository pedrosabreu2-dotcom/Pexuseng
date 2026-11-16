#!/usr/bin/env python3
"""PEXUS — ferramentas do Agente Operativo.

Subcomandos:
  carga        Carga térmica simplificada (residencial) e capacidade recomendada.
  materiais    Lista de materiais para instalação de split (saída em Markdown).
  ferramentas  Resumo do plano de aquisição de ferramentas por fase.

Exemplos:
  python3 pexus_ops.py carga --area 12 --sol --pessoas 2 --equip 1
  python3 pexus_ops.py materiais --btu 12000 --linha 4 --dreno 2 --eletrica 8
  python3 pexus_ops.py ferramentas --fase 1

Valores são de referência; confirmar sempre no manual do fabricante e NBR 5410/16401.
"""
import argparse
import csv
import math
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
CSV_FERRAMENTAS = RAIZ / "operacional" / "03-ferramentas" / "plano-aquisicao-ferramentas.csv"

def br(n):
    """Formata número no padrão brasileiro (1.234)."""
    return f"{n:,.0f}".replace(",", ".")


CAPACIDADES = [7000, 9000, 12000, 18000, 22000, 24000, 30000, 36000, 48000, 60000]

# capacidade máxima da faixa -> (líquido, sucção, isolamento mm, cabo mm², disjuntor A, PP)
TABELA = [
    (12000, '1/4"', '3/8"', 13, 2.5, 16, "4x1,5 mm²"),
    (18000, '1/4"', '1/2"', 13, 2.5, 16, "4x1,5 mm²"),
    (24000, '1/4"', '5/8"', 19, 4.0, 20, "4x2,5 mm²"),
    (36000, '3/8"', '5/8"', 19, 4.0, 25, "4x2,5 mm²"),
    (60000, '3/8"', '3/4"', 19, 6.0, 32, "conforme fabricante"),
]


def faixa(btu):
    for linha in TABELA:
        if btu <= linha[0]:
            return linha
    sys.exit(f"Capacidade {btu} BTU/h fora da faixa (máx. 60.000). Projeto comercial: usar NBR 16401.")


def cmd_carga(a):
    base = 800 if (a.sol or a.ultimo_andar) else 600
    volume_fator = max(1.0, a.pe_direito / 2.8)
    carga_area = a.area * base * volume_fator
    carga_pessoas = max(0, a.pessoas - 2) * 600
    carga_equip = a.equip * 600
    carga_vidro = a.vidro * 1000
    total = carga_area + carga_pessoas + carga_equip + carga_vidro
    rec = next((c for c in CAPACIDADES if c >= total), None)

    print(f"Área: {a.area:.1f} m² × {base} BTU/h·m² × fator pé-direito {volume_fator:.2f} = {br(carga_area)}")
    print(f"Pessoas adicionais: {max(0, a.pessoas - 2)} × 600 = {br(carga_pessoas)}")
    print(f"Equipamentos: {a.equip} × 600 = {br(carga_equip)}")
    print(f"Vidro com sol: {a.vidro:.1f} m² × 1.000 = {br(carga_vidro)}")
    print(f"TOTAL ESTIMADO: {br(total)} BTU/h ({total / 12000:.2f} TR)")
    if rec:
        print(f"Capacidade comercial recomendada: {br(rec)} BTU/h")
    else:
        print("Acima de 60.000 BTU/h: dividir em mais de um equipamento ou projeto comercial (NBR 16401).")
    print("Obs.: método simplificado para residencial; revisar pelo engenheiro responsável.")


def cmd_materiais(a):
    _, liq, suc, iso, cabo, disj, pp = faixa(a.btu)
    q = a.qtd
    L = a.linha
    cobre = L + 0.5
    barras_iso = math.ceil(L * 1.1 / 2)
    itens = [
        (f"Tubo de cobre {liq} (líquido)", "m", cobre * q),
        (f"Tubo de cobre {suc} (sucção)", "m", cobre * q),
        (f"Isolamento elastomérico {liq} × {iso} mm (barra 2 m)", "barra", barras_iso * q),
        (f"Isolamento elastomérico {suc} × {iso} mm (barra 2 m)", "barra", barras_iso * q),
        ("Fita PVC de acabamento", "rolo", math.ceil(L / 5) * q),
        ("Mangueira/tubo de dreno", "m", (a.dreno + 1) * q),
        (f"Cabo PP {pp} (interligação)", "m", (L + 1) * q),
        (f"Cabo de alimentação {str(cabo).replace('.', ',').replace(',0', '')} mm² (3 condutores)", "m", (a.eletrica * 3 + 2) * q),
        (f"Disjuntor bipolar/monopolar {disj} A curva C", "un", q),
        ("Suporte para condensadora (par)", "par", q),
        ("Coxim antivibração", "un", 4 * q),
        ("Bucha 10 + parafuso sextavado", "un", 8 * q),
        ("Massa de calafetar / silicone", "tubo", math.ceil(q / 2)),
        ("Abraçadeiras de nylon", "un", 10 * q),
    ]
    print(f"## Lista de materiais — {q} × split {br(a.btu)} BTU/h, linha {L:g} m\n")
    print("| Item | Un. | Qtd. |")
    print("|---|---|---|")
    for nome, un, qtd in itens:
        qtd_fmt = f"{qtd:g}" if isinstance(qtd, float) else str(qtd)
        print(f"| {nome} | {un} | {qtd_fmt} |")
    print()
    print(f"- Carga adicional de fluido: verificar manual (linha de {L:g} m vs. pré-carga de fábrica).")
    print("- Bitolas, cabo e disjuntor são referência — CONFIRMAR NO MANUAL DO FABRICANTE e NBR 5410.")
    print("- Itens de uso contínuo (N₂, varetas, espuma de vazamento) saem do estoque.")


def cmd_ferramentas(a):
    with open(CSV_FERRAMENTAS, newline="", encoding="utf-8") as f:
        linhas = list(csv.DictReader(f))
    if a.fase:
        linhas = [r for r in linhas if r["fase"] == str(a.fase)]
    if a.status:
        linhas = [r for r in linhas if r["status"] == a.status]
    fases = {}
    for r in linhas:
        qtd = int(r["qtd"])
        d = fases.setdefault(r["fase"], {"itens": 0, "min": 0, "max": 0, "A": 0})
        d["itens"] += 1
        d["min"] += float(r["preco_min_brl"]) * qtd
        d["max"] += float(r["preco_max_brl"]) * qtd
        if r["prioridade"] == "A":
            d["A"] += 1
    print("| Fase | Itens | Prioridade A | Investimento estimado (R$) |")
    print("|---|---|---|---|")
    for fase in sorted(fases):
        d = fases[fase]
        print(f"| {fase} | {d['itens']} | {d['A']} | {d['min']:,.0f} – {d['max']:,.0f} |".replace(",", "."))
    if a.detalhar:
        print()
        print("| Fase | Prio. | Item | Qtd | Faixa (R$) | Status |")
        print("|---|---|---|---|---|---|")
        for r in sorted(linhas, key=lambda r: (r["fase"], r["prioridade"])):
            print(f"| {r['fase']} | {r['prioridade']} | {r['item']} | {r['qtd']} | "
                  f"{r['preco_min_brl']}–{r['preco_max_brl']} | {r['status']} |")
    print("\nValores de referência: cotar com 3 fornecedores antes da compra.")


def main():
    p = argparse.ArgumentParser(description="PEXUS — Agente Operativo")
    sub = p.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("carga", help="carga térmica simplificada")
    c.add_argument("--area", type=float, required=True, help="área do ambiente em m²")
    c.add_argument("--pe-direito", type=float, default=2.7, help="pé-direito em m (padrão 2,7)")
    c.add_argument("--sol", action="store_true", help="sol da tarde direto")
    c.add_argument("--ultimo-andar", action="store_true", help="cobertura/telhado sem forro")
    c.add_argument("--pessoas", type=int, default=2)
    c.add_argument("--equip", type=int, default=0, help="nº de equipamentos que geram calor")
    c.add_argument("--vidro", type=float, default=0.0, help="m² de vidro com sol direto")
    c.set_defaults(func=cmd_carga)

    m = sub.add_parser("materiais", help="lista de materiais para split")
    m.add_argument("--btu", type=int, required=True)
    m.add_argument("--linha", type=float, required=True, help="comprimento da linha frigorígena (m)")
    m.add_argument("--dreno", type=float, default=2.0, help="comprimento do dreno (m)")
    m.add_argument("--eletrica", type=float, default=10.0, help="distância do quadro (m)")
    m.add_argument("--qtd", type=int, default=1, help="quantidade de equipamentos iguais")
    m.set_defaults(func=cmd_materiais)

    f = sub.add_parser("ferramentas", help="resumo do plano de aquisição")
    f.add_argument("--fase", type=int)
    f.add_argument("--status")
    f.add_argument("--detalhar", action="store_true")
    f.set_defaults(func=cmd_ferramentas)

    a = p.parse_args()
    a.func(a)


if __name__ == "__main__":
    main()
