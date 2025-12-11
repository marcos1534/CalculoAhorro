import streamlit as st
import database as db
import pandas as pd

st.set_page_config(page_title="Finanzas & Arcade", page_icon="🔐", layout="wide")

# Inicializar DB al arrancar
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
                if new_user == "admin":
                    st.warning("El nombre 'admin' está reservado. Usa otro.")
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
    # Para ser admin, debes registrarte con el usuario "admin" (o crearlo manualmente en DB)
    # Nota: En el registro arriba bloqueé crear 'admin' para que solo tú puedas hacerlo si quitas el bloqueo temporalmente
    # O simplemente cambia la condición aquí abajo a tu usuario real.
    
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