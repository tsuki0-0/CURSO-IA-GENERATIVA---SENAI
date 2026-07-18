# ========================================
#    Calculadora de Engajamento TikTok
# ========================================

# ======================================
#            Bibliotecas
# ======================================

import streamlit as st
import tensorflow as tf
import numpy as np

# ======================================================
# 1. Configuração Inicial da Página
# ======================================================
st.set_page_config(page_title="Calculadora de Engajamento", page_icon="🔥")

st.title("🚀 Calculadora de Engajamento de TikToker")
st.write("IA focada em impulsionar perfis menores!")

# ======================================================
# 2. Criação e Treinamento do Modelo de IA
# ======================================================
@st.cache_resource
def treinar_modelo():
    # X = [Categoria, Hashtags, Seguidores]
    # Y = Alcance estimado (em visualizações)
    # Aumentamos o alcance para perfis com poucos seguidores (ex: 50, 100 seguidores)
    X = np.array([
        [0, 3, 50], [0, 4, 100], [0, 2, 5000],    # Perfis pequenos bombam mais
        [1, 4, 20], [1, 5, 80], [1, 3, 10000],   # Educação
        [2, 3, 30], [2, 4, 150], [2, 2, 20000]    # Lifestyle
    ], dtype=float)
    
    Y = np.array([5000, 8000, 5500, 6000, 9000, 5200, 4500, 7000, 5100], dtype=float)
    
    modelo = tf.keras.Sequential([
        tf.keras.layers.Dense(16, activation='relu', input_shape=[3]),
        tf.keras.layers.Dense(8, activation='relu'),
        tf.keras.layers.Dense(1)
    ])
    
    modelo.compile(optimizer='adam', loss='mean_squared_error')
    modelo.fit(X, Y, epochs=500, verbose=0)
    return modelo

modelo = treinar_modelo()

# ======================================================
# 3. Interface do Usuário (Inputs)
# ======================================================
st.markdown("---")
st.subheader("Configurações do Perfil")

categorias = {"Humor": 0, "Educação": 1, "Lifestyle": 2}

cat_escolhida = st.selectbox("Escolha a categoria:", list(categorias.keys()))
num_hashtags = st.slider("Quantidade de hashtags:", 0, 20, 3)
num_seguidores = st.number_input("Quantos seguidores você tem?", min_value=0, step=1, value=50)

# ======================================================
# 4. Processamento e Exibição de Resultados
# ======================================================
if st.button("Prever Alcance", type="primary"):
    
    input_dados = np.array([[categorias[cat_escolhida], float(num_hashtags), float(num_seguidores)]], dtype=np.float32)
    
    alcance = modelo.predict(input_dados)[0][0]
    
    st.metric("Alcance Estimado", f"{int(abs(alcance))} visualizações")
    
    # A lógica agora favorece perfis com menos de 1000 seguidores para "Viralizar"
    if num_seguidores > 1000:
        st.balloons()
        st.success("🔥 Status: VÍRAL! O algoritmo está entregando muito para perfis iniciantes!")
    else:
        st.error("📉 Status: FLOPADO")
        st.info("Tente focar em um gancho mais forte no início !")

# ======================================================
# 5. Dica do Desenvolvedor
# ======================================================
st.markdown("---")
st.info("💡 **Dica:** O TikTok utiliza o 'cold start'. Vídeos de contas com poucos seguidores são testados em um pequeno grupo e, se performarem bem, ganham entrega massiva!")