# Importando a Bilioteca Streamlit
import streamlit as st

#Título do Site Web
title = st.header("Qual sua área de Interesse")

if "options" not in st.session_state:
    st.session_state.options = "opções"
    st.session_state.disable = False

# Coluna
col1, col2 = st.columns(2)
with col1:
    accept_new_options=True,
    st.selectbox( options = ("Python","HTML","CSS","C/C+/C++","SQL","Git"))

# Cursos
with col2:
    option = st.selectbox(
    "Aceitar os Termos de Uso",
    "Você prescisa aceitar os termos",
    st.box(st.selectbox)    
)

# Store the initial value of widgets in session state
if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"
    st.session_state.disabled = False

col1, col2, col3 = st.columns(3)

with col1:
    option = st.title(
    'Cursos',
    ["Pyton","SQL","GO","C","C+","C++","HTML","Java","C#"],
    label_visibility=st.session_state.visibility,
    disabled = st.session_state.disabled,
    )
with col2:
    option = st.selectbox(
        "How would you like to be contacted?",
        ["Email", "Home phone", "Mobile phone"],
        label_visibility=st.session_state.visibility,
        disabled = st.session_state.disabled,
    )

with col3:
    st.checkbox("Prefire não responder", key="disabled")
    st.radio(
        "selecione aqui 👉",
        key="visibility",
        options=["visible", "hidden", "collapsed"],
    )

# Botão para Enviar
if st.button["Enviar"]:
    print = ["Obrigado, iremos estrar em contato !"]
    st.success[print]