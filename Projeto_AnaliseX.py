import seaborn as sns
import matplotlib.pyplot as plt
import mysql.connector
import pandas as pd

# Conectar com o banco de dados
con = mysql.connector.connect(
    host="localhost",                     # host local
    user="root",                          # usuario do MySQL
    password="senhaimprovisada123!",      # senha para ter acesso ao banco de dados
    database="projetox"
)

# Consulta SQL
query = """
SELECT v.data_venda, p.nome AS produto, p.categoria, c.nome AS cliente, c.cidade,
       p.preco, v.quantidade, (p.preco * v.quantidade) AS total
FROM vendas v
JOIN produtos p ON v.id_produto = p.id
JOIN clientes c ON v.id_cliente = c.id
"""

# Carrega dados usando pandas em um DataFrame (Base para grande maioria de pesquisas de analise)
df = pd.read_sql(query, con)


# Imprime as 5 primeiras linhas do DataFrame
print(df.head())


# Anotações sobre bibliotecas de visualização de dados (importdas no começo do código):

# Matplotlib:
# Biblioteca base para criação de gráficos.
# O módulo 'pyplot' (importado como 'plt') simplifica a criação de gráficos
# como linhas, barras, pizza, dispersão, entre outros.

# Seaborn (importado como 'sns'):
# Biblioteca baseada no Matplotlib, focada em gráficos estatísticos.
# Oferece uma sintaxe mais simples e gráficos mais bonitos e informativos.

# Ambas as bibliotecas são usadas para transformar dados em gráficos,
# facilitando a análise e interpretação visual.



# Converter coluna de data
df['data_venda'] = pd.to_datetime(df['data_venda'])
df['mes'] = df['data_venda'].dt.to_period('M')


# Total de vendas por mês
vendas_mes = df.groupby('mes')['total'].sum()


# Plotar gráfico de barras
plt.figure(figsize=(10, 5))
plt.bar(vendas_mes.index.astype(str), vendas_mes.values, color="#3CE14A")
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.title('Total de Vendas por Mês', fontsize=16)
plt.ylabel('R$', fontsize=12)
plt.xlabel('Mês', fontsize=12)
for index, value in enumerate(vendas_mes):
    plt.text(index, value + 10, f'{value:.0f}', ha='center', fontsize=9)
plt.tight_layout()

# Salvar imagem
plt.savefig("vendas_por_mes.png")
plt.show()

#Funções importantes do 'plt' usadas:
# - plt.figure(): cria uma figura (área para o gráfico).
# - plt.title(), plt.xlabel(), plt.ylabel(): definem título e rótulos dos eixos.
# - plt.show(): exibe o gráfico na tela.
# - plt.savefig(): salva o gráfico como imagem (PNG, JPG, etc.).


# Converte em uma tabela em excel:
df.to_excel("relatorio_vendas.xlsx", index=False)

