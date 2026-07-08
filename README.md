# 💰 ClearBank — Análise Financeira com Python

Projeto final do módulo de Python aplicado à análise de dados. O notebook lê e valida um
arquivo CSV de transações bancárias, agrupa os dados por mês, calcula métricas financeiras,
sinaliza transações suspeitas e exporta o resultado em JSON.

## 📂 Estrutura do repositório

```
clearbank-analise/
├── desafio-final.ipynb   ← notebook principal (com saídas salvas)   ✅ obrigatório
├── transacoes.csv        ← dados de teste (gerado na Parte 0 do notebook)
├── relatorio.json        ← saída gerada pelo notebook
├── analise_pandas.py     ← versão alternativa com pandas (RO1, opcional)
├── grafico.png           ← gráfico de saldo mensal (RO2, opcional)
└── README.md             ← este arquivo
```

## ▶️ Como executar

**Google Colab ou Jupyter (Python 3.10+):**

1. Abra o `desafio-final.ipynb`.
2. Rode todas as células em ordem (`Runtime → Run all` no Colab, ou `Cell → Run All` no Jupyter).
3. A *Célula de Execução Principal* (Parte 8) chama todas as funções e produz o relatório final.

A Parte 0 do notebook gera o `transacoes.csv` automaticamente, então ele roda do zero em
qualquer ambiente sem precisar de arquivos externos.

**Versão pandas (opcional):**

```bash
pip install pandas matplotlib
python analise_pandas.py
```

## 📤 O que o notebook gera

- **No terminal:** resumo da limpeza (linhas lidas / válidas / inválidas), relatório mensal
  formatado em padrão monetário brasileiro (`R$ 1.234,56`), período analisado e lista de
  transações suspeitas.
- **Arquivo `relatorio.json`:** relatório completo com `gerado_em`, totais, período e o
  `resumo_mensal` por mês (quantidade, total de crédito/débito, saldo, média, maior e menor valor).
- **Arquivo `grafico.png`** (RO2): gráfico de barras com o saldo mensal.

## 🧱 Como o código está organizado

| Função | Responsabilidade |
|---|---|
| `ler_transacoes()` | Lê o CSV com `csv.DictReader` e trata `FileNotFoundError` |
| `validar_data()` / `validar_valor()` | Conversões com `try/except` (data e valor) |
| `validar_transacao()` | Valida uma linha e devolve o registro limpo (ou `None`) |
| `calcular_periodo()` | Datas mais antiga/recente e intervalo em dias |
| `gerar_relatorio()` | Agrupa por mês, calcula métricas e marca suspeitas |
| `exibir_relatorio()` | Imprime o relatório formatado |
| `salvar_json()` | Exporta o relatório em `relatorio.json` |
| `main()` | Orquestra todas as etapas |

## 🔎 Regras de validação

Uma linha é **descartada silenciosamente** se: `id` vazio ou não numérico; `cliente_id` vazio;
`data` fora do formato `AAAA-MM-DD`; `tipo` diferente de `credito`/`debito`; ou `valor` não
numérico ou menor/igual a zero.

Transações com valor acima de **R$ 10.000,00** são marcadas como suspeitas
(`LIMITE_SUSPEITO`).

## 📊 Dados de teste

O `transacoes.csv` inclui **18 registros válidos** em 4 meses (2026-01 a 2026-04),
**7 registros inválidos** (um por regra de validação) e **3 transações acima de R$ 10.000,00**.
