# PEXUS Engenharia e Soluções em Refrigeração e Climatização

Empresa de engenharia (em estruturação) fundada por Engenheiro Mecânico, atuando em
refrigeração e climatização residencial, com expansão planejada para comercial leve.

## Agentes da empresa

| Agente | Área | Onde está |
|---|---|---|
| **James** | Financeiro: precificação, orçamentos, fluxo de caixa, DRE, impostos | skill `james-financeiro-pexus` |
| **Operativo** | Operacional: projetos, gestão de obras, ferramentas, materiais | `.claude/agents/operativo-pexus.md` + pasta `operacional/` |

Fluxo entre agentes: o **Operativo** gera o escopo técnico, a lista de materiais
(quantidades) e as horas/homem; o **James** transforma isso em preço e proposta comercial.

## Estrutura do repositório

```
operacional/
  01-projetos/      procedimento de projeto, carga térmica, memorial descritivo
  02-obras/         fluxo da obra, checklists, diário de obra, termo de entrega
  03-ferramentas/   plano de aquisição de ferramentas por fase (CSV + guia)
  04-materiais/     tabelas técnicas, kits de material por serviço, requisição
ferramentas-sw/     scripts Python (calculadora de carga térmica e lista de materiais)
obras/              uma pasta por obra: obras/AAAA-NNN-cliente/
```

## Convenções

- Idioma: português do Brasil. Unidades: BTU/h, TR, m, mm², polegadas para tubos de cobre.
- Código de obra: `AAAA-NNN` (ex.: `2026-001`). Pasta: `obras/2026-001-sobrenome-cliente/`.
- Preços em tabelas de ferramentas/materiais são **estimativas de referência** — sempre cotar
  com pelo menos 3 fornecedores antes de comprar.
- Dados técnicos genéricos (bitolas, cabos, disjuntores) **nunca substituem o manual do
  fabricante** do equipamento instalado e a NBR 5410.
- Normas de referência: NBR 16401 (climatização), NBR 5410 (instalações elétricas),
  NBR 16655 (refrigeração – segurança), Lei 13.589/2018 + Portaria GM/MS 3.523/98 e
  RE ANVISA 09/2003 (PMOC), NR-10, NR-35, NR-6, NR-18.
