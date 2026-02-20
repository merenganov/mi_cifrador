import streamlit as st
from cifrado import cifrar_cesar, descifrar_cesar, cifrar_atbash, detectar_cifrado

st.set_page_config(page_title="Cipher Detector Pro", page_icon="🕵️")

st.title("🕵️ Detector de Cifrados Crítico")

# --- BARRA LATERAL ---
st.sidebar.header("🔧 Panel de Control")
modo_custom = st.sidebar.toggle("Modo Personalizado (Números/Símbolos)")

if modo_custom:
    alfabeto_input = st.sidebar.text_input("Alfabeto manual:", value="1234abcd")
    con_enie = False
else:
    alfabeto_input = None
    con_enie = st.sidebar.checkbox("Incluir letra Ñ", value=True)

# --- ÁREA DE TRABAJO ---
st.subheader("📝 Entrada de Mensaje")
texto_input = st.text_input("Texto a analizar:", placeholder="Ej: Owsi o Sloz").strip()

# Controles manuales rápidos
with st.expander("Controles Manuales (Cifrado rápido)"):
    col_d, col_b = st.columns([1,2])
    d_manual = col_d.number_input("Desplazamiento:", 1, 27, 8)
    if col_b.button("Generar César Manual"):
        st.code(cifrar_cesar(texto_input, d_manual, alfabeto_input, con_enie))

st.divider()

# --- DETECCIÓN AUTOMÁTICA ---
if st.button("🚀 EJECUTAR ANÁLISIS AUTOMÁTICO", type="primary", use_container_width=True):
    if texto_input:
        resultado_tipo = detectar_cifrado(texto_input, alfabeto_input, con_enie)
        
        st.subheader("🔍 Resultados del Escaneo")
        st.info(f"Método Identificado: **{resultado_tipo.upper()}**")
        
        if "CÉSAR" in resultado_tipo.upper():
            desp = int(resultado_tipo.split()[-1])
            descifrado = descifrar_cesar(texto_input, desp, alfabeto_input, con_enie)
        else:
            descifrado = cifrar_atbash(texto_input, alfabeto_input, con_enie)
            
        st.success(f"Texto Descifrado: **{descifrado}**")
    else:
        st.error("Debes ingresar un texto para analizar.")