import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import wikipedia
import re
import time
from PIL import Image
from datetime import datetime
from sympy import sympify, diff, integrate, symbols, latex, lambdify, Function, dsolve, Eq
from duckduckgo_search import DDGS

# 1. IDENTIDADE VISUAL E CONFIGURAÇÃO (STYLE GROK DARK)
st.set_page_config(page_title="Rufino 2.0", layout="centered", page_icon="🧠")

st.markdown("""
    <style>
    /* Fundo Total Black */
    .stApp { background-color: #000000; color: #ffffff; }
    
    /* Barra de Busca Centralizada */
    .stTextInput input {
        background-color: #111111 !important;
        color: #ffffff !important;
        border: 1px solid #333 !important;
        border-radius: 14px !important;
        padding: 20px !important;
        font-size: 18px !important;
    }
    
    /* Botões Arredondados */
    .stButton>button {
        background-color: #ffffff !important;
        color: #000000 !important;
        border-radius: 50px !important;
        font-weight: bold !important;
        height: 3.5em;
        transition: 0.3s;
    }
    .stButton>button:hover { background-color: #cccccc !important; }
    
    /* Box de Respostas Profissional */
    .result-box {
        background-color: #111111;
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #222;
        margin-top: 20px;
        line-height: 1.6;
        color: #e0e0e0;
    }
    
    /* Estilo de Sidebar e Tabs */
    [data-testid="stSidebar"] { background-color: #050505; border-right: 1px solid #222; }
    .stTabs [data-baseweb="tab-list"] { background-color: transparent; }
    .stTabs [data-baseweb="tab"] { color: #888; font-weight: bold; }
    .stTabs [data-baseweb="tab--active"] { color: white !important; border-bottom-color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. MOTORES DE INTELIGÊNCIA (PORTUGUÊS PRIORITÁRIO)
wikipedia.set_lang("pt")

def limpar_matematica(texto):
    # Converte sintaxe comum (2x -> 2*x) e (sen -> sin)
    texto = re.sub(r'(\d)([a-zA-Z\(])', r'\1*\2', texto)
    trads = {'sen': 'sin', 'tg': 'tan', '^': '**', 'ln': 'log'}
    for pt, en in trads.items(): texto = texto.replace(pt, en)
    return texto

def busca_rufino_global(query):
    resultados = []
    # 1. Busca Enciclopédia (Wikipedia)
    try:
        wiki_res = wikipedia.summary(query, sentences=4)
        resultados.append(f"📖 **Enciclopédia:** {wiki_res}")
    except: pass
    
    # 2. Busca Web Live (DuckDuckGo focado em PT-BR)
    try:
        with DDGS() as ddgs:
            ddg_res = [r for r in ddgs.text(query, region='br-pt', max_results=3)]
            for r in ddg_res:
                resultados.append(f"🌐 **Web:** {r['body']}\n\n*Fonte: {r['href']}*")
    except: pass
    
    return "\n\n---\n\n".join(resultados) if resultados else "Rufino não encontrou informações. Tente outro termo."

# Inicialização de Histórico
if 'chat_log' not in st.session_state: st.session_state.chat_log = []

# --- MENU LATERAL (PRODUTIVIDADE) ---
with st.sidebar:
    st.title("🛡️ Rufino 2.0")
    st.caption("Inteligência Omnisciente em Português")
    
    modo = st.radio("Selecione o Modo:", ["🔍 Busca Global", "🧬 Exatas", "👁️ Vision"])
    
    st.divider()
    st.subheader("⏱️ Foco Pomodoro")
    if st.button("Iniciar 25 min"):
        with st.empty():
            for t in range(25*60, 0, -1):
                m, s = divmod(t, 60)
                st.metric("Foco Rufino", f"{m:02d}:{s:02d}")
                time.sleep(1)
            st.balloons()
    
    st.divider()
    if st.button("🗑️ Limpar Tudo"):
        st.session_state.chat_log = []
        st.rerun()

# --- INTERFACE CENTRAL ---
st.markdown("<h1 style='text-align: center; margin-top: 20px;'>Rufino 2.0</h1>", unsafe_allow_html=True)

tab_conversa, tab_ferramentas = st.tabs(["💬 Conversa", "🧰 Ferramentas"])

with tab_conversa:
    # Barra Estilo Grok
    prompt = st.text_input("", placeholder="Rufino 2.0: Pergunte o que quiser...", label_visibility="collapsed")
    
    if st.button("Consultar Rufino"):
        if prompt:
            with st.spinner("Rufino 2.0 vasculhando fontes..."):
                try:
                    if modo == "🧬 Exatas":
                        x_sym = symbols('x')
                        f = sympify(limpar_matematica(prompt))
                        res_val = f.simplify()
                        der = diff(f, x_sym)
                        saida = f"**Resultado:** {latex(res_val)}  \n**Derivada:** {latex(der)}"
                        tipo = "math"
                    elif modo == "🔍 Busca Global":
                        saida = busca_rufino_global(prompt)
                        tipo = "text"
                    else:
                        saida = "Por favor, suba uma imagem na aba 'Ferramentas' para análise."
                        tipo = "text"
                    
                    st.session_state.chat_log.append({"in": prompt, "out": saida, "type": tipo})
                except:
                    st.error("Erro no processamento. Verifique a pergunta ou comando.")

    # Feed de Respostas
    for chat in reversed(st.session_state.chat_log):
        st.markdown(f"**❯ {chat['in']}**")
        st.markdown(f"<div class='result-box'>{chat['out']}</div>", unsafe_allow_html=True)
        if chat['type'] == "math":
            st.latex(chat['out'].replace('**Resultado:**', '').replace('**Derivada:**', ''))
        st.markdown("<br>", unsafe_allow_html=True)

with tab_ferramentas:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("👁️ Vision")
        foto = st.file_uploader("Enviar foto", type=["jpg", "png", "jpeg"])
        if foto:
            st.image(Image.open(foto), use_container_width=True)
            st.info("Imagem no sistema. Rufino 2.0 pronto para análise.")

    with col2:
        st.subheader("📓 Notas")
        notas = st.text_area("Rascunho de estudos:", height=150)
        st.download_button("Baixar Notas (TXT)", notas, "notas_rufino.txt")

    st.divider()
    st.subheader("📊 Gráfico Rápido")
    g_in = st.text_input("Função (ex: x**2):")
    if g_in:
        try:
            f_g = sympify(limpar_matematica(g_in))
            f_n = lambdify(symbols('x'), f_g, "numpy")
            xv = np.linspace(-10, 10, 100)
            fig = go.Figure(go.Scatter(x=xv, y=f_n(xv), line=dict(color="#00fbff")))
            fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig)
        except: st.error("Erro no gráfico.")
