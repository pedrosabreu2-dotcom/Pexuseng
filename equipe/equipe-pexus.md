# Equipe PEXUS — Como os agentes trabalham juntos

**Pedro** (Eng. Mecânico, responsável técnico e dono) decide. Os agentes preparam,
calculam, organizam e recomendam.

| Agente | Papel | Entrega para a equipe |
|---|---|---|
| **Severino** — Operações | Visita técnica, projeto, carga térmica, obra, ferramentas, materiais, estoque | Pacote técnico (escopo + materiais + H/h), cronograma, relatórios de obra, indicadores operacionais |
| **James** — Financeiro | Preço, orçamento, caixa, DRE, impostos, payback | Proposta com preço, aprovação de compras, metas de faturamento e margem |
| **Michael** — *(a definir)* | *(aguardando definição do Pedro)* | — |

## Fluxo de um serviço (do contato ao pós-venda)

```
Contato do cliente ─► Severino: visita técnica + projeto + Pacote Técnico
                                   │
                                   ▼
                     James: preço + proposta ─► cliente aprova?
                                   │ sim
                                   ▼
        Severino: requisição de compra ─► James: aprova gasto / caixa
                                   │
                                   ▼
        Severino: executa, comissiona, entrega, registra H/h e material reais
                                   │
                                   ▼
        James: fatura, recebe, apura margem real (real × orçado)
                                   │
                                   ▼
        Severino: agenda manutenção preventiva / oferta contrato recorrente
```

## Pontos de passagem (handoffs)

| De → Para | Documento | Quando |
|---|---|---|
| Severino → James | `pacote-tecnico-orcamento.md` | Ao fim de cada visita técnica |
| Severino → James | `operacional/04-materiais/modelo-requisicao-compra.md` | Antes de comprar material |
| Severino → James | Linha do `plano-aquisicao-ferramentas.csv` | Antes de comprar ferramenta > R$ 1.000 (análise de payback) |
| Severino → James | Fechamento da obra (H/h e material reais) | Na entrega — calibra o custo da hora |
| James → Severino | Proposta aprovada + condições | Libera a abertura da obra |
| James → Severino | Meta mensal de serviços | Planejamento de capacidade |

## Rotina da equipe
- **Semanal (Severino):** agenda de obras da semana, materiais a comprar, pendências de entrega.
- **Mensal (Severino + James):** indicadores operacionais × financeiros, desvio orçado × real,
  próxima ferramenta a comprar, progresso do plano de crescimento.

Plano de crescimento: `plano-crescimento.md`.
