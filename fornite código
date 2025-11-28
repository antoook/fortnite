import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Fortnite Stats", layout="wide")
st.title("🏆 Análisis de Fortnite: Solo Mode")

# 1. Cargar datos
@st.cache_data
def load_data():
    # Asegúrate de que el CSV esté en la misma carpeta
    return pd.read_csv("Fortnite_players_stats.csv")

try:
    df = load_data()

    st.header("⏳ Relación: Tiempo vs. Puntaje (Matplotlib)")
    st.write("Gráfico generado usando solo Matplotlib y Numpy para la tendencia.")

    # --- PREPARACIÓN DE DATOS ---
    x = df['Solo minutesPlayed']
    y = df['Solo score']

    # Calcular la línea de tendencia (Regresión Lineal) con Numpy
    # np.polyfit ajusta una línea (grado 1) a los datos
    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)

    # --- CREAR GRÁFICO CON MATPLOTLIB ---
    # Usamos subplots para tener control total de la figura
    fig, ax = plt.subplots(figsize=(10, 6))

    # 1. Los puntos (Scatter)
    ax.scatter(x, y, alpha=0.5, c='blue', label='Jugadores')

    # 2. La línea de tendencia
    ax.plot(x, p(x), "r--", linewidth=2, label='Tendencia (Promedio)')

    # 3. Etiquetas y Estilo
    ax.set_title(f"Relación Minutos Jugados vs Puntaje", fontsize=16)
    ax.set_xlabel("Minutos Jugados (Solo)", fontsize=12)
    ax.set_ylabel("Puntaje (Solo Score)", fontsize=12)
    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.6)

    # --- MOSTRAR EN STREAMLIT ---
    st.pyplot(fig)

    # Mostrar dato de correlación
    correlation = df['Solo minutesPlayed'].corr(df['Solo score'])
    st.info(f"💡 **Dato Matemático:** La correlación es de **{correlation:.2f}**. (Cerca de 1.0 significa relación perfecta).")

    st.divider()

    # Opción para ver los datos crudos
    if st.checkbox("Ver tabla de datos"):
        st.dataframe(df.head(20))

except FileNotFoundError:
    st.error("⚠️ Error: No se encuentra el archivo 'Fortnite_players_stats.csv'. Asegúrate de que esté en la misma carpeta.")
