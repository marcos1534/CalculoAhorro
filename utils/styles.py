def get_css(theme):
    if theme == "Oscuro":
        bg_color = "#0E1117"
        text_color = "#FAFAFA"
        input_bg = "#262730"
        card_bg = "#1e2130"
    else:
        bg_color = "#F0F2F6"
        text_color = "#31333F"
        input_bg = "#FFFFFF"
        card_bg = "#FFFFFF"

    return f"""
    <style>
    /* Fondo y Textos */
    .stApp {{
        background-color: {bg_color};
        color: {text_color};
    }}
    
    /* Inputs */
    .stTextInput > div > div > input, .stNumberInput > div > div > input {{
        background-color: {input_bg};
        color: {text_color};
        border-radius: 8px;
    }}
    
    /* Tarjetas personalizadas */
    .metric-card {{
        background-color: {card_bg};
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 10px;
        border-left: 5px solid #00C9FF;
    }}
    
    /* Botones */
    div.stButton > button {{
        background: linear-gradient(90deg, #00C9FF 0%, #007bff 100%);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: bold;
    }}
    </style>
    """
