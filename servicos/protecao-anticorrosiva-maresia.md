# Serviço: Proteção Anticorrosiva contra Maresia

**Responsáveis:** Severino (execução e custo) · James (validação do preço) · Michael (divulgação)
**Status:** cotação inicial — 16/11/2026 · Procedimento técnico: `operacional/04-materiais/kit-protecao-maresia.md`
**Recalcular:** `python3 ferramentas-sw/custo_maresia.py` (premissas no topo do arquivo)

## O que é
Proteção da condensadora (e da placa da evaporadora, se o cliente quiser) contra a corrosão causada
pelo ar salino, aumentando a vida útil do aparelho. Indicado para bairros próximos ao mar:
Copacabana, Ipanema, Leblon, Leme, Botafogo, Flamengo, Urca, Barra, Recreio, Ilha do Governador,
Niterói (Icaraí e região oceânica) etc.

## Duas versões

| Versão | O que inclui |
|---|---|
| **Básica** | Limpeza dos pontos de ferrugem + galvanização a frio no gabinete e no suporte, verniz isolante na placa eletrônica, graxa dielétrica nos bornes, silicone em spray no gabinete |
| **Completa** | Tudo da Básica **+ revestimento anticorrosivo nas aletas da serpentina** (a parte que mais sofre com a maresia e a mais cara de trocar) |

Opcional: troca dos parafusos por inox e do suporte por galvanizado a fogo (orçar à parte pelo catálogo).

## Custo e preço sugerido (por condensadora)

Premissas: hora técnica R$ 100/h · impostos 6% (Simples, quando houver CNPJ) · margem 20%
(configurada no app PEXUS) · deslocamento R$ 45 (30 km de Kicks + estacionamento) ·
preço dos produtos = meio da faixa estimada (**ainda não cotado**).

### Completa
| Capacidade | Custo material | Junto com a limpeza — custo | **Preço (PIX)** | Avulso — custo | **Preço (PIX)** |
|---|---|---|---|---|---|
| Até 12.000 | R$ 153 | R$ 253 | **R$ 340** | R$ 398 | **R$ 540** |
| 18.000–24.000 | R$ 258 | R$ 383 | **R$ 520** | R$ 553 | **R$ 745** |
| 30.000–36.000 | R$ 376 | R$ 526 | **R$ 710** | R$ 721 | **R$ 975** |

### Básica
| Capacidade | Custo material | Junto com a limpeza — custo | **Preço (PIX)** | Avulso — custo | **Preço (PIX)** |
|---|---|---|---|---|---|
| Até 12.000 | R$ 48 | R$ 98 | **R$ 135** | R$ 243 | **R$ 330** |
| 18.000–24.000 | R$ 48 | R$ 98 | **R$ 135** | R$ 268 | **R$ 360** |
| 30.000–36.000 | R$ 61 | R$ 136 | **R$ 185** | R$ 306 | **R$ 415** |

- "Junto com a limpeza" = adicional ao preço da Manutenção/Limpeza da tabela do app
  (ex.: split 12.000 = R$ 200 de limpeza + R$ 340 de proteção completa).
- Cartão: +7% aproximadamente. 2+ aparelhos no mesmo endereço: deslocamento uma vez só.
- **O revestimento da serpentina é ~70% do material da versão Completa.** Cotar esse produto
  primeiro (Osmag, Solemar e um terceiro) — o preço final pode cair bastante.

## Pendências antes de oferecer
1. Cotar os produtos (principalmente o revestimento da serpentina) e atualizar `P` no script.
2. James validar hora técnica, impostos (hoje como pessoa física) e comparar com o mercado.
3. Fazer o serviço em 1–2 aparelhos (de preferência de cliente atual em Copacabana) para medir o
   tempo real e gerar fotos de antes/depois.
4. Cadastrar "Proteção anticorrosiva" como serviço na tabela de mão de obra do app.

## Garantia sugerida
Garantia do serviço de 90 dias (CDC) e orientação de lavar a serpentina com água doce a cada 3–6 meses.
Reaplicação recomendada a cada 12–24 meses, conforme o produto e a exposição.
