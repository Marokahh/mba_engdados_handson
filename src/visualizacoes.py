import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


# ==============================================================================
# CONFIGURAÇÕES VISUAIS
# ==============================================================================

sns.set_theme(style="whitegrid")

plt.rcParams.update({
    "font.size": 10,
    "axes.titlesize": 13,
    "axes.titleweight": "bold",
    "figure.autolayout": True,
})


# ==============================================================================
# FUNÇÕES AUXILIARES
# ==============================================================================

def adicionar_rotulos_verticais(ax):
    """Adiciona porcentagens no topo das barras verticais."""
    for barra in ax.patches:
        altura = barra.get_height()

        if altura > 0:
            ax.annotate(
                f"{altura:.1f}%",
                (
                    barra.get_x() + barra.get_width() / 2,
                    altura
                ),
                ha="center",
                va="bottom",
                xytext=(0, 4),
                textcoords="offset points",
                fontsize=9,
                fontweight="semibold",
            )


def adicionar_rotulos_horizontais(ax):
    """Adiciona porcentagens na extremidade das barras horizontais."""
    for barra in ax.patches:
        largura = barra.get_width()

        if largura > 0:
            ax.annotate(
                f"{largura:.1f}%",
                (
                    largura,
                    barra.get_y() + barra.get_height() / 2
                ),
                ha="left",
                va="center",
                xytext=(5, 0),
                textcoords="offset points",
                fontsize=8.5,
                fontweight="semibold",
            )


# ==============================================================================
# 1. TAXA DE AUSÊNCIA POR ANO - CIÊNCIAS DA NATUREZA
# ==============================================================================

dados_por_ano = {
    "Ano": ["2019", "2020", "2021", "2022", "2023"],
    "Taxa_Ausencia": [27.1, 55.1, 33.7, 32.2, 31.5],
}

df_ano = pd.DataFrame(dados_por_ano)

plt.figure(figsize=(9, 5))

plt.plot(
    df_ano["Ano"],
    df_ano["Taxa_Ausencia"],
    marker="o",
    linewidth=2.5,
    markersize=8,
    color="black",
)

plt.title("Taxa de Ausência no ENEM por Ano (Ciências da Natureza)")
plt.xlabel("Ano")
plt.ylabel("Taxa de ausência (%)")
plt.ylim(0, 100)

# Porcentagem em todos os pontos
for _, linha in df_ano.iterrows():
    plt.annotate(
        f"{linha['Taxa_Ausencia']:.1f}%",
        (linha["Ano"], linha["Taxa_Ausencia"]),
        textcoords="offset points",
        xytext=(0, 10),
        ha="center",
        fontweight="bold",
    )

plt.grid(False)
plt.show()


# ==============================================================================
# 2. COMPARAÇÃO DE AUSÊNCIA - 1º DIA VS 2º DIA
# ==============================================================================

dados_dias = {
    "Ano": ["2019", "2020", "2021", "2022", "2023"],
    "1º dia - CN": [27.14, 55.06, 33.70, 32.20, 31.50],
    "2º dia - CH": [22.80, 52.30, 29.80, 28.20, 28.20],
}

df_dias = pd.DataFrame(dados_dias)

plt.figure(figsize=(9.5, 5.5))

plt.plot(
    df_dias["Ano"],
    df_dias["1º dia - CN"],
    marker="o",
    linewidth=2.2,
    markersize=7,
    label="1º dia - CN",
    color="#1f77b4",
)

plt.plot(
    df_dias["Ano"],
    df_dias["2º dia - CH"],
    marker="o",
    linewidth=2.2,
    markersize=7,
    label="2º dia - CH",
    color="#2ca02c",
)

plt.title("Taxa de Ausência: Primeiro x Segundo Dia")
plt.xlabel("Ano")
plt.ylabel("Taxa de ausência (%)")
plt.ylim(20, 60)

# Porcentagens do 1º dia
for _, linha in df_dias.iterrows():
    plt.annotate(
        f"{linha['1º dia - CN']:.1f}%",
        (linha["Ano"], linha["1º dia - CN"]),
        textcoords="offset points",
        xytext=(0, 10),
        ha="center",
        fontweight="bold",
    )

# Porcentagens do 2º dia
for _, linha in df_dias.iterrows():
    plt.annotate(
        f"{linha['2º dia - CH']:.1f}%",
        (linha["Ano"], linha["2º dia - CH"]),
        textcoords="offset points",
        xytext=(0, -18),
        ha="center",
        fontweight="bold",
    )

plt.legend()
plt.grid(False)
plt.show()


# ==============================================================================
# 3. PERFIL DEMOGRÁFICO - SEXO
# ==============================================================================

dados_sexo = {
    "Sexo": ["Feminino", "Masculino"],
    "Taxa_Ausencia": [37.07, 37.45],
}

df_sexo = pd.DataFrame(dados_sexo)

fig, ax = plt.subplots(figsize=(6.5, 5))

sns.barplot(
    data=df_sexo,
    x="Sexo",
    y="Taxa_Ausencia",
    hue="Sexo",
    palette=["#800080", "#ff7f0e"],
    legend=False,
    ax=ax,
)

ax.set_title("Taxa de Ausência por Sexo")
ax.set_xlabel("Sexo")
ax.set_ylabel("Taxa de ausência (%)")
ax.set_ylim(0, 45)

adicionar_rotulos_verticais(ax)

plt.grid(False)
plt.show()


# ==============================================================================
# 4. PERFIL DEMOGRÁFICO - FAIXA ETÁRIA
# ==============================================================================

dados_idade = {
    "Faixa_Etaria": [
        "Menor de 17 anos",
        "17 anos",
        "18 anos",
        "19 anos",
        "20 anos",
        "21 anos",
        "22 anos",
        "23 anos",
        "24 anos",
        "25 anos",
        "26 a 30 anos",
        "31 a 35 anos",
        "36 a 40 anos",
        "41 a 45 anos",
        "46 a 50 anos",
        "51 a 55 anos",
        "56 a 60 anos",
        "61 a 65 anos",
        "66 a 70 anos",
        "Maior de 70 anos",
    ],
    "Taxa_Ausencia": [
        18.57,
        19.30,
        27.17,
        35.78,
        41.31,
        45.74,
        48.69,
        51.64,
        53.85,
        55.82,
        58.03,
        59.02,
        57.91,
        56.07,
        53.61,
        52.38,
        51.15,
        49.43,
        48.32,
        49.43,
    ],
}

df_idade = pd.DataFrame(dados_idade)

fig, ax = plt.subplots(figsize=(10, 8.5))

sns.barplot(
    data=df_idade,
    y="Faixa_Etaria",
    x="Taxa_Ausencia",
    hue="Faixa_Etaria",
    palette=sns.light_palette(
        "#14243A",
        n_colors=len(df_idade)
    ),
    legend=False,
    ax=ax,
)

ax.set_title("Taxa de Ausência por Faixa Etária")
ax.set_xlabel("Taxa de ausência (%)")
ax.set_ylabel("Faixa Etária")
ax.set_xlim(0, 68)

adicionar_rotulos_horizontais(ax)

plt.grid(False)
plt.show()


# ==============================================================================
# 5. PERFIL DEMOGRÁFICO - COR / RAÇA
# ==============================================================================

dados_raca = {
    "Cor_Raca": [
        "Não declarado",
        "Branca",
        "Preta",
        "Parda",
        "Amarela",
        "Indígena",
        "Sem informação",
    ],
    "Taxa_Ausencia": [
        40.64,
        32.46,
        42.06,
        39.55,
        38.07,
        45.92,
        60.00,
    ],
}

df_raca = pd.DataFrame(dados_raca)

fig, ax = plt.subplots(figsize=(10, 5.5))

sns.barplot(
    data=df_raca,
    x="Cor_Raca",
    y="Taxa_Ausencia",
    hue="Cor_Raca",
    palette=sns.color_palette(
        "Blues",
        n_colors=len(df_raca)
    ),
    legend=False,
    ax=ax,
)

ax.set_title("Taxa de Ausência por Cor/Raça Declarada")
ax.set_xlabel("Cor / Raça")
ax.set_ylabel("Taxa de ausência (%)")
ax.set_ylim(0, 70)

plt.xticks(rotation=20, ha="right")

adicionar_rotulos_verticais(ax)

plt.grid(False)
plt.show()


# ==============================================================================
# 6. PERFIL SOCIOECONÔMICO - RENDA FAMILIAR (Q006)
# ==============================================================================

dados_renda = {
    "Faixa_Renda": [
        "A — Nenhuma renda",
        "B — Até R$ 998",
        "C — R$ 998 a R$ 1.497",
        "D — R$ 1.497 a R$ 1.996",
        "E — R$ 1.996 a R$ 2.495",
        "F — R$ 2.495 a R$ 2.994",
        "G — R$ 2.994 a R$ 3.992",
        "H — R$ 3.992 a R$ 4.990",
        "I — R$ 4.990 a R$ 5.988",
        "J — R$ 5.988 a R$ 6.986",
        "K — R$ 6.986 a R$ 7.984",
        "L — R$ 7.984 a R$ 8.982",
        "M — R$ 8.982 a R$ 9.980",
        "N — R$ 9.980 a R$ 11.976",
        "O — R$ 11.976 a R$ 14.970",
        "P — R$ 14.970 a R$ 19.960",
        "Q — Mais de R$ 19.960",
    ],
    "Taxa_Ausencia": [
        47.20,
        43.00,
        40.70,
        39.10,
        33.60,
        32.90,
        27.40,
        24.60,
        22.10,
        20.60,
        20.00,
        19.80,
        20.10,
        19.70,
        19.60,
        20.00,
        22.30,
    ],
}

df_renda = pd.DataFrame(dados_renda)

fig, ax = plt.subplots(figsize=(12, 9))

sns.barplot(
    data=df_renda,
    y="Faixa_Renda",
    x="Taxa_Ausencia",
    hue="Faixa_Renda",
    palette=sns.dark_palette(
        "#DBB5AD",
        n_colors=len(df_renda),
        reverse=True,
    ),
    legend=False,
    ax=ax,
)

ax.set_title("Taxa de Ausência por Faixa de Renda Familiar (Q006)")
ax.set_xlabel("Taxa de ausência (%)")
ax.set_ylabel("Faixa de renda familiar")

ax.set_xlim(0, 55)

adicionar_rotulos_horizontais(ax)

plt.grid(False)
plt.show()

# ==============================================================================
# 7. PERFIL GEOGRÁFICO - UNIDADE DA FEDERAÇÃO
# ==============================================================================

dados_uf = {
    "UF": [
        "AM", "RO", "RR", "MS", "MT", "AP", "AC", "TO",
        "GO", "ES", "RJ", "DF", "SP", "PR", "RS", "PA",
        "SC", "MG", "BA", "MA", "AL", "PE", "CE", "RN",
        "PB", "SE", "PI",
    ],
    "Taxa_Ausencia": [
        52.10, 45.11, 44.46, 41.77, 41.51, 41.51, 40.05,
        39.95, 39.89, 38.06, 37.69, 37.53, 37.42, 37.31,
        37.26, 37.20, 36.94, 36.56, 36.51, 35.81, 34.95,
        34.89, 34.46, 32.80, 32.63, 32.58, 32.42,
    ],
}

df_uf = pd.DataFrame(dados_uf)

fig, ax = plt.subplots(figsize=(10, 10))

sns.barplot(
    data=df_uf,
    y="UF",
    x="Taxa_Ausencia",
    hue="UF",
    palette=sns.light_palette(
        "#D50048",
        n_colors=len(df_uf),
        reverse=True,
    ),
    legend=False,
    ax=ax,
)

ax.set_title("Taxa de Ausência por Unidade da Federação (UF)")
ax.set_xlabel("Taxa de ausência (%)")
ax.set_ylabel("UF")
ax.set_xlim(0, 60)

adicionar_rotulos_horizontais(ax)

plt.grid(False)
plt.show()


# ==============================================================================
# 8. PERFIL ESCOLAR - TIPO DE ESCOLA
# ==============================================================================

dados_escola = {
    "Tipo_Escola": [
        "Não respondeu",
        "Pública",
        "Privada",
    ],
    "Taxa_Ausencia": [
        41.75,
        30.64,
        8.44,
    ],
}

df_escola = pd.DataFrame(dados_escola)

fig, ax = plt.subplots(figsize=(7.5, 5))

sns.barplot(
    data=df_escola,
    x="Tipo_Escola",
    y="Taxa_Ausencia",
    hue="Tipo_Escola",
    palette=sns.color_palette(
        "YlOrBr",
        n_colors=len(df_escola)
    ),
    legend=False,
    ax=ax,
)

ax.set_title("Taxa de Ausência por Tipo de Escola")
ax.set_xlabel("Tipo de escola")
ax.set_ylabel("Taxa de ausência (%)")
ax.set_ylim(0, 50)

adicionar_rotulos_verticais(ax)

plt.grid(False)
plt.show()


# ==============================================================================
# FINALIZAÇÃO
# ==============================================================================

print("\nVisualizações geradas com sucesso!")

# Rodei com  python .\src\visualizacoes.py 