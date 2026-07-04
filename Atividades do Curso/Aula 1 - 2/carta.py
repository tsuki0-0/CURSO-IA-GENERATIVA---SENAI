# Cartão de Visitas de Digital
# Vou usar a Biblioteca Streamlit ->
import streamlit as st
# Título do Site
st.title("Cartão de Visita")

# Subtítulo para a Apresentação do Indivíduo
st.header("Se Apresente Porfavor !")

# Nome do Indivíduo
st.text_input("Nome")

# Idade do Indivíduo
st.text_input("Idade")

# Data do Indivíduo
st.text_input("Data")

# Horário do Indivíduo
st.text_input("Horário")

# Botão para Enviar
if st.button("Enviar"):
    print = ("Enviado")
    st.success(print)