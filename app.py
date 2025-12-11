import streamlit as st
import database as db
import pandas as pd

# 1. Configuración de página
st.set_page_config(
    page_title="Finanzas & Arcade", 
    page_icon="🔐", 
    layout="wide", 
    initial_sidebar_state="expanded"  # <--- Añade esto
)

# --- ESTILOS CSS PERSONALIZADOS (SOLUCIÓN MENÚ) ---
st.markdown("""
    <style>
    /* 1. Ocultar los 3 puntos de la derecha (stToolbar) y el footer */
    [data-testid="stToolbar"] {
        visibility: hidden !important;
        display: none !important;
    }
    footer {
        visibility: hidden !important;
        display: none !important;
    }
    
    /* 2. ASEGURAR que el botón de desplegar el menú (la flecha >) sea visible */
    [data-testid="collapsedControl"] {
        visibility: visible !important;
        display: block !important;
        color: #00C9FF !important; /* Lo ponemos azul neón para que se vea bien */
    }
    
    /* 3. Estilo de Botones Premium */
    div.stButton > button {
        background: linear-gradient(90deg, #00C9FF 0%, #92FE9D 100%);
        color: black;
        font-weight: bold;
        border: none;
        border-radius: 12px;
        padding: 0.5rem 1rem;
        transition: transform 0.2s;
    }
    div.stButton > button:hover {
        transform: scale(1.05);
        color: black;
    }

    /* 4. Títulos con Degradado */
    h1 {
        background: -webkit-linear-gradient(45deg, #00C9FF, #92FE9D);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. BLOQUE CSS PARA OCULTAR MENÚS Y BOTONES DE GITHUB
# --- ESTILOS CSS PERSONALIZADOS ---
st.markdown("""
    <style>
    /* Ocultamos el menú de los 3 puntos (derecha) y el pie de página "Made with Streamlit" */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* IMPORTANTE: NO ocultamos el 'header' completo, porque ahí vive la flecha del menú móvil.
       En su lugar, ocultamos solo la decoración superior si molesta, pero dejamos la barra funcional */
    
    /* Estilo Premium para Botones (Degradado Verde/Azul) */
    div.stButton > button {
        background: linear-gradient(90deg, #00C9FF 0%, #92FE9D 100%);
        color: black;
        font-weight: bold;
        border: none;
        border-radius: 12px;
        padding: 0.5rem 1rem;
        transition: transform 0.2s;
    }
    div.stButton > button:hover {
        transform: scale(1.05);
        color: black;
    }

    /* Títulos con Degradado */
    h1 {
        background: -webkit-linear-gradient(45deg, #00C9FF, #92FE9D);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Inicializar DB al arrancar
# (Si aquí te fallaba antes es porque database.py no tenía esta función actualizada)
db.create_tables()

def login_page():
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.title("🔐 Acceso al Sistema")
        st.markdown("Plataforma de gestión financiera y entretenimiento.")
        
        menu = ["Iniciar Sesión", "Registrarse"]
        choice = st.selectbox("Selecciona opción", menu)

        if choice == "Iniciar Sesión":
            username = st.text_input("Usuario")
            password = st.text_input("Contraseña", type='password')
            if st.button("Entrar", use_container_width=True):
                hashed_pswd = db.make_hashes(password)
                result = db.login_user(username, hashed_pswd)
                if result:
                    st.success(f"Bienvenido {username}")
                    st.session_state['logged_in'] = True
                    st.session_state['username'] = username
                    st.rerun()
                else:
                    st.error("Credenciales incorrectas")

        elif choice == "Registrarse":
            new_user = st.text_input("Elige Usuario")
            new_password = st.text_input("Elige Contraseña", type='password')
            
            if st.button("Crear Cuenta", use_container_width=True):
                # --- LÓGICA ESPECIAL PARA ADMIN ---
                if new_user.lower() == "admin":
                    # AQUÍ ESTÁ EL TRUCO:
                    # Solo permite crear 'admin' si la contraseña es exactamente esta clave secreta:
                    if new_password == "ædm1nñ1":  # <--- CAMBIA ESTO POR TU CONTRASEÑA REAL
                        hashed_new_password = db.make_hashes(new_password)
                        exito = db.add_userdata(new_user, hashed_new_password)
                        if exito:
                            st.success("¡Cuenta de ADMIN creada con éxito! Ahora inicia sesión.")
                        else:
                            st.error("El usuario admin ya existe.")
                    else:
                        # Si intentan registrar admin con otra contraseña, les da error
                        st.warning("El nombre de usuario 'admin' está reservado.")
                
                # --- LÓGICA PARA USUARIOS NORMALES ---
                else:
                    hashed_new_password = db.make_hashes(new_password)
                    exito = db.add_userdata(new_user, hashed_new_password)
                    if exito:
                        st.success("Cuenta creada. Ahora inicia sesión.")
                    else:
                        st.error("Ese usuario ya existe.")

# --- LÓGICA PRINCIPAL ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    login_page()
else:
    # --- MENÚ DE NAVEGACIÓN (Importante para móvil) ---
    st.sidebar.title(f"👤 {st.session_state['username']}")
    
    if st.sidebar.button("Cerrar Sesión"):
        st.session_state['logged_in'] = False
        st.rerun()

    # --- PÁGINA DE BIENVENIDA (Dashboard) ---
    st.title("Panel Principal")
    
    # MENSAJE ESPECIAL PARA MÓVIL
    st.success(f"¡Hola, {st.session_state['username']}! Has iniciado sesión correctamente.")
    
    st.info("""
    📱 **¿Estás en el móvil?**
    Toca la flecha **(>)** en la esquina superior izquierda para abrir el menú y ver las herramientas.
    """)
    
    # Tarjetas de acceso rápido (Para no depender solo del sidebar)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        ### 📈 Mercado
        Consulta precios de acciones y criptos en tiempo real.
        """)
    with col2:
        st.markdown("""
        ### 🕹️ Arcade
        Juega a clásicos como Pac-Man y Donkey Kong.
        """)

    st.markdown("---")
    st.write("### Novedades")
    st.write("- 🏆 **Ranking Global:** Ahora puedes guardar tus puntuaciones.")
    st.write("- 📱 **Soporte Móvil:** Controles táctiles en los juegos.")