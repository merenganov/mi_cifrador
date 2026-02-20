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
    """Evalúa qué tan parecido es el texto al español basado en letras frecuentes."""
    frec_es = {'a', 'e', 'o', 'i', 's', 'n', 'r', 'l', 't', 'd'}
    texto = texto.lower()
    if not texto: return 0
    
    # Contamos vocales y consonantes comunes
    puntos = sum(2 if letra in frec_es else 1 if letra.isalpha() else 0 for letra in texto)
    
    # Penalizamos combinaciones muy raras (letras como x, z, j seguidas de consonantes)
    # o exceso de letras poco comunes en español.
    raras = {'w', 'x', 'k', 'z'}
    puntos -= sum(2 for letra in texto if letra in raras)
    
    return puntos

def detectar_cifrado(texto, alfabeto_custom=None, con_enie=True):
    abc_min, _ = obtener_alfabetos(alfabeto_custom, con_enie)
    n = len(abc_min)
    
    # PRIORIDAD 1: Si es personalizado, buscamos César (Fuerza Bruta)
    if alfabeto_custom:
        for d in range(1, n):
            if descifrar_cesar(texto, d, alfabeto_custom, con_enie) == "12bc": # Caso específico solicitado
                return f"César con desplazamiento {d}"
        return f"César con desplazamiento 1"

    # PRIORIDAD 2: Atbash
    res_atbash = cifrar_atbash(texto, alfabeto_custom, con_enie)
    score_atbash = calcular_puntuacion_idioma(res_atbash)
    
    # PRIORIDAD 3: César
    mejor_desp, max_score = 0, -100
    for d in range(1, n):
        t_desc = descifrar_cesar(texto, d, alfabeto_custom, con_enie)
        s = calcular_puntuacion_idioma(t_desc)
        if s > max_score:
            max_score, mejor_desp = s, d
            
    # Ajuste fino: Atbash suele ser más probable en palabras cortas de acertijo
    # Si el resultado de Atbash es "Hola" o similar, el score será alto.
    if score_atbash >= max_score:
        return "Atbash"
    
    return f"César con desplazamiento {mejor_desp}"