import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from datetime import datetime
from sympy import (
    sympify, diff, integrate, series, symbols, Function, 
    dsolve, Eq, Matrix, latex, lambdify, sin, cos, tan, exp, log, pi, sqrt
)

# 1. Configurações de Estilo e Página
st.set_page_config(page_title="MathLab Ultimate", layout="wide", page_icon="🧮")

# CSS para melhorar o visual dos botões
st.markdown("""
    <style>
    div.stButton > button {
        width: 100%;
        height: 50px;
        font-weight: bold;
        border-radius: 8px;
    }
    .main { background-color: #f8f9fa; }
    </style>
    """, unsafe_allow_html=True)

# Inicialização de Variáveis
x, y = symbols('x y')
if 'buffer' not in st.session_state: st.session_state.buffer = ""
if 'historico' not in st.session_state: st.session_state.historico = []

# 2. Funções de Suporte
def inserir(c): st.session_state.buffer += str(c)
def limpar(): st.session_state.buffer = ""
def registrar(mod, entrada, res):
    st.session_state.historico.append({
        "Hora": datetime.now().strftime("%H:%M"),
        "Módulo": mod, "Entrada": str(entrada), "Resultado": str(res)
    })

# --- BARRA LATERAL ---
st.sidebar.title("🎮 Painel de Controle")
modo = st.sidebar.radio("Nível de Matemática:", 
    ["Matemática Básica", "Análise & Gráficos", "Cálculo Avançado (1-4)"])

modo_explica = st.sidebar.checkbox("Modo Explicativo", value=True)

# --- TECLADO VIRTUAL (GLOBAL) ---
with st.sidebar:
    st.divider()
    st.subheader("⌨️ Teclado")
    rows = [
        ["sin(", "cos(", "tan(", "log(", "sqrt("],
        ["7", "8", "9", "/", "("],
        ["4", "5", "6", "*", ")"],
        ["1", "2", "3", "-", "pi"],
        ["0", ".", "x", "+", "^"]
    ]
    for row in rows:
        cols = st.columns(5)
        for i, char in enumerate(row):
            if cols[i].button(char, key=f"btn_{char}_{row}"):
                inserir("**" if char == "^" else char)
    if st.button("LIMPAR TUDO (AC)", type="primary"): limpar()

# --- INTERFACE PRINCIPAL ---
st.title("🧮 MathLab Ultimate")
expr_input = st.text_input("Digite ou use o teclado lateral:", value=st.session_state.buffer)

# --- MÓDULO: MATEMÁTICA BÁSICA ---
if modo == "Matemática Básica":
    st.header("🔢 Operações Fundamentais")
    op_basica = st.selectbox("Operação:", ["Calcular Expressão", "Porcentagem", "Raiz Quadrada", "Fatorial"])
    
    if st.button("Calcular Agora"):
        try:
            if op_basica == "Calcular Expressão":
                res = sympify(expr_input).evalf()
                st.success(f"Resultado: {res}")
                if modo_explica: st.info(f"Processando a expressão aritmética: {expr_input}")
            elif op_basica == "Raiz Quadrada":
                res = sqrt(sympify(expr_input))
                st.latex(latex(res))
            
            registrar("Básica", expr_input, res)
        except Exception as e: st.error(f"Erro: {e}")

# --- MÓDULO: ANÁLISE & GRÁFICOS ---
elif modo == "Análise & Gráficos":
    col1, col2 = st.columns([1, 2])
    with col1:
        tipo_g = st.radio("Tipo de Gráfico:", ["2D (f(x))", "3D (f(x,y))"])
        if st.button("Gerar Visualização"):
            try:
                f_sym = sympify(expr_input)
                if tipo_g == "2D (f(x))":
                    f_num = lambdify(x, f_sym, "numpy")
                    xv = np.linspace(-10, 10, 400)
                    yv = f_num(xv)
                    fig = go.Figure(go.Scatter(x=xv, y=yv, name="f(x)"))
                else:
                    f_num = lambdify((x, y), f_sym, "numpy")
                    v = np.linspace(-5, 5, 50)
                    X, Y = np.meshgrid(v, v)
                    Z = f_num(X, Y)
                    fig = go.Figure(data=[go.Surface(z=Z, x=X, y=Y)])
                
                with col2: st.plotly_chart(fig)
                registrar("Gráfico", expr_input, "Visualizado")
            except Exception as e: st.error(e)

# --- MÓDULO: CÁLCULO AVANÇADO ---
elif modo == "Cálculo Avançado (1-4)":
    op = st.selectbox("Escolha a Operação:", 
        ["Derivada", "Integral", "Série de Taylor", "EDO", "Matriz Determinante"])
    
    if "Matriz" in op:
        st.warning("Para matrizes, digite as linhas separadas por espaço no campo acima.")
    
    if st.button("Executar"):
        try:
            f = sympify(expr_input)
            if op == "Derivada": res = diff(f, x)
            elif op == "Integral": res = integrate(f, x)
            elif op == "Série de Taylor": res = series(f, x, 0, 5)
            elif op == "EDO":
                f_func = Function('f')
                res = dsolve(Eq(sympify(expr_input, locals={'f': f_func}), 0), f_func(x))
            
            st.latex(latex(res))
            if modo_explica: st.info(f"O cálculo foi realizado usando regras de {op}.")
            registrar(op, expr_input, res)
        except Exception as e: st.error(e)

# --- HISTÓRICO ---
st.divider()
with st.expander("📜 Histórico e Exportação"):
    if st.session_state.historico:
        df = pd.DataFrame(st.session_state.historico)
        st.table(df)
        st.download_button("Exportar CSV", df.to_csv().encode('utf-8'), "math_results.csv")
