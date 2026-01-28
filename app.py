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
# FUNCIÓN PDF
# ==========================================
def extraer_texto_pdf(archivo, max_chars=4000):
    reader = PyPDF2.PdfReader(archivo)
    texto = ""
    for page in reader.pages[:3]:  # SOLO primeras 3 páginas
        t = page.extract_text()
        if t:
            texto += t + "\n"
        if len(texto) >= max_chars:
            break
    return texto[:max_chars].strip()

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
            st.info("📄 Extrayendo texto del PDF...")
            texto = extraer_texto_pdf(archivo)

            if not texto:
                st.error("El PDF no contiene texto legible.")
                st.stop()

            modelo = obtener_modelo_flash()
            if not modelo:
                st.error("No hay modelos Gemini Flash disponibles.")
                st.stop()

            st.info(f"🤖 Usando modelo: {modelo}")
            model = genai.GenerativeModel(model_name=modelo)

            prompt = f"""
            Resume técnicamente el siguiente texto en máximo 5 párrafos.
            Sé claro, conciso y técnico.

            TEXTO:
            {texto}
            """

            respuesta = model.generate_content(
                prompt,
                request_options={"timeout": 25}
            )

            st.success("✅ Resumen generado")
            st.markdown(respuesta.text)

        except Exception as e:
            st.error(f"Error: {e}")
