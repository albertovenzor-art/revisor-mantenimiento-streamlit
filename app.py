import streamlit as st
import google.generativeai as genai
import PyPDF2
import textwrap

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

Evalúa el reporte técnico y entrega:
1. Tabla de evidencias (Markdown)
2. Observaciones técnicas
3. Calificación (0–100)
4. Recomendaciones claras
"""

# ==================================================
# FUNCIÓN: EXTRAER TEXTO DEL PDF
# ==================================================
def extraer_texto_pdf(archivo_pdf):
    lector = PyPDF2.PdfReader(archivo_pdf)
    texto = ""
    for pagina in lector.pages:
        contenido = pagina.extract_text()
        if contenido:
            texto += contenido + "\n"
    return texto.strip()

# ==================================================
# FUNCIÓN: OBTENER MODELO DISPONIBLE
# ==================================================
def obtener_modelo_disponible():
    modelos = genai.list_models()
    for m in modelos:
        if "generateContent" in m.supported_generation_methods:
            return m.name
    return None

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
            with st.spinner("Preparando evaluación..."):

                texto_pdf = extraer_texto_pdf(uploaded_file)
                if texto_pdf == "":
                    st.error("El PDF no contiene texto legible (es un escaneo).")
                    st.stop()

                texto_pdf = texto_pdf[:12000]  # límite seguro

                modelo_nombre = obtener_modelo_disponible()
                if not modelo_nombre:
                    st.error(
                        "❌ Tu API Key no tiene acceso a modelos generativos de Gemini.\n\n"
                        "Verifica que la key sea de **Google AI Studio** con Gemini habilitado."
                    )
                    st.stop()

                st.info(f"🤖 Usando modelo disponible: `{modelo_nombre}`")

                model = genai.GenerativeModel(
                    model_name=modelo_nombre,
                    system_instruction=SYSTEM_PROMPT
                )

                prompt = textwrap.dedent(f"""
                TEXTO DEL REPORTE:
                ------------------
                {texto_pdf}
                ------------------

                Realiza la evaluación completa.
                """)

                response = model.generate_content(
                    prompt,
                    request_options={"timeout": 60}
                )

                st.success("✅ Evaluación completada")
                st.markdown(response.text)

        except Exception as e:
            st.error(f"Error durante la evaluación: {e}")
