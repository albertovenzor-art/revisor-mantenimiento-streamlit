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

# ==================================================
# PROMPTS
# ==================================================
PROMPT_RESUMEN = """
Eres un ingeniero especialista en mantenimiento industrial.
Resume técnicamente el siguiente reporte en máximo 800 palabras.
Incluye:
- Objetivo
- Metodología
- Hallazgos técnicos
- Conclusiones
"""

PROMPT_EVALUACION = """
Eres un Revisor Académico de Mantenimiento Industrial.

Con base EXCLUSIVA en el resumen técnico proporcionado, entrega:

1. Tabla de evidencias (Markdown):
   Criterio | Evidencia | Nivel

2. Observaciones técnicas

3. Calificación final (0–100)

4. Recomendaciones claras

Sé técnico, directo y objetivo.
"""

# ==================================================
# FUNCIONES
# ==================================================
def extraer_texto_pdf(archivo_pdf):
    lector = PyPDF2.PdfReader(archivo_pdf)
    texto = ""
    for pagina in lector.pages:
        contenido = pagina.extract_text()
        if contenido:
            texto += contenido + "\n"
    return texto.strip()

def obtener_modelo():
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
            st.info("📄 Extrayendo texto del PDF...")
            texto_pdf = extraer_texto_pdf(uploaded_file)

            if texto_pdf == "":
                st.error("El PDF no contiene texto legible (es un escaneo).")
                st.stop()

            texto_pdf = texto_pdf[:15000]  # límite seguro

            modelo = obtener_modelo()
            if not modelo:
                st.error("No hay modelos Gemini disponibles para tu API key.")
                st.stop()

            st.info(f"🤖 Usando modelo: {modelo}")
            model = genai.GenerativeModel(model_name=modelo)

            # ---------------- FASE 1: RESUMEN ----------------
            st.info("🧠 Generando resumen técnico...")
            resumen = model.generate_content(
                textwrap.dedent(f"""
                {PROMPT_RESUMEN}

                TEXTO DEL REPORTE:
                ------------------
                {texto_pdf}
                """),
                request_options={"timeout": 60}
            ).text

            # ---------------- FASE 2: EVALUACIÓN ----------------
            st.info("📊 Evaluando con base en el resumen...")
            evaluacion = model.generate_content(
                textwrap.dedent(f"""
                {PROMPT_EVALUACION}

                RESUMEN TÉCNICO:
                ----------------
                {resumen}
                """),
                request_options={"timeout": 60}
            )

            st.success("✅ Evaluación completada")
            st.markdown(evaluacion.text)

        except Exception as e:
            st.error(f"Error durante la evaluación: {e}")

