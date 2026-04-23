import streamlit as st
import sympy as sp
from sympy import *

x, y, z, t, n = symbols('x y z t n')

st.set_page_config(page_title="IA de Matemática", page_icon="🧮", layout="centered")

st.markdown("""
    <style>
    body { background-color: #0e1117; color: white; }
    .stButton>button { background-color: #1f77b4; color: white; border-radius: 8px; }
    </style>
""", unsafe_allow_html=True)

st.title("🧮 IA de Matemática")
st.markdown("Resolva questões de **Matemática Básica** e **Cálculo 1 ao 4** com passo a passo.")

categoria = st.selectbox("Escolha a categoria:", [
    "Matemática Básica",
    "Cálculo 1 - Limites e Derivadas",
    "Cálculo 2 - Integrais",
    "Cálculo 3 - Multivariável e Séries",
    "Cálculo 4 - EDO e Álgebra Linear"
])

st.divider()

def mostrar_resultado(passos, resultado):
    st.markdown("### 📌 Passo a Passo")
    for i, p in enumerate(passos, 1):
        st.markdown(f"**Passo {i}:** {p}")
    st.success(f"✅ Resultado: {resultado}")

if categoria == "Matemática Básica":
    op = st.selectbox("Operação:", ["Simplificar", "Resolver Equação", "Fatorar", "Expandir"])
    expr = st.text_input("Digite a expressão (ex: x**2 - 4):")
    if st.button("Calcular") and expr:
        try:
            e = sympify(expr)
            if op == "Simplificar":
                mostrar_resultado(
                    [f"Expressão original: {e}", "Aplicando simplificação..."],
                    simplify(e)
                )
            elif op == "Resolver Equação":
                mostrar_resultado(
                    [f"Equação: {e} = 0", "Isolando x..."],
                    solve(e, x)
                )
            elif op == "Fatorar":
                mostrar_resultado(
                    [f"Expressão original: {e}", "Fatorando..."],
                    factor(e)
                )
            elif op == "Expandir":
                mostrar_resultado(
                    [f"Expressão original: {e}", "Expandindo..."],
                    expand(e)
                )
        except Exception as err:
            st.error(f"Erro: {err}")

elif categoria == "Cálculo 1 - Limites e Derivadas":
    op = st.selectbox("Operação:", ["Limite", "Derivada 1ª ordem", "Derivada 2ª ordem"])
    expr = st.text_input("Digite a expressão:")
    if op == "Limite":
        ponto = st.text_input("x se aproxima de (ex: 0, oo, 1):")
    if st.button("Calcular") and expr:
        try:
            e = sympify(expr)
            if op == "Limite":
                p = sympify(ponto)
                mostrar_resultado(
                    [f"f(x) = {e}", f"Calculando lim x→{p}..."],
                    limit(e, x, p)
                )
            elif op == "Derivada 1ª ordem":
                mostrar_resultado(
                    [f"f(x) = {e}", "Aplicando regras de derivação..."],
                    diff(e, x)
                )
            elif op == "Derivada 2ª ordem":
                d1 = diff(e, x)
                mostrar_resultado(
                    [f"f(x) = {e}", f"Primeira derivada: f'(x) = {d1}", "Derivando novamente..."],
                    diff(e, x, 2)
                )
        except Exception as err:
            st.error(f"Erro: {err}")

elif categoria == "Cálculo 2 - Integrais":
    op = st.selectbox("Operação:", ["Integral Indefinida", "Integral Definida"])
    expr = st.text_input("Digite a expressão:")
    if op == "Integral Definida":
        a = st.text_input("Limite inferior:")
        b = st.text_input("Limite superior:")
    if st.button("Calcular") and expr:
        try:
            e = sympify(expr)
            if op == "Integral Indefinida":
                mostrar_resultado(
                    [f"f(x) = {e}", "Aplicando técnicas de integração..."],
                    str(integrate(e, x)) + " + C"
                )
            elif op == "Integral Definida":
                la, lb = sympify(a), sympify(b)
                indef = integrate(e, x)
                mostrar_resultado(
                    [f"f(x) = {e}", f"Primitiva F(x) = {indef}", f"Calculando F({lb}) - F({la})..."],integrate(e, (x, la, lb))
                )
        except Exception as err:
            st.error(f"Erro: {err}")

elif categoria == "Cálculo 3 - Multivariável e Séries":
    op = st.selectbox("Operação:", ["Série de Taylor", "Derivada Parcial ∂/∂x", "Derivada Parcial ∂/∂y", "Gradiente"])
    expr = st.text_input("Digite a expressão:")
    if op == "Série de Taylor":
        ordem = st.number_input("Ordem da série:", min_value=1, max_value=20, value=5)
    if st.button("Calcular") and expr:
        try:
            e = sympify(expr)
            if op == "Série de Taylor":
                mostrar_resultado(
                    [f"f(x) = {e}", f"Expandindo em torno de x=0 até ordem {int(ordem)}..."],
                    series(e, x, 0, int(ordem))
                )
            elif op == "Derivada Parcial ∂/∂x":
                mostrar_resultado(
                    [f"f(x,y) = {e}", "Derivando em relação a x (y constante)..."],
                    diff(e, x)
                )
            elif op == "Derivada Parcial ∂/∂y":
                mostrar_resultado(
                    [f"f(x,y) = {e}", "Derivando em relação a y (x constante)..."],
                    diff(e, y)
                )
            elif op == "Gradiente":
                dx, dy = diff(e, x), diff(e, y)
                mostrar_resultado(
                    [f"f(x,y) = {e}", f"∂f/∂x = {dx}", f"∂f/∂y = {dy}"],
                    f"∇f = [{dx}, {dy}]"
                )
        except Exception as err:
            st.error(f"Erro: {err}")

elif categoria == "Cálculo 4 - EDO e Álgebra Linear":
    op = st.selectbox("Operação:", ["EDO", "Determinante de Matriz", "Autovalores"])
    if op == "EDO":
        expr = st.text_input("Digite a EDO (ex: f(x).diff(x) - f(x)):")
        if st.button("Calcular") and expr:
            try:
                f = Function('f')
                e = sympify(expr, locals={'f': f, 'x': x})
                mostrar_resultado(
                    [f"EDO: {e} = 0", "Aplicando método de resolução..."],
                    dsolve(Eq(e, 0), f(x))
                )
            except Exception as err:
                st.error(f"Erro: {err}")
    else:
        n_mat = st.number_input("Tamanho da matriz (ex: 2 para 2x2):", min_value=2, max_value=5, value=2)
        st.markdown("Digite os elementos (separados por espaço):")
        linhas = []
        for i in range(int(n_mat)):
            linha = st.text_input(f"Linha {i+1}:", key=f"linha_{i}")
            linhas.append(linha)
        if st.button("Calcular"):
            try:
                mat = [[sympify(v) for v in l.split()] for l in linhas]
                M = Matrix(mat)
                if op == "Determinante de Matriz":
                    mostrar_resultado(
                        [f"Matriz: {M}", "Calculando determinante..."],
                        M.det()
                    )
                elif op == "Autovalores":
                    mostrar_resultado(
                        [f"Matriz: {M}", "Calculando polinômio característico...", "Resolvendo det(A - λI) = 0..."],
                        M.eigenvals()
                    )
            except Exception as err:
                st.error(f"Erro: {err}")
