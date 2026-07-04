# Procoding -> Código bruto !
# Vou usar a Biblioteca Streamlit ->
import streamlit as st

st.title("Calculadora Simples")
n1 = st.number_input("1 Número:",) 
n2 = st.number_input("2 Número:", value = 0.0)

# Identificação ->
soma, sub, div, mult = st.columns(4)

if soma.button("Soma"):
    calcular   =  n1  + n2 
    st.success(calcular)

elif sub.button("subtração"):    
    calcular   =  n1  - n2 
    st.success(calcular)

elif div.button("Divisão"):    
    calcular   =  n1  / n2 
    st.success(calcular)

elif mult.button("Multiplicação"):    
    calcular   =  n1  * n2 
    st.success(calcular)