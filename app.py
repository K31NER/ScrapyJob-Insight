import streamlit as st 
from Agent.agent import redact_agent
from Agent.schema import JobEntry, JobsProcces

st.set_page_config(
        page_icon="💼",
    page_title="Job Intelligence Agent",
    layout="centered"
)

# Estilos personalizados
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #007bff;
        color: white;
        font-weight: bold;
    }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        border-radius: 5px;
    }
    .card {
        padding: 1.5rem;
        border-radius: 10px;
        background-color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("💼 Job Intelligence Agent")
st.caption("Extrae información estructurada de ofertas de empleo usando IA")

with st.expander("📝 Formulario de Entrada", expanded=True):
    col_t, col_l = st.columns([2, 1])
    with col_t:
        title = st.text_input("Título del cargo", placeholder="Ej: Senior Data Engineer")
    with col_l:
        location = st.text_input("Ubicación original", placeholder="Ej: Remoto, Bogotá...")
    
    description = st.text_area("Descripción completa (Requisitos)", height=250, placeholder="Pegue aquí el texto obtenido del sitio web...")

st.markdown("---")

if st.button("🚀 Analizar Oferta"):
    if not description:
        st.warning("⚠️ Por favor, pegue una descripción para comenzar el análisis.")
    else:
        with st.spinner("🧠 El agente está analizando los requisitos y detalles..."):
            try:
                entry = JobEntry(
                    title=title,
                    location=location,
                    description=description
                )
                
                response = redact_agent.run(entry)
                analisis = response.content
                
                if not isinstance(analisis, JobsProcces):
                    st.error("❌ El modelo no pudo procesar la información correctamente.")
                    st.stop()

                # Dashboard de resultados
                st.subheader("📊 Resultados del Análisis")
                
                # Fila de métricas clave
                m1, m2, m3 = st.columns(3)
                with m1:
                    st.metric("Seniority", analisis.seniority.value if hasattr(analisis.seniority, 'value') else analisis.seniority)
                with m2:
                    st.metric("País/Región", analisis.location)
                with m3:
                    st.metric("Skills", len(analisis.skills))

                # Detalle de Skills
                st.markdown("### 🛠️ Tecnologías y Herramientas")
                # Crear tags visuales para las skills
                skills_html = "".join([f'<span style="background-color: #e1f5fe; color: #01579b; padding: 5px 10px; border-radius: 15px; margin: 5px; display: inline-block; font-weight: bold;">{s}</span>' for s in analisis.skills])
                st.markdown(skills_html, unsafe_allow_html=True)
                
                st.success("✅ Procesamiento completado")
                
            except Exception as e:
                st.error(f"❌ Error crítico en el procesamiento: {e}")
