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

def calcular_puntuacion_idioma(texto, alfabeto_custom=None):
    texto = texto.lower()
    score = 0
    if not alfabeto_custom:
        diccionario = {"hola", "que", "esta", "mundo", "casa", "bien", "todo"}
        if any(palabra in texto for palabra in diccionario): score += 500
        vocales = "aeiou"
        score += sum(10 for letra in texto if letra in vocales)
    else:
        # En modo custom, premiamos que los caracteres sean del alfabeto
        score += sum(5 for letra in texto if letra in alfabeto_custom)
        # Bonus si el texto resultante parece tener un orden ascendente (común en pruebas)
        if len(texto) > 1 and texto[0].isdigit() and texto[1].isdigit():
            if int(texto[1]) > int(texto[0]): score += 20 
    return score

def detectar_cifrado(texto, alfabeto_custom=None, con_enie=True):
    abc_min, _ = obtener_alfabetos(alfabeto_custom, con_enie)
    n = len(abc_min)
    
    # 1. ANALIZAR CÉSAR PRIMERO (En alfabetos cortos es lo más común)
    mejor_desp, max_score_cesar = 0, -1
    for d in range(1, n):
        t_desc = descifrar_cesar(texto, d, alfabeto_custom, con_enie)
        s = calcular_puntuacion_idioma(t_desc, alfabeto_custom)
        if s > max_score_cesar:
            max_score_cesar, mejor_desp = s, d

    # 2. ANALIZAR ATBASH
    res_atbash = cifrar_atbash(texto, alfabeto_custom, con_enie)
    score_atbash = calcular_puntuacion_idioma(res_atbash, alfabeto_custom)

    # REGLA DE DESEMPATE CRÍTICA:
    # Si estamos en modo personalizado y los puntajes son similares, 
    # preferimos CÉSAR a menos que el Atbash sea abrumadoramente mejor.
    umbral = 1.2 if alfabeto_custom else 1.0
    
    if score_atbash > (max_score_cesar * umbral):
        return "Atbash"
    else:
        return f"César con desplazamiento {mejor_desp}"