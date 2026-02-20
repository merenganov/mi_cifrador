import streamlit as st
from cifrado import cifrar_cesar, descifrar_cesar, cifrar_atbash, detectar_cifrado

st.set_page_config(page_title="Cipher Dashboard Pro", page_icon="🔐")
st.title("🔐 Cyber-Dashboard: Pro")

st.sidebar.header("🛠️ Configuración")
modo_custom = st.sidebar.toggle("Modo Personalizado (Números/Símbolos)")
if modo_custom:
    alfabeto_input = st.sidebar.text_input("Abecedario manual:", value="1234abcd")
    con_enie = False
else:
    alfabeto_input = None
    con_enie = st.sidebar.checkbox("Incluir letra Ñ", value=True)

st.subheader("📥 Entrada de Datos")
texto_input = st.text_area("Texto a procesar:", height=100).strip()

st.write("### 🕹️ Controles Manuales")
col_ces, col_atb = st.columns(2)
with col_ces:
    desp_manual = st.number_input("Desplazamiento:", 1, 30, 1)
    if st.button("Cifrar César ➡️", use_container_width=True):
        st.code(cifrar_cesar(texto_input, desp_manual, alfabeto_input, con_enie))
with col_atb:
    st.write("")
    st.write("")
    if st.button("Procesar Atbash 🔄", use_container_width=True):
        st.code(cifrar_atbash(texto_input, alfabeto_input, con_enie))

st.divider()
if st.button("🚀 EJECUTAR ANÁLISIS AUTOMÁTICO", type="primary", use_container_width=True):
    if texto_input:
        tipo = detectar_cifrado(texto_input, alfabeto_input, con_enie)
        st.info(f"🔍 Método Identificado: **{tipo.upper()}**")
        if "CÉSAR" in tipo.upper():
            d = int(tipo.split()[-1])
            res = descifrar_cesar(texto_input, d, alfabeto_input, con_enie)
        else:
            res = cifrar_atbash(texto_input, alfabeto_input, con_enie)
        st.success(f"✅ Texto Descifrado: {res}")