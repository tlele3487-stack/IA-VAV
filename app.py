import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from datetime import datetime
from sympy import (
    sympify, diff, integrate, series, symbols, Function, 
    dsolve, Eq, Matrix, latex, lambdify, sin, cos, tan, exp, log, pi
)

# 1. Configurações de Estilo e Página
st.set_page_config(page_title="MathLab Pro", layout="wide", page_icon="🚀")

st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #007bff; color: white; }
    .stExpander { border: 1px solid #007bff; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# Inicialização de Variáveis Simbólicas
x, y, z, t = symbols('x y z t')

if 'historico' not in st.session_state:
    st.session_state.historico = []

# 2. Funções de Suporte
def registrar_historico(categoria, expressao, resultado):
    st.session_state.historico.append({
        "Horário": datetime.now().strftime("%H:%M:%S"),
        "Módulo": categoria,
        "Entrada": str(expressao),
        "Resultado": str(resultado)
    })

def exibir_math(obj_sympy, passos=None):
    st.success("Cálculo Concluído!")
    st.latex(latex(obj_sympy))
    if passos and st.sidebar.checkbox("Mostrar Explicação", value=True):
        for p in passos:
            st.info(f"💡 {p}")

# 3. Sidebar de Controle
st.sidebar.title("🚀 MathLab Pro")
modo = st.sidebar.radio("Nível de Cálculo:", 
    ["Análise & Gráficos", "Cálculo 1 & 2", "Cálculo Multivariável", "EDO & Álgebra Linear"])

st.title("🧮 MathLab: Sistema de Computação Simbólica")
st.divider()

# --- MÓDULO 1: ANÁLISE & GRÁFICOS ---
if modo == "Análise & Gráficos":
    col1, col2 = st.columns([1, 2])
    with col1:
        st.header("Função 2D")
        func_input = st.text_input("f(x) =", "sin(x) * exp(-x/5)")
        range_x = st.slider("Intervalo de x", -50, 50, (-10, 10))
        
        if st.button("Gerar Visualização"):
            try:
                f_sym = sympify(func_input)
                f_num = lambdify(x, f_sym, "numpy")
                x_vals = np.linspace(range_x[0], range_x[1], 500)
                y_vals = f_num(x_vals)
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=x_vals, y=y_vals, name="f(x)", line=dict(color='#007bff', width=3)))
                fig.update_layout(template="plotly_white", title=f"Gráfico de {func_input}")
                
                with col2:
                    st.plotly_chart(fig, use_container_width=True)
                registrar_historico("Gráficos", func_input, "Gráfico Gerado")
            except Exception as e: st.error(f"Erro na função: {e}")

# --- MÓDULO 2: CÁLCULO 1 & 2 ---
elif modo == "Cálculo 1 & 2":
    op = st.selectbox("Operação:", ["Derivada", "Integral Indefinida", "Integral Definida", "Limite"])
    expr = st.text_input("Expressão f(x):", "x**2 * ln(x)")
    
    col_a, col_b = st.columns(2)
    if op == "Integral Definida":
        a = col_a.text_input("De (a):", "0")
        b = col_b.text_input("Até (b):", "1")
    elif op == "Limite":
        a = col_a.text_input("x tende a:", "0")

    if st.button("Executar Cálculo"):
        try:
            f = sympify(expr)
            if op == "Derivada":
                res = diff(f, x)
                exibir_math(res, [f"Derivando {f} em relação a x", "Aplicando regras de derivação (produto/cadeia)."])
            elif op == "Integral Indefinida":
                res = integrate(f, x)
                exibir_math(res, [f"Calculando a primitiva de {f}", "Resultado omitindo a constante C."])
            elif op == "Integral Definida":
                res = integrate(f, (x, sympify(a), sympify(b)))
                exibir_math(res, [f"Área sob a curva de {a} até {b}"])
            
            registrar_historico(op, expr, res)
        except Exception as e: st.error(e)

# --- MÓDULO 3: CÁLCULO MULTIVARIÁVEL (Visual 3D) ---
elif modo == "Cálculo Multivariável":
    st.header("Campos Escalares e Vetoriais")
    expr = st.text_input("Função f(x, y):", "sin(x) * cos(y)")
    op = st.selectbox("Operação:", ["Gradiente", "Laplaciano", "Gráfico de Superfície 3D"])
    
    if st.button("Calcular / Visualizar"):
        f = sympify(expr)
        if op == "Gráfico de Superfície 3D":
            f_num = lambdify((x, y), f, "numpy")
            v = np.linspace(-5, 5, 50)
            X, Y = np.meshgrid(v, v)
            Z = f_num(X, Y)
            fig = go.Figure(data=[go.Surface(z=Z, x=X, y=Y, colorscale='Viridis')])
            st.plotly_chart(fig)
        else:
            res = [diff(f, x), diff(f, y)] if op == "Gradiente" else diff(f, x, 2) + diff(f, y, 2)
            exibir_math(res)
            registrar_historico(op, expr, res)

# --- MÓDULO 4: EDO & ÁLGEBRA ---
elif modo == "EDO & Álgebra Linear":
    aba1, aba2 = st.tabs(["Equações Diferenciais", "Álgebra Linear"])
    
    with aba1:
        edo_input = st.text_input("EDO (use f(x)):", "f(x).diff(x) + 2*f(x) - exp(x)")
        if st.button("Resolver EDO"):
            f_func = Function('f')
            sol = dsolve(Eq(sympify(edo_input, locals={'f': f_func}), 0), f_func(x))
            exibir_math(sol)
            registrar_historico("EDO", edo_input, sol)

    with aba2:
        n = st.number_input("Dimensão da Matriz", 2, 5, 2)
        st.write("Elementos (separe por espaço):")
        grid = [st.text_input(f"Linha {i+1}", "1 0") for i in range(n)]
        if st.button("Processar Matriz"):
            m = Matrix([[sympify(v) for v in r.split()] for r in grid])
            col1, col2 = st.columns(2)
            col1.write("Determinante:")
            col1.latex(latex(m.det()))
            col2.write("Inversa:")
            col2.latex(latex(m.inv() if m.det() != 0 else "Não inversível"))
            registrar_historico("Matriz", str(m), f"Det: {m.det()}")

# --- RODAPÉ: HISTÓRICO ---
st.divider()
with st.expander("📂 Histórico da Sessão & Exportação"):
    if st.session_state.historico:
        df = pd.DataFrame(st.session_state.historico)
        st.dataframe(df, use_container_width=True)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Baixar Relatório CSV", csv, "calculos.csv", "text/csv")
    else:
        st.write("Nenhum dado registrado.")
