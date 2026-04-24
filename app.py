import streamlit as st
import plotly.graph_objects as go
import numpy as np
import wikipedia
import re
from PIL import Image
from sympy import sympify, diff, symbols, latex, lambdify
from duckduckgo_search import DDGS
from datetime import datetime

# 1. ESTÉTICA GROK (ULTRA-DARK & FEED)
st.set_page_config(page_title="Rufino 2.0", layout="centered", page_icon="🧠")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #e5e7eb; }
    
    /* Feed de Mensagens */
    .chat-row { margin-bottom: 35px; animation: fadeIn 0.4s ease-out; }
    .user-tag { color: #666; font-weight: bold; font-size: 11px; text-transform: uppercase; letter-spacing: 1px; }
    .rufino-tag { color: #ffffff; font-weight: bold; font-size: 11px; text-transform: uppercase; letter-spacing: 1px; }
    .message-text { font-size: 17px; line-height: 1.7; margin-top: 5px; color: #d1d5db; }
    
    /* Input Estilo Grok */
    .stTextInput input {
        background-color: #0f0f0f !important;
        color: #ffffff !important;
        border: 1px solid #333 !important;
        border-radius: 12px !important;
        padding: 15px !important;
    }
    
    /* Esconder UI Padrão */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
    </style>
    """, unsafe_allow_html=True)

# 2. MOTOR DE INTELIGÊNCIA RUFINO 2.0 (PORTUGUÊS)
wikipedia.set_lang("pt")

def motor_rufino_universal(query):
    query_clean = query.strip().lower()
    respostas = []

    # FERRAMENTA: EXATAS (SYMPY)
    try:
        if any(c in query_clean for c in '0123456789+-*/^'):
            q_math = re.sub(r'(\d)([a-z\(])', r'\1*\2', query_clean).replace('^', '**')
            res = sympify(q_math)
            respostas.append(f"🧬 **PROCESSO MATEMÁTICO:**\nResultado: $${latex(res)}$$\nDerivada: $${latex(diff(res, symbols('x')))}$$")
    except: pass

    # FERRAMENTA: BUSCA GLOBAL LIVE (DUCKDUCKGO)
    try:
        with DDGS() as ddgs:
            search_data = [r for r in ddgs.text(query_clean, region='br-pt', max_results=3)]
            if search_data:
                web_text = "🌐 **PESQUISA WEB (TEMPO REAL):**\n"
                for r in search_data:
                    web_text += f"• {r['body']} \n*(Fonte: {r['href']})*\n"
                respostas.append(web_text)
    except: pass

    # FERRAMENTA: CONHECIMENTO ESTRUTURADO (WIKIPEDIA COM CORREÇÃO)
    try:
        sugestoes = wikipedia.search(query_clean)
        if sugestoes:
            resumo = wikipedia.summary(sugestoes[0], sentences=5)
            respostas.append(f"📚 **BASE ENCICLOPÉDICA:**\n{resumo}")
    except: pass

    return "\n\n---\n\n".join(respostas) if respostas else "Rufino 2.0 não localizou dados. Tente simplificar a pergunta."

# 3. GESTÃO DO FEED (HISTÓRICO)
if 'history' not in st.session_state:
    st.session_state.history = []

# --- INTERFACE CENTRAL ---
if not st.session_state.history:
    st.markdown("<h1 style='text-align: center; margin-top: 100px; font-size: 55px; letter-spacing: -2px;'>Rufino 2.0</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #444; font-size: 18px;'>Omnisciente • Sem Filtros • Vision • Live Web</p>", unsafe_allow_html=True)

# Exibição do Feed
for chat in st.session_state.history:
    st.markdown(f"<div class='chat-row'><div class='user-tag'>Você</div><div class='message-text'>{chat['q']}</div></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='chat-row'><div class='rufino-tag'>Rufino 2.0</div><div class='message-text'>{chat['a']}</div></div>", unsafe_allow_html=True)

# FERRAMENTA: INPUT E FORMULÁRIO (RODAPÉ)
with st.form(key='grok_input', clear_on_submit=True):
    prompt = st.text_input("", placeholder="Rufino 2.0: Pergunte sobre qualquer assunto...", label_visibility="collapsed")
    enviar = st.form_submit_button("Consultar")

if enviar and prompt:
    with st.spinner(""):
        resposta = motor_rufino_universal(prompt)
        st.session_state.history.append({"q": prompt, "a": resposta})
    st.rerun()

# --- SIDEBAR: FERRAMENTAS EXTRA (VISION E GRÁFICOS) ---
with st.sidebar:
    st.title("⚙️ Rufino 2.0")
    
    st.divider()
    st.subheader("👁️ Vision")
    foto = st.file_uploader("Upload de Imagem para Análise", type=['png', 'jpg', 'jpeg'])
    if foto:
        st.image(Image.open(foto), use_container_width=True)
        st.info("Imagem no sistema. Rufino 2.0 pronto para análise visual.")

    st.divider()
    st.subheader("📊 Gráficos Express")
    g_in = st.text_input("Função (ex: x**2):")
    if g_in:
        try:
            f_g = sympify(g_in.replace('^', '**'))
            f_n = lambdify(symbols('x'), f_g, "numpy")
            xv = np.linspace(-10, 10, 100)
            fig = go.Figure(go.Scatter(x=xv, y=f_n(xv), line=dict(color="white")))
            fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
        except: st.error("Erro na função.")

    st.divider()
    if st.button("Limpar Conversa"):
        st.session_state.history = []
        st.rerun()
