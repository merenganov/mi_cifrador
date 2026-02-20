import streamlit as st
from cifrado import cifrar_cesar, descifrar_cesar, cifrar_atbash, obtener_mejores_candidatos

st.set_page_config(page_title="Cipher Dashboard Pro", layout="wide")
st.title("🔐 Cyber-Dashboard: Análisis Comparativo")

# --- Configuración ---
st.sidebar.header("🛠️ Configuración")
modo_custom = st.sidebar.toggle("Modo Personalizado")
if modo_custom:
    alfabeto_input = st.sidebar.text_input("Abecedario manual:", value="1234abcd")
    con_enie = False
else:
    alfabeto_input = None
    con_enie = st.sidebar.checkbox("Incluir letra Ñ", value=True)

# --- Entrada ---
texto_input = st.text_input("Ingresa el texto a procesar:").strip()

# --- Manual ---
col_m1, col_m2 = st.columns(2)
with col_m1:
    d_man = st.number_input("Desplazamiento manual:", 1, 30, 1)
    if st.button("Cifrar César ➡️"):
        st.code(cifrar_cesar(texto_input, d_man, alfabeto_input, con_enie))
with col_m2:
    st.write("##") # Espaciador
    if st.button("Procesar Atbash 🔄"):
        st.code(cifrar_atbash(texto_input, alfabeto_input, con_enie))

st.divider()

# --- Análisis Automático Comparativo ---
if st.button("🚀 EJECUTAR ANÁLISIS AUTOMÁTICO", type="primary", use_container_width=True):
    if texto_input:
        candidatos = obtener_mejores_candidatos(texto_input, alfabeto_input, con_enie)
        
        st.subheader("🔍 Comparativa de Resultados")
        col1, col2 = st.columns(2)
        
        with col1:
            st.info("### Opción A: ATBASH")
            st.success(f"**Resultado:** {candidatos['atbash']['texto']}")
            st.caption(f"Confianza: {candidatos['atbash']['score']} pts")
            
        with col2:
            st.info(f"### Opción B: CÉSAR (Desp. {candidatos['cesar']['desp']})")
            st.success(f"**Resultado:** {candidatos['cesar']['texto']}")
            st.caption(f"Confianza: {candidatos['cesar']['score']} pts")
            
        st.warning("⚠️ **Nota:** Elige el resultado que tenga más sentido para tu mensaje original.")
    else:
        st.error("Ingresa un texto primero.")