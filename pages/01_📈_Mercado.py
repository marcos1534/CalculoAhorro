import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

st.set_page_config(page_title="Mercado", page_icon="📈", layout="wide")

st.title("Monitor de Mercado Global")
st.markdown("Datos en tiempo real y gráficos históricos.")

tickers = {
    "S&P 500 (SPY)": "SPY",
    "MSCI World (URTH)": "URTH",
    "Nasdaq 100 (QQQ)": "QQQ",
    "Oro (GLD)": "GLD",
    "Bitcoin (BTC)": "BTC-USD"
}

seleccion = st.selectbox("Selecciona Activo:", list(tickers.keys()))
simbolo = tickers[seleccion]
periodo = st.select_slider("Periodo:", options=["1mo", "6mo", "1y", "5y", "10y", "max"], value="1y")

try:
    with st.spinner('Descargando datos...'):
        data = yf.Ticker(simbolo).history(period=periodo)
    
    ultimo = data['Close'].iloc[-1]
    previo = data['Close'].iloc[-2]
    var = ultimo - previo
    var_pct = (var / previo) * 100
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Precio", f"{ultimo:.2f}", f"{var:.2f}")
    c2.metric("Variación %", f"{var_pct:.2f}%")
    c3.metric("Volumen", f"{data['Volume'].iloc[-1]:,.0f}")

    fig = go.Figure(data=[go.Candlestick(x=data.index, open=data['Open'], high=data['High'], low=data['Low'], close=data['Close'])])
    fig.update_layout(template="plotly_dark", title=f"Gráfico {seleccion}")
    st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"Error cargando datos: {e}")