import streamlit as st
import yfinance as yf

st.set_page_config(page_title="Máquina del Tiempo", page_icon="🔮")

st.title("🔮 La Máquina del Tiempo")
st.write("Calcula cuánto tendrías hoy si hubieras invertido en el pasado.")

col1, col2 = st.columns(2)
ticker = col1.text_input("Ticker (ej: AAPL, BTC-USD, NVDA)", "NVDA")
dinero = col2.number_input("Inversión Inicial (€/$)", 1000)

if st.button("Viajar al pasado (10 años)"):
    try:
        hist = yf.Ticker(ticker).history(period="10y")
        if not hist.empty:
            p_ini = hist['Close'].iloc[0]
            p_fin = hist['Close'].iloc[-1]
            total = (dinero / p_ini) * p_fin
            ganancia_pct = ((total - dinero) / dinero) * 100
            
            st.success(f"¡Resultado!")
            st.metric("Valor Hoy", f"{total:,.2f}", f"+{ganancia_pct:,.0f}%")
            st.line_chart(hist['Close'])
        else:
            st.error("No hay datos suficientes.")
    except:
        st.error("Ticker no encontrado.")