# ======================================================
#                Biblioteca Utilizada
# ======================================================

import streamlit as st

# ======================================================
#           Função de Análise Financeira
# ======================================================

def analisar_credito(idade, renda, parcela):
    """
    Realiza o cálculo de viabilidade financeira conforme as regras do banco.
    Retorna: (status_aprovacao, mensagem_feedback, valor_referencia)
    """
    
    # REGRA 1: Verificação de maioridade legal
    if idade < 18:
        return False, "Crédito negado: Apenas maiores de 18 anos podem financiar.", 0
    
    # REGRA 2: Cálculo de comprometimento de renda (máximo 30%)
    # A lei financeira considera o teto de 30% para margem consignável ou financiamento
    limite_maximo = renda * 0.30
    
    # Verificação se o valor da parcela cabe no limite calculado
    if parcela > limite_maximo:
        # Retorna False e sugere o valor máximo permitido para aprovação
        return False, f"Parcela acima da margem permitida (Máximo de 30% da renda: R${limite_maximo:.2f})", limite_maximo
    
    # Caso passe em todas as validações, retorna status positivo
    return True, "Crédito Aprovado com sucesso!", 0.95

# ======================================================
#                 Interface do Usuário 
# ======================================================

st.title("🏦 Simulador ACB 🏦")
st.header("Simulador de Análise de Crédito Bancário")
st.write("Insira seus dados para verificar se o banco libera seu financiamento.")

# Criação do formulário para coleta de dados
with st.form("credito_form"):
    idade = st.number_input("Idade:", min_value=0, max_value=100, value=20)
    renda = st.number_input("Renda Mensal (R$):", min_value=0.0, format="%.2f")
    parcela = st.number_input("Valor da Parcela Desejada (R$):", min_value=0.0, format="%.2f")
    
    # Botão de envio que dispara a análise
    submit = st.form_submit_button("Analisar Crédito")

# ======================================================
#          Lógica de Exibição de Resultados
# ======================================================

if submit:
    # Chama a função de análise com os dados do formulário
    aprovado, mensagem, valor = analisar_credito(idade, renda, parcela)
    
    # Feedback visual baseado no resultado da análise
    if aprovado:
        st.success(f"✅ {mensagem}")
        st.balloons() # Efeito visual de comemoração
    else:
        st.error(f"❌ {mensagem}")
        # Se houve sugestão de valor, exibe para o usuário
        if valor > 0: 
            st.warning(f"💡 Sugestão do Banco: Para ser aprovado, tente ajustar a parcela para até **R${valor:.2f}**.")