import streamlit as st
import google.generativeai as genai
import PyPDF2

# ==================================================
# CONFIGURACIÓN DE LA PÁGINA
# ==================================================
st.set_page_config(
    page_title="Revisor Académico de Mantenimiento",
    page_icon="🛠️",
    layout="centered"
)

st.title("🛠️ Revisor Académico de Mantenimiento")

# ==================================================
# CONEXIÓN CON GEMINI
# ==================================================
genai.configure(api_key=st.secrets["GEMINI_KEY"])

SYSTEM_PROMPT = """
Eres un Revisor Académico de Mantenimiento Industrial.

Evalúa el contenido del reporte técnico y entrega OBLIGATORIAMENTE:

1. Tabla de evidencias en formato Markdown con columnas:
   - Criterio
   - Evidencia encontrada
   - Nivel (Insuficiente / Básico / Adecuado / Avanzado)

2. Observaciones técnicas claras y profesionales.

3. Calificación final numérica de 0 a 100.

4. Recomendaciones concretas para mejorar el reporte.

Sé técnico, objetivo y directo. No inventes información.
"""

# ==================================================
# FUNCIÓN PARA EXTRAER TEXTO DEL PDF
# ==================================================
def extraer_texto_pdf(archivo_pdf):
    lector = PyPDF2.PdfReader(archivo_pdf)
    texto = ""
    for pagina in lector.pages:
        contenido = pagina.extract_text()
        if contenido:
            texto += contenido + "\n"
    return texto

# ==================================================
# INTERFAZ
# ==================================================
uploaded_file = st.file_uploader(
    "Cargar Reporte Técnico (PDF)",
    type=["pdf"]
)

if uploaded_file:
    if st.button("Iniciar Evaluación"):
        try:
            with st.spinner("Analizando el reporte técnico..."):

                texto_pdf = extraer_texto_pdf(uploaded_file)

                if texto_pdf.strip() == "":
                    st.error("El PDF no contiene texto legible (posiblemente es un escaneo).")
                else:
                    model = genai.GenerativeModel(
                        model_name="gemini-pro",
                        system_instruction=SYSTEM_PROMPT
                    )

                    prompt = f"""
                    TEXTO DEL REPORTE:
                    ------------------
                    {texto_pdf}
                    ------------------

                    Realiza la evaluación conforme a tu rol.
                    """

                    response = model.generate_content(prompt)

                    st.success("Evaluación completada")
                    st.markdown(response.text)

        except Exception as e:
            st.error(f"Error durante la evaluación: {e}")


