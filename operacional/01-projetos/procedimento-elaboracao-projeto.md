# Procedimento de Elaboração de Projeto — PEXUS

## Etapas

| # | Etapa | Entregável | Responsável |
|---|---|---|---|
| 1 | Contato inicial / triagem | Tipo de serviço, endereço, ambientes, prazo desejado | Operativo |
| 2 | Visita técnica | `ficha-visita-tecnica.md` preenchida + fotos | Eng. responsável |
| 3 | Carga térmica | Planilha/relatório por ambiente (`pexus_ops.py carga`) | Operativo |
| 4 | Seleção de equipamentos | Modelo, capacidade, tensão, tecnologia (inverter) | Operativo |
| 5 | Traçado | Posição evaporadora/condensadora, rota da tubulação, dreno, ponto elétrico | Operativo |
| 6 | Lista de materiais + H/h | `pexus_ops.py materiais` + estimativa de horas | Operativo |
| 7 | Precificação | Proposta comercial | **James** |
| 8 | Memorial descritivo + ART | `modelo-memorial-descritivo.md` + ART no CREA | Eng. responsável |
| 9 | Liberação para obra | Abertura da pasta `obras/AAAA-NNN-cliente/` | Operativo |

## Critérios de classificação do projeto

| Classe | Exemplo | Método de carga térmica | Documentação |
|---|---|---|---|
| R1 — Residencial simples | 1 a 3 splits hi-wall | Simplificado (BTU/m² + pessoas + equipamentos + insolação) | Ficha + lista de materiais + termo de entrega |
| R2 — Residencial completo | Casa inteira, multi-split, infraestrutura em obra | Simplificado por ambiente, revisado pelo engenheiro | + memorial descritivo + ART |
| C1 — Comercial leve | Lojas, consultórios, escritórios até ~60.000 BTU/h por ambiente | NBR 16401 (vazão de ar externo, ocupação, iluminação) | + memorial + ART + **PMOC** |
| C2 — Comercial/VRF | Acima disso, VRF, dutos | Software de carga térmica (cálculo hora a hora) | Projeto completo + ART + PMOC |

> Comercial de uso coletivo exige **PMOC** (Lei 13.589/2018) com responsável técnico habilitado.

## Regras práticas de traçado (residencial)

- Comprimento de linha: respeitar mínimo e máximo do fabricante (muitos splits pedem
  mínimo de ~3 m e têm carga de fábrica para 5 a 7,5 m; acima disso calcular carga adicional).
- Desnível máximo evaporadora × condensadora conforme manual.
- Dreno com caimento mínimo de 1% (recomendado 2%); prever sifão quando ligado a esgoto.
- Condensadora: afastamento livre de parede conforme manual (tipicamente ≥ 10–30 cm atrás,
  ≥ 50 cm na descarga), sem recirculação de ar quente, acesso seguro para manutenção.
- Evaporadora: longe de fontes de calor, sem jato direto sobre cama/mesa de trabalho,
  ≥ 15 cm do teto (conforme manual).
- Circuito elétrico **exclusivo** para cada equipamento, com DR/DPS conforme NBR 5410.
