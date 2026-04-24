import streamlit as st
import plotly.graph_objects as go
import numpy as np
import wikipedia
import re
import time
from PIL import Image
from sympy import sympify, diff, symbols, latex, lambdify
from duckduckgo_search import DDGS

# 1. ESTÉTICA GROK (ULTRA-DARK & FEED CONTÍNUO)
st.set_page_config(page_title="Rufino 2.0", layout="centered", page_icon="🧠")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    header, footer, #MainMenu { visibility: hidden; }
    
    .chat-row { margin-bottom: 40px; padding-bottom: 20px; border-bottom: 1px solid #111; }
    .label { font-weight: 800; font-size: 12px; letter-spacing: 1px; color: #555; text-transform: uppercase; }
    .msg { font-size: 17px; line-height: 1.8; color: #d1d5db; margin-top: 5px; }
    
    .stTextInput { position: fixed; bottom: 30px; left: 50%; transform: translateX(-50%); width: 90%; max-width: 750px; z-index: 1000; }
    .stTextInput input { 
        background-color: #0a0a0a !important; color: white !important; 
        border: 1px solid #222 !important; border-radius: 12px !important; 
        padding: 20px !important; font-size: 16px !important;
    }
    .spacer { height: 180px; }
    </style>
    """, unsafe_allow_html=True)

# 2. MOTOR DE BUSCA OMNISCIENTE (A RESPOSTA PARA TUDO)
wikipedia.set_lang("pt")

def motor_rufino_omnisciente(query):
    q_clean = query.strip().lower()
    resumo_final = ""

    # --- CAMADA 1: EXATAS (MATEMÁTICA E LÓGICA) ---
    if any(c in q_clean for c in '0123456789+-*/^'):
        try:
            q_math = re.sub(r'(\d)([a-z\(])', r'\1*\2', q_clean).replace('^', '**').replace('sen', 'sin')
            res = sympify(q_math)
            resumo_final += f"🧬 **ANÁLISE DE EXATAS:**\nResultado: $${latex(res)}$$\n\n"
        except: pass

    # --- CAMADA 2: PESQUISA WEB LIVE (NOTÍCIAS E ATUALIDADES) ---
    try:
        with DDGS() as ddgs:
            # region 'br-pt' garante respostas em português
            search_res = [r for r in ddgs.text(q_clean, region='br-pt', max_results=5)]
            if search_res:
                resumo_final += "🌐 **CONHECIMENTO LIVE (WEB):**\n\n"
                for r in search_res:
                    resumo_final += f"• {r['body']} \n*(Fonte: {r['href']})*\n\n"
    except: pass

    # --- CAMADA 3: ENCICLOPÉDIA (HISTÓRIA E CIÊNCIA PROFUNDA) ---
    try:
        # wikipedia.search corrige erros de digitação (ex: "catolika" -> "católica")
        sugestoes = wikipedia.search(q_clean)
        if sugestoes:
            wiki_res = wikipedia.summary(sugestoes[0], sentences=5)
            resumo_final += f"📚 **BASE ENCICLOPÉDICA:**\n\n{wiki_res}"
    except: pass

    return resumo_final if resumo_final else "Rufino 2.0 não encontrou dados. Tente usar outras palavras-chave."

# 3. GESTÃO DO FEED
if 'feed' not in st.session_state: st.session_state.feed = []

# --- INTERFACE CENTRAL ---
st.markdown("<h1 style='text-align: center; margin-top: 30px; font-size: 60px;'>Rufino 2.0</h1>", unsafe_allow_html=True)

abas = st.tabs(["💬 CHAT OMNISCIENTE", "👁️ VISION & TOOLS"])

with abas[0]:
    for chat in st.session_state.feed:
        st.markdown(f"<div class='chat-row'><div class='label'>VOCÊ</div><div class='msg'>{chat['q']}</div></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='chat-row'><div class='label' style='color: white;'>RUFINO 2.0</div><div class='msg'>{chat['a']}</div></div>", unsafe_allow_html=True)
    
    st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)
    
    with st.container():
        with st.form(key='chat_form', clear_on_submit=True):
            prompt = st.text_input("", placeholder="Rufino 2.0: Pergunte o que quiser...", label_visibility="collapsed")
            enviar = st.form_submit_button("➔")
    
    if enviar and prompt:
        with st.spinner("Rufino 2.0 consultando fontes mundiais..."):
            resposta = motor_rufino_omnisciente(prompt)
            st.session_state.feed.insert(0, {"q": prompt, "a": resposta})
        st.rerun()

with abas[1]:
    st.subheader("👁️ Vision Analysis")
    foto = st.file_uploader("Suba uma imagem para análise", type=['png', 'jpg', 'jpeg'])
    if foto: st.image(Image.open(foto), use_container_width=True)
    
    st.divider()
    if st.button("🗑️ Limpar Tudo"):
        st.session_state.feed = []
        st.rerun()
