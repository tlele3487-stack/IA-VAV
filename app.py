import streamlit as st
import plotly.graph_objects as go
import numpy as np
import wikipedia
import re
import time
from PIL import Image
from sympy import sympify, diff, integrate, symbols, latex, lambdify
from duckduckgo_search import DDGS

# 1. INTERFACE IDÊNTICA AO GROK (OLED BLACK & INPUT NO RODAPÉ)
st.set_page_config(page_title="Rufino 2.0", layout="centered", page_icon="🧠")

st.markdown("""
    <style>
    /* Reset total para Preto Absoluto */
    .stApp { background-color: #000000; color: #e5e7eb; }
    header, footer, #MainMenu { visibility: hidden; }

    /* Estilização do Feed de Diálogo (Grok Style) */
    .chat-block { margin-bottom: 45px; max-width: 750px; margin-left: auto; margin-right: auto; }
    
    .user-header { font-weight: 800; color: #ffffff; font-size: 14px; letter-spacing: 1px; margin-bottom: 5px; text-transform: uppercase; }
    .rufino-header { font-weight: 800; color: #ffffff; font-size: 14px; letter-spacing: 1px; margin-bottom: 5px; text-transform: uppercase; }
    
    .msg-body { 
        font-size: 18px; line-height: 1.8; color: #d1d5db; 
        border-left: 2px solid #222; padding-left: 25px; margin-left: 5px;
    }

    /* Barra de Pesquisa Fixa no Rodapé (UX de Celular e Desktop) */
    .stTextInput {
        position: fixed; bottom: 35px; left: 50%; transform: translateX(-50%);
        width: 90%; max-width: 750px; z-index: 1000;
    }
    .stTextInput input {
        background-color: #0d0d0d !important; color: white !important;
        border: 1px solid #262626 !important; border-radius: 14px !important;
        padding: 25px !important; font-size: 17px !important;
        box-shadow: 0 -10px 50px rgba(0,0,0,0.9);
    }
    
    /* Botão de Envio Discreto (Ícone Seta) */
    .stButton button {
        position: fixed; bottom: 50px; right: calc(50% - 350px);
        background: transparent !important; color: #555 !important;
        border: none !important; z-index: 1001; font-size: 24px !important;
    }

    /* Espaçador para o Feed não sumir atrás da barra de busca */
    .spacer { height: 180px; }
    </style>
    """, unsafe_allow_html=True)

# 2. MOTOR DE BUSCA (FONTES DO GROK: LIVE WEB + WIKI PT-BR)
wikipedia.set_lang("pt")

def motor_rufino_core(query):
    query_clean = query.strip().lower()
    respostas = []

    # FONTE 1: WEB LIVE (DuckDuckGo Live Search - 100% Português)
    try:
        with DDGS() as ddgs:
            # region='br-pt' garante busca em fontes brasileiras/portuguesas
            search_data = [r for r in ddgs.text(query_clean, region='br-pt', max_results=4)]
            if search_data:
                web_text = "🌐 **PESQUISA EM TEMPO REAL**\n\n"
                for r in search_data:
                    web_text += f"• {r['body']} \n*(Fonte: {r['href']})*\n\n"
                respostas.append(web_text)
    except: pass

    # FONTE 2: WIKIPEDIA PT (Base Histórica Estruturada)
    try:
        sugestao = wikipedia.search(query_clean)
        if sugestao:
            wiki_res = wikipedia.summary(sugestao, sentences=6)
            respostas.append(f"📚 **BASE DE CONHECIMENTO**\n\n{wiki_res}")
    except: pass

    # FONTE 3: ENGINE MATEMÁTICO (SymPy)
    if any(c in query_clean for c in '0123456789+-*/^'):
        try:
            # Normaliza 2x -> 2*x e ^ -> **
            q_math = re.sub(r'(\d)([a-z\(])', r'\1*\2', query_clean).replace('^', '**')
            res = sympify(q_math)
            respostas.append(f"🧬 **CÁLCULO E LÓGICA**\n\nResultado: $${latex(res)}$$")
        except: pass

    return "\n\n---\n\n".join(respostas) if respostas else "Rufino 2.0: Não foram localizados dados em português para esta solicitação."

# 3. GESTÃO DO FEED CONTÍNUO (SESSÃO)
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# TELA INICIAL (Aparece apenas quando o feed está vazio)
if not st.session_state.chat_history:
    st.markdown("<h1 style='text-align: center; margin-top: 180px; font-size: 65px; letter-spacing: -2px;'>Rufino 2.0</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #444; font-size: 19px;'>No que o Rufino 2.0 pode ajudar você agora?</p>", unsafe_allow_html=True)

# EXIBIÇÃO DO FEED (Ordem Cronológica de cima para baixo)
for chat in st.session_state.chat_history:
    st.markdown(f"""
        <div class='chat-block'>
            <div class='user-header'>VOCÊ</div>
            <div class='msg-body'>{chat['q']}</div>
        </div>
        <div class='chat-block'>
            <div class='rufino-header'>RUFINO 2.0</div>
            <div class='msg-body'>{chat['a']}</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)

# INPUT NO RODAPÉ (Formulário para resetar ao enviar)
with st.form(key='chat_input_form', clear_on_submit=True):
    prompt = st.text_input("", placeholder="Pergunte ao Rufino 2.0...", label_visibility="collapsed")
    enviar = st.form_submit_button("➔")

if enviar and prompt:
    with st.spinner(""):
        resposta = motor_rufino_core(prompt)
        st.session_state.chat_history.append({"q": prompt, "a": resposta})
    st.rerun()

# 4. SIDEBAR: FERRAMENTAS EXTRAS (VISION & GRÁFICOS)
with st.sidebar:
    st.title("⚙️ Rufino 2.0")
    if st.button("Limpar Conversa"):
        st.session_state.chat_history = []
        st.rerun()
    
    st.divider()
    st.subheader("👁️ Vision")
    foto = st.file_uploader("Enviar Imagem", type=['png', 'jpg', 'jpeg'])
    if foto:
        st.image(Image.open(foto), use_container_width=True)
        st.info("Imagem carregada no sistema.")

    st.divider()
    st.subheader("📊 Gráficos")
    g_in = st.text_input("Função:")
    if g_in:
        try:
            f_g = sympify(g_in.replace('^', '**'))
            f_n = lambdify(symbols('x'), f_g, "numpy")
            xv = np.linspace(-10, 10, 100)
            fig = go.Figure(go.Scatter(x=xv, y=f_n(xv), line=dict(color="#ffffff")))
            fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
        except: st.error("Função inválida.")
