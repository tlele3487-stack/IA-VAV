import streamlit as st
import plotly.graph_objects as go
import numpy as np
import wikipedia
import re
import time
from PIL import Image
from sympy import sympify, diff, integrate, symbols, latex, lambdify
from duckduckgo_search import DDGS

# 1. ESTÉTICA GROK (ULTRA-DARK & FEED CONTÍNUO)
st.set_page_config(page_title="Rufino 2.0", layout="centered", page_icon="🧠")

st.markdown("""
    <style>
    /* Fundo Total Black */
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
        color: #888;
        font-weight: bold;
        margin-top: 40px;
        font-size: 13px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Box de Resposta Estruturada (Feed) */
    .result-box {
        background-color: #0f0f0f;
        padding: 30px;
        border-radius: 15px;
        border: 1px solid #222;
        margin-top: 10px;
        line-height: 1.8;
        color: #e0e0e0;
        border-left: 4px solid #ffffff;
    }
    
    .section-title { color: #00fbff; font-weight: bold; font-size: 19px; margin-top: 15px; }
    .source-tag { color: #555; font-size: 12px; font-style: italic; }

    /* Esconder elementos padrão */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# 2. MOTORES DE INTELIGÊNCIA RUFINO (100% PORTUGUÊS)
wikipedia.set_lang("pt")

def limpar_matematica(texto):
    texto = re.sub(r'(\d)([a-zA-Z\(])', r'\1*\2', texto)
    trads = {'sen': 'sin', 'tg': 'tan', '^': '**', 'ln': 'log'}
    for pt, en in trads.items(): texto = texto.replace(pt, en)
    return texto

def motor_explica_tudo(query):
    # Lógica Matemática
    try:
        if any(c in query for c in '+-*/^') or 'x' in query:
            x_s = symbols('x')
            f = sympify(limpar_matematica(query))
            return f"""
            <div class='section-title'>🧬 Análise Matemática</div>
            O Rufino 2.0 identificou uma operação simbólica:
            <br><br>
            **Resultado:** $${latex(f)}$$
            **Derivada:** $${latex(diff(f, x_s))}$$
            """
    except: pass

    # Lógica de Busca Global (Sem Filtros)
    try:
        resumo = wikipedia.summary(query, sentences=8)
        explicacao = f"<div class='section-title'>📚 Explicação Completa</div>{resumo}<br><br><div class='section-title'>🌐 Pesquisa Web Live</div>"
        
        with DDGS() as ddgs:
            # Busca filtrada para região Brasil/Portugal
            links = [r for r in ddgs.text(query, region='br-pt', max_results=3)]
            for r in links:
                explicacao += f"• {r['body']}<br><span class='source-tag'>Fonte: {r['href']}</span><br><br>"
        return explicacao
    except:
        return "Rufino 2.0 não encontrou dados suficientes na rede. Tente reformular a pergunta."

# 3. GESTÃO DE HISTÓRICO (FEED ESTILO GROK)
if 'feed' not in st.session_state:
    st.session_state.feed = []

# --- INTERFACE CENTRAL ---
st.markdown("<h1 style='text-align: center; margin-top: 30px;'>Rufino 2.0</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #555;'>Omnisciente • Sem Filtros • Feed Contínuo</p>", unsafe_allow_html=True)

# Container de Entrada Fixo no Fluxo
with st.container():
    pergunta_usuario = st.text_input("", placeholder="Rufino 2.0: Pergunte absolutamente qualquer coisa...", key="input_main", label_visibility="collapsed")
    if st.button("Consultar Rufino"):
        if pergunta_usuario:
            with st.spinner(""):
                resposta = motor_explica_tudo(pergunta_usuario)
                # Insere no início para o Feed mostrar o mais novo primeiro
                st.session_state.feed.insert(0, {"q": pergunta_usuario, "a": resposta})

st.divider()

# --- EXIBIÇÃO DO FEED (ORDEM DE CHAT) ---
for item in st.session_state.feed:
    st.markdown(f"<div class='user-query'>❯ {item['q']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='result-box'>{item['a']}</div>", unsafe_allow_html=True)

# --- SIDEBAR (FERRAMENTAS AUXILIARES) ---
with st.sidebar:
    st.title("🛡️ Rufino 2.0")
    st.caption("Versão Final Omnisciente")
    
    st.divider()
    st.subheader("👁️ Vision")
    foto = st.file_uploader("Análise de Imagem", type=["jpg", "png", "jpeg"])
    if foto:
        st.image(Image.open(foto), use_container_width=True)
        st.info("Imagem carregada no sistema Rufino.")

    st.divider()
    st.subheader("📊 Gráficos")
    g_in = st.text_input("Função (ex: sin(x)):")
    if g_in:
        try:
            f_g = sympify(limpar_matematica(g_in))
            f_n = lambdify(symbols('x'), f_g, "numpy")
            xv = np.linspace(-10, 10, 100)
            fig = go.Figure(go.Scatter(x=xv, y=f_n(xv), line=dict(color="white")))
            fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig)
        except: st.error("Erro na função.")

    st.divider()
    if st.button("🗑️ Limpar Conversa"):
        st.session_state.feed = []
        st.rerun()
