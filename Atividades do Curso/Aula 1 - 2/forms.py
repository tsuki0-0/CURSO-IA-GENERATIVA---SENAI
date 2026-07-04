# Desafio 2: Formulário de Cadastro de Usuário (Entrada de Dados)
# Vou usar a Biblioteca Streamlit ->
import streamlit as st
# Título do Site
st.title("Informe seus Dados")

# Subtítulo para a Apresentação do Indivíduo
st.header("SE APRESENTE !")

# Nome do Indivíduo
st.text_input("Nome")

# Idade do Indivíduo
Idade = st.number_input("Idade", value = 0)
if Idade >= 18:
    st.success("Maior de Idade")
else:
     st.error("Menor de Idade")

# Cursos Feitos
st.checkbox("Aceitar os Termos de Uso")

# Botão para Enviar
if st.button("Enviar"):
    print = ("Obrigado, iremos estrar em contato !")
    st.success(print)