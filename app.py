import streamlit as st
import plotly.graph_objects as go
import numpy as np
import wikipedia
import re
import concurrent.futures
from PIL import Image
from sympy import sympify, latex
from duckduckgo_search import DDGS

# --- CONFIGURAÇÃO DE ALTA PERFORMANCE ---
st.set_page_config(
    page_title="Rufino 2.0 | Omni Intelligence", 
    layout="wide", 
    page_icon="🧠",
    initial_sidebar_state="collapsed"
)

# --- ESTILIZAÇÃO CUSTOMIZADA (CSS INJECT) ---
def apply_ultra_dark_theme():
    st.markdown("""
        <style>
        @import url('https://googleapis.com');
        
        html, body, [data-testid="stAppViewContainer"] {
            background-color: #050505 !important;
            font-family: 'Inter', sans-serif;
            color: #E0E0E0;
        }
        
        .stTabs [data-baseweb="tab-list"] { background-color: transparent; gap: 20px; }
        .stTabs [data-baseweb="tab"] { color: #555; border: none !important; }
        .stTabs [data-baseweb="tab-highlight"] { background-color: #ffffff; }
        
        .chat-container { border-left: 2px solid #1A1A1A; padding-left: 25px; margin: 30px 0; }
        .user-label { color: #4A4A4A; font-weight: 900; font-size: 0.7rem; letter-spacing: 2px; }
        .rufino-label { color: #FFFFFF; font-weight: 900; font-size: 0.7rem; letter-spacing: 2px; }
        .msg-text { font-size: 1.05rem; line-height: 1.6; margin-top: 8px; }
        
        /* Input Fixo Minimalista */
        .stTextInput input {
            background-color: #0D0D0D !important;
            border: 1px solid #222 !important;
            border-radius: 8px !important;
            color: white !important;
        }
        </style>
    """, unsafe_allow_html=True)

# --- ENGINE DE INTELIGÊNCIA ---
class RufinoEngine:
    @staticmethod
    def solve_math(query):
        """Camada 1: Processamento Simbólico."""
        try:
            # Limpeza para evitar injeção de código e padronizar sintaxe
            clean_q = re.sub(r'[^0-9+\-*/^().,a-zA-Z]', '', query.replace(' ', ''))
            expr = sympify(clean_q.replace('^', '**'))
            return f"🧬 **CÁLCULO EXATO:**\n$${latex(expr)}$$"
        except:
            return None

    @staticmethod
    def fetch_web(query):
        """Camada 2: Live Web Search (Assíncrono simulado)."""
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(query, region='br-pt', max_results=3))
                if not results: return None
                header = "🌐 **CONTEXTO EM TEMPO REAL:**\n"
                body = "\n".join([f"• {r['body'][:250]}... [Fonte]({r['href']})" for r in results])
                return header + body
        except:
            return None

    @staticmethod
    def fetch_wiki(query):
        """Camada 3: Conhecimento Estruturado."""
        try:
            wikipedia.set_lang("pt")
            search = wikipedia.search(query)
            if not search: return None
            summary = wikipedia.summary(search[0], sentences=3)
            return f"📚 **ENCICLOPÉDIA:**\n{summary}"
        except:
            return None

# --- ORQUESTRAÇÃO DE RESPOSTA ---
def processar_query(query):
    # Uso de ThreadPoolExecutor para rodar as buscas em paralelo (Ganho de velocidade)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        f_math = executor.submit(RufinoEngine.solve_math, query)
        f_web = executor.submit(RufinoEngine.fetch_web, query)
        f_wiki = executor.submit(RufinoEngine.fetch_wiki, query)
        
        # Coleta os resultados conforme terminam
        res_math = f_math.result()
        res_web = f_web.result()
        res_wiki = f_wiki.result()

    if not any([res_math, res_web, res_wiki]):
        return "⚠️ Não encontrei dados suficientes. Tente refinar sua pergunta."

    return "\n\n---\n\n".join(filter(None, [res_math, res_web, res_wiki]))

# --- UI / UX ---
def main():
    apply_ultra_dark_theme()
    
    if 'history' not in st.session_state:
        st.session_state.history = []

    st.title("RUFINO 2.0")
    st.caption("Advanced Omni-Search Engine | v2.1.0-Stable")

    tab_chat, tab_vision = st.tabs(["🗨️ OMNI FEED", "👁️ VISION & SYSTEM"])

    with tab_chat:
        # Renderização do Feed (Top-Down para leitura natural)
        for chat in st.session_state.history:
            st.markdown(f"""
            <div class="chat-container">
                <div class="user-label">USER_REQUEST</div>
                <div class="msg-text">{chat['q']}</div>
                <div style="height:20px"></div>
                <div class="rufino-label">RUFINO_RESPONSE</div>
                <div class="msg-text">{chat['a']}</div>
            </div>
            """, unsafe_allow_html=True)

        # Input fixo no fundo
        st.write("---")
        with st.form("chat_input", clear_on_submit=True):
            user_input = st.text_input("Comando:", placeholder="Digite sua dúvida aqui...")
            col_submit, col_clear = st.columns([1, 6])
            with col_submit:
                btn_send = st.form_submit_button("EXECUTAR")

        if btn_send and user_input:
            with st.spinner("Sincronizando bases de dados..."):
                response = processar_query(user_input)
                # Insere no início para aparecer primeiro (opcional, mude para append se preferir bottom)
                st.session_state.history.insert(0, {"q": user_input, "a": response})
                st.rerun()

    with tab_vision:
        st.subheader("Análise de Mídia")
        uploaded_file = st.file_uploader("Upload de imagem", type=['jpg', 'jpeg', 'png'])
        if uploaded_file:
            img = Image.open(uploaded_file)
            st.image(img, caption="Preview", use_container_width=True)
            st.info("Módulo de Visão Computacional aguardando API Key externa.")
        
        if st.button("RESET SYSTEM"):
            st.session_state.history = []
            st.rerun()

if __name__ == "__main__":
    main()
