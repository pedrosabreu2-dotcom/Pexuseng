#!/usr/bin/env python3
"""Gera projetos/modelo/PEXUS-Projeto-e-Orcamento.xlsx — modelo de levantamento,
cálculo e orçamento de projetos (climatização + engenharia de acabamentos).
Rode de novo para recriar o modelo em branco (com 1 linha de exemplo por aba)."""
from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.comments import Comment
from openpyxl.utils import get_column_letter as L

OUT = Path(__file__).resolve().parent.parent / "projetos" / "modelo" / "PEXUS-Projeto-e-Orcamento.xlsx"
NAVY = "0F2340"; GELO = "DCE8F5"; AMB = "F29D38"
F = "Arial"
fH = Font(name=F, bold=True, color="FFFFFF", size=10); fillH = PatternFill("solid", fgColor=NAVY)
fT = Font(name=F, bold=True, size=14, color=NAVY)
fS = Font(name=F, bold=True, size=11, color=NAVY)
fN = Font(name=F, size=10); fB = Font(name=F, size=10, bold=True)
fIn = Font(name=F, size=10, color="0000FF"); fillIn = PatternFill("solid", fgColor="FFF9DB")
fLink = Font(name=F, size=10, color="008000")
fillTot = PatternFill("solid", fgColor=GELO); fillAmb = PatternFill("solid", fgColor="FDE7CC")
fNote = Font(name=F, size=9, italic=True, color="5B6B7A")
thin = Side(style="thin", color="C9D3DD"); BOX = Border(left=thin, right=thin, top=thin, bottom=thin)
RS = '"R$" #,##0.00;-"R$" #,##0.00;"-"'; NUM = '#,##0.00;-#,##0.00;"-"'; INT = '#,##0;-#,##0;"-"'; PCT = '0.0%'

wb = Workbook()
def sheet(name, title, sub=None):
    ws = wb.create_sheet(name)
    ws["A1"] = title; ws["A1"].font = fT
    if sub: ws["A2"] = sub; ws["A2"].font = fNote
    ws.sheet_view.showGridLines = False
    return ws
def hdr(ws, row, cols, widths=None):
    for i, c in enumerate(cols, 1):
        x = ws.cell(row=row, column=i, value=c); x.font = fH; x.fill = fillH
        x.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center"); x.border = BOX
    ws.row_dimensions[row].height = 42
    if widths:
        for i, w in enumerate(widths, 1): ws.column_dimensions[L(i)].width = w
def inp(c, v=None, fmt=None):
    if v is not None: c.value = v
    c.font = fIn; c.fill = fillIn; c.border = BOX
    if fmt: c.number_format = fmt
def calc(c, v, fmt=None, bold=False):
    c.value = v; c.font = fB if bold else fN; c.border = BOX
    if fmt: c.number_format = fmt
def dv_list(ws, src, rng):
    d = DataValidation(type="list", formula1=src, allow_blank=True); ws.add_data_validation(d); d.add(rng)

wb.remove(wb.active)

# ===================== LEIAME =====================
ws = sheet("LEIAME", "PEXUS Engenharia — Projeto e Orçamento", "Modelo de uso na visita técnica · versão 1.0 · nov/2026")
txt = [
 ("Como usar", None),
 ("1. Salve uma cópia com o código da obra (ex.: 2026-005-Zainho.xlsx) e preencha a aba Cliente.", None),
 ("2. Preencha só as células AMARELAS com texto AZUL. Todo o resto é calculado.", None),
 ("3. Use as abas das disciplinas que o cliente pediu; abas vazias não entram no orçamento.", None),
 ("4. A aba Resumo mostra custo, preço (PIX e cartão), margem e prazo. A aba Proposta é a que vai para o cliente.", None),
 ("5. A 1ª linha de cada aba é um EXEMPLO (nome começa com 'EXEMPLO'): substitua ou apague os dados de entrada dela.", None),
 ("", None),
 ("Abas", None),
 ("Cliente — dados da obra e da visita.", None),
 ("CargaTermica — método simplificado residencial (BTU/m² + pessoas + equipamentos + insolação).", None),
 ("CargaComercial — pré-dimensionamento por componentes (NBR 16401) para comércio/escritório; projeto final em software.", None),
 ("Climatizacao — equipamentos: bitolas, materiais, fluido adicional, horas e custo; opção de proteção contra maresia.", None),
 ("Drywall — forro/rebaixamento, sanca ou enclausuramento de tubulação, paredes e shafts.", None),
 ("Eletrica / Hidraulica — composições prontas por ponto (escolha na lista e informe a quantidade).", None),
 ("Pintura — paredes, tetos e forros, com ou sem massa corrida.", None),
 ("Outros — qualquer serviço avulso (material e horas informados à mão).", None),
 ("Parceiros — marcenaria (Douglas Batista), alvenaria e outros terceiros, com taxa de gestão da PEXUS.", None),
 ("Precos / Listas — base de preços e coeficientes. Atualize os preços após cada cotação (3 fornecedores).", None),
 ("Parametros — hora técnica, ajudante, deslocamento, impostos, margem. Valores iniciais são premissas a validar com o James.", None),
 ("", None),
 ("Avisos técnicos", None),
 ("• Bitolas, cabos, disjuntores e carga adicional de fluido são referência: confirme sempre no manual do fabricante e na NBR 5410.", None),
 ("• Carga térmica simplificada vale para residencial. Comercial/industrial: use a aba CargaComercial só como estimativa e faça o projeto final em software.", None),
 ("• Preços de drywall, elétrica, hidráulica e pintura são ESTIMATIVAS iniciais: cote e atualize na aba Precos/Listas.", None),
]
for i, (t, _) in enumerate(txt, 4):
    c = ws.cell(row=i, column=1, value=t)
    c.font = fS if t in ("Como usar", "Abas", "Avisos técnicos") else fN
ws.column_dimensions["A"].width = 130

# ===================== PARAMETROS =====================
wp = sheet("Parametros", "Parâmetros do orçamento", "Premissas — validar com o James. Células amarelas podem ser alteradas.")
hdr(wp, 3, ["Parâmetro", "Valor", "Observação"], [44, 16, 70])
P = [
 ("Hora técnica (R$/h)", 100, RS, "Premissa: valor da hora do Pedro (custo de mão de obra)."),
 ("Diária do ajudante (R$/dia)", 150, RS, "Premissa: ajustar ao valor combinado com o Jacó/ajudante."),
 ("Horas produtivas por dia", 8, NUM, "Usado para calcular os dias de obra."),
 ("Custo por km (R$/km)", 1.00, RS, "Kicks 1.6: combustível ~R$0,60 + desgaste ~R$0,40."),
 ("Km ida e volta por dia", 30, NUM, "Média no Rio; ajuste por obra."),
 ("Estacionamento/pedágio por dia (R$)", 15, RS, ""),
 ("Alimentação por pessoa/dia (R$)", 35, RS, ""),
 ("Impostos sobre o preço", 0.06, PCT, "Premissa: Simples Nacional Anexo III (após CNPJ). Validar com contador."),
 ("Margem de lucro", 0.20, PCT, "Margem configurada no app PEXUS."),
 ("Taxa de cartão", 0.05, PCT, "Só quando o cliente paga no cartão."),
 ("Contingência sobre materiais", 0.05, PCT, "Perdas e itens miúdos não listados."),
 ("Taxa de gestão sobre parceiros", 0.10, PCT, "Quando a PEXUS coordena o serviço do parceiro."),
 ("Validade da proposta (dias)", 15, INT, ""),
 ("Garantia dos serviços (dias)", 90, INT, "Mínimo legal (CDC art. 26)."),
]
for i, (n, v, fm, o) in enumerate(P, 4):
    calc(wp.cell(row=i, column=1), n); inp(wp.cell(row=i, column=2), v, fm); calc(wp.cell(row=i, column=3), o)
    wp.cell(row=i, column=3).font = fNote
PR = {k: f"Parametros!$B${i}" for i, k in enumerate(
    ["hora","diaria","hdia","km_custo","km","estac","alim","imp","margem","cartao","cont","gestao","valid","garantia"], 4)}

# ===================== LISTAS =====================
wl = sheet("Listas", "Listas e coeficientes", "Tabelas de referência usadas nos cálculos. Pode editar valores (amarelo); não mude a ordem das colunas.")
# capacidades
hdr(wl, 3, ["Capacidade (BTU/h)", "Líquido (pol)", "Sucção (pol)", "Cabo alim. (mm²)", "Disjuntor (A)", "Cód. cabo PP",
            "Cód. suporte", "Horas base instalação", "Material maresia (R$)", "Horas maresia", "Fluido adic. padrão (g/m)"],
    [16,12,12,13,12,14,14,14,14,12,15])
caps = [(7000,"1/4","3/8","2,5",16,"PP_4x1,5","SUP_9000",3.5,153,1.0,20),
        (9000,"1/4","3/8","2,5",16,"PP_4x1,5","SUP_9000",3.5,153,1.0,20),
        (12000,"1/4","3/8","2,5",16,"PP_4x1,5","SUP_12000",3.5,153,1.0,20),
        (18000,"1/4","1/2","2,5",16,"PP_4x1,5","SUP_18000",4.5,258,1.25,20),
        (22000,"1/4","5/8","4",20,"PP_4x2,5","SUP_24000",4.5,258,1.25,20),
        (24000,"1/4","5/8","4",20,"PP_4x2,5","SUP_24000",4.5,258,1.25,20),
        (30000,"3/8","5/8","4",25,"PP_4x2,5","SUP_30000",6,376,1.5,50),
        (36000,"3/8","5/8","4",25,"PP_4x2,5","SUP_36000",6,376,1.5,50),
        (48000,"3/8","3/4","6",32,"PP_4x4","SUP_48000",8,450,2.0,50),
        (60000,"3/8","3/4","6",32,"PP_4x4","SUP_60000",8,450,2.0,50)]
for r, row in enumerate(caps, 4):
    for c, v in enumerate(row, 1):
        cell = wl.cell(row=r, column=c)
        inp(cell, v, INT if c in (1,5) else (RS if c == 9 else None))
CAP = "Listas!$A$4:$A$13"
def capcol(col): return f"Listas!${col}$4:${col}$13"
wl["A15"] = "Bitolas/cabos/disjuntores: referência típica — confirmar no manual do fabricante e NBR 5410. Fluido adicional padrão: 20 g/m (linha 1/4\") e 50 g/m (3/8\")."; wl["A15"].font = fNote
# tipos de equipamento
wl["A17"] = "Tipo de equipamento"; wl["B17"] = "Horas extras"; 
for c in ("A17","B17"): wl[c].font = fH; wl[c].fill = fillH
tipos = [("Split hi-wall",0),("Piso-teto",1.5),("Cassete",2.5),("Evaporadora de multi-split",0.5)]
for r,(t,h) in enumerate(tipos,18): inp(wl.cell(row=r,column=1),t); inp(wl.cell(row=r,column=2),h,NUM)
TIP = "Listas!$A$18:$A$21"; TIPH = "Listas!$B$18:$B$21"
wl["A23"] = "Horas por metro de linha acima de 5 m"; inp(wl["B23"], 0.15, NUM); HLINHA = "Listas!$B$23"
wl["A24"] = "Carga de fábrica padrão (m de linha)"; inp(wl["B24"], 5, NUM); CARGAFAB = "Listas!$B$24"
wl["A26"] = "Fluidos"; wl["A26"].font = fS
for r, g in enumerate(["R-32","R-410A","R-22","R-134a"], 27): inp(wl.cell(row=r,column=1), g)
FLU = "Listas!$A$27:$A$30"
wl["A32"] = "S/N"; inp(wl["A33"],"S"); inp(wl["A34"],"N"); SN = "Listas!$A$33:$A$34"
# drywall
wl["D17"] = "Tipo de drywall"; wl["E17"] = "Faces de placa"; wl["F17"] = "Horas por m²"; wl["G17"] = "Cód. perfil"; wl["H17"] = "Cód. guia/tabica"
for c in ("D17","E17","F17","G17","H17"): wl[c].font = fH; wl[c].fill = fillH
dws = [("Forro / rebaixamento de teto",1,0.5,"PERFIL_F530","TABICA"),
       ("Sanca ou enclausuramento de tubulação",1,1.2,"PERFIL_F530","CANTONEIRA"),
       ("Parede de drywall",2,0.4,"MONTANTE_48","GUIA_48"),
       ("Fechamento de shaft / caixa",1,0.6,"MONTANTE_48","GUIA_48")]
for r, row in enumerate(dws, 18):
    for c, v in enumerate(row, 4): inp(wl.cell(row=r, column=c), v, NUM if c in (5,6) else None)
DWT = "Listas!$D$18:$D$21"
wl["D22"] = "Horas por m² de face (inclui estrutura, placas e tratamento de juntas). Produtividade de referência — ajuste com o tempo real."; wl["D22"].font = fNote
wl["D24"] = "Placas"; wl["D24"].font = fS
for r, p in enumerate(["ST","RU","RF"], 25): inp(wl.cell(row=r, column=4), p)
PLC = "Listas!$D$25:$D$27"
# composições elétricas
def comp_table(col0, row0, title, rows):
    a, b, c = L(col0), L(col0+1), L(col0+2)
    wl[f"{a}{row0}"] = title; wl[f"{b}{row0}"] = "Material (R$/un)"; wl[f"{c}{row0}"] = "Horas/un"
    for x in (a, b, c): wl[f"{x}{row0}"].font = fH; wl[f"{x}{row0}"].fill = fillH
    for i, (n, m, h) in enumerate(rows, row0+1):
        inp(wl[f"{a}{i}"], n); inp(wl[f"{b}{i}"], m, RS); inp(wl[f"{c}{i}"], h, NUM)
    last = row0 + len(rows)
    return f"Listas!${a}${row0+1}:${a}${last}", f"Listas!${b}${row0+1}:${b}${last}", f"Listas!${c}${row0+1}:${c}${last}"
wl.column_dimensions["J"].width = 52; wl.column_dimensions["N"].width = 52; wl.column_dimensions["R"].width = 40
ELE = comp_table(10, 3, "Composição elétrica", [
 ("Ponto de tomada/interruptor novo em drywall", 35, 0.8),
 ("Ponto de tomada/interruptor novo em alvenaria (com rasgo)", 40, 1.5),
 ("Ponto de iluminação no teto/forro", 30, 0.8),
 ("Instalação de spot/luminária embutida (sem a luminária)", 10, 0.4),
 ("Troca de tomada/interruptor", 20, 0.3),
 ("Circuito exclusivo 2,5 mm² até 15 m (ar-condicionado)", 150, 2.5),
 ("Circuito exclusivo 4 mm² até 15 m", 225, 3.0),
 ("Circuito exclusivo 6 mm² até 15 m", 320, 3.5),
 ("Instalação/troca de disjuntor", 35, 0.3),
 ("DR bipolar 30 mA", 150, 0.8),
 ("DPS (jogo)", 120, 0.8),
 ("Quadro de distribuição novo (até 12 disjuntores)", 250, 4.0),
 ("Instalação de ventilador de teto", 15, 1.5),
 ("Instalação de chuveiro elétrico (ponto existente)", 20, 1.0),
 ("Passagem de cabo em eletroduto existente (por metro)", 4, 0.1),
])
HID = comp_table(14, 3, "Composição hidráulica", [
 ("Ponto de água fria (PVC soldável)", 45, 2.0),
 ("Ponto de água quente (PPR/CPVC)", 70, 2.5),
 ("Ponto de esgoto 40/50 mm", 55, 2.5),
 ("Ligação de dreno do ar ao esgoto (com sifão)", 25, 1.0),
 ("Registro de gaveta/pressão", 90, 1.5),
 ("Troca de torneira/misturador", 15, 0.5),
 ("Instalação hidráulica de bancada/cuba", 30, 2.0),
 ("Caixa sifonada / ralo", 50, 1.5),
 ("Reparo de vazamento aparente", 20, 1.0),
])
# pintura
wl["R3"] = "Pintura (por m²)"; wl["S3"] = "Material (R$/m²)"; wl["T3"] = "Horas/m²"
for x in ("R3","S3","T3"): wl[x].font = fH; wl[x].fill = fillH
pint = [("Selador/fundo",1.2,0.08),("Massa corrida (2 demãos + lixa)",3.0,0.30),("Tinta acrílica (por demão)",1.5,0.12),("Consumíveis (fita, lixa, rolo, lona)",1.0,0)]
for i,(n,m,h) in enumerate(pint,4): inp(wl[f"R{i}"],n); inp(wl[f"S{i}"],m,RS); inp(wl[f"T{i}"],h,NUM)
wl["R9"] = "Superfícies"; wl["R9"].font = fS
for i,s in enumerate(["Parede","Teto","Forro de drywall novo"],10): inp(wl[f"R{i}"], s)
SUP = "Listas!$R$10:$R$12"
wl["R14"] = "Estimativas iniciais — atualize com cotações e tempos reais."; wl["R14"].font = fNote
# parceiros
wl["R16"] = "Quem fatura"; wl["R16"].font = fS; inp(wl["R17"], "PEXUS"); inp(wl["R18"], "Parceiro"); FAT = "Listas!$R$17:$R$18"

# ===================== PRECOS =====================
wpr = sheet("Precos", "Base de preços de materiais", "Climatização: catálogo do app PEXUS (Osmag/Solemar, nov/2026). Drywall: estimativas — cotar.")
hdr(wpr, 4, ["Código", "Item", "Unidade", "Preço (R$)", "Fonte"], [16, 46, 12, 13, 40])
precos = [
 ("COBRE_1/4","Tubo de cobre 1/4\"","m",18.85,"App PEXUS — Osmag"),("COBRE_3/8","Tubo de cobre 3/8\"","m",28.97,"App PEXUS — Osmag"),
 ("COBRE_1/2","Tubo de cobre 1/2\"","m",39.15,"App PEXUS — Osmag"),("COBRE_5/8","Tubo de cobre 5/8\"","m",50.66,"App PEXUS — Osmag"),
 ("COBRE_3/4","Tubo de cobre 3/4\"","m",65.18,"App PEXUS — Osmag"),
 ("ISO_1/4","Isolamento 1/4\" (barra 2 m)","barra",3.20,"App PEXUS — Osmag"),("ISO_3/8","Isolamento 3/8\" (barra 2 m)","barra",3.40,"App PEXUS — Osmag"),
 ("ISO_1/2","Isolamento 1/2\" (barra 2 m)","barra",4.20,"App PEXUS — Osmag"),("ISO_5/8","Isolamento 5/8\" (barra 2 m)","barra",5.80,"App PEXUS — Osmag"),
 ("ISO_3/4","Isolamento 3/4\" (barra 2 m)","barra",6.80,"App PEXUS — Osmag"),
 ("FITA_PVC","Fita PVC de acabamento","rolo",4.00,"App PEXUS — Osmag"),("DRENO","Mangueira de dreno 3/4\"","m",6.50,"App PEXUS"),
 ("PP_4x1,5","Cabo PP 4 vias 1,5 mm²","m",8.00,"App PEXUS — Osmag"),("PP_4x2,5","Cabo PP 4 vias 2,5 mm²","m",12.00,"App PEXUS — Osmag"),
 ("PP_4x4","Cabo PP 4 vias 4 mm²","m",18.00,"App PEXUS — Osmag"),
 ("CAB_2,5","Cabo flexível 2,5 mm²","m",2.50,"App PEXUS"),("CAB_4","Cabo flexível 4 mm²","m",4.15,"App PEXUS"),("CAB_6","Cabo flexível 6 mm²","m",6.20,"App PEXUS"),
 ("DISJ","Disjuntor","un",35.00,"App PEXUS"),
 ("SUP_9000","Suporte condensadora até 9.000","par",35.00,"App PEXUS"),("SUP_12000","Suporte condensadora 12.000","par",77.00,"App PEXUS — só Solemar; recotar"),
 ("SUP_18000","Suporte condensadora 18.000","par",50.00,"App PEXUS"),("SUP_24000","Suporte condensadora 24.000","par",60.00,"App PEXUS"),
 ("SUP_30000","Suporte condensadora 30.000","par",75.00,"App PEXUS"),("SUP_36000","Suporte condensadora 36.000","par",85.00,"App PEXUS"),
 ("SUP_48000","Suporte condensadora 48.000","par",190.00,"App PEXUS"),("SUP_60000","Suporte condensadora 60.000","par",240.00,"App PEXUS"),
 ("COXIM","Suporte antivibração (jogo)","jogo",22.00,"App PEXUS"),("BUCHA10","Bucha + parafuso sextavado 10 mm","un",2.50,"App PEXUS"),
 ("MASSA_CAL","Massa de calafetar","un",14.00,"App PEXUS"),("ABRAC","Abraçadeira","un",1.00,"App PEXUS"),("TERMINAL","Terminal elétrico","un",0.90,"App PEXUS"),
 ("GAS_R-32","Fluido R-32","kg",55.00,"App PEXUS"),("GAS_R-410A","Fluido R-410A","kg",50.00,"App PEXUS"),
 ("GAS_R-22","Fluido R-22","kg",110.00,"App PEXUS"),("GAS_R-134a","Fluido R-134a","kg",84.85,"App PEXUS"),
 ("PLACA_ST","Placa drywall ST 1,20×1,80 (2,16 m²)","un",48.00,"ESTIMATIVA — cotar"),("PLACA_RU","Placa drywall RU (verde) 1,20×1,80","un",62.00,"ESTIMATIVA — cotar"),
 ("PLACA_RF","Placa drywall RF (rosa) 1,20×1,80","un",65.00,"ESTIMATIVA — cotar"),
 ("PERFIL_F530","Perfil F530 (canaleta de forro)","m",5.50,"ESTIMATIVA — cotar"),("TABICA","Tabica de acabamento","m",6.00,"ESTIMATIVA — cotar"),
 ("CANTONEIRA","Cantoneira / perfil L","m",5.00,"ESTIMATIVA — cotar"),("GUIA_48","Guia 48 mm","m",6.50,"ESTIMATIVA — cotar"),
 ("MONTANTE_48","Montante 48 mm","m",7.50,"ESTIMATIVA — cotar"),("TIRANTE","Tirante + regulador + fixação (kit)","un",4.00,"ESTIMATIVA — cotar"),
 ("PARAFUSO_DW","Parafuso drywall (placa/metal)","un",0.08,"ESTIMATIVA — cotar"),("MASSA_DW","Massa para juntas de drywall","kg",4.50,"ESTIMATIVA — cotar"),
 ("FITA_DW","Fita para juntas","m",0.25,"ESTIMATIVA — cotar"),("LA","Lã mineral (isolamento acústico)","m²",15.00,"ESTIMATIVA — cotar"),
]
for r, row in enumerate(precos, 5):
    for c, v in enumerate(row, 1):
        cell = wpr.cell(row=r, column=c)
        if c == 4: inp(cell, v, RS)
        else: calc(cell, v)
LASTP = 4 + len(precos) + 20
for r in range(5 + len(precos), LASTP + 1):
    for c in range(1, 6): inp(wpr.cell(row=r, column=c))
wpr["A3"] = "Linhas amarelas vazias no fim: para novos itens (use um código único)."; wpr["A3"].font = fNote
def PRC(code_expr): return f"INDEX(Precos!$D$5:$D${LASTP},MATCH({code_expr},Precos!$A$5:$A${LASTP},0))"

# ===================== CLIENTE =====================
wc = sheet("Cliente", "Dados da obra e da visita técnica")
campos = ["Código da obra (AAAA-NNN)","Cliente","Telefone","Endereço","Bairro / Cidade","Tipo de imóvel (casa/apto/comercial)",
          "Data da visita","Responsável técnico","Serviços solicitados","Prazo desejado pelo cliente","Observações / restrições do local (condomínio, horários, acesso)"]
ex = ["2026-000","EXEMPLO — Nome do cliente","(21) 9xxxx-xxxx","Rua Exemplo, 100 — apto 201","Bairro / Rio de Janeiro","Apartamento",
      "18/11/2026","Eng. Mecânico Pedro — PEXUS","Climatização + rebaixamento de teto + elétrica","30 dias","Condomínio: obras de seg. a sex., 8h–17h"]
wc.column_dimensions["A"].width = 52; wc.column_dimensions["B"].width = 70
for i, (k, v) in enumerate(zip(campos, ex), 4):
    calc(wc.cell(row=i, column=1), k); inp(wc.cell(row=i, column=2), v)

# ===================== CARGA TÉRMICA RESIDENCIAL =====================
wt = sheet("CargaTermica", "Carga térmica — residencial (método simplificado)",
           "600 BTU/h·m² (800 com sol da tarde ou último andar) × fator pé-direito + 600 por pessoa acima de 2 + 600 por equipamento + 1.000 por m² de vidro com sol.")
hdr(wt, 4, ["Ambiente","Comprimento (m)","Largura (m)","Área (m²)","Pé-direito (m)","Sol da tarde / último andar (S/N)",
            "Pessoas","Equipamentos que esquentam","Vidro com sol (m²)","Carga calculada (BTU/h)","Capacidade recomendada (BTU/h)"],
    [30,13,12,11,12,16,10,14,12,16,18])
for r in range(5, 25):
    for c in "ABCEFGHI": inp(wt[f"{c}{r}"], fmt=NUM if c in "BCEI" else None)
    calc(wt[f"D{r}"], f'=IF(OR(B{r}="",C{r}=""),"",B{r}*C{r})', NUM)
    calc(wt[f"J{r}"], f'=IF(D{r}="","",D{r}*IF(F{r}="S",800,600)*MAX(1,IF(E{r}="",2.7,E{r})/2.8)+MAX(0,G{r}-2)*600+H{r}*600+I{r}*1000)', INT, True)
    calc(wt[f"K{r}"], f'=IF(J{r}="","",IF(J{r}>60000,"Dividir em mais aparelhos / ver CargaComercial",INDEX({CAP},COUNTIF({CAP},"<"&J{r})+1)))', INT, True)
dv_list(wt, f"={SN}", "F5:F24")
for c, v in zip("ABCEFGHI", ["EXEMPLO — Quarto casal", 3.5, 3.0, 2.7, "S", 2, 2, 0]): wt[f"{c}5"].value = v
wt["A26"] = "Escolha sempre a capacidade comercial imediatamente acima da carga calculada. Revisão final: engenheiro responsável."; wt["A26"].font = fNote

# ===================== CARGA TÉRMICA COMERCIAL =====================
wk = sheet("CargaComercial", "Carga térmica — comercial (pré-dimensionamento por componentes)",
           "Estimativa para orçamento de comércio/escritório/indústria leve. Projeto executivo: cálculo hora a hora em software, conforme NBR 16401.")
cond = [("Temperatura externa de projeto (°C)",35),("Temperatura interna (°C)",24),("Diferença de umidade absoluta ext.–int. (kg/kg)",0.008),
        ("U parede externa (W/m²·K)",2.5),("U cobertura/laje exposta (W/m²·K)",2.0),("U vidro (W/m²·K)",5.8),
        ("Acréscimo de temperatura por sol em parede (K)",5),("Acréscimo por sol em cobertura (K)",15),("Fator de segurança",1.10)]
wk["A3"] = "Condições de projeto (Rio de Janeiro — ajustar)"; wk["A3"].font = fS
for i, (n, v) in enumerate(cond, 4):
    calc(wk.cell(row=i, column=1), n); inp(wk.cell(row=i, column=2), v, NUM if v < 1 else NUM)
TE, TI, DW, UPAR, UCOB, UVID, DSP, DSC, FS = [f"$B${i}" for i in range(4, 13)]
hdr(wk, 15, ["Ambiente","Área de piso (m²)","Parede externa (m²)","Vidro (m²)","Ganho solar no vidro (W/m²)","Cobertura exposta (m²)",
             "Pessoas","Calor sensível/pessoa (W)","Calor latente/pessoa (W)","Iluminação (W/m²)","Equipamentos (W)",
             "Ar externo (L/s por pessoa)","Ar externo (L/s por m²)","Carga total (W)","Carga (BTU/h)","Carga (TR)","Sugestão"],
    [30,11,11,9,12,11,9,11,11,11,12,11,11,13,13,9,30])
for r in range(16, 31):
    for c in "ABCDEFGHIJKLM": inp(wk[f"{c}{r}"], fmt=NUM if c != "A" else None)
    dt = f"({TE}-{TI})"
    vazao = f"(G{r}*L{r}+B{r}*M{r})"
    w = (f"(C{r}*{UPAR}*({dt}+{DSP})+F{r}*{UCOB}*({dt}+{DSC})+D{r}*({UVID}*{dt}+E{r})+G{r}*(H{r}+I{r})+B{r}*J{r}+K{r}"
         f"+1.23*{vazao}*{dt}+3010*{vazao}*{DW})*{FS}")
    calc(wk[f"N{r}"], f'=IF(B{r}="","",{w})', INT, True)
    calc(wk[f"O{r}"], f'=IF(N{r}="","",N{r}*3.412)', INT, True)
    calc(wk[f"P{r}"], f'=IF(O{r}="","",O{r}/12000)', NUM)
    calc(wk[f"Q{r}"], f'=IF(O{r}="","",IF(O{r}<=60000,"1 aparelho de "&INDEX({CAP},COUNTIF({CAP},"<"&O{r})+1)&" BTU/h","Dividir ou sistema central/VRF"))')
for c, v in zip("ABCDEFGHIJKLM", ["EXEMPLO — Loja 60 m²",60,18,8,200,60,8,75,55,12,1500,2.5,0.3]): wk[f"{c}16"].value = v
wk["A32"] = "Referências de calor por pessoa: escritório 75 W sensível + 55 W latente; loja/varejo 75 + 70; academia 210 + 315. Ar externo NBR 16401-3: escritório ~2,5 L/s·pessoa + 0,3 L/s·m²."; wk["A32"].font = fNote

# ===================== CLIMATIZAÇÃO =====================
wa = sheet("Climatizacao", "Climatização — equipamentos, materiais, fluido e mão de obra",
           "Uma linha por aparelho. Bitolas e carga adicional: confirmar no manual. Deixe 'Carga de fábrica' e 'g/m' vazios para usar o padrão.")
cols = ["Ambiente","Tipo","Capacidade (BTU/h)","Fluido","Linha frigorígena (m)","Dreno (m)","Distância do quadro (m)",
        "Carga de fábrica até (m)","Fluido adicional (g/m)","Suporte novo? (S/N)","Proteção maresia? (S/N)",
        "Líquido (pol)","Sucção (pol)","Cobre líquido (m)","Cobre sucção (m)","Isolamento (barras de 2 m, cada linha)","Cabo PP (m)",
        "Cabo alimentação (m)","Disjuntor (A)","Fluido adicional (g)","Material (R$)","Horas","Mão de obra (R$)","Custo total (R$)"]
hdr(wa, 4, cols, [26,20,13,10,11,9,11,11,11,10,11,9,9,10,10,13,9,11,10,11,13,8,13,14])
for r in range(5, 25):
    for c in "ABCDEFGHIJK": inp(wa[f"{c}{r}"], fmt=NUM if c in "EFGHI" else (INT if c == "C" else None))
    blank = f'$C{r}=""'
    calc(wa[f"L{r}"], f'=IF({blank},"",INDEX({capcol("B")},MATCH(C{r},{CAP},0)))')
    calc(wa[f"M{r}"], f'=IF({blank},"",INDEX({capcol("C")},MATCH(C{r},{CAP},0)))')
    calc(wa[f"N{r}"], f'=IF({blank},"",E{r}+0.5)', NUM)
    calc(wa[f"O{r}"], f'=IF({blank},"",E{r}+0.5)', NUM)
    calc(wa[f"P{r}"], f'=IF({blank},"",ROUNDUP(E{r}*1.1/2,0))', INT)
    calc(wa[f"Q{r}"], f'=IF({blank},"",E{r}+1)', NUM)
    calc(wa[f"R{r}"], f'=IF({blank},"",G{r}*3+2)', NUM)
    calc(wa[f"S{r}"], f'=IF({blank},"",INDEX({capcol("E")},MATCH(C{r},{CAP},0)))', INT)
    gpm = f'IF(I{r}="",INDEX({capcol("K")},MATCH(C{r},{CAP},0)),I{r})'
    calc(wa[f"T{r}"], f'=IF({blank},"",MAX(0,E{r}-IF(H{r}="",{CARGAFAB},H{r}))*{gpm})', INT, True)
    mat = ("=IF({b},\"\",N{r}*{c1}+O{r}*{c2}+P{r}*({i1}+{i2})+ROUNDUP(E{r}/5,0)*{fita}+F{r}*{dreno}+Q{r}*{pp}+R{r}*{cab}+{disj}"
           "+IF(J{r}=\"S\",{sup},0)+{cox}+8*{bucha}+0.5*{massa}+10*{abrac}+10*{term}+T{r}/1000*{gas}"
           "+IF(K{r}=\"S\",INDEX({mm},MATCH(C{r},{cap},0)),0))").format(
        b=blank, r=r, c1=PRC(f'"COBRE_"&L{r}'), c2=PRC(f'"COBRE_"&M{r}'), i1=PRC(f'"ISO_"&L{r}'), i2=PRC(f'"ISO_"&M{r}'),
        fita=PRC('"FITA_PVC"'), dreno=PRC('"DRENO"'), pp=PRC(f'INDEX({capcol("F")},MATCH(C{r},{CAP},0))'),
        cab=PRC(f'"CAB_"&INDEX({capcol("D")},MATCH(C{r},{CAP},0))'), disj=PRC('"DISJ"'),
        sup=PRC(f'INDEX({capcol("G")},MATCH(C{r},{CAP},0))'), cox=PRC('"COXIM"'), bucha=PRC('"BUCHA10"'),
        massa=PRC('"MASSA_CAL"'), abrac=PRC('"ABRAC"'), term=PRC('"TERMINAL"'), gas=PRC(f'"GAS_"&IF(D{r}="","R-32",D{r})'),
        mm=capcol("I"), cap=CAP)
    calc(wa[f"U{r}"], mat, RS)
    hrs = (f'=IF({blank},"",INDEX({capcol("H")},MATCH(C{r},{CAP},0))+IFERROR(INDEX({TIPH},MATCH(B{r},{TIP},0)),0)'
           f'+MAX(0,E{r}-5)*{HLINHA}+IF(K{r}="S",INDEX({capcol("J")},MATCH(C{r},{CAP},0)),0))')
    calc(wa[f"V{r}"], hrs, NUM)
    calc(wa[f"W{r}"], f'=IF({blank},"",V{r}*{PR["hora"]})', RS)
    calc(wa[f"X{r}"], f'=IF({blank},"",U{r}+W{r})', RS, True)
dv_list(wa, f"={TIP}", "B5:B24"); dv_list(wa, f"={CAP}", "C5:C24"); dv_list(wa, f"={FLU}", "D5:D24"); dv_list(wa, f"={SN}", "J5:K24")
for c, v in zip("ABCDEFGJK", ["EXEMPLO — Quarto casal","Split hi-wall",12000,"R-32",6,2,10,"S","N"]): wa[f"{c}5"].value = v
wa["A25"] = "TOTAL"; wa["A25"].font = fB
for c, fm in (("T", INT), ("U", RS), ("V", NUM), ("W", RS), ("X", RS)):
    calc(wa[f"{c}25"], f"=SUM({c}5:{c}24)", fm, True); wa[f"{c}25"].fill = fillTot
wa["A27"] = "Material inclui: cobre, isolamento, fita, dreno, cabo PP, cabo de alimentação, disjuntor, suporte (se marcado), antivibração, fixação, vedação, fluido adicional e kit maresia (se marcado). Equipamento (aparelho) NÃO incluso — some na aba Outros se a PEXUS fornecer."; wa["A27"].font = fNote

# ===================== DRYWALL =====================
wd = sheet("Drywall", "Drywall — forro, rebaixamento, sanca, enclausuramento de tubulação, paredes e shafts",
           "Forro: comprimento × largura do ambiente. Sanca/enclausuramento: comprimento × desenvolvimento (soma das faces, ex.: 0,30 + 0,30 = 0,60 m). Parede/shaft: comprimento × altura.")
hdr(wd, 4, ["Ambiente","Tipo","Comprimento (m)","Largura / altura / desenvolvimento (m)","Placa (ST/RU/RF)","Lã mineral? (S/N)",
            "Área (m²)","Faces de placa","Placas (un)","Perfil estrutural (m)","Guia / tabica / cantoneira (m)","Tirantes (un)",
            "Parafusos (un)","Massa (kg)","Fita (m)","Lã (m²)","Material (R$)","Horas","Mão de obra (R$)","Custo total (R$)"],
    [26,30,12,15,10,10,10,8,9,11,12,9,10,9,9,8,13,8,13,14])
for r in range(5, 30):
    for c in "ABCDEF": inp(wd[f"{c}{r}"], fmt=NUM if c in "CD" else None)
    b = f'$C{r}=""'; t = f"MATCH(B{r},{DWT},0)"
    calc(wd[f"G{r}"], f'=IF({b},"",C{r}*D{r})', NUM)
    calc(wd[f"H{r}"], f'=IF({b},"",INDEX(Listas!$E$18:$E$21,{t}))', INT)
    calc(wd[f"I{r}"], f'=IF({b},"",ROUNDUP(G{r}*H{r}*1.08/2.16,0))', INT)
    calc(wd[f"J{r}"], f'=IF({b},"",CHOOSE({t},G{r}*2.1,C{r}*3,(C{r}/0.6+1)*D{r},(C{r}/0.6+1)*D{r}))', NUM)
    calc(wd[f"K{r}"], f'=IF({b},"",CHOOSE({t},2*(C{r}+D{r}),2*C{r},2*C{r},2*C{r}))', NUM)
    calc(wd[f"L{r}"], f'=IF({b},"",CHOOSE({t},ROUNDUP(G{r}*1.4,0),ROUNDUP(C{r}/0.6,0)+1,0,0))', INT)
    calc(wd[f"M{r}"], f'=IF({b},"",ROUNDUP(G{r}*H{r}*16+J{r}*2,0))', INT)
    calc(wd[f"N{r}"], f'=IF({b},"",G{r}*H{r}*0.5)', NUM)
    calc(wd[f"O{r}"], f'=IF({b},"",G{r}*H{r}*1.5)', NUM)
    calc(wd[f"P{r}"], f'=IF({b},"",IF(F{r}="S",G{r},0))', NUM)
    mat = (f'=IF({b},"",I{r}*{PRC(chr(34)+"PLACA_"+chr(34)+"&IF(E"+str(r)+"=\"\",\"ST\",E"+str(r)+")")}'
           f'+J{r}*{PRC(f"INDEX(Listas!$G$18:$G$21,{t})")}+K{r}*{PRC(f"INDEX(Listas!$H$18:$H$21,{t})")}'
           f'+L{r}*{PRC(chr(34)+"TIRANTE"+chr(34))}+M{r}*{PRC(chr(34)+"PARAFUSO_DW"+chr(34))}+N{r}*{PRC(chr(34)+"MASSA_DW"+chr(34))}'
           f'+O{r}*{PRC(chr(34)+"FITA_DW"+chr(34))}+P{r}*{PRC(chr(34)+"LA"+chr(34))})')
    calc(wd[f"Q{r}"], mat, RS)
    calc(wd[f"R{r}"], f'=IF({b},"",G{r}*H{r}*INDEX(Listas!$F$18:$F$21,{t}))', NUM)
    calc(wd[f"S{r}"], f'=IF({b},"",R{r}*{PR["hora"]})', RS)
    calc(wd[f"T{r}"], f'=IF({b},"",Q{r}+S{r})', RS, True)
dv_list(wd, f"={DWT}", "B5:B29"); dv_list(wd, f"={PLC}", "E5:E29"); dv_list(wd, f"={SN}", "F5:F29")
for c, v in zip("ABCDEF", ["EXEMPLO — Rebaixamento sala","Forro / rebaixamento de teto",4.0,3.5,"ST","N"]): wd[f"{c}5"].value = v
wd["A30"] = "TOTAL"; wd["A30"].font = fB
for c, fm in (("G", NUM), ("Q", RS), ("R", NUM), ("S", RS), ("T", RS)):
    calc(wd[f"{c}30"], f"=SUM({c}5:{c}29)", fm, True); wd[f"{c}30"].fill = fillTot
wd["A32"] = "Coeficientes por m²: placas +8% de perda; F530 a cada 0,60 m; tirantes ~1,4/m²; 16 parafusos/m² de face; massa 0,5 kg e fita 1,5 m por m² de face. Pintura do forro vai na aba Pintura."; wd["A32"].font = fNote

# ===================== ELÉTRICA / HIDRÁULICA =====================
def comp_sheet(name, title, comp, n, ex):
    ws = sheet(name, title, "Escolha a composição na lista, informe a quantidade. Material e horas por unidade vêm da aba Listas.")
    hdr(ws, 4, ["Ambiente","Composição","Qtd","Material (R$/un)","Horas/un","Material (R$)","Horas","Mão de obra (R$)","Custo total (R$)"],
        [26,56,8,13,9,13,9,13,14])
    nm, mt, hr = comp
    for r in range(5, 5 + n):
        inp(ws[f"A{r}"]); inp(ws[f"B{r}"]); inp(ws[f"C{r}"], fmt=NUM)
        b = f'OR($B{r}="",$C{r}="")'
        calc(ws[f"D{r}"], f'=IF({b},"",INDEX({mt},MATCH(B{r},{nm},0)))', RS)
        calc(ws[f"E{r}"], f'=IF({b},"",INDEX({hr},MATCH(B{r},{nm},0)))', NUM)
        calc(ws[f"F{r}"], f'=IF({b},"",C{r}*D{r})', RS)
        calc(ws[f"G{r}"], f'=IF({b},"",C{r}*E{r})', NUM)
        calc(ws[f"H{r}"], f'=IF({b},"",G{r}*{PR["hora"]})', RS)
        calc(ws[f"I{r}"], f'=IF({b},"",F{r}+H{r})', RS, True)
    dv_list(ws, f"={nm}", f"B5:B{4+n}")
    for c, v in zip("ABC", ex): ws[f"{c}5"].value = v
    t = 5 + n; ws[f"A{t}"] = "TOTAL"; ws[f"A{t}"].font = fB
    for c, fm in (("F", RS), ("G", NUM), ("H", RS), ("I", RS)):
        calc(ws[f"{c}{t}"], f"=SUM({c}5:{c}{t-1})", fm, True); ws[f"{c}{t}"].fill = fillTot
    return t
TE_ = comp_sheet("Eletrica", "Elétrica — pontos, circuitos e quadro", ELE, 40, ["EXEMPLO — Quarto casal","Circuito exclusivo 2,5 mm² até 15 m (ar-condicionado)",1])
TH_ = comp_sheet("Hidraulica", "Hidráulica — pontos, registros e ligações", HID, 30, ["EXEMPLO — Área de serviço","Ligação de dreno do ar ao esgoto (com sifão)",1])

# ===================== PINTURA =====================
wpi = sheet("Pintura", "Pintura e acabamento", "Parede: perímetro × pé-direito. Teto/forro: comprimento × largura. Desconte portas e janelas (m²).")
hdr(wpi, 4, ["Ambiente","Superfície","Comprimento ou perímetro (m)","Altura ou largura (m)","Desconto de aberturas (m²)",
             "Massa corrida? (S/N)","Demãos de tinta","Área (m²)","Material (R$)","Horas","Mão de obra (R$)","Custo total (R$)"],
    [26,22,14,12,12,11,10,10,13,9,13,14])
for r in range(5, 30):
    for c in "ABCDEFG": inp(wpi[f"{c}{r}"], fmt=NUM if c in "CDEG" else None)
    b = f'OR($C{r}="",$D{r}="")'
    calc(wpi[f"H{r}"], f'=IF({b},"",MAX(0,C{r}*D{r}-E{r}))', NUM)
    calc(wpi[f"I{r}"], f'=IF({b},"",H{r}*(Listas!$S$4+IF(F{r}="S",Listas!$S$5,0)+Listas!$S$6*IF(G{r}="",2,G{r})+Listas!$S$7))', RS)
    calc(wpi[f"J{r}"], f'=IF({b},"",H{r}*(Listas!$T$4+IF(F{r}="S",Listas!$T$5,0)+Listas!$T$6*IF(G{r}="",2,G{r})+Listas!$T$7))', NUM)
    calc(wpi[f"K{r}"], f'=IF({b},"",J{r}*{PR["hora"]})', RS)
    calc(wpi[f"L{r}"], f'=IF({b},"",I{r}+K{r})', RS, True)
dv_list(wpi, f"={SUP}", "B5:B29"); dv_list(wpi, f"={SN}", "F5:F29")
for c, v in zip("ABCDEFG", ["EXEMPLO — Forro da sala","Forro de drywall novo",4.0,3.5,0,"N",2]): wpi[f"{c}5"].value = v
wpi["A30"] = "TOTAL"; wpi["A30"].font = fB
for c, fm in (("H", NUM), ("I", RS), ("J", NUM), ("K", RS), ("L", RS)):
    calc(wpi[f"{c}30"], f"=SUM({c}5:{c}29)", fm, True); wpi[f"{c}30"].fill = fillTot

# ===================== OUTROS =====================
wo = sheet("Outros", "Outros serviços e fornecimentos", "Qualquer item fora das abas anteriores: aparelho fornecido pela PEXUS, rodapé, prateleira, desinstalação, caçamba etc.")
hdr(wo, 4, ["Descrição","Unidade","Qtd","Material (R$/un)","Horas/un","Material (R$)","Horas","Mão de obra (R$)","Custo total (R$)"],
    [48,10,8,13,9,13,9,13,14])
for r in range(5, 25):
    for c in "ABCDE": inp(wo[f"{c}{r}"], fmt=RS if c == "D" else (NUM if c in "CE" else None))
    b = f'$C{r}=""'
    calc(wo[f"F{r}"], f'=IF({b},"",C{r}*D{r})', RS); calc(wo[f"G{r}"], f'=IF({b},"",C{r}*E{r})', NUM)
    calc(wo[f"H{r}"], f'=IF({b},"",G{r}*{PR["hora"]})', RS); calc(wo[f"I{r}"], f'=IF({b},"",F{r}+H{r})', RS, True)
for c, v in zip("ABCDE", ["EXEMPLO — Retirada de entulho (sacos)","sc",5,3,0.1]): wo[f"{c}5"].value = v
wo["A25"] = "TOTAL"; wo["A25"].font = fB
for c, fm in (("F", RS), ("G", NUM), ("H", RS), ("I", RS)):
    calc(wo[f"{c}25"], f"=SUM({c}5:{c}24)", fm, True); wo[f"{c}25"].fill = fillTot

# ===================== PARCEIROS =====================
wpa = sheet("Parceiros", "Parceiros — marcenaria, alvenaria e outros terceiros",
            "PEXUS fatura: o preço inclui taxa de gestão e impostos. Parceiro fatura: o cliente paga direto ao parceiro e a PEXUS recebe a taxa de gestão do parceiro.")
hdr(wpa, 4, ["Parceiro","Serviço","Valor cobrado pelo parceiro (R$)","Quem fatura","Taxa de gestão","Preço ao cliente (R$)","Receita da PEXUS (R$)"],
    [26,46,16,13,11,16,16])
for r in range(5, 15):
    inp(wpa[f"A{r}"]); inp(wpa[f"B{r}"]); inp(wpa[f"C{r}"], fmt=RS); inp(wpa[f"D{r}"]); inp(wpa[f"E{r}"], fmt=PCT)
    b = f'$C{r}=""'; tx = f'IF(E{r}="",{PR["gestao"]},E{r})'
    calc(wpa[f"F{r}"], f'=IF({b},"",IF(D{r}="Parceiro",C{r},C{r}*(1+{tx})/(1-{PR["imp"]})))', RS, True)
    calc(wpa[f"G{r}"], f'=IF({b},"",IF(D{r}="Parceiro",C{r}*{tx},F{r}*(1-{PR["imp"]})-C{r}))', RS)
dv_list(wpa, f"={FAT}", "D5:D14")
for c, v in zip("ABCD", ["Douglas Batista (marcenaria)","EXEMPLO — Armário embutido do quarto",3500,"PEXUS"]): wpa[f"{c}5"].value = v
wpa["A15"] = "TOTAL"; wpa["A15"].font = fB
for c in "CFG": calc(wpa[f"{c}15"], f'=SUMIF($D$5:$D$14,"PEXUS",{c}5:{c}14)' if c == "C" else f"=SUM({c}5:{c}14)", RS, True); wpa[f"{c}15"].fill = fillTot
wpa["H4"] = "Custo PEXUS (só o que a PEXUS fatura)"; wpa["H4"].font = fNote
wpa["A17"] = "Parceiros atuais: Douglas Batista — marcenaria (armários, embutidos). Alvenaria: parceria a definir."; wpa["A17"].font = fNote

# ===================== RESUMO =====================
wr = sheet("Resumo", "Resumo de custo e preço", "Preço = custo direto ÷ (1 − impostos − margem). Método do James. Tudo calculado.")
hdr(wr, 4, ["Disciplina","Material (R$)","Material + contingência (R$)","Horas","Mão de obra (R$)","Terceiros (R$)","Custo direto (R$)","Preço PIX (R$)"],
    [34,14,16,9,14,14,15,15])
div = f'(1-{PR["imp"]}-{PR["margem"]})'
disc = [("Climatização","Climatizacao!U25","Climatizacao!V25"),("Drywall","Drywall!Q30","Drywall!R30"),
        ("Elétrica",f"Eletrica!F{TE_}",f"Eletrica!G{TE_}"),("Hidráulica",f"Hidraulica!F{TH_}",f"Hidraulica!G{TH_}"),
        ("Pintura e acabamento","Pintura!I30","Pintura!J30"),("Outros serviços","Outros!F25","Outros!G25")]
for i, (n, m, h) in enumerate(disc, 5):
    calc(wr[f"A{i}"], n); calc(wr[f"B{i}"], f"={m}", RS); wr[f"B{i}"].font = fLink
    calc(wr[f"C{i}"], f"=B{i}*(1+{PR['cont']})", RS); calc(wr[f"D{i}"], f"={h}", NUM); wr[f"D{i}"].font = fLink
    calc(wr[f"E{i}"], f"=D{i}*{PR['hora']}", RS); calc(wr[f"F{i}"], 0, RS)
    calc(wr[f"G{i}"], f"=C{i}+E{i}+F{i}", RS); calc(wr[f"H{i}"], f"=G{i}/{div}", RS, True)
# parceiros
r = 11; calc(wr[f"A{r}"], "Parceiros (marcenaria, alvenaria…)")
for c in "BCDE": calc(wr[f"{c}{r}"], 0, RS if c != "D" else NUM)
calc(wr[f"F{r}"], "=Parceiros!C15", RS); wr[f"F{r}"].font = fLink; calc(wr[f"G{r}"], f"=F{r}", RS)
calc(wr[f"H{r}"], '=SUMIF(Parceiros!$D$5:$D$14,"PEXUS",Parceiros!$F$5:$F$14)', RS, True)
# logística
wr["A14"] = "Logística da obra"; wr["A14"].font = fS
log = [("Ajudante na obra? (S/N)", "S", None, True), ("Visitas extras (orçamento, medição, entrega)", 1, INT, True),
       ("Total de horas de serviço", "=SUM(D5:D10)", NUM, False), ("Dias de obra", f"=IF(B17=0,0,ROUNDUP(B17/{PR['hdia']},0))", INT, False),
       ("Custo do ajudante (R$)", f"=IF(B15=\"S\",B18*{PR['diaria']},0)", RS, False),
       ("Deslocamento (R$)", f"=(B18+B16)*({PR['km']}*{PR['km_custo']}+{PR['estac']})", RS, False),
       ("Alimentação (R$)", f"=B18*{PR['alim']}*IF(B15=\"S\",2,1)", RS, False)]
for i, (n, v, fm, isin) in enumerate(log, 15):
    calc(wr[f"A{i}"], n)
    (inp if isin else calc)(wr[f"B{i}"], v, fm)
dv_list(wr, f"={SN}", "B15")
r = 12; calc(wr[f"A{r}"], "Mobilização e logística (ajudante, deslocamento, alimentação)")
for c in "BCDE": calc(wr[f"{c}{r}"], 0, RS if c != "D" else NUM)
calc(wr[f"F{r}"], "=B19+B20+B21", RS); calc(wr[f"G{r}"], f"=F{r}", RS); calc(wr[f"H{r}"], f"=G{r}/{div}", RS, True)
r = 13; calc(wr[f"A{r}"], "TOTAL", None, True)
for c in "BCDEFGH": calc(wr[f"{c}{r}"], f"=SUM({c}5:{c}12)", NUM if c == "D" else RS, True); wr[f"{c}{r}"].fill = fillTot
wr["A13"].fill = fillTot
wr["D24"] = "Resultado"; wr["D24"].font = fS
res = [("Preço total à vista (PIX)", "=H13", RS), ("Preço total no cartão", f"=H13*{div}/({div}-{PR['cartao']})", RS),
       ("Impostos estimados", f"=H13*{PR['imp']}", RS), ("Custo direto total", "=G13", RS),
       ("Lucro estimado (PIX)", "=H13-D27-D28", RS), ("Margem sobre o preço", "=IF(H13=0,0,D29/H13)", PCT),
       ("Prazo estimado (dias de obra)", "=B18", INT), ("Fluido adicional total (g)", "=Climatizacao!T25", INT)]
for i, (n, v, fm) in enumerate(res, 25):
    calc(wr[f"C{i}"], n); calc(wr[f"D{i}"], v, fm, True); wr[f"D{i}"].fill = fillAmb if i in (25, 26) else fillTot
wr.column_dimensions["C"].width = 30
wr["A34"] = "Preços de parceiros com 'Parceiro fatura' não entram no total da PEXUS (o cliente paga direto ao parceiro)."; wr["A34"].font = fNote

# ===================== PROPOSTA =====================
wpp = sheet("Proposta", "PEXUS Engenharia e Soluções em Refrigeração e Climatização", "Proposta comercial — revise antes de enviar ao cliente.")
wpp.column_dimensions["A"].width = 46; wpp.column_dimensions["B"].width = 22; wpp.column_dimensions["C"].width = 50
info = [("Proposta / obra nº", "=Cliente!B4"), ("Cliente", "=Cliente!B5"), ("Telefone", "=Cliente!B6"), ("Endereço", "=Cliente!B7&\" — \"&Cliente!B8"),
        ("Data da visita", "=Cliente!B10"), ("Responsável técnico", "=Cliente!B11")]
for i, (k, v) in enumerate(info, 4): calc(wpp[f"A{i}"], k, None, True); calc(wpp[f"B{i}"], v); wpp.merge_cells(f"B{i}:C{i}")
wpp["A11"] = "Escopo e investimento"; wpp["A11"].font = fS
hdr(wpp, 12, ["Serviço", "Valor (R$)", "Observação"])
escopo = [("Climatização (instalação e infraestrutura)", "Resumo!H5", "Materiais e mão de obra; aparelhos conforme proposta"),
          ("Drywall (forro, rebaixamento, sancas, paredes)", "Resumo!H6", ""), ("Elétrica", "Resumo!H7", "Conforme NBR 5410"),
          ("Hidráulica", "Resumo!H8", ""), ("Pintura e acabamento", "Resumo!H9", ""), ("Outros serviços", "Resumo!H10", ""),
          ("Serviços de parceiros (marcenaria etc.)", "Resumo!H11", "Coordenados pela PEXUS"), ("Mobilização, deslocamento e equipe", "Resumo!H12", "")]
for i, (n, ref, o) in enumerate(escopo, 13):
    calc(wpp[f"A{i}"], f'=IF({ref}>0,"{n}","")'); calc(wpp[f"B{i}"], f'=IF({ref}>0,{ref},"")', RS); calc(wpp[f"C{i}"], f'=IF({ref}>0,"{o}","")')
calc(wpp["A21"], "TOTAL À VISTA (PIX)", None, True); calc(wpp["B21"], "=Resumo!D25", RS, True); wpp["B21"].fill = fillAmb
calc(wpp["A22"], "Total no cartão", None, True); calc(wpp["B22"], "=Resumo!D26", RS, True)
cond_ = [("Prazo de execução", '=Resumo!D31&" dia(s) de obra, a combinar o início"'),
         ("Validade da proposta", f'={PR["valid"]}&" dias"'), ("Garantia dos serviços", f'={PR["garantia"]}&" dias, conforme termo de entrega"'),
         ("Condições de pagamento", "Entrada de 50% e 50% na entrega (a confirmar com o financeiro)"),
         ("Não incluso", "Aparelhos de ar-condicionado (se não listados), alvenaria, obras civis, licenças e taxas de condomínio, itens não descritos acima")]
for i, (k, v) in enumerate(cond_, 24):
    calc(wpp[f"A{i}"], k, None, True); (calc if str(v).startswith("=") else inp)(wpp[f"B{i}"], v); wpp.merge_cells(f"B{i}:C{i}")
    wpp[f"B{i}"].alignment = Alignment(wrap_text=True)
wpp["A30"] = "PEXUS Engenharia — engenharia e soluções completas para a sua casa ou empresa: climatização, elétrica, drywall, hidráulica e acabamento."; wpp["A30"].font = fNote

# ordem das abas
order = ["LEIAME","Cliente","CargaTermica","CargaComercial","Climatizacao","Drywall","Eletrica","Hidraulica","Pintura","Outros",
         "Parceiros","Resumo","Proposta","Parametros","Precos","Listas"]
wb._sheets = [wb[n] for n in order]
for ws in wb.worksheets: ws.freeze_panes = "B5" if ws.title not in ("LEIAME","Cliente","Parametros","Proposta","Resumo","Listas","Precos") else None
OUT.parent.mkdir(parents=True, exist_ok=True)
wb.save(OUT); print(OUT)
