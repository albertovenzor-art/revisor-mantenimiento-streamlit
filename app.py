import streamlit as st
import google.generativeai as genai
from genai.types import Part

# --------------------------------------------------
# CONFIGURACIÓN DE LA PÁGINA
# --------------------------------------------------
st.set_page_config(
    page_title="Revisor Mantenimiento",
    page_icon="🛠️"
)

st.title("🛠️ Revisor Académico de Mantenimiento")

# --------------------------------------------------
# CONEXIÓN CON GEMINI
# --------------------------------------------------
genai.configure(api_key=st.secrets["GEMINI_KEY"])

SYSTEM_PROMPT = """
Eres un Revisor Académico de Mantenimiento Industrial.

Evalúa el PDF y entrega:
1. Tabla de evidencias (criterio | evidencia | nivel)
2. Observaciones técnicas
3. Calificación estimada (0–100)
4. Recomendaciones claras y accionables
"""

# --------------------------------------------------
# INTERFAZ
# --------------------------------------------------
uploaded_file = st.fi_
