# Biblioteca Utilizada
import streamlit as st
from datetime import datetime


# ============================================================
# CONFIGURAÇÃO INICIAL DA PÁGINA
# Define título, ícone e formato de exibição do aplicativo
# ============================================================

st.set_page_config(
    page_title="Painel de Interesses e Cursos",
    page_icon="🎓",
    layout="wide"
)


# ============================================================
# GERENCIAMENTO DO ESTADO DA APLICAÇÃO
# O session_state mantém valores mesmo quando o Streamlit
# atualiza a página após uma interação do usuário
# ============================================================

def inicializar_estado():

    # Valores padrão utilizados pela aplicação
    estados_iniciais = {
        "form_disabled": False,       # Controla se os campos ficam bloqueados
        "label_visibility": "visible",# Controla a exibição dos textos dos campos
        "enviado": False              # Guarda se o formulário foi enviado
    }


    # Cria as variáveis somente se elas ainda não existirem
    for chave, valor in estados_iniciais.items():

        if chave not in st.session_state:
            st.session_state[chave] = valor



# Executa a inicialização do estado
inicializar_estado()



# ============================================================
# CABEÇALHO DA APLICAÇÃO
# ============================================================

st.title("🎓 Painel de Interesses e Cursos")

st.caption(
    "Selecione seu curso de interesse e as tecnologias que deseja aprender."
)



# ============================================================
# CONTROLES DA INTERFACE
# Estes componentes alteram o comportamento do formulário
# ============================================================

st.subheader("⚙️ Configurações")


col1, col2 = st.columns(2)


with col1:

    # Checkbox altera diretamente o valor:
    # st.session_state.form_disabled
    st.checkbox(
        "🔒 Desabilitar formulário",
        key="form_disabled"
    )



with col2:

    # Radio controla como os textos dos campos aparecem
    # Opções:
    # visible   -> mostra normalmente
    # hidden    -> esconde mantendo espaço
    # collapsed -> remove totalmente
    st.radio(
        "👁️ Visibilidade dos rótulos",
        options=[
            "visible",
            "hidden",
            "collapsed"
        ],
        key="label_visibility",
        horizontal=True
    )



st.divider()



# ============================================================
# BANCO DE OPÇÕES
# Em um projeto real estas listas poderiam vir de um banco
# de dados ou de uma API
# ============================================================

cursos = [
    "Python",
    "Web Design",
    "Ciência de Dados",
    "DevOps",
    "Java"
]


tecnologias = [
    "HTML",
    "CSS",
    "JavaScript",
    "SQL",
    "Git",
    "Docker",
    "C++"
]



# ============================================================
# FORMULÁRIO PRINCIPAL
# O st.form evita que toda alteração atualize a página.
# O processamento ocorre somente quando o botão é clicado.
# ============================================================

with st.form("formulario_interesses"):


    col1, col2 = st.columns(2)



    with col1:

        # Selectbox permite selecionar apenas UMA opção
        curso = st.selectbox(
            "Qual seu curso principal de interesse?",
            options=cursos,

            # Usa a configuração definida pelo usuário
            label_visibility=st.session_state.label_visibility,

            # Bloqueia o campo se o checkbox estiver ativo
            disabled=st.session_state.form_disabled
        )



    with col2:

        # Multiselect permite selecionar várias opções
        tecnologias_escolhidas = st.multiselect(
            "Selecione as tecnologias que deseja aprender:",

            options=tecnologias,

            # Opções selecionadas inicialmente
            default=[
                "HTML",
                "CSS"
            ],

            label_visibility=st.session_state.label_visibility,

            disabled=st.session_state.form_disabled
        )



    # Botão responsável por enviar os dados do formulário
    enviar = st.form_submit_button(
        "🚀 Enviar Inscrição",

        # Também fica bloqueado se o formulário estiver desativado
        disabled=st.session_state.form_disabled
    )



# ============================================================
# PROCESSAMENTO DOS DADOS
# Executa somente quando o usuário clicar em enviar
# ============================================================

if enviar:


    # Validação:
    # O usuário precisa escolher pelo menos uma tecnologia
    if not tecnologias_escolhidas:


        st.warning(
            "⚠️ Selecione pelo menos uma tecnologia antes de enviar."
        )


    else:


        # Marca que o cadastro foi concluído
        st.session_state.enviado = True



        # Estrutura que representa os dados cadastrados
        # Futuramente poderia ser salva em banco de dados
        cadastro = {

            "Curso": curso,

            "Tecnologias": tecnologias_escolhidas,

            "Data Cadastro": datetime.now().strftime(
                "%d/%m/%Y %H:%M"
            )
        }



        # Mensagem de confirmação
        st.success(
            "✅ Inscrição realizada com sucesso!"
        )



        st.divider()



        # ====================================================
        # EXIBIÇÃO DO RESUMO DO CADASTRO
        # ====================================================

        st.subheader(
            "📋 Resumo da sua inscrição"
        )


        col1, col2 = st.columns(2)



        with col1:

            st.metric(
                "Curso escolhido",
                cadastro["Curso"]
            )



        with col2:

            st.metric(
                "Tecnologias selecionadas",
                len(cadastro["Tecnologias"])
            )



        st.write(
            "**Tecnologias escolhidas:**"
        )


        # Lista cada tecnologia selecionada
        for tecnologia in cadastro["Tecnologias"]:

            st.write(
                f"✔️ {tecnologia}"
            )



        st.info(
            f"Cadastro realizado em: {cadastro['Data Cadastro']}"
        )



# ============================================================
# RODAPÉ
# ============================================================

st.divider()

st.caption(
    "🎓 Painel de Interesses e Cursos desenvolvido com Streamlit"
)
