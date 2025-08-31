import pandas as pd
import numpy as np
from datetime import datetime, timezone
import matplotlib.pyplot as plt
from pandas.plotting import scatter_matrix

df = pd.read_csv("lab01_data.csv")


df["createdAt"] = pd.to_datetime(df["createdAt"], utc=True, errors="coerce")
df["updatedAt"] = pd.to_datetime(df["updatedAt"], utc=True, errors="coerce")

# 🕒 Calcular idade e dias desde última atualização
agora_utc = datetime.now(timezone.utc)
df["idade_anos"] = (agora_utc - df["createdAt"]).dt.days / 365
df["dias_desde_update"] = (agora_utc - df["updatedAt"]).dt.days


df["primaryLanguage"] = df["primaryLanguage"].fillna("Unknown")


df["issues_total_aj"] = df["issues"].replace(0, np.nan)
df["percentual_issues_fechadas"] = (df["closedIssues"] / df["issues_total_aj"]) * 100

# 🔝 Top 10 linguagens (barra)
contagem_linguagens = df["primaryLanguage"].value_counts().head(10)
plt.figure()
contagem_linguagens.plot(kind="bar")
plt.title("Top 10 Linguagens por Número de Repositórios")
plt.xlabel("Linguagem")
plt.ylabel("Repositórios")
plt.tight_layout()
plt.show()

# Scatter plot (Top 5 linguagens)
top_langs = df["primaryLanguage"].value_counts().head(5).index
df_pair = df[df["primaryLanguage"].isin(top_langs)]

plt.figure(figsize=(10, 6))
for lang in top_langs:
    sub_df = df_pair[df_pair["primaryLanguage"] == lang]
    plt.scatter(sub_df["idade_anos"], sub_df["mergedPullRequests"], label=lang, alpha=0.6, s=50)
plt.title("Dispersão: Idade do Repositório vs PRs Aceitas (Top 5 Linguagens)")
plt.xlabel("Idade do Repositório (anos)")
plt.ylabel("PRs Aceitas")
plt.legend()
plt.tight_layout()
plt.show()

# Linha mediana de PRs aceitas por ano
df["ano_criacao"] = df["createdAt"].dt.year
serie_linha = df.groupby("ano_criacao")["mergedPullRequests"].median().dropna()
plt.figure()
plt.plot(serie_linha.index, serie_linha.values, marker="o")
plt.title("Mediana de PRs Aceitas por Ano de Criação do Repositório")
plt.xlabel("Ano de criação")
plt.ylabel("PRs aceitas (mediana)")
plt.tight_layout()
plt.show()

# 🔄 4º gráfico: Violino para Distribuição de Dias desde a Última Atualização
plt.figure()
plt.violinplot(df["dias_desde_update"].dropna(), showmedians=True, showmeans=True)
plt.title("Distribuição de Dias desde a Última Atualização")
plt.ylabel("Dias")
plt.tight_layout()
plt.show()

# Boxplot PRs aceitas sem outliers
plt.figure()
plt.boxplot(df["mergedPullRequests"].dropna(), vert=True, showfliers=False)
plt.title("Distribuição de PRs Aceitas (sem outliers)")
plt.ylabel("PRs aceitas")
plt.tight_layout()
plt.show()

# Correlação entre métricas
cols_corr = ["idade_anos","mergedPullRequests","releases","dias_desde_update","issues","closedIssues","percentual_issues_fechadas"]
mat = df[cols_corr].astype(float).corr()
plt.figure()
plt.imshow(mat, interpolation="nearest", aspect="auto")
plt.title("Correlação entre Métricas")
plt.xticks(range(len(cols_corr)), cols_corr, rotation=45, ha="right")
plt.yticks(range(len(cols_corr)), cols_corr)
plt.colorbar()
plt.tight_layout()
plt.show()

# Matriz de dispersão
amostra = df[["idade_anos","mergedPullRequests","releases","dias_desde_update"]].dropna()
if len(amostra) > 1000:
    amostra = amostra.sample(1000, random_state=42)
axs = scatter_matrix(amostra, figsize=(8,8), diagonal="hist")
for ax in axs[:,0]:
    ax.yaxis.label.set_rotation(0)
    ax.yaxis.label.set_ha("right")
for ax in axs[-1,:]:
    ax.xaxis.label.set_rotation(45)
    ax.xaxis.label.set_ha("right")
plt.suptitle("Matriz de Dispersão (Amostra)")
plt.tight_layout()
plt.show()

# Violino PRs por top 5 linguagens
top5_langs = df["primaryLanguage"].value_counts().head(5).index.tolist()
dados_violin = [df.loc[df["primaryLanguage"]==lang,"mergedPullRequests"].dropna().values for lang in top5_langs]
plt.figure()
plt.violinplot(dados_violin, showmedians=True, showmeans=False)
plt.title("Distribuição de PRs Aceitas por Linguagem (Top 5)")
plt.xlabel("Linguagem")
plt.ylabel("PRs aceitas")
plt.xticks(range(1,len(top5_langs)+1), top5_langs, rotation=0)
plt.tight_layout()
plt.show()

# Issues abertas vs fechadas (Top 8 linguagens)
agg_issues = df.groupby("primaryLanguage")[["issues","closedIssues"]].sum().sort_values("issues",ascending=False).head(8)
agg_issues["abertas"] = (agg_issues["issues"] - agg_issues["closedIssues"]).clip(lower=0)

langs = agg_issues.index.tolist()
fechadas = agg_issues["closedIssues"].values
abertas = agg_issues["abertas"].values

x = np.arange(len(langs))
plt.figure()
plt.bar(x, abertas, label="Abertas")
plt.bar(x, fechadas, bottom=abertas, label="Fechadas")
plt.title("Issues Abertas vs Fechadas por Linguagem (Top 8)")
plt.xlabel("Linguagem")
plt.ylabel("Quantidade de Issues")
plt.xticks(x, langs, rotation=0)
plt.legend()
plt.tight_layout()
plt.show()

# Scatter PRs x Releases
plt.figure()
plt.scatter(df["mergedPullRequests"], df["releases"], alpha=0.5)
plt.title("Relação entre PRs Aceitas e Releases")
plt.xlabel("PRs aceitas")
plt.ylabel("Releases")
plt.tight_layout()
plt.show()

# Medianas e top 10 linguagens
print("Mediana da idade (anos):", round(df["idade_anos"].median(),2))
print("Mediana de PRs aceitas:", int(df["mergedPullRequests"].median()))
print("Mediana de releases:", int(df["releases"].median()))
print("Mediana de dias desde última atualização:", int(df["dias_desde_update"].median()))
print("Mediana de % issues fechadas:", round(df["percentual_issues_fechadas"].median(),2))
print("Top 10 linguagens:\n", contagem_linguagens)
print("\n✅ Gráficos exibidos!")
