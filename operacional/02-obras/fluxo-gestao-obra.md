# Fluxo de Gestão de Obra — PEXUS

## Abertura
1. Proposta aprovada (James) → gerar código `AAAA-NNN`.
2. Criar `obras/AAAA-NNN-cliente/` e copiar os modelos desta pasta:
   `cronograma.md`, `checklist-pre-obra.md`, `checklist-instalacao-split.md`,
   `diario-de-obra.md`, `checklist-comissionamento.md`, `termo-de-entrega.md`.
3. Gerar `materiais.md` com `python3 ferramentas-sw/pexus_ops.py materiais ...`.
4. Emitir requisição de compra (`04-materiais/modelo-requisicao-compra.md`).

## Status da obra
`ORÇADA → APROVADA → MATERIAL SOLICITADO → MATERIAL RECEBIDO → EM EXECUÇÃO →
COMISSIONADA → ENTREGUE → EM GARANTIA → ENCERRADA`

## Cronograma padrão (referência de horas/homem, equipe de 2)

| Serviço | Duração típica | Observação |
|---|---|---|
| Instalação split 9–12k (linha até 5 m, parede simples) | 3–4 h | + 1 h por andar com acesso difícil |
| Instalação split 18–24k | 4–5 h | |
| Instalação split 30–36k / piso-teto | 5–7 h | suportes e linha mais pesados |
| Infraestrutura (pré-instalação) por ponto em obra | 2–3 h | rasgo e embutimento de linha |
| Manutenção preventiva split (limpeza completa) | 1–1,5 h | |
| Higienização com desmontagem da evaporadora | 2–3 h | |
| Desinstalação com recolhimento de gás | 1–1,5 h | |

Somar: deslocamento, compra de material de última hora, limpeza do local.

## Indicadores operacionais (acompanhar mensalmente)
- Obras entregues no prazo (%)
- Retornos em garantia (%) e causa (vazamento, dreno, elétrica, ruído)
- H/h real × H/h orçada (desvio %) → retroalimenta o James
- Desvio de material (consumido × previsto)
- Incidentes de segurança (meta: zero)
