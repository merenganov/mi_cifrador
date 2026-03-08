import string

def obtener_alfabetos(alfabeto_custom=None, con_enie=True):
    if alfabeto_custom:
        alfabeto_limpio = "".join(dict.fromkeys(alfabeto_custom))
        return alfabeto_limpio, alfabeto_limpio.upper()
    # El abecedario español estándar tiene 27 o 28 letras dependiendo de la Ñ
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
    # IMPORTANTE: Para descifrar, el desplazamiento es negativo
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
    
    # DICCIONARIO TÉCNICO EXTENDIDO
    diccionario = {
     # palabras comunes
     "de","la","el","los","las","un","una","unos","unas",
     "es","son","en","para","con","sin","por","porque",
     "que","cual","como","cuando","donde","quien",
     "este","esta","estos","estas",
     "su","sus","del","al",

     # palabras de examen
     "definir","define","explicar","explica","menciona",
     "indica","describe","selecciona","identifica",
     "correcto","incorrecto","verdadero","falso",
     "ejemplo","funcion","proceso","metodo",
     "sistema","concepto","caracteristica",

     # ciberseguridad general
     "seguridad","ciberseguridad","seguridad_informatica",
     "proteccion","riesgo","amenaza","vulnerabilidad",
     "ataque","defensa","seguro","incidente",
     "prevencion","deteccion","monitoreo",

     # triada cia
     "confidencialidad","integridad","disponibilidad",

     # autenticacion y acceso
     "autenticacion","autorizacion","acceso",
     "usuario","administrador","permiso",
     "credenciales","identidad","login","password",
     "contraseña","token",

     # criptografia
     "criptografia","cifrado","descifrado",
     "encriptacion","desencriptacion",
     "clave","llave","hash","algoritmo",
     "firma","digital","certificado",

     # ataques
     "malware","virus","gusano","troyano",
     "phishing","ransomware","spyware",
     "ataque","fuerza","bruta","inyeccion",
     "sql","ddos","spoofing",

     # redes
     "red","redes","internet","protocolo",
     "tcp","ip","http","https","dns",
     "router","switch","servidor","cliente",
     "conexion","paquete","puerto",

     # seguridad de red
     "firewall","vpn","segmentacion",
     "filtrado","monitorizacion",

     # datos
     "datos","informacion","base","datos",
     "almacenamiento","backup","respaldo",
     "recuperacion",

     # ingenieria social
     "ingenieria","social","engaño",
     "manipulacion","usuario","confianza",

     # software y sistemas
     "sistema","operativo","software",
     "hardware","aplicacion","programa",
     "actualizacion","parche","configuracion",

      # otros conceptos
     "politica","seguridad","auditoria",
     "control","gestion","riesgo",
     "evaluacion","analisis","proteccion"
     }
    
    # 1. Búsqueda de palabras reales (Máxima prioridad)
    palabras_en_texto = texto.split()
    for palabra in palabras_en_texto:
        if palabra in diccionario:
            score += 2000 

    if not alfabeto_custom:
        # 2. Análisis de frecuencia (El español abunda en estas letras)
        letras_comunes = "eaosrnidlc" 
        for letra in texto:
            if letra in letras_comunes:
                score += 15
        # Bonus por espacios (Indica estructura de frase)
        score += texto.count(" ") * 30
    else:
        score += sum(10 for letra in texto if letra in alfabeto_custom)
        
    return score

def obtener_mejores_candidatos(texto, alfabeto_custom=None, con_enie=True):
    abc_min, _ = obtener_alfabetos(alfabeto_custom, con_enie)
    n = len(abc_min)
    
    # Candidato Atbash
    res_atbash = cifrar_atbash(texto, alfabeto_custom, con_enie)
    score_atbash = calcular_puntuacion_idioma(res_atbash, alfabeto_custom)
    
    # Mejor Candidato César
    mejor_desp, max_score_cesar = 0, -1
    for d in range(1, n):
        t_desc = descifrar_cesar(texto, d, alfabeto_custom, con_enie)
        s = calcular_puntuacion_idioma(t_desc, alfabeto_custom)
        if s > max_score_cesar:
            max_score_cesar, mejor_desp = s, d
            
    res_cesar = descifrar_cesar(texto, mejor_desp, alfabeto_custom, con_enie)
    
    return {
        "atbash": {"texto": res_atbash, "score": score_atbash},
        "cesar": {"texto": res_cesar, "score": max_score_cesar, "desp": mejor_desp}
    }