import streamlit as st
import openai
import os
from dotenv import load_dotenv

# Configuração básica da página
st.set_page_config(
    page_title="🔍 IA de Sugestão de Carreira",
    page_icon="💼",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Remove qualquer estilo forçado anterior
st.markdown("""
<style>
    .stTextInput input, .stTextArea textarea {
        border-radius: 8px !important;
        padding: 10px !important;
    }
    .stButton>button {
        border-radius: 8px !important;
        padding: 10px 24px !important;
        width: 100% !important;
        transition: all 0.3s !important;
    }
    .stButton>button:hover {
        transform: scale(1.02) !important;
    }
</style>
""", unsafe_allow_html=True)

def main():
    st.title("🔍 IA de Sugestão de Carreira")
    st.markdown("Descubra profissões ideais para suas habilidades!")
    
    with st.form(key='career_form'):
        nome = st.text_input("Seu nome:", placeholder="Ex: João Silva")
        habilidades = st.text_area(
            "Suas habilidades (separadas por vírgula):",
            placeholder="Ex: Python, comunicação, design gráfico, liderança",
            height=150
        )
        
        submit_button = st.form_submit_button(label="🔎 Analisar Minhas Habilidades")
    
    if submit_button:
        if not habilidades:
            st.warning("Por favor, insira suas habilidades.")
        else:
            with st.spinner("Analisando suas habilidades..."):
                try:
                    load_dotenv()
                    openai.api_key = os.getenv("OPENAI_API_KEY")
                    
                    if not openai.api_key:
                        st.error("Chave API não configurada")
                        st.stop()
                    
                    prompt = f"""
                    Atue como um consultor de carreira. Com base nestas habilidades:
                    {habilidades}

                    Sugira 3 carreiras ideais no formato:
                    
                    1. [Carreira] - [Emoji]
                    • [Descrição breve]
                    
                    2. [Carreira] - [Emoji]
                    • [Descrição breve]
                    
                    3. [Carreira] - [Emoji]
                    • [Descrição breve]
                    """
                    
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "Você é um consultor de carreira especializado."},
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.7,
                        max_tokens=600
                    )
                    
                    st.subheader(f"💡 Sugestões para {nome if nome else 'você'}:")
                    st.markdown(response.choices[0].message.content)
                    
                    st.divider()
                    st.caption("ℹ️ Sugestões geradas por IA - Consulte um profissional para orientação detalhada.")
                    
                except Exception as e:
                    st.error(f"Erro ao processar: {str(e)}")

if __name__ == "__main__":
    main()