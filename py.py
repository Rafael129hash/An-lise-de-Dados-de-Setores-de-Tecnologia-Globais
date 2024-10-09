import streamlit as st
import pandas as pd
import json

# Carregar o arquivo CSV
df = pd.read_csv('Big_Japan_vs_China_Technology.csv')

# Exibir o dataframe no Streamlit
st.title("Visualização de Dados: Japão vs China - Tecnologia")
st.write("Exibindo as primeiras linhas do conjunto de dados:")
st.dataframe(df.head())  # Exibe as primeiras linhas do dataframe

# Criar a barra lateral com filtros
st.sidebar.title("Filtros")

# Filtro de ano
unique_years = df['Year'].unique()
selected_year = st.sidebar.selectbox("Selecione o ano:", unique_years)

# Filtro de setor tecnológico
unique_sectors = df['Tech Sector'].unique()
selected_sector = st.sidebar.selectbox("Selecione o setor tecnológico:", unique_sectors)

# Filtrar os dados com base nos filtros selecionados
filtered_data = df[(df['Year'] == selected_year) & (df['Tech Sector'] == selected_sector)]

# Exibir o resultado filtrado
st.sidebar.write("Dados filtrados:")
st.sidebar.dataframe(filtered_data)

# Filtrar o ano mais recente (2022) caso nada seja selecionado
df_2022 = df[df['Year'] == 2022]

# Encontrar o setor com maior investimento em P&D
top_rd_investment_sector_2022 = df_2022.loc[df_2022['R&D Investment (in USD)'].idxmax()]

# Formatar o valor do investimento com separador de milhar e duas casas decimais
investment_formatted = f"{top_rd_investment_sector_2022['R&D Investment (in USD)']:,.2f}"

# Exibir o resultado formatado
st.title("Setor com Maior Investimento em P&D em 2022")
st.write(f"O setor com maior investimento em P&D em 2022 é o **{top_rd_investment_sector_2022['Tech Sector']}** com um investimento de **{investment_formatted} USD**.")

# Criar os dados para o gráfico de P&D
data = {
    "labels": [top_rd_investment_sector_2022['Tech Sector']],
    "datasets": [{
        "label": "Investimento em P&D (USD)",
        "data": [top_rd_investment_sector_2022['R&D Investment (in USD)']],
        "backgroundColor": ["#4CAF50"],  # Cor do gráfico
    }]
}

# Gerar o código HTML e JavaScript para o Chart.js
chart_data = json.dumps(data)

# HTML para o gráfico
html_string = f"""
<div style="width: 100%; display: flex; justify-content: center;">
    <canvas id="myChart" width="400" height="200"></canvas>
</div>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
    const ctx = document.getElementById('myChart').getContext('2d');
    const myChart = new Chart(ctx, {{
        type: 'bar',
        data: {chart_data},
        options: {{
            scales: {{
                y: {{
                    beginAtZero: true
                }}
            }}
        }}
    }});
</script>
"""

# Exibir o gráfico no Streamlit
st.components.v1.html(html_string, height=300)

# Encontrar os países com maior cobertura de 5G por ano sem o aviso de depreciação
top_5g_coverage = df.loc[df.groupby('Year')['5G Network Coverage (%)'].idxmax()]

# Formatar os valores de cobertura de 5G para duas casas decimais
top_5g_coverage['5G Network Coverage (%)'] = top_5g_coverage['5G Network Coverage (%)'].apply(lambda x: f"{x:.2f}%")

# Exibir os resultados
st.title("Países com Maior Cobertura de 5G por Ano")
st.write(top_5g_coverage[['Year', 'Country', '5G Network Coverage (%)']])

# Criar os dados para o gráfico de cobertura de 5G
data = {
    "labels": top_5g_coverage['Year'].astype(str).tolist(),  # Anos como strings
    "datasets": [{
        "label": "Cobertura de 5G (%)",
        "data": [float(cov[:-1]) for cov in top_5g_coverage['5G Network Coverage (%)']],  # Remover '%' e converter para float
        "backgroundColor": "#2196F3",  # Cor do gráfico
    }]
}

# Gerar o código HTML e JavaScript para o Chart.js
chart_data = json.dumps(data)

# HTML para o gráfico
html_string = f"""
<div style="width: 100%; display: flex; justify-content: center;">
    <canvas id="myChart" width="400" height="200"></canvas>
</div>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
    const ctx = document.getElementById('myChart').getContext('2d');
    const myChart = new Chart(ctx, {{
        type: 'bar',
        data: {chart_data},
        options: {{
            scales: {{
                y: {{
                    beginAtZero: true,
                    title: {{
                        display: true,
                        text: 'Cobertura de 5G (%)'
                    }}
                }},
                x: {{
                    title: {{
                        display: true,
                        text: 'Ano'
                    }}
                }}
            }}
        }}
    }});
</script>
"""

# Exibir o gráfico no Streamlit
st.components.v1.html(html_string, height=300)

# Calcular a correlação
correlation = df['Number of Startups'].corr(df['Venture Capital Funding (in USD)'])

# Exibir a correlação
st.title("Correlação entre Startups e Financiamento de Capital de Risco")
st.write(f"A correlação entre o número de startups e o financiamento de capital de risco é de **{correlation:.2f}**.")

# Criar os dados para o gráfico de correlação
data = {
    "labels": df['Number of Startups'].astype(str).tolist(),
    "datasets": [{
        "label": "Financiamento de Capital de Risco (USD)",
        "data": df['Venture Capital Funding (in USD)'].tolist(),
        "backgroundColor": "rgba(75, 192, 192, 0.6)",  # Cor do ponto
        "borderColor": "rgba(75, 192, 192, 1)",  # Cor da borda do ponto
        "borderWidth": 1,
        "pointRadius": 5,
    }]
}

# Gerar o código HTML e JavaScript para o Chart.js
chart_data = json.dumps(data)

# HTML para o gráfico de correlação
html_string = f"""
<div style="width: 100%; display: flex; justify-content: center;">
    <canvas id="myScatterChart" width="400" height="200"></canvas>
</div>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
    const ctx = document.getElementById('myScatterChart').getContext('2d');
    const myScatterChart = new Chart(ctx, {{
        type: 'scatter',
        data: {{
            datasets: [{{
                label: 'Startups vs Financiamento',
                data: {json.dumps([{"x": startups, "y": funding} for startups, funding in zip(df['Number of Startups'], df['Venture Capital Funding (in USD)'])])},
                backgroundColor: 'rgba(75, 192, 192, 0.6)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1,
                pointRadius: 5,
            }}]
        }},
        options: {{
            scales: {{
                x: {{
                    title: {{
                        display: true,
                        text: 'Número de Startups'
                    }}
                }},
                y: {{
                    title: {{
                        display: true,
                        text: 'Financiamento de Capital de Risco (USD)'
                    }},
                    beginAtZero: true
                }}
            }}
        }}
    }});
</script>
"""

# Exibir o gráfico no Streamlit
st.components.v1.html(html_string, height=300)

# Encontrar o setor de tecnologia com maior exportação para cada país sem o aviso de depreciação
top_exports_by_country = df.loc[df.groupby('Country')['Tech Exports (in USD)'].idxmax()]

# Formatar os valores de exportação em USD para um formato mais legível (ex: bilhões)
top_exports_by_country['Tech Exports (in USD)'] = top_exports_by_country['Tech Exports (in USD)'].apply(lambda x: f"${x / 1e9:.2f}B")

# Configurar os dados para o gráfico de exportações
data = {
    "labels": top_exports_by_country['Country'].tolist(),
    "datasets": [{
        "label": "Exportações de Tecnologia (em Bilhões USD)",
        "data": top_exports_by_country['Tech Exports (in USD)'].str.replace('$', '').str.replace('B', '').astype(float).tolist(),
        "backgroundColor": "rgba(54, 162, 235, 0.6)",  # Cor das barras
        "borderColor": "rgba(54, 162, 235, 1)",  # Cor da borda das barras
        "borderWidth": 1
    }]
}

# Gerar o código HTML e JavaScript para o Chart.js
chart_data = json.dumps(data)

# HTML para o gráfico de exportações
html_string = f"""
<div style="width: 100%; display: flex; justify-content: center;">
    <canvas id="myBarChart" width="400" height="200"></canvas>
</div>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
    const ctx = document.getElementById('myBarChart').getContext('2d');
    const myBarChart = new Chart(ctx, {{
        type: 'bar',
        data: {{
            labels: {json.dumps(top_exports_by_country['Country'].tolist())},
            datasets: [{{
                label: 'Exportações de Tecnologia (em Bilhões USD)',
                data: {json.dumps(top_exports_by_country['Tech Exports (in USD)'].str.replace('$', '').str.replace('B', '').astype(float).tolist())},
                backgroundColor: 'rgba(54, 162, 235, 0.6)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }}]
        }},
        options: {{
            scales: {{
                y: {{
                    beginAtZero: true,
                    title: {{
                        display: true,
                        text: 'Exportações (Bilhões USD)'
                    }}
                }},
                x: {{
                    title: {{
                        display: true,
                        text: 'Países'
                    }}
                }}
            }},
            responsive: true,
            plugins: {{
                legend: {{
                    position: 'top',
                }},
                title: {{
                    display: true,
                    text: 'Setores com Maior Exportação por País'
                }}
            }}
        }}
    }});
</script>
"""

# Exibir o gráfico no Streamlit
st.components.v1.html(html_string, height=400)
