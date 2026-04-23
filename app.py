import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from datetime import datetime
from sympy import (
    sympify, diff, integrate, series, symbols, Function, 
    dsolve, Eq, Matrix, latex, lambdify, sin, cos, tan, exp, log, pi, sqrt, limit
)

# 1. Configurações de Estilo e Página (Responsivo e Dark Mode)
st.set_page_config(page_title="MathLab Pro Ultimate", layout="wide", page_icon="🚀")

st.markdown("""
    <style>
    /* Estilo Dark Mode Profissional */
    .stApp { background-color: #0e1117; color: #ffffff; }
    
    /* Grid de botões ajustável para Celular */
    @media (max-width: 768px) {
        div[data-testid="column"] {
            width: 19% !important;
            flex: 1 1 19% !important;
            min-width: 19% !important;
        }
    }
    
    /* Estilo dos Botões do Teclado */
    div.stButton > button {
        width: 100%;
        height: 55px;
        font-weight: bold;
        border-radius: 8px;
        background-color: #262730 !important;
        color: white !important;
        border: 1px solid #444 !important;
    }
    
    /* Destaque para botões de ação */
    .stButton>button[kind="primary"] { background-color: #ff4b4b !important; border: none !important; }
    
    /* Campo de exibição estilo Calculadora */
    .stTextInput input {
        background-color: #1e1e1e !important;
        color: #00ff00 !important;
        font-family: 'Courier New', monospace !important;
        font-size: 24px !important;
        text-align: right;
    }
    </style>
    """, unsafe_allow_html=True)

# Inicialização de Variáveis
x, y, z, t = symbols('x y z t')
if 'buffer' not in st.session_state: st.session_state.buffer = ""
if 'historico' not in st.session_state: st.session_state.historico = []
if 'ultimo_res' not in st.session_state: st.session_state.ultimo_res = ""

# Funções de Controle
def inserir(c):
    st.session_state.buffer += str(c)
    st.rerun()

def limpar():
    st.session_state.buffer = ""
    st.session_state.ultimo_res = ""
    st.rerun()

def registrar_historico(categoria, expressao, resultado):
    st.session_state.historico.append({
        "Horário": datetime.now().strftime("%H:%M:%S"),
        "Módulo": categoria,
        "Entrada": str(expressao),
        "Resultado": str(resultado)
    })
    st.session_state.ultimo_res = str(resultado)

# --- BARRA LATERAL ---
st.sidebar.title("🚀 MathLab Pro")
modo = st.sidebar.radio("Nível de Cálculo:", 
    ["Matemática Básica", "Análise & Gráficos", "Cálculo 1 & 2", "Cálculo Multivariável", "EDO & Álgebra Linear"])
modo_explica = st.sidebar.checkbox("Mostrar Explicação Detalhada", value=True)

# --- INTERFACE PRINCIPAL ---
st.title("🧮 Sistema de Computação Simbólica")

# Display da Calculadora
expr_input = st.text_input("Expressão Atual:", value=st.session_state.buffer, placeholder="0")

# --- TECLADO VIRTUAL (RESPONSIVO) ---
with st.container():
    teclas = [
        ["sin(", "cos(", "tan(", "sqrt(", "AC"],
        ["7", "8", "9", "/", "("],
        ["4", "5", "6", "*", ")"],
        ["1", "2", "3", "-", "pi"],
        ["0", ".", "x", "+", "^"]
    ]
    for linha in teclas:
        cols = st.columns(5)
        for i, tecla in enumerate(linha):
            label = "x²" if tecla == "^" else tecla
            if cols[i].button(label, key=f"key_{tecla}_{linha}"):
                if tecla == "AC": limpar()
                else: inserir("**" if tecla == "^" else tecla)

st.divider()

# --- LÓGICA POR MÓDULO ---

# MÓDULO 0: BÁSICA
if modo == "Matemática Básica":
    if st.button("🔢 CALCULAR RESULTADO", type="primary", use_container_width=True):
        try:
            res = sympify(expr_input).evalf()
            st.success(f"Resultado Numérico: {res}")
            registrar_historico("Básica", expr_input, res)
        except Exception as e: st.error(e)

# MÓDULO 1: ANÁLISE & GRÁFICOS
elif modo == "Análise & Gráficos":
    col1, col2 = st.columns([1, 2])
    with col1:
        tipo_g = st.radio("Dimensão:", ["2D (f(x))", "3D (f(x,y))"])
        if st.button("📊 GERAR GRÁFICO", use_container_width=True, type="primary"):
            try:
                f_sym = sympify(expr_input)
                if tipo_g == "2D (f(x))":
                    f_num = lambdify(x, f_sym, "numpy")
                    xv = np.linspace(-10, 10, 400)
                    yv = f_num(xv)
                    fig = go.Figure(go.Scatter(x=xv, y=yv, line=dict(color='#007bff')))
                else:
                    f_num = lambdify((x, y), f_sym, "numpy")
                    v = np.linspace(-5, 5, 50)
                    X, Y = np.meshgrid(v, v)
                    Z = f_num(X, Y)
                    fig = go.Figure(data=[go.Surface(z=Z)])
                with col2: st.plotly_chart(fig, use_container_width=True)
                registrar_historico("Gráficos", expr_input, "Gráfico Visualizado")
            except Exception as e: st.error(e)

# MÓDULO 2: CÁLCULO 1 & 2
elif modo == "Cálculo 1 & 2":
    op = st.selectbox("Operação:", ["Derivada", "Integral Indefinida", "Integral Definida", "Limite"])
    col_a, col_b = st.columns(2)
    a, b = "0", "1"
    if op == "Integral Definida":
        a = col_a.text_input("Limite Inferior:", "0")
        b = col_b.text_input("Limite Superior:", "pi")
    elif op == "Limite":
        a = col_a.text_input("x tende a:", "0")

    if st.button("⚙️ EXECUTAR CÁLCULO", type="primary", use_container_width=True):
        try:
            f = sympify(expr_input)
            if op == "Derivada": res = diff(f, x)
            elif op == "Integral Indefinida": res = integrate(f, x)
            elif op == "Integral Definida": res = integrate(f, (x, sympify(a), sympify(b)))
            elif op == "Limite": res = limit(f, x, sympify(a))
            
            st.latex(latex(res))
            registrar_historico(op, expr_input, res)
        except Exception as e: st.error(e)

# MÓDULO 3: MULTIVARIÁVEL
elif modo == "Cálculo Multivariável":
    op = st.selectbox("Operação:", ["Gradiente", "Laplaciano"])
    if st.button("Vector Calc", type="primary", use_container_width=True):
        try:
            f = sympify(expr_input)
            res = [diff(f, x), diff(f, y)] if op == "Gradiente" else diff(f, x, 2) + diff(f, y, 2)
            st.latex(latex(res))
            registrar_historico(op, expr_input, res)
        except Exception as e: st.error(e)

# MÓDULO 4: EDO & ÁLGEBRA
elif modo == "EDO & Álgebra Linear":
    aba1, aba2 = st.tabs(["Equações Diferenciais", "Álgebra Linear"])
    with aba1:
        if st.button("Resolver EDO", type="primary"):
            try:
                f_func = Function('f')
                sol = dsolve(Eq(sympify(expr_input, locals={'f': f_func}), 0), f_func(x))
                st.latex(latex(sol))
                registrar_historico("EDO", expr_input, sol)
            except Exception as e: st.error(e)
    with aba2:
        st.write("Digite as linhas da matriz separadas por espaços no campo superior.")
        if st.button("Processar Matriz"):
            try:
                # Exemplo de entrada: "1 2" no buffer vira uma linha
                m = Matrix([[sympify(v) for v in expr_input.split()]])
                st.latex(latex(m))
                st.info("Nota: Para matrizes completas, use o teclado físico para digitar espaços entre números.")
            except Exception as e: st.error(e)

# --- RODAPÉ: COPIAR E HISTÓRICO ---
if st.session_state.ultimo_res:
    st.divider()
    st.subheader("📋 Copiar Resultado")
    st.code(st.session_state.ultimo_res, language="text")
    st.caption("Toque e segure acima para copiar.")

with st.expander("📂 Histórico da Sessão"):
    if st.session_state.historico:
        df = pd.DataFrame(st.session_state.historico)
        st.dataframe(df, use_container_width=True)
        st.download_button("📥 Baixar CSV", df.to_csv(index=False).encode('utf-8'), "math_results.csv")
