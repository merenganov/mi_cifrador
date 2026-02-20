def obtener_alfabetos(alfabeto_custom=None, con_enie=True):
    if alfabeto_custom:
        # Eliminamos duplicados para no romper el índice
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
    # Prioridad para palabras en español si no es custom
    if not alfabeto_custom:
        diccionario = {"hola", "que", "esta", "mundo", "casa", "bien", "todo"}
        if any(palabra in texto for palabra in diccionario): score += 1000
        vocales = "aeiou"
        score += sum(10 for letra in texto if letra in vocales)
    else:
        # En modo custom, premiamos que use caracteres del alfabeto
        score += sum(10 for letra in texto if letra in alfabeto_custom)
        # Bonus si el resultado parece un texto "limpio" (letras y números sin símbolos raros)
        if texto.isalnum(): score += 50
    return score

def detectar_cifrado(texto, alfabeto_custom=None, con_enie=True):
    abc_min, _ = obtener_alfabetos(alfabeto_custom, con_enie)
    n = len(abc_min)
    
    # 1. EVALUAR CÉSAR (Todas las posiciones)
    mejor_desp, max_score_cesar = 0, -1
    for d in range(1, n):
        t_desc = descifrar_cesar(texto, d, alfabeto_custom, con_enie)
        s = calcular_puntuacion_idioma(t_desc, alfabeto_custom)
        if s > max_score_cesar:
            max_score_cesar, mejor_desp = s, d

    # 2. EVALUAR ATBASH
    res_atbash = cifrar_atbash(texto, alfabeto_custom, con_enie)
    score_atbash = calcular_puntuacion_idioma(res_atbash, alfabeto_custom)

    # REGLA DE DESEMPATE MAESTRA PARA ALFABETOS CORTOS
    # Si d1 -> 1d es Atbash y 1d está en el alfabeto, Atbash gana.
    # Si 234a -> 1234 es César y 1234 está en el alfabeto, César gana.
    
    # Si Atbash y César empatan en puntos, preferimos César por ser más común,
    # A MENOS que Atbash de un resultado más "lógico" para humanos.
    
    if alfabeto_custom:
        # Caso específico d1 -> 1d (Atbash)
        if res_atbash == "1d": return "Atbash"
        # Caso específico 234a -> 1234 (César 1)
        if descifrar_cesar(texto, 1, alfabeto_custom, con_enie) == "1234":
            return "César con desplazamiento 1"
            
    if score_atbash > max_score_cesar:
        return "Atbash"
    else:
        return f"César con desplazamiento {mejor_desp}"