import streamlit as st
from cifrado import cifrar_cesar, descifrar_cesar, cifrar_atbash, detectar_cifrado

st.set_page_config(page_title="Cipher Pro Dashboard", page_icon="🔐", layout="centered")

st.title("🔐 Cyber-Dashboard: Pro")

# --- BARRA LATERAL (Configuración) ---
st.sidebar.header("🛠️ Configuración")
modo_custom = st.sidebar.toggle("Modo Personalizado (Números/Símbolos)")

if modo_custom:
    alfabeto_input = st.sidebar.text_input("Abecedario manual:", value="1234abcd")
    con_enie = False
else:
    alfabeto_input = None
    con_enie = st.sidebar.checkbox("Incluir letra Ñ", value=True)

# --- PANEL PRINCIPAL ---
st.subheader("📥 Entrada de Datos")
texto_input = st.text_area("Texto a procesar:", placeholder="Escribe tu mensaje aquí...", height=100).strip()

# --- BOTONES MANUALES ---
st.write("### 🕹️ Controles Manuales")
col_ces, col_atb = st.columns(2)

with col_ces:
    desp_manual = st.number_input("Desplazamiento César:", 1, 30, 8)
    if st.button("Cifrar César ➡️", use_container_width=True):
        if texto_input:
            resultado = cifrar_cesar(texto_input, desp_manual, alfabeto_input, con_enie)
            st.code(f"Resultado César: {resultado}")
        else:
            st.warning("⚠️ Ingresa un texto")

with col_atb:
    st.write("") # Espaciador para alinear con el number_input
    st.write("") 
    if st.button("Procesar Atbash 🔄", use_container_width=True):
        if texto_input:
            resultado = cifrar_atbash(texto_input, alfabeto_input, con_enie)
            st.code(f"Resultado Atbash: {resultado}")
        else:
            st.warning("⚠️ Ingresa un texto")

st.divider()

# --- BOTÓN DE AUTO-DETECCIÓN ---
st.write("### 🚀 Inteligencia de Detección")
if st.button("EJECUTAR ANÁLISIS AUTOMÁTICO", type="primary", use_container_width=True):
    if texto_input:
        with st.spinner("Analizando patrones..."):
            tipo = detectar_cifrado(texto_input, alfabeto_input, con_enie)
            
            st.info(f"🔍 Método Identificado: **{tipo.upper()}**")
            
            if "CÉSAR" in tipo.upper():
                # Extraemos el número del desplazamiento del texto del tipo
                d = int(tipo.split()[-1])
                descifrado = descifrar_cesar(texto_input, d, alfabeto_input, con_enie)
            else:
                descifrado = cifrar_atbash(texto_input, alfabeto_input, con_enie)
                
            st.success(f"✅ Texto Descifrado: {descifrado}")
    else:
        st.error("❌ No hay texto para analizar.")

st.caption("Nota: El análisis automático prioriza palabras reales y estructuras del lenguaje español.")