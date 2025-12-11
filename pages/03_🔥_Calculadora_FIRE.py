import streamlit as st

st.set_page_config(page_title="Calculadora FIRE", page_icon="🔥", layout="wide")

# --- TEMA ---
tema = st.sidebar.radio("Tema Visual:", ["Claro", "Oscuro"], horizontal=True)
from utils import styles
st.markdown(styles.get_css(tema), unsafe_allow_html=True)

st.title("🔥 ¿Cuándo seré libre financieramente?")
st.markdown("Esta herramienta calcula cuánto necesitas ahorrar para **dejar de trabajar** y vivir de tus rentas.")

col1, col2 = st.columns(2)

with col1:
    gastos_mensuales = st.number_input("¿Cuánto gastas al mes para vivir bien? (€)", value=1500.0, step=100.0)
    ahorros_actuales = st.number_input("¿Cuánto tienes ahorrado ya? (€)", value=5000.0, step=500.0)
    ahorro_mensual = st.number_input("¿Cuánto puedes ahorrar al mes? (€)", value=500.0, step=50.0)
    interes = st.slider("Rentabilidad Inversión (%)", 2.0, 12.0, 7.0)

with col2:
    # Regla del 4% (Standard FIRE)
    objetivo_fire = gastos_mensuales * 12 * 25
    st.markdown(f"""
    <div class="metric-card">
        <h3>🏁 Tu Meta (Número FIRE)</h3>
        <h1 style="color: #00C9FF">{objetivo_fire:,.0f} €</h1>
        <p>Según la regla del 4%, con esta cantidad podrías retirar {gastos_mensuales:,.0f}€/mes indefinidamente sin que se acabe el dinero.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Cálculo de años
    if ahorro_mensual > 0:
        saldo = ahorros_actuales
        meses = 0
        tasa_mensual = (1 + interes/100)**(1/12) - 1
        
        while saldo < objetivo_fire and meses < 1200: # Límite 100 años
            saldo = saldo * (1 + tasa_mensual) + ahorro_mensual
            meses += 1
        
        anios = meses // 12
        rest_meses = meses % 12
        
        if meses < 1200:
            st.success(f"🎉 Alcanzarás la Libertad Financiera en **{anios} años y {rest_meses} meses**.")
            st.progress(min(saldo / objetivo_fire, 1.0))
        else:
            st.warning("Con ese ritmo de ahorro, tardarás más de 100 años. Intenta aumentar tu ahorro o la rentabilidad.")
    else:
        st.error("Necesitas ahorrar algo cada mes para llegar a la meta.")
