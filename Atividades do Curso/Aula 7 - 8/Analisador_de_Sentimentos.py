# ==================================
#           Biblioteca
# ==================================
import streamlit as st
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from deep_translator import GoogleTranslator

# ============================
#   Baixa o léxico do VADER
# ============================
nltk.download('vader_lexicon', quiet=True)

# ==========================================
#   Inicializa o analisador de sentimentos
# ==========================================
sid = SentimentIntensityAnalyzer()

# ==============================
#    Interface do Streamlit
# ==============================
st.title("Analisador de Sentimentos")

# =====================================
#   Entrada de texto em português
# =====================================
texto_pt = st.text_area("Digite o texto em português:")

# ====================================
#   Botão para iniciar a análise
# ====================================
if st.button("Analisar") and texto_pt:
    
    # Traduz o texto para inglês para o VADER conseguir processar
    texto_en = GoogleTranslator(source='pt', target='en').translate(texto_pt)
    
    # Gera as pontuações e extrai o compound
    score = sid.polarity_scores(texto_en)
    compound = score['compound']
    
    # Define o label baseado no valor do compound
    if compound >= 0.05:
        label = "Positivo"
    elif compound <= -0.05:
        label = "Negativo"
    else:
        label = "Neutro"
        
    # Exibe o label e o score final
    st.write(f"**Sentimento:** {label}")
    st.write(f"**Score (Compound):** {compound}")