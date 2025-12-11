import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Simulador FIRE España", page_icon="📈", layout="wide")

# --- FUNCIONES DE LÓGICA (Tus funciones de antes) ---
TRAMOS_IRPF = [
    (6000, 0.19),
    (50000, 0.21),
    (200000, 0.23),
    (300000, 0.27),
    (float('inf'), 0.28)
]

def calcular_impuesto_ganancia(ganancia):
    if ganancia <= 0: return 0.0
    cuota = 0.0
    resto = ganancia
    tramo_anterior = 0
    for limite, tipo in TRAMOS_IRPF:
        base = min(resto, limite - tramo_anterior)
        if base > 0:
            cuota += base * tipo
            resto -= base
            tramo_anterior = limite
        if resto <= 0: break
    return cuota

def simular_inversion(p_inicial, p_mensual, tasa_anual, anyos, retiro_anio=None, retiro_cantidad=0):
    """
    Simula la inversión mes a mes y devuelve un DataFrame con los datos.
    Permite simular un retiro puntual en un año específico.
    """
    datos = []
    
    saldo = p_inicial
    invertido = p_inicial
    tasa_mensual = (1 + tasa_anual / 100)**(1/12) - 1
    
    # Lógica simplificada FIFO para la gráfica (promedio ponderado)
    # Para la web app visual, usaremos el saldo total vs invertido para la gráfica rápida
    
    total_meses = anyos * 12
    mes_retiro = (retiro_anio * 12) if retiro_anio else -1
    
    for m in range(1, total_meses + 1):
        # 1. Interés
        saldo = saldo * (1 + tasa_mensual)
        
        # 2. Aportación
        saldo += p_mensual
        invertido += p_mensual
        
        # 3. Evento de Retirada (si toca este mes)
        if m == mes_retiro and retiro_cantidad > 0:
            # Aquí asumimos que el usuario saca BRUTO para simplificar la gráfica
            # O podríamos calcular el neto inverso, pero para visualizar el impacto:
            saldo -= retiro_cantidad
            # Al retirar, técnicamente se reduce lo invertido proporcionalmente, 
            # pero para ver "cuánto puse yo", solemos dejar la línea de 'invertido' acumulada 
            # o la restamos. Vamos a restarla para que sea realista.
            ratio_retiro = retiro_cantidad / (saldo + retiro_cantidad) # Porcentaje que sacamos
            invertido = invertido * (1 - ratio_retiro)

        # Guardar datos anuales o mensuales
        datos.append({
            "Mes": m,
            "Año": m / 12,
            "Saldo Total": round(saldo, 2),
            "Capital Invertido": round(invertido, 2),
            "Beneficio Bruto": round(saldo - invertido, 2)
        })
        
    return pd.DataFrame(datos)

# --- INTERFAZ GRÁFICA (SIDEBAR) ---
st.sidebar.header("⚙️ Configuración de Inversión")

capital_inicial = st.sidebar.number_input("Capital Inicial (€)", value=10000.0, step=1000.0)
aportacion_mensual = st.sidebar.number_input("Aportación Mensual (€)", value=500.0, step=50.0)
tasa_interes = st.sidebar.slider("Rentabilidad Anual Esperada (%)", min_value=1.0, max_value=15.0, value=8.0, step=0.1)
anyos = st.sidebar.slider("Duración Inversión (Años)", min_value=5, max_value=50, value=20)

st.sidebar.markdown("---")
st.sidebar.header("💸 Simular Gasto (Coche/Casa)")
activar_retiro = st.sidebar.checkbox("Simular una retirada de dinero")

retiro_anio = None
retiro_cantidad = 0.0

if activar_retiro:
    col1, col2 = st.sidebar.columns(2)
    retiro_anio = col1.number_input("Año del retiro", min_value=1, max_value=anyos, value=int(anyos/2))
    retiro_cantidad = col2.number_input("Cantidad (€)", min_value=0.0, value=50000.0, step=1000.0)
    st.sidebar.info(f"Se retirarán {retiro_cantidad:,.0f}€ en el año {retiro_anio}.")

# --- LÓGICA PRINCIPAL ---

# 1. Calcular datos
df = simular_inversion(capital_inicial, aportacion_mensual, tasa_interes, anyos, retiro_anio, retiro_cantidad)

# Obtener valores finales
final_saldo = df.iloc[-1]["Saldo Total"]
final_invertido = df.iloc[-1]["Capital Invertido"]
final_beneficio = df.iloc[-1]["Beneficio Bruto"]

# Cálculo fiscal final
impuestos_finales = calcular_impuesto_ganancia(final_beneficio)
neto_final = final_saldo - impuestos_finales

# --- MOSTRAR RESULTADOS EN PANTALLA ---

st.title("🇪🇸 Simulador de Inversión Fiscal (España)")
st.markdown("Visualiza cómo crece tu dinero y calcula los impuestos reales de Hacienda.")

# Métricas Principales (Top Dashboard)
col1, col2, col3, col4 = st.columns(4)
col1.metric("Patrimonio Final Bruto", f"{final_saldo:,.0f} €", delta=f"{tasa_interes}% Interés")
col2.metric("Dinero de tu bolsillo", f"{final_invertido:,.0f} €")
col3.metric("Beneficio antes de Impuestos", f"{final_beneficio:,.0f} €")
col4.metric("💰 Neto (Tras Hacienda)", f"{neto_final:,.0f} €", delta_color="off")

st.markdown("---")

# Gráfico
tab1, tab2 = st.tabs(["📈 Gráfico Evolución", "📋 Tabla Detallada"])

with tab1:
    st.subheader("Evolución de tu Patrimonio")
    
    fig = go.Figure()
    
    # Línea de Saldo Total
    fig.add_trace(go.Scatter(
        x=df["Año"], y=df["Saldo Total"],
        mode='lines', name='Saldo Total (Interés Compuesto)',
        line=dict(color='#00CC96', width=3),
        fill='tozeroy' # Relleno debajo
    ))
    
    # Línea de Invertido
    fig.add_trace(go.Scatter(
        x=df["Año"], y=df["Capital Invertido"],
        mode='lines', name='Tu Dinero Invertido',
        line=dict(color='#636EFA', width=2, dash='dash')
    ))
    
    # Marcador de retiro si existe
    if activar_retiro and retiro_anio:
        # Encontrar el saldo en ese punto aproximado para poner el punto
        saldo_en_retiro = df.loc[df['Mes'] == retiro_anio*12, 'Saldo Total'].values[0]
        fig.add_annotation(
            x=retiro_anio, y=saldo_en_retiro,
            text=f"Retirada: -{retiro_cantidad/1000:.0f}k",
            showarrow=True, arrowhead=1
        )

    fig.update_layout(
        xaxis_title="Años",
        yaxis_title="Euros (€)",
        hovermode="x unified",
        template="plotly_dark"  # Modo oscuro queda muy bien
    )
    
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Desglose Año a Año")
    # Filtramos para mostrar solo el mes 12 de cada año para no saturar la tabla
    df_anual = df[df['Mes'] % 12 == 0].copy()
    df_anual['Año'] = df_anual['Año'].astype(int)
    
    # Formateo de columnas
    st.dataframe(
        df_anual[["Año", "Capital Invertido", "Beneficio Bruto", "Saldo Total"]].style.format("{:,.2f} €"),
        use_container_width=True
    )

# --- SECCIÓN DE IMPUESTOS ---
st.markdown("---")
st.subheader("🏛️ La factura de Hacienda (Detalle Final)")

if final_beneficio > 0:
    col_imp_1, col_imp_2 = st.columns([1, 2])
    
    with col_imp_1:
        st.write("Si retirases **todo** hoy, pagarías:")
        st.error(f"Impuestos IRPF: {impuestos_finales:,.2f} €")
        tipo_medio = (impuestos_finales / final_beneficio) * 100
        st.caption(f"Tipo medio efectivo: {tipo_medio:.2f}% sobre beneficios")
        
    with col_imp_2:
        st.info("💡 **Consejo:** En España, si solo retiras una parte, se aplica el método FIFO (se venden primero las participaciones más antiguas). Este cálculo asume una venta total del patrimonio.")
else:
    st.warning("No tienes beneficios, por lo que no pagarías impuestos.")