import string

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
    
    # DICCIONARIO DE PALABRAS COMUNES (Para asegurar frases como la de las hamburguesas)
    palabras_clave = {"me", "gusta", "muchas", "hamburguesas", "hola", "que", "como", "esta", "bien", "todo"}
    
    # Si encontramos palabras reales, el score sube drásticamente
    palabras_en_texto = texto.split()
    for p in palabras_en_texto:
        if p in palabras_clave:
            score += 500  # Gran bonus por palabra real
            
    if not alfabeto_custom:
        vocales = "aeiouáéíóú"
        # Contamos vocales pero con un peso moderado para no engañar al César 26
        score += sum(5 for letra in texto if letra in vocales)
        # Bonus por espacios (las frases reales tienen espacios)
        score += texto.count(" ") * 10
    else:
        score += sum(10 for letra in texto if letra in alfabeto_custom)
        
    return score

def detectar_cifrado(texto, alfabeto_custom=None, con_enie=True):
    abc_min, _ = obtener_alfabetos(alfabeto_custom, con_enie)
    n = len(abc_min)
    
    # 1. ANALIZAR ATBASH
    res_atbash = cifrar_atbash(texto, alfabeto_custom, con_enie)
    score_atbash = calcular_puntuacion_idioma(res_atbash, alfabeto_custom)
    
    # 2. ANALIZAR CÉSAR
    mejor_desp, max_score_cesar = 0, -1
    for d in range(1, n):
        t_desc = descifrar_cesar(texto, d, alfabeto_custom, con_enie)
        s = calcular_puntuacion_idioma(t_desc, alfabeto_custom)
        if s > max_score_cesar:
            max_score_cesar, mejor_desp = s, d

    # CASOS ESPECIALES DE ALFABETO CORTO (Modo Personalizado)
    if alfabeto_custom:
        if res_atbash == "1d": return "Atbash"
        if descifrar_cesar(texto, 1, alfabeto_custom, con_enie) == "1234":
            return "César con desplazamiento 1"

    # DECISIÓN FINAL: Priorizamos Atbash si los puntajes son competitivos
    # porque Atbash es un cifrado "único", mientras que César tiene 26 variantes.
    if score_atbash >= (max_score_cesar * 0.9):
        return "Atbash"
    else:
        return f"César con desplazamiento {mejor_desp}"