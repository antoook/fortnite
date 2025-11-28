import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Fortnite Stats", layout="wide")
st.title("Análisis de Fortnite: Modo Solo")

# 1. Cargar datos
@st.cache_data
def load_data():
    return pd.read_csv("Fortnite_players_stats.csv")

try:
    df = load_data()

    # --- DISEÑO DE COLUMNAS (Gráfico chico a la izq, Tabla a la der) ---
    col_izquierda, col_derecha = st.columns([1, 2]) 

    # --- COLUMNA IZQUIERDA: EL GRÁFICO PEQUEÑO ---
    with col_izquierda:
        st.subheader("Minutos vs Puntaje")
        
        # Datos y Tendencia
        x = df['Solo minutesPlayed']
        y = df['Solo score']
        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)

        # Gráfico compacto
        fig, ax = plt.subplots(figsize=(5, 3.5)) 
        ax.scatter(x, y, alpha=0.5, c='#1f77b4', s=5)
        ax.plot(x, p(x), "r--", linewidth=1, label='Tendencia')

        # Estilos
        ax.set_title("Relación Tiempo/Puntaje", fontsize=9)
        ax.set_xlabel("Minutos", fontsize=7)
        ax.set_ylabel("Puntaje", fontsize=7)
        ax.tick_params(labelsize=6)
        ax.legend(fontsize=6)
        ax.grid(True, alpha=0.3)

        st.pyplot(fig, use_container_width=True)
        
        corr = df['Solo minutesPlayed'].corr(df['Solo score'])
        st.caption(f"Correlación: {corr:.2f}")

    # --- COLUMNA DERECHA: TABLA FILTRADA ---
    with col_derecha:
        st.subheader("Datos del Modo Solitario")
        st.write("Explora las estadísticas detalladas de los jugadores.")

        # --- AQUÍ ESTÁ EL CAMBIO PARA FILTRAR COLUMNAS ---
        # 1. Creamos una lista con 'Player' y todas las columnas que tengan "Solo" en el nombre
        df_filtrado = df[['Player', 'Solo score', 'Solo minutesPlayed']]

        # Ordenamos por puntaje (de mayor a menor) para que se vea como un ranking
        df_filtrado = df_filtrado.sort_values(by='Solo score', ascending=False)

        # hide_index=True quita la columna de números 0,1,2... de la izquierda para que se vea más limpio
        st.dataframe(df_filtrado, height=400, hide_index=True)
except FileNotFoundError:
    st.error("No encuentro el archivo 'Fortnite_players_stats.csv'.")
