# ======================================================
#       O Filtro Antispam de DM do Instagram
# ======================================================

import streamlit as st
import tensorflow as tf
import numpy as np

# ======================================================
# 1. Configuração da Página
# ======================================================

st.set_page_config(page_title="O Filtro Antispam de DM", page_icon="🛡️")

# ======================================================
# 2. Pipeline de Texto e Modelo
# ======================================================

@st.cache_resource
def treinar_modelo_robusto():
    # Aumentando drasticamente o vocabulário de treino
    textos = [
        # Seguros (Label 1)
        "Oi, amei seu conteúdo!", "Quer fazer uma parceria com nossa marca?",
        "Como foi seu dia?", "Pode me seguir de volta?",
        "Que vídeo legal, parabéns!", "Adorei sua última foto!",
        "Você viu meu comentário?", "Adorei a dica do post de ontem.",
        "Poderia me indicar um bom curso?", "Parabéns pelo sucesso, você merece!",
        "Qual a câmera que você usa?", "Estou acompanhando seu trabalho, continue assim.",
        
        # Spam/Golpes (Label 0)
        "Clique aqui para ganhar um iPhone grátis!", "Sua conta será bloqueada, entre no link.",
        "Ganhe dinheiro rápido trabalhando de casa.", "Clique para ver fotos exclusivas da minha conta.",
        "Participe do sorteio exclusivo clicando no link abaixo.", "Sua conta apresenta atividade suspeita, valide agora.",
        "Ganhe 500 reais por dia agora.", "O link do grupo vip está na minha bio.",
        "Você foi selecionado para uma promoção exclusiva.", "Acesse este link para evitar o banimento da conta."
    ]
    labels = np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

    vetorizador = tf.keras.layers.TextVectorization(max_tokens=200, output_mode='int', output_sequence_length=15)
    vetorizador.adapt(textos)

    modelo = tf.keras.Sequential([
        vetorizador,
        tf.keras.layers.Embedding(200, 32),
        tf.keras.layers.GlobalAveragePooling1D(),
        tf.keras.layers.Dense(32, activation='relu'),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])
    
    modelo.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    # Treinando com mais épocas para fixar o aprendizado
    modelo.fit(np.array(textos, dtype=object), labels, epochs=100, verbose=0)
    return modelo

modelo = treinar_modelo_robusto()

# ======================================================
# 3. Lógica de Segurança (Filtro Híbrido)
# ======================================================

def verificar_seguranca(texto):
    texto_lower = texto.lower()
    palavras_perigo = ["clique", "link", "bloqueada", "prêmio", "ganhe", "dinheiro", "valide", "efetue"]
    for palavra in palavras_perigo:
        if palavra in texto_lower:
            return True, 0.20 # Força score de SPAM
    
    score = modelo.predict(np.array([texto], dtype=object))[0][0]
    return False, float(score)

# ======================================================
# 4. Interface do Usuário
# ======================================================

st.title("🛡️ O Filtro Antispam de DMs 🛡️")
dm_input = st.text_area("Cole a DM aqui para análise:")

if st.button("Analisar Mensagem", type="primary"):
    if dm_input:
        foi_detectado_pela_regra, score = verificar_seguranca(dm_input)
        
        # Lógica de Classificação customizada:
        if score >= 0.65:
            st.success(f"✅ Mensagem SEGURA! (Confiança: {score:.2%})")
        elif score >= 0.45:
            st.warning(f"🛡️ Mensagem CONFIÁVEL. (Confiança: {score:.2%})")
        elif score >= 0.25:
            st.info(f"⚠️ Mensagem SUSPEITA. (Confiança: {score:.2%})")
        else:
            st.error(f"🚫 SPAM / ENGANOSO / GOLPE! (Score: {score:.2%})")
    else:
        st.warning("Por favor, cole um texto para análise.")

# ======================================================
# 5. Dica do Desenvolvedor
# ======================================================

st.markdown("")
st.info("⚠️ **AVISO:** ⚠️ O sistema utiliza IA combinada com detecção de palavras-chave para analizar a menssagem, a IA pode cometer erros !")