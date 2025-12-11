import streamlit as st
import yfinance as yf
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="Mercado", page_icon="📈", layout="wide")

# --- SELECTOR DE TEMA ---
tema = st.sidebar.radio("Tema Visual:", ["Claro", "Oscuro"], horizontal=True)
from utils import styles
st.markdown(styles.get_css(tema), unsafe_allow_html=True)

st.title("📈 Mercado: Entiende dónde inviertes")
st.markdown("""
Aquí no verás solo números. Te explicamos qué es cada cosa para que decidas mejor.
Selecciona un fondo para ver cómo se ha comportado en el pasado.
""")

# Diccionario con explicación amigable
activos = {
    "S&P 500 (SPY)": {
        "ticker": "SPY",
        "desc": "Las 500 empresas más grandes de EE.UU. (Apple, Microsoft, Amazon...). Es la inversión estándar por excelencia.",
        "riesgo": "Medio"
    },
    "Mundo Entero (URTH)": {
        "ticker": "URTH",
        "desc": "Invierte en empresas de todo el mundo desarrollado. Más diversificado que el S&P 500.",
        "riesgo": "Medio-Bajo"
    },
    "Tecnología (QQQ)": {
        "ticker": "QQQ",
        "desc": "Las 100 mayores empresas tecnológicas del Nasdaq. Alto potencial de crecimiento, pero más volátil.",
        "riesgo": "Alto"
    },
    "Oro (GLD)": {
        "ticker": "GLD",
        "desc": "Oro físico. Se usa como refugio cuando hay crisis o mucha inflación.",
        "riesgo": "Bajo (pero crece menos)"
    }
}

col1, col2 = st.columns([1, 2])

with col1:
    seleccion = st.selectbox("¿Qué quieres analizar?", list(activos.keys()))
    info = activos[seleccion]
    
    st.markdown(f"""
    <div class="metric-card">
        <h3>🔍 {seleccion}</h3>
        <p><strong>¿Qué es?</strong> {info['desc']}</p>
        <p><strong>Nivel de Riesgo:</strong> {info['riesgo']}</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    periodo = st.select_slider("Ver evolución de:", options=["1 Año", "5 Años", "10 Años", "Máximo"], value="5 Años")
    mapa_periodo = {"1 Año": "1y", "5 Años": "5y", "10 Años": "10y", "Máximo": "max"}
    
    try:
        with st.spinner('Consultando la bolsa...'):
            ticker = info['ticker']
            data = yf.Ticker(ticker).history(period=mapa_periodo[periodo])
            
            # Gráfico limpio
            fig = px.area(data, x=data.index, y="Close", title=f"Evolución de 1 participación de {ticker}")
            fig.update_layout(xaxis_title="", yaxis_title="Precio ($)", template="plotly_white" if tema == "Claro" else "plotly_dark")
            st.plotly_chart(fig, use_container_width=True)
            
            # Rentabilidad calculada
            precio_ini = data['Close'].iloc[0]
            precio_fin = data['Close'].iloc[-1]
            rentabilidad = ((precio_fin - precio_ini) / precio_ini) * 100
            
            st.info(f"💡 Si hubieras invertido aquí hace {periodo.lower()}, tu dinero habría crecido un **{rentabilidad:.2f}%**.")
            
    except:
        st.error("No se pudieron cargar los datos. Revisa tu conexión.")
