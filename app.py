import streamlit as st
import google.generativeai as genai
from google.generativeai.types import Part

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
uploaded_file = st.file_uploader(
    "Cargar Reporte (PDF)",
    type=["pdf"]
)

if uploaded_file:
    if st.button("Iniciar Evaluación"):
        try:
            with st.spinner("Analizando documento..."):

                model = genai.GenerativeModel(
                    model_name="models/gemini-1.5-flash",
                    system_instruction=SYSTEM_PROMPT
                )

                pdf_part = Part.from_bytes(
                    data=uploaded_file.read(),
                    mime_type="application/pdf"
                )

                response = model.generate_content(
                    [
                        pdf_part,
                        "Evalúa este documento conforme a los criterios de mantenimiento."
                    ]
                )

                st.success("Evaluación completada")
                st.markdown(response.text)

        except Exception as e:
            st.error(f"Error detectado: {e}")
