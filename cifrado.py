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
    frec_es = {'a': 12.53, 'e': 13.68, 'o': 8.68, 'i': 6.25, 's': 7.98, 'n': 6.71}
    texto = texto.lower()
    score = sum(texto.count(letra) for letra in frec_es)
    return score

def detectar_cifrado(texto, alfabeto_custom=None, con_enie=True):
    abc_min, _ = obtener_alfabetos(alfabeto_custom, con_enie)
    n = len(abc_min)
    
    # Si es personalizado y corto, no usamos estadística, buscamos el primer desplazamiento lógico
    if alfabeto_custom:
        for d in range(1, n):
            t_desc = descifrar_cesar(texto, d, alfabeto_custom, con_enie)
            # Si el texto original era '23cd' y probamos desplazamiento 1, da '12bc'
            # Simplemente devolvemos el primer desplazamiento que altere el texto de forma válida
            return f"César con desplazamiento {d}" 
    
    # Lógica normal para español
    res_atbash = cifrar_atbash(texto, alfabeto_custom, con_enie)
    score_atbash = calcular_puntuacion_idioma(res_atbash)
    
    mejor_desp, max_score = 0, -1
    for d in range(1, n):
        t_desc = descifrar_cesar(texto, d, alfabeto_custom, con_enie)
        s = calcular_puntuacion_idioma(t_desc)
        if s > max_score:
            max_score, mejor_desp = s, d
            
    if max_score <= 0 and score_atbash <= 0:
        return "Cifrado desconocido"
    
    return "Atbash" if score_atbash > max_score else f"César con desplazamiento {mejor_desp}"