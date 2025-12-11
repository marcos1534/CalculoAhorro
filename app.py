import streamlit as st
import database as db

st.set_page_config(page_title="Finanzas & Arcade", page_icon="🔐", layout="wide")

# Inicializar DB
db.create_usertable()

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
                db.add_userdata(new_user, db.make_hashes(new_password))
                st.success("Cuenta creada. Ahora inicia sesión.")

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    login_page()
else:
    st.title(f"Hola, {st.session_state['username']} 👋")
    st.info("👈 ¡Bienvenido! Usa el menú lateral para navegar por las diferentes herramientas y juegos.")
    
    st.markdown("### 📌 Novedades de la versión")
    st.write("- Nuevo simulador fiscal ajustado a 2025.")
    st.write("- Sala de Arcade ampliada con clásicos: Pac-Man, Tetris, DK y Space Invaders.")
    
    if st.button("Cerrar Sesión"):
        st.session_state['logged_in'] = False
        st.rerun()