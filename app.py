import streamlit as st
import plotly.graph_objects as go
import numpy as np
import re
from PIL import Image
from sympy import sympify, diff, symbols, latex
from duckduckgo_search import DDGS

# 1. INTERFACE IDÊNTICA AO GROK (OLED BLACK & INPUT NO RODAPÉ)
st.set_page_config(page_title="Rufino 2.0", layout="centered", page_icon="🧠")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #e5e7eb; }
    header, footer, #MainMenu { visibility: hidden; }

    .chat-block { margin-bottom: 45px; max-width: 750px; margin-left: auto; margin-right: auto; }
    .user-header { font-weight: 800; color: #ffffff; font-size: 14px; text-transform: uppercase; letter-spacing: 1px; }
    .rufino-header { font-weight: 800; color: #ffffff; font-size: 14px; text-transform: uppercase; letter-spacing: 1px; }
    
    .msg-body { 
        font-size: 18px; line-height: 1.7; color: #d1d5db; 
        border-left: 2px solid #333; padding-left: 25px; margin-left: 5px;
    }

    /* Input Fixo Estilo Grok/Google */
    .stTextInput {
        position: fixed; bottom: 35px; left: 50%; transform: translateX(-50%);
        width: 90%; max-width: 750px; z-index: 1000;
    }
    .stTextInput input {
        background-color: #0d0d0d !important; color: white !important;
        border: 1px solid #262626 !important; border-radius: 14px !important;
        padding: 25px !important; font-size: 17px !important;
    }
    
    .stButton button {
        position: fixed; bottom: 50px; right: calc(50% - 350px);
        background: transparent !important; color: #555 !important;
        border: none !important; z-index: 1001; font-size: 24px !important;
    }
    .spacer { height: 180px; }
    </style>
    """, unsafe_allow_html=True)

# 2. MOTOR DE RESPOSTA OBJETIVA (GOOGLE SNIPPET STYLE)
def motor_rufino_objetivo(query):
    query_clean = query.strip().lower()
    
    # 1. Lógica Matemática Direta
    try:
        if any(c in query_clean for c in '0123456789+-*/^'):
            q_math = re.sub(r'(\d)([a-z\(])', r'\1*\2', query_clean).replace('^', '**')
            res = sympify(q_math)
            return f"**Resultado:** {res}"
    except: pass

    # 2. Busca Snippet (DuckDuckGo Live - Objetiva)
    try:
        with DDGS() as ddgs:
            # Busca resultados curtos e diretos (filtramos o texto para ser snippet)
            res_gen = ddgs.text(query_clean, region='br-pt', max_results=3)
            snippet = ""
            for r in res_gen:
                # Se encontrar uma data ou definição curta, prioriza
                body = r['body']
                if len(body) > 50:
                    snippet += f"• {body}\n\n"
            
            if snippet:
                return f"**Destaque da Web:**\n\n{snippet}"
    except: pass

    return "Rufino 2.0: Não encontrei uma resposta objetiva para este termo."

# 3. FEED CONTÍNUO
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if not st.session_state.chat_history:
    st.markdown("<h1 style='text-align: center; margin-top: 180px; font-size: 65px; letter-spacing: -2px;'>Rufino 2.0</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #444; font-size: 19px;'>Objetivo. Direto. Conectado.</p>", unsafe_allow_html=True)

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

with st.form(key='chat_form', clear_on_submit=True):
    prompt = st.text_input("", placeholder="Digite sua pergunta...", label_visibility="collapsed")
    enviar = st.form_submit_button("➔")

if enviar and prompt:
    with st.spinner(""):
        resposta = motor_rufino_objetivo(prompt)
        st.session_state.chat_history.append({"q": prompt, "a": resposta})
    st.rerun()
