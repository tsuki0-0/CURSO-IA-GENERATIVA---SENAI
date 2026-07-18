# ======================================================
#                     Biblioteca
# ======================================================
import streamlit as st

# ======================================================
#                     Configuração
# ======================================================
st.set_page_config(page_title="Spotify Express", page_icon="🎵", layout="wide")

# ======================================================
#       Banco de Dados de Músicas (Dicionário)
# ======================================================
# Estrutura: Gênero -> Lista de músicas (Nome, Artista, Capa_Emoji, Explícito: True/False)
base_musicas = {
    "Rock": [("Sweet Child O' Mine", "Guns N' Roses", "🎸", False), ("Killing In The Name", "RATM", "🔥", True)],
    "Pop": [("Flowers", "Miley Cyrus", "🌸", False), ("WAP", "Cardi B", "💎", True)],
    "Lofi": [("Chill Study", "Lofi Girl", "📚", False), ("Midnight", "Study Vibe", "🌙", False)],
    "Sertanejo": [("Evidências", "Chitãozinho & Xororó", "🤠", False), ("Coração de Isca", "Gusttavo Lima", "💔", False)],
    "Gospel": [("Porque Ele Vive", "Harpa Cristã", "🙏", False), ("Aos Olhos do Pai", "Diante do Trono", "🕊️", False)],
    "MPB": [("Garota de Ipanema", "Tom Jobim", "🌊", False), ("Águas de Março", "Elis Regina", "🍃", False)],
    "Trap": [("Sicko Mode", "Travis Scott", "🌵", True), ("No Stylist", "Drake", "🕶️", True)],
    "Rap": [("Lose Yourself", "Eminem", "🎤", False), ("Life Goes On", "2Pac", "🌟", True)],
    "Funk": [("Baile de Favela", "MC João", "🔊", True), ("Oh Juliana", "MC Niack", "💃", True)]
}

# ======================================================
#            Lógica de Recomendação e Filtro
# ======================================================
def recomendar_musica(energia, tristeza, permitir_explicito):
    # Lógica de processamento de IA (mapeamento por quadrantes/níveis)
    if energia >= 80 and tristeza < 30: genero = "Rock"
    elif energia >= 80 and tristeza >= 30: genero = "Trap"
    elif energia >= 50 and tristeza >= 70: genero = "Rap"
    elif energia >= 50 and tristeza >= 30: genero = "Pop"
    elif energia >= 50 and tristeza < 30: genero = "Funk"
    elif energia < 50 and tristeza >= 70: genero = "Lofi"
    elif energia < 50 and tristeza >= 30: genero = "MPB"
    elif energia < 30 and tristeza < 30: genero = "Gospel"
    else: genero = "Sertanejo"
    
    # Filtragem de conteúdo explícito
    opcoes = base_musicas[genero]
    if not permitir_explicito:
        opcoes = [m for m in opcoes if not m[3]]
        
    return genero, opcoes

# ======================================================
#           Sidebar - Painel de Controle
# ======================================================
st.sidebar.title("🎵 Spotify Express")
energia = st.sidebar.slider("Energia", 0, 100, 50)
tristeza = st.sidebar.slider("Tristeza", 0, 100, 50)
explicito = st.sidebar.checkbox("Permitir conteúdo explícito?", value=False)

# ======================================================
#                     Main Panel
# ======================================================
st.title("Biblioteca de Sugestões")
genero, musicas = recomendar_musica(energia, tristeza, explicito)

st.subheader(f"Gênero: {genero}")

if musicas:
    # Cabeçalho estilo tabela de biblioteca
    col_a, col_b, col_c = st.columns([1, 4, 2])
    col_a.write("**Capa**")
    col_b.write("**Título e Artista**")
    col_c.write("**Status**")
    
    st.divider()

    # Exibição estilo lista de biblioteca (Spotify/YouTube)
    for titulo, artista, emoji, is_explicito in musicas:
        c1, c2, c3 = st.columns([1, 4, 2])
        c1.write(f"## {emoji}")
        c2.write(f"### {titulo}\n*{artista}*")
        c3.write("🔞 Explícito" if is_explicito else "✅ Limpa")
        st.write("---")
else:
    st.warning("Nenhuma música encontrada com este filtro de conteúdo.")

# ======================================================
#                   Rodapé
# ======================================================
st.caption("Filtros aplicados: Energia/Tristeza e Preferência de Conteúdo.")