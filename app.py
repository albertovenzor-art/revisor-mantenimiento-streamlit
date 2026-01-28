import streamlit as st
import google.generativeai as genai
import PyPDF2

# ==========================================
# CONFIGURACIÓN
# ==========================================
st.set_page_config(
    page_title="Resumen Técnico de Mantenimiento",
    page_icon="🛠️",
    layout="centered"
)

st.title("🛠️ Resumen Técnico de Mantenimiento")

genai.configure(api_key=st.secrets["GEMINI_KEY"])

# ==========================================
# PROMPT ULTRA SIMPLE
# ==========================================
PROMPT_RESUMEN = """
Resume el siguiente texto técnico de mantenimiento industrial
en máximo 10 líneas claras y concisas.
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
    if st.button("Generar resumen"):
        try:
            st.info("📄 Extrayendo texto...")
            texto = extraer_texto_pdf(archivo)

            if not texto:
                st.error("El PDF no contiene texto legible.")
                st.stop()

            # 🔪 RECORTE EXTREMO (CLAVE)
            texto = texto[:3000]

            modelo = obtener_modelo_flash()
            if not modelo:
                st.error("No hay modelos Gemini Flash disponibles.")
                st.stop()

            st.info(f"🤖 Usando modelo rápido: {modelo}")

            model = genai.GenerativeModel(model_name=modelo)

            respuesta = model.generate_content(
                f"{PROMPT_RESUMEN}\n\nTEXTO:\n{texto}",
                request_options={"timeout": 20}
            )

            st.success("✅ Resumen generado")
            st.markdown(respuesta.text)

        except Exception as e:
            st.error(f"Error: {e}")
