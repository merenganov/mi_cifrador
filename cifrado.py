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
    frec_es = {
        'a': 12.53, 'b': 1.42, 'c': 4.68, 'd': 5.86, 'e': 13.68, 'f': 0.69,
        'g': 1.01, 'h': 0.70, 'i': 6.25, 'j': 0.44, 'k': 0.02, 'l': 4.97,
        'm': 3.15, 'n': 6.71, 'ñ': 0.31, 'o': 8.68, 'p': 2.51, 'q': 0.88,
        'r': 6.87, 's': 7.98, 't': 4.63, 'u': 3.93, 'v': 0.90, 'w': 0.01,
        'x': 0.22, 'y': 0.90, 'z': 0.52
    }
    texto = texto.lower()
    letras_solo = [c for c in texto if c in frec_es or c.isdigit()]
    total = len(letras_solo)
    if total == 0: return 0
    score = 0
    for letra, f_esperada in frec_es.items():
        f_real = (texto.count(letra) / total) * 100
        score += (15 - abs(f_real - f_esperada))
    return score

def detectar_cifrado(texto, alfabeto_custom=None, con_enie=True):
    res_atbash = cifrar_atbash(texto, alfabeto_custom, con_enie)
    score_atbash = calcular_puntuacion_idioma(res_atbash)
    
    abc_min, _ = obtener_alfabetos(alfabeto_custom, con_enie)
    n = len(abc_min)
    mejor_desp, max_score = 0, -float('inf')
    
    for d in range(1, n):
        t_desc = descifrar_cesar(texto, d, alfabeto_custom, con_enie)
        s = calcular_puntuacion_idioma(t_desc)
        if s > max_score:
            max_score, mejor_desp = s, d
            
    # Si es alfabeto personalizado, forzamos que devuelva el mejor resultado encontrado
    if alfabeto_custom:
        # Priorizamos Atbash si su score es decente, si no, el mejor César
        if score_atbash >= max_score:
            return "Atbash"
        return f"César con desplazamiento {mejor_desp}"

    # Para alfabeto normal, mantenemos un filtro de seguridad
    if max_score < 30 and score_atbash < 30:
        return "Cifrado desconocido"

    return "Atbash" if score_atbash >= max_score else f"César con desplazamiento {mejor_desp}"