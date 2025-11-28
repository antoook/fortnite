import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Fortnite Stats", layout="wide")
st.title("🏆 Análisis de Fortnite")

# 1. Cargar datos
@st.cache_data
def load_data():
    return pd.read_csv("Fortnite_players_stats.csv")

try:
    df = load_data()

    st.write("Aquí abajo verás el gráfico mucho más pequeño 👇")

    # --- EL TRUCO PARA HACERLO CHICO ---
    # Dividimos la pantalla en 3 columnas invisibles.
    # col1: Izquierda (Pequeña) | col2: Centro (Grande) | col3: Derecha (Pequeña)
    # Los números [1, 2] significan que la segunda columna es el doble de ancha que la primera.
    col_izquierda, col_derecha = st.columns([1, 2]) 

    # "with col_izquierda:" le dice a Streamlit: "Pon esto SOLO en la columna de la izquierda"
    with col_izquierda:
        st.subheader("⏳ Minutos vs Puntaje")
        
        # Datos
        x = df['Solo minutesPlayed']
        y = df['Solo score']
        
        # Tendencia
        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)

        # Gráfico (figsize pequeño: 5 pulgadas de ancho x 3.5 de alto)
        fig, ax = plt.subplots(figsize=(5, 3.5)) 
        
        ax.scatter(x, y, alpha=0.5, c='#1f77b4', s=5) # Puntos muy pequeños
        ax.plot(x, p(x), "r--", linewidth=1, label='Tendencia')

        # Textos más pequeños para que quepan bien
        ax.set_title("Relación Tiempo/Puntaje", fontsize=9)
        ax.set_xlabel("Minutos", fontsize=7)
        ax.set_ylabel("Puntaje", fontsize=7)
        ax.tick_params(labelsize=6)
        ax.legend(fontsize=6)
        ax.grid(True, alpha=0.3)

        # Importante: use_container_width=True hace que se ajuste al ancho de ESTA columna pequeña
        st.pyplot(fig, use_container_width=True)
        
        # Nota explicativa debajo del gráfico
        corr = df['Solo minutesPlayed'].corr(df['Solo score'])
        st.caption(f"Correlación exacta: {corr:.2f}")

    # En la columna de la derecha puedes poner otra cosa (o dejarla vacía)
    with col_derecha:
        st.info("👈 El gráfico está confinado en la columna izquierda para no verse gigante.")
        st.write("Aquí puedes poner tablas o texto explicativo.")
        if st.checkbox("Ver datos"):
            st.dataframe(df.head(10))

except FileNotFoundError:
    st.error("⚠️ No encuentro el archivo 'Fortnite_players_stats.csv'.")
