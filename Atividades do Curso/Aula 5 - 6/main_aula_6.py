# ==========================
#        Bibliotecas
# streamlit
# tensorflow
# numpy
# scikit-learn
# pickle-mixin / pickle
# ==========================
import streamlit as st
import tensorflow as tf
import pickle
from tensorflow.keras.preprocessing.sequence import pad_sequences

# ==========================
#   Configuração da página
# ==========================

st.set_page_config(
    page_title="Detector de Spam",
    page_icon="📩",
    layout="centered"
)

# ==========================
#   Carregamento do modelo
# ==========================

@st.cache_resource
def carregar_modelo():
    modelo = tf.keras.models.load_model("spam_model.keras")

    with open("tokenizer.pkl", "rb") as arquivo:
        tokenizer = pickle.load(arquivo)

    return modelo, tokenizer

modelo, tokenizer = carregar_modelo()

# ===============================
# Tamanho máximo das sequências
# ===============================

MAX_LEN = 100

# ==========================
#        Interface
# ==========================

st.title("📩 Detector de Spam")

st.write(
    "Digite uma mensagem abaixo e clique em **Classificar**."
)

mensagem = st.text_area(
    "Mensagem",
    height=150,
    placeholder="Ex.: Você ganhou um prêmio! Clique aqui..."
)

# ==========================
#         Predição
# ==========================

if st.button("🔍 Classificar"):

    if mensagem.strip() == "":
        st.warning("Digite uma mensagem antes de classificar.")

    else:

        sequencia = tokenizer.texts_to_sequences([mensagem])

        texto = pad_sequences(
            sequencia,
            maxlen=MAX_LEN,
            padding="post"
        )

        probabilidade = modelo.predict(texto, verbose=0)[0][0]

        st.subheader("Resultado")

        if probabilidade >= 0.5:
            st.error("🚨 Esta mensagem é SPAM")
        else:
            st.success("✅ Esta mensagem NÃO é SPAM")

        st.progress(float(probabilidade))

        st.write(
            f"**Probabilidade de Spam:** {probabilidade:.2%}"
        )