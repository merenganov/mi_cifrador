import streamlit as st
from cifrado import cifrar_cesar, descifrar_cesar, cifrar_atbash, detectar_cifrado

st.set_page_config(page_title="Cipher Pro", page_icon="🔐")

st.title("🔐 Cyber-Dashboard")

# Sidebar
st.sidebar.header("Configuración")
modo_custom = st.sidebar.toggle("Modo Personalizado")
alfabeto_input = st.sidebar.text_input("Alfabeto:", value="1234abcd") if modo_custom else None
con_enie = st.sidebar.checkbox("Usar Ñ", value=True) if not modo_custom else False

# Entrada
texto_input = st.text_area("Entrada:", placeholder="Ej: 23cd")
desp_manual = st.number_input("Desplazamiento César:", 1, 30, 1)

col1, col2, col3 = st.columns(3)
with col1: btn_cifrar = st.button("Cifrar")
with col2: btn_atbash = st.button("Atbash")
with col3: btn_auto = st.button("AUTO-DETECTAR", type="primary")

st.divider()

if texto_input:
    if btn_cifrar:
        st.code(cifrar_cesar(texto_input, desp_manual, alfabeto_input, con_enie))
    elif btn_atbash:
        st.code(cifrar_atbash(texto_input, alfabeto_input, con_enie))
    elif btn_auto:
        tipo = detectar_cifrado(texto_input, alfabeto_input, con_enie)
        st.info(f"Método: {tipo}")
        if "César" in tipo:
            d = int(tipo.split()[-1])
            st.success(f"Resultado: {descifrar_cesar(texto_input, d, alfabeto_input, con_enie)}")
        else:
            st.success(f"Resultado: {cifrar_atbash(texto_input, alfabeto_input, con_enie)}")