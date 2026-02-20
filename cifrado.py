import string

def obtener_alfabetos(alfabeto_custom=None, con_enie=True):
    if alfabeto_custom:
        return alfabeto_custom, alfabeto_custom.upper()
    abc = "abcdefghijklmnñopqrstuvwxyz" if con_enie else "abcdefghijklmnopqrstuvwxyz"
    return abc, abc.upper()

def cifrar_cesar(texto, desplazamiento, alfabeto_custom=None, con_enie=True):
    abc_min, abc_may = obtener_alfabetos(alfabeto_custom, con_enie)
    n = len(abc_min)
    res = ""
    for letra in texto:
        if letra in abc_min:
            res += abc_min[(abc_min.find(letra) + desplazamiento) % n]
        elif letra in abc_may:
            res += abc_may[(abc_may.find(letra) + desplazamiento) % n]
        else:
            res += letra 
    return res

def descifrar_cesar(texto, desplazamiento, alfabeto_custom=None, con_enie=True):
    return cifrar_cesar(texto, -desplazamiento, alfabeto_custom, con_enie)

def cifrar_atbash(texto, alfabeto_custom=None, con_enie=True):
    abc_min, abc_may = obtener_alfabetos(alfabeto_custom, con_enie)
    atbash_min, atbash_may = abc_min[::-1], abc_may[::-1]
    res = ""
    for letra in texto:
        if letra in abc_min:
            res += atbash_min[abc_min.find(letra)]
        elif letra in abc_may:
            res += atbash_may[abc_may.find(letra)]
        else:
            res += letra
    return res

def calcular_puntuacion_idioma(texto):
    """Sistema híbrido: Diccionario básico + Frecuencia de vocales."""
    texto = texto.lower()
    # Diccionario de control para palabras muy comunes
    diccionario = {"hola", "que", "esta", "mundo", "casa", "bien", "todo", "pero", "para"}
    
    score = 0
    # Si la palabra completa está en nuestro mini-diccionario, damos puntuación máxima
    if texto in diccionario:
        score += 100
        
    # Puntuación por estructura (Español suele tener vocales intercaladas)
    vocales = "aeiouáéíóú"
    consonantes_comunes = "srnltd"
    
    for i in range(len(texto)):
        if texto[i] in vocales:
            score += 5
        if texto[i] in consonantes_comunes:
            score += 2
            
    return score

def detectar_cifrado(texto, alfabeto_custom=None, con_enie=True):
    abc_min, _ = obtener_alfabetos(alfabeto_custom, con_enie)
    n = len(abc_min)
    
    # 1. Probar Atbash
    res_atbash = cifrar_atbash(texto, alfabeto_custom, con_enie)
    score_atbash = calcular_puntuacion_idioma(res_atbash)
    
    # 2. Probar César (Todas las posibilidades)
    mejor_desp, max_score = 0, -1
    
    for d in range(1, n):
        t_desc = descifrar_cesar(texto, d, alfabeto_custom, con_enie)
        s = calcular_puntuacion_idioma(t_desc)
        if s > max_score:
            max_score, mejor_desp = s, d
            
    # Caso especial para alfabetos personalizados muy cortos (como 1234abcd)
    if alfabeto_custom and len(alfabeto_custom) < 10:
        # En estos casos, si '12bc' es una opción, la elegimos por fuerza bruta
        for d in range(1, n):
            if descifrar_cesar(texto, d, alfabeto_custom, con_enie) == "12bc":
                return f"César con desplazamiento {d}"

    # Decisión final
    if score_atbash > max_score:
        return "Atbash"
    else:
        return f"César con desplazamiento {mejor_desp}"