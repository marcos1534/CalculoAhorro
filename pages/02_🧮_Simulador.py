import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Simulador", page_icon="🧮", layout="wide")

# --- TEMA ---
tema = st.sidebar.radio("Tema Visual:", ["Claro", "Oscuro"], horizontal=True)
from utils import styles
st.markdown(styles.get_css(tema), unsafe_allow_html=True)

# Lógica Fiscal (Igual que antes)
TRAMOS_IRPF = [(6000, 0.19), (50000, 0.21), (200000, 0.23), (300000, 0.27), (float('inf'), 0.28)]
def calc_impuesto(ganancia):
    if ganancia <= 0: return 0.0
    cuota, resto, ant = 0.0, ganancia, 0
    for lim, tipo in TRAMOS_IRPF:
        base = min(resto, lim - ant)
        if base > 0: cuota += base * tipo; resto -= base; ant = lim
        if resto <= 0: break
    return cuota

st.title("🧮 Simulador Avanzado de Inversión")

# --- COLUMNA DE DATOS ---
col_datos, col_graf = st.columns([1, 2])

with col_datos:
    st.subheader("1. Tu Plan")
    ini = st.number_input("Capital Inicial (€)", value=0.0, step=100.0)
    men = st.number_input("Aportación Mensual (€)", value=0.0, step=50.0)
    anos = st.number_input("Años de Inversión", value=20, step=1)
    
    st.subheader("2. Rentabilidad")
    tipo_activo = st.selectbox("¿Dónde inviertes?", ["Manual", "S&P 500 (Histórico ~10%)", "Mundo (Histórico ~8%)", "Conservador (~4%)"])
    
    if tipo_activo == "Manual":
        interes = st.number_input("Interés Anual Estimado (%)", value=5.0, step=0.1)
    elif "S&P 500" in tipo_activo: interes = 10.0
    elif "Mundo" in tipo_activo: interes = 8.0
    else: interes = 4.0
    
    if tipo_activo != "Manual":
        st.caption(f"Aplicando un {interes}% anual basado en medias históricas.")

    st.subheader("3. Retiradas (Hipoteca/Coche)")
    usar_retiro = st.checkbox("Quiero sacar dinero en el futuro")
    retiro_anio = 0
    retiro_cant = 0.0
    
    if usar_retiro:
        retiro_anio = st.slider("¿En qué año sacas el dinero?", 1, int(anos), int(anos/2))
        retiro_cant = st.number_input("¿Cuánto necesitas sacar? (€)", value=20000.0)
        st.caption(f"El simulador restará {retiro_cant:,.0f}€ en el año {retiro_anio} y seguirá invirtiendo el resto.")

# --- CÁLCULOS ---
saldo = ini
invertido = ini
tasa_men = (1 + interes/100)**(1/12) - 1
datos = []

# Guardamos el mes del retiro
mes_retiro_obj = retiro_anio * 12

for m in range(1, int(anos*12) + 1):
    # 1. Interés compuesto
    saldo = saldo * (1 + tasa_men)
    
    # 2. Aportación mensual
    saldo += men
    invertido += men
    
    # 3. Retirada (si toca)
    evento = ""
    if usar_retiro and m == mes_retiro_obj:
        if saldo >= retiro_cant:
            saldo -= retiro_cant
            # Al sacar dinero, reducimos proporcionalmente lo que consideramos "invertido" 
            # para no falsear el cálculo de beneficios futuros.
            ratio = retiro_cant / (saldo + retiro_cant)
            invertido = invertido * (1 - ratio)
            evento = "🔴 Retirada"
        else:
            evento = "❌ Saldo insuficiente"

    # Guardamos datos anuales para la gráfica (mes 12, 24, etc)
    if m % 12 == 0:
        datos.append({
            "Año": int(m/12),
            "Saldo": saldo,
            "Invertido": invertido,
            "Beneficio": saldo - invertido,
            "Evento": evento
        })

df = pd.DataFrame(datos)

# --- RESULTADOS VISUALES ---
with col_graf:
    # Métricas Finales
    fin_saldo = df.iloc[-1]["Saldo"]
    fin_ben = df.iloc[-1]["Beneficio"]
    impuestos = calc_impuesto(fin_ben)
    neto = fin_saldo - impuestos
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Patrimonio Bruto", f"{fin_saldo:,.0f} €")
    c2.metric("Impuestos (Est.)", f"{impuestos:,.0f} €")
    c3.metric("Neto al Bolsillo", f"{neto:,.0f} €", delta="Dinero Real")
    
    # Gráfica
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["Año"], y=df["Saldo"], fill='tozeroy', name='Valor Cartera', line=dict(color='#00C9FF')))
    fig.add_trace(go.Scatter(x=df["Año"], y=df["Invertido"], name='Tu Dinero', line=dict(color='gray', dash='dash')))
    
    # Marcador de retirada
    if usar_retiro and retiro_cant <= df[df["Año"]==retiro_anio]["Saldo"].values[0] + retiro_cant:
        y_pos = df[df["Año"]==retiro_anio]["Saldo"].values[0]
        fig.add_annotation(x=retiro_anio, y=y_pos, text="Gasto", showarrow=True, arrowhead=1)

    fig.update_layout(title="Evolución de tu Patrimonio", template="plotly_white" if tema == "Claro" else "plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

# Tabla
st.write("### Desglose Año a Año")
st.dataframe(df.style.format({"Saldo": "{:,.2f} €", "Invertido": "{:,.2f} €", "Beneficio": "{:,.2f} €"}), use_container_width=True)
