# ========================================
#    Previsão da Conta de Luz no Verão
# ========================================

# ======================================
#            Bibliotecas
# ======================================

import streamlit as st
import tensorflow as tf
import numpy as np
import pandas as pd

# ======================================================
# 1. Configuração Inicial da Página
# ======================================================
# Define o título e o ícone da aba do navegador
st.set_page_config(page_title="Previsão de Conta de Luz", page_icon="⚡")

st.title("⚡ Previsão da Conta de Luz no Verão")
st.write("Descubra como o uso do ar-condicionado impacta o seu bolso")

# ======================================================
# 2. Criação e Treinamento do Modelo de IA
# ======================================================
# Usamos o decorador @st.cache_resource para garantir que o modelo
# seja treinado apenas uma vez quando o app for carregado, poupando recursos.
@st.cache_resource
def carregar_modelo():
    # Dados de histórico fictícios para treinar a nossa IA:
    # X = horas de ar-condicionado no mês
    # Y = valor da conta de luz em Reais (R$)
    # (Neste cenário base: R$ 80 de taxa fixa + R$ 1.50 por hora de uso)
    x_treino = np.array([0, 50, 100, 150, 200, 250, 300], dtype=float)
    y_treino = np.array([80, 155, 230, 305, 380, 455, 530], dtype=float)
    
    # Criamos a arquitetura da Rede Neural. 
    # Como o problema é simples (regressão linear), uma camada densa com 1 neurônio basta.
    modelo = tf.keras.Sequential([
        tf.keras.layers.Dense(units=1, input_shape=[1])
    ])
    
    # Compilamos o modelo definindo a taxa de aprendizado do otimizador Adam
    # e a função de perda (Erro Quadrático Médio)
    modelo.compile(optimizer=tf.keras.optimizers.Adam(0.1), loss='mean_squared_error')
    
    # Treinamos a rede com nossos dados por 500 épocas (ciclos de aprendizado)
    modelo.fit(x_treino, y_treino, epochs=500, verbose=0)
    
    return modelo

# Inicializa o nosso modelo de previsão
modelo = carregar_modelo()

# ======================================================
# 3. Interface do Usuário (Inputs)
# ======================================================
st.markdown("---")
st.subheader("Parâmetros do Mês")

# Coletamos a estimativa de uso do usuário através de um input numérico
horas_uso = st.number_input(
    "Quantas horas de ar-condicionado você usará neste mês?", 
    min_value=0, 
    max_value=744, # Máximo de horas em um mês de 31 dias
    value=100,
    step=10,
    help="Exemplo: Se usar 4 horas por dia durante 30 dias, digite 120."
)

# ======================================================
# 4. Processamento e Exibição de Resultados
# ======================================================
if st.button("Calcular Projeção", type="primary"):
    
    # O TensorFlow exige que o input seja uma matriz 2D, por isso passamos [[horas_uso]]
    # O retorno também é uma matriz, extraímos o valor exato com [0][0]
    # CORREÇÃO: Conversão explícita para array numpy de float32
    previsao_atual = modelo.predict(np.array([[float(horas_uso)]], dtype=np.float32))[0][0]
    
    # Exibe o valor final projetado em destaque
    st.success(f"Sua conta de luz estimada é de: **R$ {previsao_atual:.2f}**")
    
    # ======================================================
    # 5. Geração do Gráfico de Evolução (st.line_chart)
    # ======================================================
    st.subheader("📈 Evolução do Gasto")
    st.write("Veja como a sua conta aumenta gradativamente de acordo com as horas:")
    
    # Criamos um array de pontos de 0 até as horas informadas para traçar o gráfico
    # Usamos 20 passos (pontos no gráfico) para criar uma linha suave
    passos_horas = np.linspace(0, horas_uso, num=20)
    
    # Pedimos para a IA prever o valor da conta para cada um desses passos
    # O reshape(-1, 1) transforma o array 1D em 2D, conforme o TF exige
    # CORREÇÃO: Adicionado .astype(np.float32) para compatibilidade
    previsoes_grafico = modelo.predict(passos_horas.reshape(-1, 1).astype(np.float32)).flatten()
    
    # Organizamos os dados em um DataFrame do Pandas para facilitar a plotagem no Streamlit
    df_grafico = pd.DataFrame({
        "Horas de Uso": passos_horas,
        "Valor Estimado (R$)": previsoes_grafico
    }).set_index("Horas de Uso") # Define o eixo X como as horas de uso
    
    # Renderizamos o gráfico de linha nativo do Streamlit
    st.line_chart(df_grafico)
    
    st.info("💡 **Dica financeira:** Cada grau a menos no termostato do ar-condicionado pode representar um aumento de até 8% no consumo. Tente mantê-lo em 23°C ou 24°C para um melhor custo-benefício!")