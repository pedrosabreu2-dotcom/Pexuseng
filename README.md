# PEXUS Engenharia — Operacional

Base de trabalho do **Agente Operativo** da PEXUS Engenharia e Soluções em Refrigeração e
Climatização: projetos, gestão de obras, aquisição de ferramentas e de materiais.

## Início rápido

```bash
# Carga térmica de um quarto de 12 m² com sol da tarde e 1 TV
python3 ferramentas-sw/pexus_ops.py carga --area 12 --sol --equip 1

# Lista de materiais para 2 splits de 12.000 BTU/h com linha de 4 m
python3 ferramentas-sw/pexus_ops.py materiais --btu 12000 --linha 4 --dreno 2 --eletrica 8 --qtd 2

# Investimento em ferramentas por fase
python3 ferramentas-sw/pexus_ops.py ferramentas --detalhar
```

Nova obra: siga `operacional/02-obras/fluxo-gestao-obra.md`.
Veja `CLAUDE.md` para a estrutura completa e a divisão entre agentes (Operativo × James).
