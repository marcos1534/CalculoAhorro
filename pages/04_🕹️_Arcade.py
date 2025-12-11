import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import sys
import os

# Importar juegos y DB
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import games_data
import database as db

st.set_page_config(page_title="Arcade Retro", page_icon="🕹️", layout="wide")

st.title("🕹️ SALA RECREATIVA RETRO")
st.markdown("Juega y registra tu puntuación para entrar en el **Top 5 Global**.")

# Pestañas de juegos
tab1, tab2, tab3, tab4 = st.tabs(["🟡 PAC-MAN", "🧱 TETRIS", "👾 SPACE INVADERS", "🦍 DONKEY KONG"])

def mostrar_juego_y_ranking(nombre_juego, codigo_html, key_suffix):
    col_juego, col_ranking = st.columns([2, 1])
    
    with col_juego:
        # Renderizar Juego
        components.html(codigo_html, height=550)
        
        st.info("👇 **¿Has terminado la partida?** Registra tu puntuación aquí:")
        
        # Formulario de registro de récord
        with st.form(key=f'form_{key_suffix}'):
            puntos = st.number_input("Tu Puntuación Final:", min_value=0, step=10)
            submit = st.form_submit_button("💾 Guardar Récord")
            
            if submit:
                if puntos > 0:
                    db.add_score(nombre_juego, st.session_state['username'], puntos)
                    st.success(f"¡Puntuación de {puntos} guardada para {st.session_state['username']}!")
                    st.rerun() # Recargar para ver cambios en la tabla
                else:
                    st.warning("Juega primero para obtener puntos.")

    with col_ranking:
        st.markdown(f"### 🏆 TOP 5 - {nombre_juego.upper()}")
        
        # Obtener datos de la DB
        records = db.get_top_5_scores(nombre_juego)
        
        if records:
            df = pd.DataFrame(records, columns=["Jugador", "Puntos", "Fecha"])
            # Estilizar tabla: índice empezando en 1
            df.index = df.index + 1
            st.table(df[["Jugador", "Puntos"]])
            
            # Comprobar si el usuario actual es el líder
            top_player = df.iloc[0]["Jugador"]
            if top_player == st.session_state['username']:
                st.balloons()
                st.caption("¡ERES EL LÍDER ACTUAL! 👑")
        else:
            st.write("Todavía no hay récords. ¡Sé el primero!")

# --- LÓGICA DE PESTAÑAS ---

with tab1:
    mostrar_juego_y_ranking("Pac-Man", games_data.get_pacman_game(), "pac")

with tab2:
    mostrar_juego_y_ranking("Tetris", games_data.get_tetris_game(), "tet")

with tab3:
    mostrar_juego_y_ranking("Space Invaders", games_data.get_space_invaders(), "inv")

with tab4:
    mostrar_juego_y_ranking("Donkey Kong", games_data.get_donkey_kong(), "dk")