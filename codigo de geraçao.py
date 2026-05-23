import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# ==============================
# Configurações iniciais
# ==============================
ARQUIVO_CSV = 'ecommerce_preparados.csv'
PASTA_SAIDA = 'graficos'

os.makedirs(PASTA_SAIDA, exist_ok=True)

# Carrega os dados
df = pd.read_csv(ARQUIVO_CSV)

# Converte colunas numéricas relevantes (valores inválidos viram NaN)
for coluna in ['Nota', 'N_Avaliações', 'Desconto', 'Preço', 'Qtd_Vendidos_Cod']:
    df[coluna] = pd.to_numeric(df[coluna], errors='coerce')

# Estilo visual
sns.set_theme(style='whitegrid', context='talk')

# ==============================
# 1) Histograma
# ==============================
plt.figure(figsize=(10, 6))
sns.histplot(data=df, x='Preço', bins=30, kde=False, color='#1f77b4')
plt.title('Distribuição de Preços dos Produtos')
plt.xlabel('Preço (R$)')
plt.ylabel('Frequência de Produtos')
plt.tight_layout()
plt.savefig(f'{PASTA_SAIDA}/01_histograma_preco.png', dpi=180)
plt.close()

# ==============================
# 2) Gráfico de dispersão
# ==============================
plt.figure(figsize=(10, 6))
base_dispersao = df.dropna(subset=['Preço', 'Nota'])
sns.scatterplot(data=base_dispersao, x='Preço', y='Nota', alpha=0.6, s=40, color='#ff7f0e')
plt.title('Relação entre Preço e Nota')
plt.xlabel('Preço (R$)')
plt.ylabel('Nota do Produto')
plt.tight_layout()
plt.savefig(f'{PASTA_SAIDA}/02_dispersao_preco_nota.png', dpi=180)
plt.close()

# ==============================
# 3) Mapa de calor (correlação)
# ==============================
plt.figure(figsize=(9, 7))
corr = df[['Nota', 'N_Avaliações', 'Desconto', 'Preço', 'Qtd_Vendidos_Cod']].corr(numeric_only=True)
sns.heatmap(corr, annot=True, fmt='.2f', cmap='YlGnBu', linewidths=0.5)
plt.title('Mapa de Calor de Correlação entre Variáveis Numéricas')
plt.xlabel('Variáveis')
plt.ylabel('Variáveis')
plt.tight_layout()
plt.savefig(f'{PASTA_SAIDA}/03_mapa_calor_correlacao.png', dpi=180)
plt.close()

# ==============================
# 4) Gráfico de barras (top marcas)
# ==============================
plt.figure(figsize=(12, 7))
top_marcas = df['Marca'].fillna('Não informado').value_counts().head(10)
sns.barplot(x=top_marcas.values, y=top_marcas.index, color='#4c78a8')
plt.title('Top 10 Marcas com Maior Número de Produtos')
plt.xlabel('Quantidade de Produtos')
plt.ylabel('Marca')
plt.tight_layout()
plt.savefig(f'{PASTA_SAIDA}/04_barra_top_marcas.png', dpi=180)
plt.close()

# ==============================
# 5) Gráfico de pizza (gênero)
# ==============================
plt.figure(figsize=(9, 9))
genero = df['Gênero'].fillna('Não informado').value_counts().head(6)
plt.pie(genero.values, labels=genero.index, autopct='%1.1f%%', startangle=140)
plt.title('Participação dos Principais Gêneros nos Produtos')
plt.tight_layout()
plt.savefig(f'{PASTA_SAIDA}/05_pizza_genero.png', dpi=180)
plt.close()

# ==============================
# 6) Gráfico de densidade
# ==============================
plt.figure(figsize=(10, 6))
sns.kdeplot(data=df, x='Preço', fill=True, color='#2ca02c', bw_adjust=1.1)
plt.title('Densidade de Probabilidade dos Preços')
plt.xlabel('Preço (R$)')
plt.ylabel('Densidade')
plt.tight_layout()
plt.savefig(f'{PASTA_SAIDA}/06_densidade_preco.png', dpi=180)
plt.close()

# ==============================
# 7) Gráfico de regressão
# ==============================
plt.figure(figsize=(10, 6))
base_regressao = df.dropna(subset=['N_Avaliações', 'Qtd_Vendidos_Cod'])

# Remove 1% de extremos para melhorar visualização
q99_x = base_regressao['N_Avaliações'].quantile(0.99)
q99_y = base_regressao['Qtd_Vendidos_Cod'].quantile(0.99)
base_regressao_plot = base_regressao[
    (base_regressao['N_Avaliações'] <= q99_x) &
    (base_regressao['Qtd_Vendidos_Cod'] <= q99_y)
]

sns.regplot(
    data=base_regressao_plot,
    x='N_Avaliações',
    y='Qtd_Vendidos_Cod',
    scatter_kws={'alpha': 0.35, 's': 30},
    line_kws={'color': 'red'}
)
plt.title('Regressão: Avaliações vs Quantidade Vendida (sem extremos 1%)')
plt.xlabel('Número de Avaliações')
plt.ylabel('Quantidade Vendida (codificada)')
plt.tight_layout()
plt.savefig(f'{PASTA_SAIDA}/07_regressao_avaliacoes_vendas.png', dpi=180)
plt.close()

print('Gráficos gerados com sucesso em ./graficos')
