import streamlit as st
import database as db
import pandas as pd

# 1. Configuración de página
st.set_page_config(page_title="Finanzas & Arcade", page_icon="🔐", layout="wide")

# 2. BLOQUE CSS PARA OCULTAR MENÚS Y BOTONES DE GITHUB
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

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
                # Protección simple para que nadie se registre como admin excepto tú (si lo desbloqueas)
                if new_user.lower() == "admin":
                     st.warning("El usuario 'admin' está reservado.")
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
    # BARRA LATERAL (Logout y Admin)
    st.sidebar.title(f"👤 {st.session_state['username']}")
    
    if st.button("Cerrar Sesión"):
        st.session_state['logged_in'] = False
        st.rerun()
        
    st.title("Panel Principal")
    st.info("👈 ¡Usa el menú lateral para navegar!")

    # --- PANEL DE ADMIN ---
    if st.session_state['username'] == 'admin':
        st.sidebar.markdown("---")
        st.sidebar.header("🛠️ Panel Admin")
        
        if st.sidebar.checkbox("Ver Usuarios Registrados"):
            st.subheader("Base de Datos de Usuarios")
            users = db.view_all_users()
            st.table(pd.DataFrame(users, columns=["Usuarios"]))
            
        if st.sidebar.button("Borrar TODOS los Récords"):
            db.delete_all_scores()
            st.sidebar.success("Tabla de puntuaciones reseteada.")

    st.markdown("---")
    st.write("### Novedades")
    st.write("- 🏆 **Ranking Global:** Ahora puedes guardar tus puntuaciones en la Zona Arcade.")
    st.write("- 👑 **Top 5:** Compite por aparecer en el tablón de honor.")