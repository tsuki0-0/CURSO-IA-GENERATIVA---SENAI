import streamlit as st

# Título do Site Web
st.header("🎓 Painel de Interesses e Cursos")

# Inicializando o Session State (Garante que as variáveis existam ao carregar a página)
if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"
if "disabled" not in st.session_state:
    st.session_state.disabled = False

# --- CONFIGURAÇÕES DE CONTROLE (Coluna da Direita/Visual) ---
# Movido para cima para que o usuário possa interagir e afetar o resto da página
col_ctrl1, col_ctrl2 = st.columns(2)

with col_ctrl1:
    # O componente st.checkbox com a chave "disabled" altera diretamente o st.session_state.disabled
    st.checkbox("Desabilitar formulário", key="disabled")

with col_ctrl2:
    # O st.radio com a chave "visibility" altera diretamente o st.session_state.visibility
    st.radio(
        "Visibilidade dos rótulos 👉",
        key="visibility",
        options=["visible", "hidden", "collapsed"],
        horizontal=True
    )

st.divider()

# --- FORMULÁRIO DE SELEÇÃO (Requisito do Desafio 3) ---

col1, col2 = st.columns(2)

with col1:
    # REQUISITO 1: Escolher APENAS UM curso (st.selectbox)
    curso_unico = st.selectbox(
        "Qual seu Curso Principal de Interesse?",
        options=["Python", "Web Design", "Ciência de Dados", "DevOps", "Java"],
        label_visibility=st.session_state.visibility,
        disabled=st.session_state.disabled
    )

with col2:
    # REQUISITO 2: Escolher MÚLTIPLAS tecnologias (st.multiselect)
    tecnologias_multiplas = st.multiselect(
        "Selecione as Tecnologias que deseja aprender:",
        options=["HTML", "CSS", "SQL", "Git", "JavaScript", "Docker", "C++"],
        default=["HTML", "CSS"], # Começa com essas marcadas
        label_visibility=st.session_state.visibility,
        disabled=st.session_state.disabled
    )

st.divider()

# --- EXIBIÇÃO EM TEMPO REAL E BOTÃO ---

st.subheader("📋 Resumo das suas escolhas:")
st.write(f"**Curso Escolhido:** {curso_unico}")
st.write(f"**Tecnologias Selecionadas:** {', '.join(tecnologias_multiplas) if tecnologias_multiplas else 'Nenhuma'}")

# Botão para Enviar (Usa parênteses!)
if st.button("Enviar Inscrição"):
    st.success("Obrigado! Suas preferências foram salvas e iremos entrar em contato!")