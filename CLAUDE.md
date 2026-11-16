# PEXUS Engenharia e Soluções em Refrigeração e Climatização

Empresa de engenharia (em estruturação) fundada por Engenheiro Mecânico, atuando em
refrigeração e climatização residencial, com expansão planejada para comercial leve.

## Equipe de agentes da PEXUS

| Agente | Área | Onde está |
|---|---|---|
| **Severino** | Operações: projetos, gestão de obras, ferramentas, materiais | `.claude/agents/severino-operativo-pexus.md` + `operacional/` |
| **James** | Financeiro: precificação, orçamentos, fluxo de caixa, DRE, impostos | skill `james-financeiro-pexus` |
| **Michael** | Marketing: redes sociais, captação de clientes, divulgação da marca | definição própria do Michael |

Como a equipe trabalha junta: `equipe/equipe-pexus.md`.

## Estrutura do repositório

```
equipe/           equipe de agentes, fluxo entre áreas, plano de crescimento
operacional/
  01-projetos/      procedimento de projeto, carga térmica, memorial descritivo
  02-obras/         fluxo da obra, checklists, diário de obra, termo de entrega
  03-ferramentas/   plano de aquisição de ferramentas por fase (CSV + guia)
  04-materiais/     tabelas técnicas, kits de material (inclui proteção contra maresia), requisição
ferramentas-sw/     scripts Python (carga térmica, lista de materiais, custo de serviços)
obras/              uma pasta por obra: obras/AAAA-NNN-cliente/
servicos/           fichas de serviços (escopo, custo, preço sugerido)
marketing/          campanhas prontas (artes + legendas) para o Michael
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
