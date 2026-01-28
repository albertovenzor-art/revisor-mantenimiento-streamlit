import streamlit as st
import google.generativeai as genai
import PyPDF2

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

Evalúa el texto del reporte y entrega:
1. Tabla de evidencias (criterio | evidencia | nivel)
2. Observaciones técnicas
3. Calificación estimada (0–100)
4. Recomendaciones claras y accionables
"""

# --------------------------------------------------
# FUNCIÓN PARA EXTRAER TEXTO DEL PDF
# --------------------------------------------------
def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

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

                pdf_text = extract_text_from_pdf(uploaded_file)

                model = genai.GenerativeModel(
                    model_name="models/gemini-1.5-flash",
                    system_instruction=SYSTEM_PROMPT
                )

                response = model.generate_content(
                    f"Texto del reporte:\n\n{pdf_text}\n\nEvalúa conforme a criterios de mantenimiento."
                )

                st.success("Evaluación completada")
                st.markdown(response.text)

        except Exception as e:
            st.error(f"Error detectado: {e}")
