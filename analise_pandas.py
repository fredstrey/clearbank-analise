"""RO1 — Análise Financeira ClearBank com pandas.

Versão alternativa da leitura e do agrupamento usando pandas, para comparar com
a solução nativa (módulo csv) do notebook. Os valores devem ser idênticos.

Uso:
    python analise_pandas.py
"""
import pandas as pd

ARQUIVO_CSV = "transacoes.csv"
LIMITE_SUSPEITO = 10000.00
TIPOS_VALIDOS = ["credito", "debito"]


def carregar_e_limpar(caminho):
    """Lê o CSV e aplica as mesmas regras de validação da solução nativa."""
    df = pd.read_csv(caminho, dtype=str)

    df["valor_num"] = pd.to_numeric(df["valor"], errors="coerce")
    df["data_dt"] = pd.to_datetime(df["data"], format="%Y-%m-%d", errors="coerce")

    valido = (
        df["id"].str.fullmatch(r"\d+", na=False)
        & df["cliente_id"].str.strip().ne("") & df["cliente_id"].notna()
        & df["data_dt"].notna()
        & df["tipo"].str.lower().isin(TIPOS_VALIDOS)
        & df["valor_num"].notna() & (df["valor_num"] > 0)
    )

    limpo = df[valido].copy()
    limpo["tipo"] = limpo["tipo"].str.lower()
    limpo["mes"] = limpo["data_dt"].dt.strftime("%Y-%m")
    invalidas = len(df) - len(limpo)
    return limpo, invalidas


def metricas_por_mes(grupo):
    """Calcula as métricas de um grupo (mês)."""
    credito = grupo.loc[grupo["tipo"] == "credito", "valor_num"].sum()
    debito = grupo.loc[grupo["tipo"] == "debito", "valor_num"].sum()
    return pd.Series({
        "quantidade": len(grupo),
        "total_credito": round(credito, 2),
        "total_debito": round(debito, 2),
        "saldo": round(credito - debito, 2),
        "media": round(grupo["valor_num"].mean(), 2),
        "maior_valor": round(grupo["valor_num"].max(), 2),
        "menor_valor": round(grupo["valor_num"].min(), 2),
    })


def main():
    limpo, invalidas = carregar_e_limpar(ARQUIVO_CSV)

    resumo = limpo.groupby("mes").apply(metricas_por_mes, include_groups=False)
    print("===== RESUMO MENSAL (pandas) =====")
    print(resumo.to_string())

    print(f"\nTransações válidas: {len(limpo)} | inválidas: {invalidas}")

    suspeitas = limpo[limpo["valor_num"] > LIMITE_SUSPEITO]
    print("\n===== TRANSAÇÕES SUSPEITAS =====")
    if suspeitas.empty:
        print("Nenhuma transação suspeita encontrada.")
    else:
        for _, t in suspeitas.iterrows():
            print(f"ID: {t['id']} | Cliente: {t['cliente_id']} | "
                  f"Data: {t['data']} | Valor: R$ {t['valor_num']:,.2f}")


if __name__ == "__main__":
    main()
