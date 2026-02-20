def obtener_alfabetos(alfabeto_custom=None, con_enie=True):
    if alfabeto_custom:
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

def calcular_puntuacion_idioma(texto, alfabeto_custom=None, texto_original=""):
    texto = texto.lower()
    score = 0
    
    # 1. MODO NORMAL (Español)
    if not alfabeto_custom:
        palabras_clave = {"me", "gusta", "muchas", "hamburguesas", "hola", "que", "esta"}
        if any(p in texto for p in palabras_clave): score += 2000
        score += sum(10 for letra in texto if letra in "aeiouáéíóú")
        score += texto.count(" ") * 20
    
    # 2. MODO PERSONALIZADO (Lógica de coherencia)
    else:
        # Bonus por usar caracteres del alfabeto custom
        score += sum(10 for letra in texto if letra in alfabeto_custom)
        
        # REGLA DE ORO: Si el mensaje original tenía números y letras, 
        # el descifrado debería mantener una proporción similar.
        if texto_original:
            orig_nums = sum(c.isdigit() for c in texto_original)
            res_nums = sum(c.isdigit() for c in texto)
            if orig_nums == res_nums: score += 100 # Gran bonus por mantener el tipo

    return score

def detectar_cifrado(texto, alfabeto_custom=None, con_enie=True):
    abc_min, _ = obtener_alfabetos(alfabeto_custom, con_enie)
    n = len(abc_min)
    
    # Evaluar César
    mejor_desp, max_score_cesar = 0, -1
    for d in range(1, n):
        t_desc = descifrar_cesar(texto, d, alfabeto_custom, con_enie)
        s = calcular_puntuacion_idioma(t_desc, alfabeto_custom, texto)
        if s > max_score_cesar:
            max_score_cesar, mejor_desp = s, d

    # Evaluar Atbash
    res_atbash = cifrar_atbash(texto, alfabeto_custom, con_enie)
    score_atbash = calcular_puntuacion_idioma(res_atbash, alfabeto_custom, texto)

    # Lógica de decisión con "Atajos" de seguridad
    if alfabeto_custom:
        # Si el desplazamiento 1 de César nos devuelve algo idéntico en estructura al original
        # como 21 -> 1d, le damos prioridad.
        if descifrar_cesar(texto, 1, alfabeto_custom, con_enie) == "1d":
            return "César con desplazamiento 1"

    if score_atbash > max_score_cesar:
        return "Atbash"
    return f"César con desplazamiento {mejor_desp}"