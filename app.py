import streamlit as st
import google.generativeai as genai
import PyPDF2

# ==========================================
# CONFIGURACIÓN
# ==========================================
st.set_page_config(
    page_title="Revisor Académico de Mantenimiento",
    page_icon="🛠️",
    layout="centered"
)

st.title("🛠️ Revisor Académico de Mantenimiento")

genai.configure(api_key=st.secrets["GEMINI_KEY"])

PROMPT = """
Eres un Revisor Académico de Mantenimiento Industrial.

Evalúa el siguiente texto y entrega SOLO:

1. Tabla de evidencias (Markdown):
   Criterio | Evidencia | Nivel

2. Calificación final (0–100)

3. 3 observaciones técnicas breves

Sé claro y conciso.
"""

# ==========================================
# FUNCIONES
# ==========================================
def extraer_texto_pdf(archivo):
    reader = PyPDF2.PdfReader(archivo)
    texto = ""
    for page in reader.pages:
        t = page.extract_text()
        if t:
            texto += t + "\n"
    return texto.strip()

def obtener_modelo_flash():
    for m in genai.list_models():
        if "flash" in m.name and "generateContent" in m.supported_generation_methods:
            return m.name
    return None

# ==========================================
# UI
# ==========================================
archivo = st.file_uploader(
    "Cargar Reporte Técnico (PDF)",
    type=["pdf"]
)

if archivo:
    if st.button("Iniciar Evaluación"):
        try:
            st.info("📄 Extrayendo texto...")
            texto = extraer_texto_pdf(archivo)

            if not texto:
                st.error("El PDF no contiene texto legible.")
                st.stop()

            # 🔒 límite agresivo (clave para velocidad)
            texto = texto[:8000]

            modelo = obtener_modelo_flash()
            if not modelo:
                st.error("No hay modelos Gemini Flash disponibles.")
                st.stop()

            st.info(f"🤖 Usando modelo rápido: {modelo}")
            model = genai.GenerativeModel(model_name=modelo)

            respuesta = model.generate_content(
                f"{PROMPT}\n\nTEXTO:\n{texto}",
                request_options={"timeout": 40}
            )

            st.success("✅ Evaluación completada")
            st.markdown(respuesta.text)

        except Exception as e:
            st.error(f"Error: {e}")
