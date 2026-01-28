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
# INTERFAZ
# ==================================================
uploaded_file = st.file_uploader(
    "Cargar Reporte Técnico (PDF)",
    type=["pdf"]
)

# Estado para evitar re-ejecución
if "evaluado" not in st.session_state:
    st.session_state.evaluado = False

if uploaded_file and not st.session_state.evaluado:
    if st.button("Iniciar Evaluación"):
        try:
            st.session_state.evaluado = True

            st.info("📄 Extrayendo texto del PDF...")
            texto_pdf = extraer_texto_pdf(uploaded_file)

            if texto_pdf == "":
                st.error("El PDF no contiene texto legible (es un escaneo).")
                st.stop()

            # 🔒 LIMITAR TEXTO (CRÍTICO)
            MAX_CHARS = 12000
            texto_pdf = texto_pdf[:MAX_CHARS]

            st.info("🤖 Enviando texto a Gemini (análisis en curso)...")

            model = genai.GenerativeModel(
                model_name="gemini-pro",
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
                request_options={"timeout": 60}  # ⏱️ evita cuelgues
            )

            st.success("✅ Evaluación completada")
            st.markdown(response.text)

        except Exception as e:
            st.error(f"Error durante la evaluación: {e}")


