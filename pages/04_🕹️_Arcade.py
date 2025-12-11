import streamlit as st
import streamlit.components.v1 as components
import sys
import os

# Importar juegos desde utils
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import games_data

st.set_page_config(page_title="Arcade Retro", page_icon="🕹️", layout="wide")

st.title("🕹️ SALA RECREATIVA RETRO")
st.markdown("Clásicos recreados en HTML5. Sin descargas. ¡Juega ahora!")

tab1, tab2, tab3, tab4 = st.tabs(["🟡 PAC-MAN", "🧱 TETRIS", "👾 SPACE INVADERS", "🦍 DONKEY KONG"])

with tab1:
    st.caption("Usa las FLECHAS del teclado.")
    components.html(games_data.get_pacman_game(), height=500)

with tab2:
    st.caption("Flechas: Mover/Rotar | Abajo: Caer rápido")
    components.html(games_data.get_tetris_game(), height=500)

with tab3:
    st.caption("Flechas: Mover | Espacio: Disparar")
    components.html(games_data.get_space_invaders(), height=500)

with tab4:
    st.caption("Flechas: Mover/Subir escaleras. ¡Cuidado con los barriles!")
    components.html(games_data.get_donkey_kong(), height=600)