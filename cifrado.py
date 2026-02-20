import string

def obtener_alfabetos(alfabeto_custom=None, con_enie=True):
    if alfabeto_custom:
        # Eliminamos duplicados para evitar errores de mapeo
        alfabeto_limpio = "".join(dict.fromkeys(alfabeto_custom))
        return alfabeto_limpio, alfabeto_limpio.upper()
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

def calcular_puntuacion_idioma(texto, alfabeto_custom=None):
    texto = texto.lower()
    score = 0
    
    # Si NO es custom, usamos reglas de español
    if not alfabeto_custom:
        diccionario = {"hola", "que", "esta", "mundo", "casa", "bien", "todo"}
        if any(palabra in texto for palabra in diccionario): score += 100
        vocales = "aeiou"
        score += sum(5 for letra in texto if letra in vocales)
    else:
        # Si ES custom, simplemente puntuamos que los caracteres sean válidos
        score += len([letra for letra in texto if letra in alfabeto_custom])
        
    return score

def detectar_cifrado(texto, alfabeto_custom=None, con_enie=True):
    abc_min, _ = obtener_alfabetos(alfabeto_custom, con_enie)
    n = len(abc_min)
    
    # 1. Probar Atbash (Tiene prioridad en modos simétricos como 1d -> d1)
    res_atbash = cifrar_atbash(texto, alfabeto_custom, con_enie)
    score_atbash = calcular_puntuacion_idioma(res_atbash, alfabeto_custom)
    
    # 2. Probar César
    mejor_desp, max_score = 0, -1
    for d in range(1, n):
        t_desc = descifrar_cesar(texto, d, alfabeto_custom, con_enie)
        s = calcular_puntuacion_idioma(t_desc, alfabeto_custom)
        if s > max_score:
            max_score, mejor_desp = s, d

    # Lógica de decisión: Si Atbash devuelve algo coherente, es muy probable que sea Atbash
    # Especialmente en casos como d1 -> 1d
    if score_atbash >= max_score:
        return "Atbash"
    return f"César con desplazamiento {mejor_desp}"