# Bibliotecas
import streamlit as st
import tensorflow as tf
import numpy as np

# Configuração de página para melhor UX
st.set_page_config(page_title="Precificador Sênior", layout="centered")

@st.cache_resource
def get_trained_model():
    """
    Simulação de carregamento/treinamento do modelo.
    Em produção, aqui entraría o carregamento de um modelo (.h5 ou SavedModel).
    """
    X = np.array([10, 20, 30, 40, 50, 60, 70, 80, 90, 100], dtype=float)
    y = np.array([90, 85, 80, 75, 70, 65, 60, 55, 50, 45], dtype=float)
    
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(units=1, input_shape=[1])
    ])
    model.compile(optimizer=tf.keras.optimizers.SGD(learning_rate=0.0001), loss='mse')
    model.fit(X, y, epochs=500, verbose=0)
    return model

# Lógica de Interface
def main():
    st.title("🚗 Precificador de Veículos")
    st.markdown("---")
    
    model = get_trained_model()
    
    km_input = st.slider(
        "Quilometragem (mil km):", 
        min_value=0, max_value=200, value=50, step=1
    )
    
    # Execução da predição
    if st.button("Calcular Preço"):
        prediction = model.predict(np.array([[float(km_input)]]))
        preco = prediction[0][0]
        
        st.success(f"### Preço estimado: R$ {max(0, preco):.2f} mil")
        st.info("Nota: Este é um modelo preditivo baseado em regressão linear simples.")

if __name__ == "__main__":
    main()
