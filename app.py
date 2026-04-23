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
    /* Design Fundo Total Black */
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

    /* Estilo das Perguntas no Feed */
    .user-query {
        color: #666;
        font-weight: bold;
        margin-top: 45px;
        font-size: 13px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Box de Resposta do Rufino (Estilo Feed do Grok) */
    .result-box {
        background-color: #0f0f0f;
        padding: 30px;
        border-radius: 15px;
        border: 1px solid #222;
        margin-top: 10px;
        line-height: 1.8;
        color: #e0e0e0;
        border-left: 4px solid #00fbff; /* Destaque Neon */
    }
    
    .section-title { color: #00fbff; font-weight: bold; font-size: 19px; margin-top: 10px; }
    .source-tag { color: #444; font-size: 11px; font-style: italic; }

    /* Esconder elementos padrão do Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# 2. MOTOR DE INTELIGÊNCIA RUFINO (BUSCA GLOBAL MULTIFONTES)
wikipedia.set_lang("pt")

def motor_rufino_global(query):
    query_limpa = query.strip().lower()
    explicacao_final = ""

    # --- CAMADA 1: MATEMÁTICA ---
    try:
        if any(c in query_limpa for c in '0123456789+-*/^'):
            # Corrige 2x para 2*x e ^ para **
            q_math = re.sub(r'(\d)([a-z\(])', r'\1*\2', query_limpa).replace('^', '**')
            res = sympify(q_math)
            explicacao_final = f"<div class='section-title'>🧬 Cálculo</div>Resultado: $${latex(res)}$$<br><br>"
    except: pass

    # --- CAMADA 2: BUSCA WEB LIVE (PESQUISA EM TODA A REDE) ---
    try:
        with DDGS() as ddgs:
            # region 'br-pt' para priorizar resultados em português do Brasil
            search_results = [r for r in ddgs.text(query_limpa, region='br-pt', max_results=4)]
            if search_results:
                explicacao_final += "<div class='section-title'>🌐 Pesquisa Web em Tempo Real</div>"
                for r in search_results:
                    explicacao_final += f"• {r['body']}<br><span class='source-tag'>Fonte: {r['href']}</span><br><br>"
    except: pass

    # --- CAMADA 3: WIKIPEDIA (BASE ESTRUTURADA COM CORREÇÃO ORTOGRÁFICA) ---
    try:
        # wikipedia.search corrige erros como "catolika" para "católica"
        sugestoes = wikipedia.search(query_limpa)
        if sugestoes:
            wiki_res = wikipedia.summary(sugestoes[0], sentences=5)
            explicacao_final += f"<div class='section-title'>📚 Base de Conhecimento</div>{wiki_res}"
    except: pass

    return explicacao_final if explicacao_final else "Rufino 2.0 não encontrou dados suficientes. Tente ser mais específico."

# 3. GESTÃO DE HISTÓRICO (O SEGREDO DO FEED CONTÍNUO)
if 'feed' not in st.session_state:
    st.session_state.feed = []

# --- INTERFACE CENTRAL ---
st.markdown("<h1 style='text-align: center; margin-top: 30px;'>Rufino 2.0</h1>", unsafe_allow_html=True)

with st.container():
    # Barra de pesquisa única que limpa após o envio
    prompt = st.text_input("", placeholder="Pesquise notícias, ciência, resolva contas ou pergunte qualquer coisa...", key="input_usuario", label_visibility="collapsed")
    
    col1, col2 = st.columns([4,1])
    if col1.button("Consultar Mundo"):
        if prompt:
            with st.spinner("Rufino 2.0 vasculhando a rede..."):
                resposta = motor_rufino_global(prompt)
                # Insere no topo da lista para o Feed mostrar o mais novo primeiro
                st.session_state.feed.insert(0, {"q": prompt, "a": resposta})
                # Força a atualização para mostrar o novo item
                st.rerun()

st.divider()

# --- EXIBIÇÃO DO FEED CONTÍNUO ---
# Este loop percorre a memória da sessão e desenha todas as conversas anteriores
for item in st.session_state.feed:
    st.markdown(f"<div class='user-query'>❯ {item['q']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='result-box'>{item['a']}</div>", unsafe_allow_html=True)

# --- SIDEBAR (FERRAMENTAS) ---
with st.sidebar:
    st.title("🛡️ Rufino 2.0")
    st.caption("A IA que conecta você a toda a rede mundial.")
    
    st.divider()
    st.subheader("👁️ Vision")
    foto = st.file_uploader("Upload de imagem para análise", type=["jpg", "png", "jpeg"])
    if foto:
        st.image(Image.open(foto), use_container_width=True)
    
    st.divider()
    st.subheader("📊 Gráficos")
    g_in = st.text_input("Função (ex: x**2):")
    if g_in:
        try:
            f_g = sympify(g_in.replace('^', '**'))
            f_n = lambdify(symbols('x'), f_g, "numpy")
            xv = np.linspace(-10, 10, 100)
            fig = go.Figure(go.Scatter(x=xv, y=f_n(xv), line=dict(color="#00fbff")))
            fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig)
        except: st.error("Erro na função.")

    st.divider()
    # Botão para limpar o feed quando quiser começar do zero
    if st.button("🗑️ Limpar Feed"):
        st.session_state.feed = []
        st.rerun()
