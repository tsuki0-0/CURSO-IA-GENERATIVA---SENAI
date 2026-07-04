# Bibliotecas
import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

# Analise de Vendas
st.header('ANALISE DE VENDAS - PREVENDO')
d = pd.read_csv('teste.csv')

# print(d)
Vendas = pd.DataFrame({
'vendas': d['vendas'],
'temperatura':d['temperatura']
})
print(Vendas)

# Área do Gráfico
st.bar_chart(Vendas, x = 'temperatura', y= 'vendas')
modelo_venda = LinearRegression() 
modelo_venda.fit(Vendas[['temperatura']], Vendas['vendas'])


# h_estudo = st.slider('horas de estudos', 0,12,5)
temperatura = st.number_input('Temperarura', value = 0)
# n  =  np.array(temperatura)
valor_final = modelo_venda.predict([[temperatura]])
st.write(valor_final)

# Comportamento do Gráfico
st.metric(f'sua Venda' ,f'{min(valor_final[0], 1000.0):.1f}')
