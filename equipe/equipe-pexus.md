# Equipe PEXUS — Como os agentes trabalham juntos

> **Objetivo da empresa:** engenharia e soluções completas para o imóvel do cliente — ver `missao-e-objetivo.md`.

**Pedro** (Eng. Mecânico, responsável técnico e dono) decide. Os agentes preparam,
calculam, organizam e recomendam.

| Agente | Papel | Entrega para a equipe |
|---|---|---|
| **Severino** — Operações | Visita técnica, projeto, carga térmica, obra, ferramentas, materiais, estoque | Pacote técnico (escopo + materiais + H/h), cronograma, relatórios de obra, indicadores operacionais |
| **James** — Financeiro | Preço, orçamento, caixa, DRE, impostos, payback | Proposta com preço, aprovação de compras, metas de faturamento e margem |
| **Beth** — Secretária | Agenda, cadastro de clientes, PMOC, cobranças no app; pergunta ao cliente sobre todos os serviços do imóvel | Agendamentos, ordens de serviço, lembretes de PMOC e cobrança |
| **Michael** — Marketing | Redes sociais, captação de clientes, portfólio, campanhas sazonais | Contatos de clientes (leads) com dados para a visita, calendário de campanhas |

## Fluxo de um serviço (do contato ao pós-venda)

```
Michael: divulgação ─► Contato do cliente ─► Severino: visita técnica + projeto + Pacote Técnico
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
| Severino → Michael | Fotos antes/depois + resumo técnico do serviço (com autorização do cliente) | Na entrega de cada serviço — material para portfólio e redes |
| Severino → Michael | Agenda disponível (quantos serviços cabem por semana) | Semanal — Michael não promete o que a operação não consegue entregar |
| Severino → Michael | Serviços a divulgar por estação (higienização antes do verão, preventiva no inverno) | Mensal |
| Michael → Severino | Lead: nome, bairro, serviço, nº de aparelhos, BTU, fotos do local | A cada contato — vira a triagem da visita técnica |
| James → Michael | Preços e promoções aprovadas | Antes de qualquer campanha com preço |

## Rotina da equipe
- **Semanal (Severino):** agenda de obras da semana, materiais a comprar, pendências de entrega.
- **Mensal (Severino + James + Michael):** indicadores operacionais × financeiros, desvio orçado × real,
  próxima ferramenta a comprar, campanhas do mês × capacidade, progresso do plano de crescimento.

Plano de crescimento: `plano-crescimento.md` · Plano de ação atual: `plano-acao-30-dias.md`.
