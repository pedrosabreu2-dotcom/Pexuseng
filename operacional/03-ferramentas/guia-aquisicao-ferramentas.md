# Guia de Aquisição de Ferramentas — PEXUS

Dados completos em `plano-aquisicao-ferramentas.csv` (atualize a coluna `status`:
`pendente → cotando → comprado`).

## Fases

| Fase | Gatilho para iniciar | Objetivo | Investimento estimado* |
|---|---|---|---|
| **1 — Essencial** | Antes da 1ª obra como PEXUS | Instalar, manter e higienizar splits até 36k com qualidade e segurança | ~R$ 9 mil a R$ 24 mil |
| **2 — Crescimento** | ~8 a 10 serviços/mês ou 1º contrato de PMOC | Recolhimento de gás, diagnóstico avançado, comercial leve | ~R$ 8 mil a R$ 19 mil |
| **3 — Comercial/VRF** | 1º projeto comercial C2 ou contrato recorrente grande | Linhas longas, VRF, produtividade | ~R$ 7,5 mil a R$ 20 mil + software |

\* Somatório das faixas do CSV, valores de referência — **cotar com 3 fornecedores**.
Rode `python3 ferramentas-sw/pexus_ops.py ferramentas` para o total atualizado.

## Critérios de prioridade
- **A** — sem ela o serviço não é executado corretamente ou com segurança.
- **B** — aumenta produtividade/qualidade; comprar no 1º ou 2º mês.
- **C** — comprar quando houver demanda comprovada ou alugar.

## Regras de compra
1. Ferramentas de medição (vacuômetro, manifold, alicate, balança): priorizar marcas com
   assistência técnica e certificado de calibração no Brasil.
2. Fluido R-32 é levemente inflamável (A2L): ferramentas (bomba de vácuo, recolhedora,
   detector) devem ser **compatíveis com A2L**.
3. Itens de uso esporádico (andaime, oxiacetileno, termovisor): **alugar** antes de comprar.
4. Registrar cada ferramenta comprada com nº de série, data e nota fiscal (controle patrimonial
   e garantia) — informar ao James para depreciação.
5. Calibração/verificação: vacuômetro e manifold anualmente; balança semestral (peso padrão).
