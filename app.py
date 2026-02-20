import streamlit as st
from cifrado import cifrar_cesar, descifrar_cesar, cifrar_atbash, detectar_cifrado

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Cyber-Dashboard | Cipher Pro",
    page_icon="🔐",
    layout="centered"
)

# Estilo personalizado para que se vea más profesional
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stCodeBlock {
        border: 2px solid #2ecc71 !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🔐 Cyber-Dashboard: Sistema de Cifrado")
st.write("Herramienta avanzada con análisis de frecuencias estadístico para el idioma español.")

# --- SIDEBAR: Configuración del Alfabeto ---
st.sidebar.header("🛠️ Configuración de Lenguaje")

modo_custom = st.sidebar.toggle("Modo Personalizado", help="Permite usar un abecedario propio (ej: números o símbolos)")

if modo_custom:
    alfabeto_input = st.sidebar.text_input("Abecedario personalizado:", placeholder="Ej: 0123456789abcdef")
    con_enie = False
    st.sidebar.info("En modo personalizado, la Ñ se ignora a menos que la incluyas en tu lista.")
else:
    alfabeto_input = None
    con_enie = st.sidebar.checkbox("Incluir Ñ (Alfabeto de 27 letras)", value=True)

st.sidebar.divider()
st.sidebar.caption("Proyecto de Ciberseguridad - Sistema de Análisis Estadístico")

# --- CUERPO PRINCIPAL ---
st.subheader("📥 Entrada de Datos")
texto_input = st.text_area("Ingresa el texto a procesar:", placeholder="Escribe o pega aquí el mensaje...", height=150)

# Columnas para los controles manuales
col_op, col_btn = st.columns([1, 2])

with col_op:
    desp_manual = st.selectbox("Desplazamiento César:", options=list(range(1, 31)), index=0)

with col_btn:
    st.write("") # Espaciador
    c1, c2 = st.columns(2)
    with c1:
        btn_cifrar = st.button("Cifrar César", use_container_width=True)
    with c2:
        btn_atbash = st.button("Atbash (C/D)", use_container_width=True)

# Botón de Inteligencia / Detección Automática
btn_auto = st.button("🚀 AUTO-DETECTAR Y DESCIFRAR", type="primary", use_container_width=True)

st.divider()

# --- ÁREA DE RESULTADOS ---
st.subheader("🖥️ Consola de Resultados")

if texto_input:
    if btn_cifrar:
        resultado = cifrar_cesar(texto_input, desp_manual, alfabeto_input, con_enie)
        st.success("Cifrado César manual completado:")
        st.code(resultado, language=None)

    elif btn_atbash:
        resultado = cifrar_atbash(texto_input, alfabeto_input, con_enie)
        st.success("Procesamiento Atbash completado:")
        st.code(resultado, language=None)

    elif btn_auto:
        with st.spinner("Analizando patrones estadísticos..."):
            tipo = detectar_cifrado(texto_input, alfabeto_input, con_enie)
            
            if "César" in tipo:
                try:
                    desp = int(tipo.split()[-1])
                    final = descifrar_cesar(texto_input, desp, alfabeto_input, con_enie)
                except:
                    final = "Error al extraer el desplazamiento."
            elif tipo == "Atbash":
                final = cifrar_atbash(texto_input, alfabeto_input, con_enie)
            else:
                final = "El análisis estadístico no halló un patrón claro de lenguaje español."

            st.balloons()
            st.info(f"Método detectado: **{tipo.upper()}**")
            st.code(final, language=None)
else:
    if btn_cifrar or btn_atbash or btn_auto:
        st.warning("⚠️ Por favor, ingresa un texto para procesar.")

st.markdown("---")
st.caption("Tip: Para mejores resultados en auto-detección, usa textos de más de 15 caracteres.")