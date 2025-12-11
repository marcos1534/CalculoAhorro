import streamlit as st
import database as db
import pandas as pd

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Finanzas & Arcade", 
    page_icon="🔐", 
    layout="wide",
    initial_sidebar_state="expanded"  # Ayuda a que el menú se vea mejor en móviles
)

# --- 2. INICIALIZAR BASE DE DATOS ---
# Se asegura de que las tablas existan antes de hacer nada
db.create_tables()

# --- 3. ESTILOS CSS (SOLO ESTÉTICA, SIN OCULTAR MENÚS) ---
st.markdown("""
    <style>
    /* Ocultamos solo el pie de página de "Made with Streamlit" para limpiar */
    footer {visibility: hidden;}
    
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
    
    /* Input fields más bonitos */
    .stTextInput > div > div > input {
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. FUNCIÓN DE LA PÁGINA DE LOGIN ---
def login_page():
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.title("🔐 Acceso al Sistema")
        st.info("💡 **Nota:** Puedes abrir el menú lateral (>) y acceder a los juegos o al mercado sin iniciar sesión.")
        
        menu = ["Iniciar Sesión", "Registrarse"]
        choice = st.selectbox("Selecciona una opción", menu)

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
                    st.rerun() # Recargar para entrar al panel
                else:
                    st.error("Usuario o contraseña incorrectos")

        elif choice == "Registrarse":
            st.subheader("Crear nueva cuenta")
            new_user = st.text_input("Elige un Usuario")
            new_password = st.text_input("Elige una Contraseña", type='password')
            
            if st.button("Crear Cuenta", use_container_width=True):
                # --- LÓGICA ESPECIAL PARA ADMIN (PUERTA TRASERA) ---
                if new_user.lower() == "admin":
                    # Solo permite registrar 'admin' si la contraseña es la clave maestra
                    if new_password == "SoyElJefe123": 
                        hashed_new_password = db.make_hashes(new_password)
                        exito = db.add_userdata(new_user, hashed_new_password)
                        if exito:
                            st.success("¡Cuenta de ADMIN creada! Ahora inicia sesión.")
                        else:
                            st.error("El admin ya existe.")
                    else:
                        st.warning("El nombre de usuario 'admin' está reservado.")
                
                # --- REGISTRO USUARIO NORMAL ---
                else:
                    hashed_new_password = db.make_hashes(new_password)
                    exito = db.add_userdata(new_user, hashed_new_password)
                    if exito:
                        st.success("Cuenta creada correctamente. Ahora inicia sesión.")
                    else:
                        st.error("Ese nombre de usuario ya está en uso.")

# --- 5. CONTROL DE FLUJO PRINCIPAL ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# Si NO está logueado, mostramos Login (pero el menú lateral sigue accesible)
if not st.session_state['logged_in']:
    login_page()

# Si ESTÁ logueado, mostramos el Panel de Bienvenida y opciones extra
else:
    # Barra lateral solo para el usuario logueado (Logout y Admin)
    st.sidebar.title(f"👤 {st.session_state['username']}")
    
    if st.sidebar.button("Cerrar Sesión"):
        st.session_state['logged_in'] = False
        st.rerun()
        
    # Contenido Principal
    st.title("Panel Principal")
    st.success(f"¡Hola, {st.session_state['username']}! Has iniciado sesión.")
    
    st.markdown("""
    ### 🚀 Accesos Rápidos
    Usa el menú de la izquierda ( **>** ) para navegar:
    
    * **📈 Mercado:** Consulta el precio de Bitcoin, S&P 500 y más.
    * **🧮 Simulador:** Calcula tus impuestos y beneficios netos.
    * **🕹️ Arcade:** Juega a Pac-Man y Donkey Kong (¡Ahora con ranking!).
    * **🔮 Time Machine:** Mira cuánto dinero tendrías si hubieras invertido antes.
    """)

    # --- PANEL DE ADMIN (SOLO VISIBLE PARA 'admin') ---
    if st.session_state['username'] == 'admin':
        st.sidebar.markdown("---")
        st.sidebar.header("🛠️ Panel Admin")
        
        if st.sidebar.checkbox("Ver todos los usuarios"):
            st.subheader("Base de Datos de Usuarios")
            users = db.view_all_users()
            st.table(pd.DataFrame(users, columns=["Usuarios Registrados"]))
            
        if st.sidebar.button("Borrar TODOS los Récords"):
            db.delete_all_scores()
            st.sidebar.success("Tabla de puntuaciones reseteada a cero.")