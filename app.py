import streamlit as st
from cifrado import cifrar_cesar, descifrar_cesar, cifrar_atbash, detectar_cifrado

st.set_page_config(page_title="Cipher Pro", page_icon="🔐", layout="centered")

st.title("🔐 Cyber-Dashboard")

# --- SIDEBAR ---
st.sidebar.header("Configuración")
modo_custom = st.sidebar.toggle("Modo Personalizado")
if modo_custom:
    alfabeto_input = st.sidebar.text_input("Abecedario personalizado:", value="1234abcd")
    con_enie = False
else:
    alfabeto_input = None
    con_enie = st.sidebar.checkbox("Usar Ñ", value=True)

# --- ENTRADA ---
texto_input = st.text_area("Entrada:", placeholder="Escribe tu mensaje...")
desp_manual = st.number_input("Desplazamiento César (Manual):", 1, 30, 1)

c1, c2, c3 = st.columns(3)
with c1: btn_cifrar = st.button("Cifrar", use_container_width=True)
with c2: btn_atbash = st.button("Atbash", use_container_width=True)
with c3: btn_auto = st.button("AUTO-DETECTAR", type="primary", use_container_width=True)

st.divider()

# --- LÓGICA ---
if texto_input:
    if btn_cifrar:
        res = cifrar_cesar(texto_input, desp_manual, alfabeto_input, con_enie)
        st.success(f"Cifrado César: {res}")
        
    elif btn_atbash:
        res = cifrar_atbash(texto_input, alfabeto_input, con_enie)
        st.success(f"Resultado Atbash: {res}")
        
    elif btn_auto:
        tipo = detectar_cifrado(texto_input, alfabeto_input, con_enie)
        st.info(f"Método Detectado: {tipo}")
        
        if "César" in tipo:
            d = int(tipo.split()[-1])
            descifrado = descifrar_cesar(texto_input, d, alfabeto_input, con_enie)
        else:
            descifrado = cifrar_atbash(texto_input, alfabeto_input, con_enie)
            
        st.success(f"Texto Descifrado: {descifrado}")
else:
    if btn_cifrar or btn_atbash or btn_auto:
        st.warning("Por favor ingresa un texto.")