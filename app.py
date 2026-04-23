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
from duckduckgo_search import DDGS # Motor de busca em tempo real

# 1. CONFIGURAÇÕES DE ESTÉTICA GROK (ULTRA DARK) - IDENTIDADE RUFINO 2.0
st.set_page_config(page_title="Rufino 2.0 - Global", layout="centered", page_icon="🧠")

st.markdown("""
    <style>
    /* Design Sistema Rufino 2.0 (Grok Style) */
    .stApp { background-color: #000000; color: #ffffff; }
    
    /* Barra de Busca Central */
    .stTextInput input {
        background-color: #161616 !important;
        color: white !important;
        border: 1px solid #333 !important;
        border-radius: 12px !important;
        padding: 20px !important;
        font-size: 18px !important;
    }
    
    /* Botão de Ação */
    .stButton>button {
        background-color: #ffffff !important;
        color: black !important;
        border-radius: 50px !important;
        font-weight: bold !important;
        border: none !important;
        height: 3em;
        transition: 0.3s;
    }
    .stButton>button:hover { background-color: #cccccc !important; }
    
    /* Cards de Resposta */
    .result-box {
        background-color: #161616;
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #333;
        margin-top: 20px;
        line-height: 1.6;
    }
    
    .source-tag { color: #00fbff; font-size: 12px; font-weight: bold; }
    
    /* Sidebar */
    [data-testid="stSidebar"] { background-color: #0a0a0a; border-right: 1px solid #222; }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] { background-color: transparent; }
    .stTabs [data-baseweb="tab"] { color: #888; }
    .stTabs [data-baseweb="tab--active"] { color: white !important; border-bottom-color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. MOTOR DE INTELIGÊNCIA RUFINO
wikipedia.set_lang("pt")

def corrigir_sintaxe(texto):
    texto = re.sub(r'(\d)([a-zA-Z\(])', r'\1*\2', texto)
    trads = {'sen': 'sin', 'tg': 'tan', '^': '**', 'ln': 'log'}
    for pt, en in trads.items(): texto = texto.replace(pt, en)
    return texto

def busca_global_live(query):
    resultados = []
    # Busca 1: Wikipedia
    try:
        wiki_res = wikipedia.summary(query, sentences=3)
        resultados.append(f"**[Enciclopédia]** {wiki_res}")
    except: pass
    
    # Busca 2: Web Live (DuckDuckGo)
    try:
        with DDGS() as ddgs:
            ddg_results = [r for r in ddgs.text(query, max_results=3)]
            for res in ddg_results:
                resultados.append(f"**[Web Live]** {res['body']} \n\n*Fonte: {res['href']}*")
    except: pass
    
    return "\n\n---\n\n".join(resultados) if resultados else "Nenhum dado encontrado na rede mundial."

if 'historico' not in st.session_state: st.session_state.historico = []

# --- MENU LATERAL (FUNÇÕES RUFINO 2.0) ---
with st.sidebar:
    st.title("🛡️ Rufino 2.0")
    modo = st.radio("Modo de Operação:", ["🔍 Pesquisa Global", "🧬 Exatas", "👁️ Vision"])
    
    st.divider()
    st.subheader("⏱️ Foco Pomodoro")
    if st.button("Iniciar 25 min"):
        with st.empty():
            for t in range(25*60, 0, -1):
                m, s = divmod(t, 60)
                st.metric("Tempo Rufino", f"{m:02d}:{s:02d}")
                time.sleep(1)
            st.balloons()
    
    st.divider()
    if st.button("🗑️ Limpar Conversa"):
        st.session_state.historico = []
        st.rerun()

# --- INTERFACE CENTRAL ---
st.markdown("<h1 style='text-align: center; margin-top: 30px;'>Rufino 2.0</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666;'>Omnisciente • Conectado • Minimalista</p>", unsafe_allow_html=True)

tab_chat, tab_ferramentas = st.tabs(["💬 Chat", "🧰 Ferramentas"])

with tab_chat:
    # Barra de Pesquisa Única
    prompt = st.text_input("", placeholder="Rufino 2.0: Pergunte sobre qualquer assunto ou resolva equações...", label_visibility="collapsed")
    
    if st.button("Executar"):
        if prompt:
            with st.spinner("Rufino 2.0 vasculhando a rede e processando dados..."):
                try:
                    if modo == "🧬 Exatas":
                        x = symbols('x')
                        f = sympify(corrigir_sintaxe(prompt))
                        res_val = f.simplify()
                        der = diff(f, x)
                        saida = f"Resultado: {latex(res_val)} | Derivada: {latex(der)}"
                        tipo = "math"
                    elif modo == "🔍 Pesquisa Global":
                        saida = busca_global_live(prompt)
                        tipo = "text"
                    else:
                        saida = "Aguardando imagem na aba ferramentas para análise..."
                        tipo = "text"
                    
                    st.session_state.historico.append({"in": prompt, "out": saida, "type": tipo})
                except:
                    st.error("Erro no processamento. Rufino 2.0 recomenda verificar a escrita ou conexão.")

    # EXIBIÇÃO DO FEED (ORDEM INVERSA)
    for chat in reversed(st.session_state.historico):
        st.markdown(f"**❯ {chat['in']}**")
        st.markdown(f"<div class='result-box'>{chat['out']}</div>", unsafe_allow_html=True)
        if chat['type'] == "math":
            st.latex(chat['out'].replace('|', r'\\'))
        st.markdown("<br>", unsafe_allow_html=True)

with tab_ferramentas:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("👁️ Vision")
        foto = st.file_uploader("Suba uma foto de exercício", type=["jpg", "png"])
        if foto:
            img = Image.open(foto)
            st.image(img, use_container_width=True)
            st.info("Imagem carregada no Rufino 2.0. Use o modo 'Vision' no chat.")

    with col2:
        st.subheader("📓 Notas do Rufino")
        notas = st.text_area("Rascunho de estudos:", height=200)
        if st.button("Salvar Notas"):
            st.download_button("Baixar TXT", notas, "notas_rufino.txt")

    st.divider()
    st.subheader("📊 Gráficos Rufino 2.0")
    g_input = st.text_input("Função (ex: sin(x)):")
    if g_input:
        try:
            f_g = sympify(corrigir_sintaxe(g_input))
            f_num = lambdify(symbols('x'), f_g, "numpy")
            xv = np.linspace(-10, 10, 100)
            fig = go.Figure(go.Scatter(x=xv, y=f_num(xv), line=dict(color="white")))
            fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig)
        except: st.error("Erro ao gerar gráfico.")
