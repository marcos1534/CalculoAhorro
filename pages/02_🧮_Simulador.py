import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Simulador", page_icon="🧮", layout="wide")

TRAMOS_IRPF = [(6000, 0.19), (50000, 0.21), (200000, 0.23), (300000, 0.27), (float('inf'), 0.28)]

def calc_impuesto(ganancia):
    if ganancia <= 0: return 0.0
    cuota = 0.0
    resto = ganancia
    tramo_ant = 0
    for limite, tipo in TRAMOS_IRPF:
        base = min(resto, limite - tramo_ant)
        if base > 0:
            cuota += base * tipo
            resto -= base
            tramo_ant = limite
        if resto <= 0: break
    return cuota

st.title("Simulador de Estrategia de Inversión")

c_input, c_result = st.columns([1, 2])
with c_input:
    ini = st.number_input("Capital Inicial (€)", 1000.0, step=500.0)
    men = st.number_input("Aportación Mensual (€)", 200.0, step=50.0)
    int_anual = st.slider("Interés Anual (%)", 1.0, 15.0, 8.0)
    anos = st.slider("Duración (Años)", 5, 50, 20)

    # Lógica de cálculo
    datos = []
    saldo = ini
    inv = ini
    tasa_mensual = (1 + int_anual/100)**(1/12) - 1
    
    for m in range(1, anos*12 + 1):
        saldo = saldo * (1 + tasa_mensual) + men
        inv += men
        if m % 12 == 0:
            datos.append({"Año": m//12, "Invertido": inv, "Total": saldo, "Beneficio": saldo-inv})
    
    df = pd.DataFrame(datos)
    
    # Resultados finales
    final_total = df.iloc[-1]["Total"]
    final_inv = df.iloc[-1]["Invertido"]
    final_ben = df.iloc[-1]["Beneficio"]
    imp = calc_impuesto(final_ben)
    neto = final_total - imp

with c_result:
    m1, m2, m3 = st.columns(3)
    m1.metric("Patrimonio Bruto", f"{final_total:,.0f} €")
    m2.metric("Impuestos IRPF", f"{imp:,.0f} €", delta_color="inverse")
    m3.metric("Neto Real", f"{neto:,.0f} €")
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["Año"], y=df["Total"], fill='tozeroy', name='Total Acumulado'))
    fig.add_trace(go.Scatter(x=df["Año"], y=df["Invertido"], name='Tu dinero (Bolsillo)', line=dict(dash='dash')))
    fig.update_layout(template="plotly_dark", height=400)
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Tabla detallada")
st.dataframe(df, use_container_width=True)