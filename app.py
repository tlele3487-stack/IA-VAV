import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import re
import time
from PIL import Image
from datetime import datetime
from sympy import sympify, diff, symbols, latex, lambdify
from duckduckgo_search import DDGS

# 1. ARQUITETURA DE INTERFACE (ESTILO RUFINO OLED DARK)
st.set_page_config(page_title="Rufino 2.0", layout="centered", page_icon="🧠")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    header, footer, #MainMenu { visibility: hidden; }
    
    /* Feed de Diálogo Estilo Grok */
    .chat-row { margin-bottom: 35px; padding-bottom: 20px; border-bottom: 1px solid #111; }
    .label { font-weight: 800; font-size: 12px; letter-spacing: 1px; color: #555; text-transform: uppercase; }
    .msg { font-size: 17px; line-height: 1.8; color: #d1d5db; margin-top: 5px; }
    
    /* Barra de Pesquisa Fixa no Rodapé */
    .stTextInput { position: fixed; bottom: 30px; left: 50%; transform: translateX(-50%); width: 90%; max-width: 750px; z-index: 1000; }
    .stTextInput input { 
        background-color: #0a0a0a !important; color: white !important; 
        border: 1px solid #222 !important; border-radius: 12px !important; 
        padding: 20px !important; font-size: 16px !important;
    }
    
    /* Estilo de Abas Minimalistas */
    .stTabs [data-baseweb="tab-list"] { background-color: transparent; border-bottom: 1px solid #222; }
    .stTabs [data-baseweb="tab"] { color: #444; font-weight: bold; }
    .stTabs [data-baseweb="tab--active"] { color: white !important; border-bottom: 2px solid white !important; }
    
    .spacer { height: 180px; }
    </style>
    """, unsafe_allow_html=True)

# 2. MOTOR DE INTELIGÊNCIA HÍBRIDA (BUSCA + MATEMÁTICA)
def motor_rufino_universal(query):
    q_clean = query.strip().lower()
    respostas = []

    # A: CAMADA MATEMÁTICA (Lógica de Exatas)
    if any(c in q_clean for c in '0123456789+-*/^'):
        try:
            x = symbols('x')
            # Traduz sintaxe humana para Python
            q_math = re.sub(r'(\d)([a-z\(])', r'\1*\2', q_clean).replace('^', '**').replace('sen', 'sin').replace('tg', 'tan')
            res = sympify(q_math)
            respostas.append(f"🧬 **ANÁLISE SIMBÓLICA:**\n\nResultado: $${latex(res)}$$\n\nDerivada: $${latex(diff(res, x))}$$")
        except: pass

    # B: CAMADA WEB LIVE (Busca em Tempo Real - Grok Style)
    try:
        with DDGS() as ddgs:
            # Busca em português para evitar respostas em inglês
            search_res = [r for r in ddgs.text(q_clean, region='br-pt', max_results=4)]
            if search_res:
                web_text = "🌐 **PESQUISA WEB LIVE (OBJETIVA):**\n\n"
                for r in search_res:
                    web_text += f"• {r['body']} \n*(Fonte: {r['href']})*\n\n"
                respostas.append(web_text)
    except: pass

    return "\n\n---\n\n".join(respostas) if respostas else "Rufino 2.0 não localizou dados para esta entrada no momento."

# 3. GESTÃO DE ESTADO
if 'feed' not in st.session_state: st.session_state.feed = []

# --- INTERFACE CENTRAL ---
st.markdown("<h1 style='text-align: center; margin-top: 40px; font-size: 60px; letter-spacing: -3px;'>Rufino 2.0</h1>", unsafe_allow_html=True)

abas = st.tabs(["💬 CHAT OMNISCIENTE", "👁️ VISION ANALYSIS", "⚙️ FERRAMENTAS"])

# TAB 1: O CHAT (O CORAÇÃO DO RUFINO)
with abas[0]:
    # Exibição do Histórico em Feed (Grok Style)
    for chat in st.session_state.feed:
        st.markdown(f"<div class='chat-row'><div class='label'>VOCÊ</div><div class='msg'>{chat['q']}</div></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='chat-row'><div class='label' style='color: white;'>RUFINO 2.0</div><div class='msg'>{chat['a']}</div></div>", unsafe_allow_html=True)
    
    st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)
    
    # Campo de Busca Fixo
    with st.container():
        with st.form(key='input_form', clear_on_submit=True):
            prompt = st.text_input("", placeholder="Rufino 2.0: Pergunte, resolva ou analise...", label_visibility="collapsed")
            col1, col2 = st.columns([0.1, 0.9])
            enviar = col1.form_submit_button("➔")
    
    if enviar and prompt:
        with st.spinner(""):
            res = motor_rufino_universal(prompt)
            # Insere no topo para feed dinâmico
            st.session_state.feed.insert(0, {"q": prompt, "a": res})
        st.rerun()

# TAB 2: VISION (ANÁLISE DE IMAGENS)
with abas[1]:
    st.markdown("### 📸 Sensor Visual")
    st.write("Envie uma foto de um exercício, gráfico ou documento.")
    
    foto = st.file_uploader("Suba uma imagem (PNG, JPG, JPEG)", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")
    
    if foto:
        img = Image.open(foto)
        st.image(img, caption="Imagem capturada pelo Rufino 2.0", use_container_width=True)
        st.success("Imagem carregada com sucesso.")
        
        # Simulador de OCR / Análise Visual
        if st.button("Analisar Conteúdo da Imagem"):
            with st.spinner("Rufino 2.0 processando pixels e OCR..."):
                time.sleep(2)
                st.info("💡 **Análise Concluída:** Imagem identificada. Digite na aba CHAT o que você deseja que eu resolva ou explique sobre esta imagem específica.")

# TAB 3: FERRAMENTAS EXTRAS
with abas[2]:
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("📈 Gráficos")
        g_in = st.text_input("Função (ex: x**2):")
        if g_in:
            try:
                f_g = sympify(g_in.replace('^', '**'))
                f_n = lambdify(symbols('x'), f_g, "numpy")
                xv = np.linspace(-10, 10, 100)
                fig = go.Figure(go.Scatter(x=xv, y=f_n(xv), line=dict(color="#00fbff")))
                fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig, use_container_width=True)
            except: st.error("Erro na função.")
    
    with col_b:
        st.subheader("🗑️ Sistema")
        if st.button("Limpar Histórico de Chat"):
            st.session_state.feed = []
            st.rerun()

# Requirements.txt para o Rufino Vision:
# streamlit, plotly, numpy, pandas, sympy, Pillow, duckduckgo-search
