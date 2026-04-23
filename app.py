import streamlit as st
import plotly.graph_objects as go
import numpy as np
import wikipedia
import re
import time
from PIL import Image
from sympy import sympify, diff, symbols, latex
from duckduckgo_search import DDGS

# 1. ESTÉTICA GROK (ULTRA-DARK & FEED CONTÍNUO)
st.set_page_config(page_title="Rufino 2.0", layout="centered", page_icon="🧠")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    
    /* Barra de Busca Estilo Grok */
    .stTextInput input {
        background-color: #0f0f0f !important;
        color: #ffffff !important;
        border: 1px solid #333 !important;
        border-radius: 14px !important;
        padding: 20px !important;
        font-size: 18px !important;
    }
    
    /* Botão de Envio Minimalista */
    .stButton>button {
        background-color: #ffffff !important;
        color: #000000 !important;
        border-radius: 50px !important;
        font-weight: bold !important;
        height: 3.5em;
        border: none !important;
        width: 100%;
    }

    /* Feed de Histórico */
    .user-query {
        color: #666;
        font-weight: bold;
        margin-top: 35px;
        font-size: 14px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .result-box {
        background-color: #0f0f0f;
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #222;
        margin-top: 10px;
        line-height: 1.8;
        color: #e0e0e0;
        border-left: 4px solid #ffffff;
    }
    
    .section-title { color: #00fbff; font-weight: bold; font-size: 19px; margin-bottom: 8px; }
    .source-tag { color: #444; font-size: 11px; font-style: italic; }

    /* UI Fixes */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# 2. MOTOR DE INTELIGÊNCIA ROBUSTO (PORTUGUÊS 100%)
wikipedia.set_lang("pt")

def motor_rufino_robusto(query):
    query_limpa = query.strip().lower()
    
    # --- TENTATIVA 1: MATEMÁTICA ---
    try:
        # Detecta se há números ou operadores
        if any(c in query_limpa for c in '0123456789+-*/^'):
            q_math = re.sub(r'(\d)([a-z\(])', r'\1*\2', query_limpa).replace('^', '**')
            res = sympify(q_math)
            return f"<div class='section-title'>🧬 Cálculo</div>Resultado: $${latex(res)}$$"
    except: pass

    # --- TENTATIVA 2: BUSCA GLOBAL (WIKI + WEB LIVE) ---
    resumo_final = ""
    
    # Wikipedia com busca por aproximação (corrige erros ortográficos)
    try:
        sugestoes = wikipedia.search(query_limpa)
        if sugestoes:
            # Pega o resultado mais provável, ignorando erros de digitação
            conteudo = wikipedia.summary(sugestoes[0], sentences=8)
            resumo_final = f"<div class='section-title'>📚 Explicação</div>{conteudo}"
    except: pass

    # Busca Web Live (Reforço Crítico via DuckDuckGo)
    try:
        with DDGS() as ddgs:
            # region 'br-pt' garante respostas no nosso idioma
            links = [r for r in ddgs.text(query_limpa, region='br-pt', max_results=3)]
            if links:
                if resumo_final:
                    resumo_final += "<br><br><div class='section-title'>🌐 Contexto Live</div>"
                else:
                    resumo_final = "<div class='section-title'>🌐 Resultados da Web</div>"
                
                for r in links:
                    resumo_final += f"• {r['body']}<br><span class='source-tag'>Fonte: {r['href']}</span><br><br>"
    except: pass

    return resumo_final if resumo_final else "Rufino 2.0 não encontrou dados. Tente usar outras palavras ou simplificar."

# 3. GESTÃO DE ESTADO (FEED)
if 'feed' not in st.session_state:
    st.session_state.feed = []

# --- INTERFACE CENTRAL ---
st.markdown("<h1 style='text-align: center; margin-top: 20px;'>Rufino 2.0</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #444;'>Omnisciente • Sem Filtros • Inteligência Total</p>", unsafe_allow_html=True)

with st.container():
    # Barra de pesquisa principal
    prompt = st.text_input("", placeholder="Pergunte qualquer coisa (mesmo com erros de digitação)...", key="main_input", label_visibility="collapsed")
    if st.button("Consultar Rufino"):
        if prompt:
            with st.spinner(""):
                resposta = motor_rufino_robusto(prompt)
                # Adiciona ao topo do feed (estilo Grok/Chat)
                st.session_state.feed.insert(0, {"q": prompt, "a": resposta})

st.divider()

# EXIBIÇÃO DO FEED CONTÍNUO
for item in st.session_state.feed:
    st.markdown(f"<div class='user-query'>❯ {item['q']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='result-box'>{item['a']}</div>", unsafe_allow_html=True)

# SIDEBAR (FERRAMENTAS)
with st.sidebar:
    st.title("🛡️ Rufino 2.0")
    st.divider()
    st.subheader("👁️ Vision")
    foto = st.file_uploader("Upload de imagem", type=["jpg", "png", "jpeg"])
    if foto:
        st.image(Image.open(foto), use_container_width=True)
    
    st.divider()
    if st.button("🗑️ Limpar Feed"):
        st.session_state.feed = []
        st.rerun()
