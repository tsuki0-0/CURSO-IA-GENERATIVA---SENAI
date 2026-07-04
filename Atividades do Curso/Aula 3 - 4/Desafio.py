# Bibliotecas
import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression

# Cabeçalho do Site
st.header("Previsão de Vendas")

# Dados: [Investimento em Marketing] -> Faturamento
dados_vendas = pd.DataFrame({
    'investimento': [100, 200, 300, 400, 500, 600],
    'faturamento': [1200, 2500, 3200, 4800, 5100, 6300]
})

# Gráfico com X sendo o Investimento e Y o Faturamento
st.scatter_chart(dados_vendas, x ='investimento', y ='faturamento')

# X = investimento , y = faturamento
modelo_invest = LinearRegression() 
modelo_invest.fit(dados_vendas[['investimento']], dados_vendas['faturamento'])

# Configuração do Slider
invest_valor = st.slider('Escolha o valor a ser investido (R$):', 100,600,50)

# Realizando a previsão com o valor do slider
dados_previsao = pd.DataFrame({'investimento': [invest_valor]})
valor_final = modelo_invest.predict(dados_previsao)

# Como o Gráfico vai se comportar
st.metric(label='Faturamento Estimado:', value=f'R$ {valor_final[0]:.2f}')
