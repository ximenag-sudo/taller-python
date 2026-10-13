# =====================================================================
# TALLER INDIVIDUAL: Análisis, depuración e integración de Python
# Un solo archivo con los nueve ejercicios.
# Ejecutar:  python taller.py   y elegir el número del ejercicio (1 a 9)
# En cada ejercicio, la PREDICCIÓN está escrita en comentarios antes del
# código; al ejecutar se contrasta con el resultado real.
# =====================================================================


# =====================================================================
# EJERCICIO 1: Entrada, conversión y control de un ciclo
# =====================================================================
# PREDICCIÓN (antes de ejecutar). Programa ORIGINAL:
#
#   total = 0.0
#   cantidad = 0
#   while True:
#       texto = input("Medición o fin: ")
#       valor = float(texto)
#       if texto == "fin":
#           break
#       if valor >= 0:
#           total += valor
#       cantidad += 1
#   print(total / cantidad)
#
# Entradas: "4", "-2", "6", "fin"
#   inicio: total = 0.0  | cantidad = 0
#   "4"   : valor = 4.0  | total = 4.0  | cantidad = 1
#   "-2"  : valor = -2.0 | no entra al if, total = 4.0 | cantidad = 2
#   "6"   : valor = 6.0  | total = 10.0 | cantidad = 3
#   "fin" : float("fin") lanza ValueError; valor no se asigna.
# Se interrumpe en  valor = float(texto)  al escribir "fin".
# NO llega a imprimir promedio: el "if texto == 'fin'" está después de
# la conversión y print(total / cantidad) nunca se ejecuta.
# Otros errores: (1) se convierte antes de revisar "fin";
# (2) cantidad += 1 está fuera del if, cuenta negativos;
# (3) sin mediciones aceptadas, total / cantidad da ZeroDivisionError.
#
# RESULTADO REAL AL EJECUTAR EL ORIGINAL: ValueError al escribir "fin".
#   ¿Coincidió con mi predicción? Sí.
#
# CORRECCIÓN: ver promedio_mediciones() más abajo.
# Casos que muestran por qué era necesario cambiarlo:
#   4, -2, 6, fin  -> original: ValueError | corregido: 5.0
#                     (si solo se moviera "fin" y cantidad siguiera fuera
#                      del if, daría 10/3 = 3.33: error silencioso)
#   abc, 3, fin    -> original: ValueError | corregido: mensaje y 3.0
#   -5, fin        -> original: ValueError | corregido: "No se aceptó..."
#   fin            -> original: ValueError | corregido: "No se aceptó..."
#
# ¿POR QUÉ NO CAMBIAR float(texto) POR eval(texto)?
#   El contrato es «recibir una medición numérica». float convierte
#   texto numérico y rechaza lo demás con ValueError. eval EJECUTA
#   cualquier expresión de Python:
#   1) Seguridad: __import__("os").system("...") ejecuta código arbitrario.
#   2) Acepta lo que no es medición: eval("[1,2]") da lista,
#      eval("'hola'") da cadena; luego fallan con TypeError.
#   3) Lanza NameError (eval("abc")) o SyntaxError (eval("3 +")), que un
#      except ValueError no captura.
#   4) eval("True") da True, que Python trata como 1.
#   float VALIDA y CONVIERTE; eval INTERPRETA y EJECUTA.

def promedio_mediciones():
    total = 0.0
    cantidad = 0

    while True:
        texto = input("Medición o fin: ")

        if texto == "fin":              # Cambio 1: revisar "fin" ANTES de convertir
            break

        try:                            # Cambio 2: rechazar no numéricas y seguir
            valor = float(texto)
        except ValueError:
            print("Entrada no válida: escriba un número o 'fin'.")
            continue

        if valor >= 0:                  # Cambio 3: negativos no suman ni cuentan
            total += valor
            cantidad += 1

    if cantidad == 0:                   # Cambio 4: informar sin dividir
        print("No se aceptó ninguna medición.")
    else:
        print(total / cantidad)


# =====================================================================
# EJERCICIO 2: Colecciones, alias y estado de una función
# =====================================================================
# PREDICCIÓN. Programa ORIGINAL:
#
#   def registrar(valores, registro):
#       copia = valores.copy()
#       copia[0] = copia[0] + 1
#       registro["ultima"] = copia
#       return copia
#
#   datos = [2, 4]; registro = {}
#   salida = registrar(datos, registro)
#   salida.append(8)
#   print(datos); print(registro); print(salida)
#
# Traza: valores.copy() crea una lista NUEVA B = [2, 4]; copia[0] + 1
# la deja [3, 4]; registro["ultima"] apunta a B (alias); salida también
# apunta a B; salida.append(8) hace B = [3, 4, 8].
# Salidas:  [2, 4]   {'ultima': [3, 4, 8]}   [3, 4, 8]
# Objetos distintos: datos, la lista B y el diccionario registro.
# Misma lista B: copia, registro["ultima"] y salida.
# ¿Copiar valores evita todas las modificaciones compartidas? NO: solo
# protege a datos. B se comparte entre registro y salida.
#
# RESULTADO REAL AL EJECUTAR: igual a la predicción.
#   ¿Coincidió con mi predicción? Sí.
#
# CORRECCIÓN (única línea cambiada de la asignación):
#   registro["ultima"] = copia.copy()
# Basta con números porque los enteros son inmutables: una copia
# superficial ya no comparte nada que pueda cambiar. Con listas internas
# haría falta copy.deepcopy.
# Caso: tras salida.append(8), original deja registro = {'ultima':
# [3, 4, 8]}; corregido lo deja {'ultima': [3, 4]}.
#
# SI datos FUERA LA TUPLA (2, 4): la primera operación que falla es
# valores.copy() -> AttributeError (las tuplas no tienen .copy()).
# Cambio: copia = list(valores)   (acepta lista o tupla y crea lista
# nueva; copia[0] = ... sigue funcionando porque es una lista).

def registrar_original(valores, registro):
    copia = valores.copy()
    copia[0] = copia[0] + 1
    registro["ultima"] = copia
    return copia


def registrar_corregida(valores, registro):
    copia = list(valores)               # acepta lista o tupla
    copia[0] = copia[0] + 1
    registro["ultima"] = copia.copy()   # el registro guarda su propia copia
    return copia


def ejercicio_2():
    print("===== EJERCICIO 2 =====")
    print("\n--- Original ---")
    datos = [2, 4]
    registro = {}
    salida = registrar_original(datos, registro)
    salida.append(8)
    print(datos)        # [2, 4]
    print(registro)     # {'ultima': [3, 4, 8]}
    print(salida)       # [3, 4, 8]
    print("salida is registro['ultima']:", salida is registro["ultima"])

    print("\n--- Corregida ---")
    datos = [2, 4]
    registro = {}
    salida = registrar_corregida(datos, registro)
    salida.append(8)
    print(datos)        # [2, 4]
    print(registro)     # {'ultima': [3, 4]}
    print(salida)       # [3, 4, 8]
    print("salida is registro['ultima']:", salida is registro["ultima"])

    print("\n--- Tupla (2, 4) ---")
    try:
        registrar_original((2, 4), {})
    except AttributeError as error:
        print("Original falla:", error)
    print("Corregida:", registrar_corregida((2, 4), {}))   # [3, 4]


# =====================================================================
# EJERCICIO 3: Primalidad, break y for...else
# =====================================================================
# PREDICCIÓN. Programa ORIGINAL:
#
#   def es_primo(n):
#       for divisor in range(2, n):
#           if n % divisor == 0:
#               resultado = False
#               break
#       else:
#           resultado = True
#       return resultado
#
# El else de un for se ejecuta cuando el ciclo termina SIN break
# (incluso si nunca entró).
#   n = 1: range(2, 1) vacío, el ciclo no se ejecuta, se alcanza el
#          else -> True (INCORRECTO: 1 no es primo).
#   n = 2: range(2, 2) vacío, no se ejecuta, se alcanza el else -> True.
#   n = 9: range(2, 9) = 2..8, el ciclo sí se ejecuta. Se prueban 2
#          (9 % 2 = 1) y 3 (9 % 3 = 0 -> resultado = False, break).
#          Hay break, el else NO se alcanza -> False. Los divisores
#          4 a 8 no se prueban.
# Predicción: es_primo(1) = True, es_primo(2) = True, es_primo(9) = False.
#
# RESULTADO REAL AL EJECUTAR: True, True, False.
#   ¿Coincidió con mi predicción? Sí.
#
# CORRECCIÓN: guarda al inicio  if n < 2: return False
# Casos: es_primo(1), (0), (-7): original True, corregida False;
#        es_primo(2) sigue True y es_primo(9) sigue False.
#
# REFUTACIÓN de «el else significa que el último if fue falso»:
#   El else pertenece al CICLO, no al if. Con n = 1 el ciclo nunca
#   entra, el if jamás se evalúa (no existe "último if") y aun así el
#   else se ejecuta. Con n = 9 el if fue falso para 2, pero el else NO
#   se ejecuta porque hubo break. El else significa «el ciclo terminó
#   sin break».

def es_primo_original(n):
    for divisor in range(2, n):
        if n % divisor == 0:
            resultado = False
            break
    else:
        resultado = True
    return resultado


def es_primo_corregida(n):
    if n < 2:
        return False
    for divisor in range(2, n):
        if n % divisor == 0:
            resultado = False
            break
    else:
        resultado = True
    return resultado


def ejercicio_3():
    print("===== EJERCICIO 3 =====")
    print("\n--- Original ---")
    print("es_primo(1):", es_primo_original(1))   # True (error)
    print("es_primo(2):", es_primo_original(2))   # True
    print("es_primo(9):", es_primo_original(9))   # False
    print("Divisores probados para 9:")
    for divisor in range(2, 9):
        print("  probando", divisor, "-> 9 %", divisor, "=", 9 % divisor)
        if 9 % divisor == 0:
            print("  break: no se alcanza el else")
            break

    print("\n--- Original vs. corregida ---")
    for n in [-7, 0, 1, 2, 9, 13]:
        print("es_primo(", n, "): original =", es_primo_original(n),
              "| corregida =", es_primo_corregida(n))

    print("\n--- Refutación: el else no es 'el último if fue falso' ---")
    evaluo_if = False
    for divisor in range(2, 1):
        evaluo_if = True
    else:
        print("n = 1: ¿se evaluó algún if?", evaluo_if,
              "-> y aun así el else se ejecutó")


# =====================================================================
# EJERCICIO 4: Recursividad: contrato, caso base y progreso
# =====================================================================
# PREDICCIÓN euclides(84, 30):
#   euclides(84, 30) -> euclides(30, 24)
#   euclides(30, 24) -> euclides(24, 6)
#   euclides(24, 6)  -> euclides(6, 0)
#   euclides(6, 0)   -> caso base, devuelve a = 6. Ese 6 sube por todas
#   las llamadas. Resultado: 6.
# Disminuye el segundo argumento b: 30 -> 24 -> 6 -> 0. El nuevo b es
# a % b, con 0 <= a % b < b: estrictamente menor y no negativo. Una
# sucesión de enteros no negativos que decrece estrictamente no puede
# ser infinita; llega a 0 y se activa el caso base.
#
# RESULTADO REAL: 6.   ¿Coincidió con mi predicción? Sí.
#
# factorial: probar 0 y 4 no basta porque son entradas VÁLIDAS; el
# contrato exige además decidir qué pasa con negativos, y n <= 1
# devuelve 1 en silencio para cualquier negativo (error silencioso).
# CORRECCIÓN: if n < 0: raise ValueError(...)
# Caso: factorial(-3) original = 1; corregida = ValueError.
#
# factorial(4): al LLEGAR al caso base factorial(1) = 1 siguen pendientes
# 2 * (...), 3 * (...) y 4 * (...): ninguna se ha calculado. La vuelta
# resuelve 2*1 = 2, 3*2 = 6, 4*6 = 24. Llegar al caso base detiene las
# llamadas nuevas; la ejecución termina cuando factorial(4) devuelve 24.

def euclides(a, b):
    if b == 0:
        return a
    return euclides(b, a % b)


def euclides_con_traza(a, b):
    print("  euclides(", a, ",", b, ")")
    if b == 0:
        print("  caso base: devuelve", a)
        return a
    return euclides_con_traza(b, a % b)


def factorial_original(n):
    return 1 if n <= 1 else n * factorial_original(n - 1)


def factorial_corregida(n):
    if n < 0:
        raise ValueError("factorial no está definido para negativos")
    return 1 if n <= 1 else n * factorial_corregida(n - 1)


def factorial_con_traza(n, nivel=0):
    sangria = "  " * nivel
    if n <= 1:
        print(sangria + "factorial(", n, ") -> CASO BASE, devuelve 1")
        print(sangria + "  (quedan pendientes las multiplicaciones de arriba)")
        return 1
    print(sangria + "factorial(", n, ") espera:", n, "* factorial(", n - 1, ")")
    resultado = n * factorial_con_traza(n - 1, nivel + 1)
    print(sangria + "factorial(", n, ") =", resultado)
    return resultado


def ejercicio_4():
    print("===== EJERCICIO 4 =====")
    print("\n--- euclides(84, 30) ---")
    print("Resultado:", euclides_con_traza(84, 30))   # 6

    print("\n--- factorial ---")
    print("original(0) =", factorial_original(0))      # 1
    print("original(4) =", factorial_original(4))      # 24
    print("original(-3) =", factorial_original(-3))    # 1 (incorrecto)
    print("corregida(0) =", factorial_corregida(0))    # 1
    print("corregida(4) =", factorial_corregida(4))    # 24
    try:
        factorial_corregida(-3)
    except ValueError as error:
        print("corregida(-3) lanza ValueError:", error)

    print("\n--- Traza de factorial(4) ---")
    print("Resultado final:", factorial_con_traza(4))  # 24


# =====================================================================
# EJERCICIO 5: Diseño de velocidades(intervalos, *pares, **opciones)
# =====================================================================
# CONTRATO: intervalos = duraciones en segundos (todas > 0); *pares = uno
# o más pares (inicial, final) en metros; **opciones = solo "escala"
# (por defecto 1). Velocidad = (final - inicial) / intervalo * escala.
# Devuelve lista nueva; no modifica entradas ni imprime. ValueError si:
# no hay pares, longitudes distintas, intervalo <= 0 u opción desconocida.
#
# PREDICCIÓN con intervalos=[2, 4], pares=[(1, 7), (8, 0)], escala=3.6:
#   (7 - 1) / 2 = 3.0 -> x 3.6 = 10.8
#   (0 - 8) / 4 = -2.0 -> x 3.6 = -7.2
#   Resultado: [10.8, -7.2] (puede salir 10.8 con error mínimo de float).
# Longitudes distintas: velocidades([2, 4], (1, 7)) -> ValueError.
#
# ¿Por qué zip sin verificar longitudes oculta un error? zip se detiene
# en la colección más corta sin avisar: con 2 intervalos y 1 par daría
# 1 velocidad, sin excepción, y se pierde el segundo dato.
#
# ¿Qué recibiría la función con pares SIN *? La lista completa llega
# como UN solo argumento: pares = ([(1, 7), (8, 0)],), una tupla de un
# elemento. len(pares) = 1 frente a 2 intervalos -> ValueError.
#
# Opción mal escrita esacala=3.6: **opciones la recibe sin quejarse
# ({"esacala": 3.6}); con opciones.get("escala", 1) se usaría 1 y
# devolvería [3.0, -2.0] sin avisar. Por eso se validan las claves.
#
# RESULTADO REAL: coincide.   ¿Coincidió con mi predicción? Sí.

def velocidades(intervalos, *pares, **opciones):
    """Calcula velocidades a partir de duraciones y pares de posiciones.

    Contrato:
        intervalos: lista de duraciones en segundos, todas positivas.
        *pares: uno o más pares (posicion_inicial, posicion_final) en metros.
        **opciones: solo "escala" (numérica, por defecto 1).

    Devuelve una lista nueva con (final - inicial) / intervalo * escala.
    No modifica las entradas ni imprime.
    Lanza ValueError si hay opción desconocida, no hay pares, las
    cantidades no coinciden o algún intervalo es <= 0.
    """
    desconocidas = [clave for clave in opciones if clave != "escala"]
    if desconocidas:
        raise ValueError("opción desconocida: " + ", ".join(desconocidas))
    escala = opciones.get("escala", 1)

    if len(pares) == 0:
        raise ValueError("debe haber al menos un par de posiciones")
    if len(intervalos) != len(pares):
        raise ValueError("la cantidad de intervalos (" + str(len(intervalos))
                         + ") no coincide con la de pares ("
                         + str(len(pares)) + ")")
    for intervalo in intervalos:
        if intervalo <= 0:
            raise ValueError("todos los intervalos deben ser positivos")

    resultado = []
    for intervalo, par in zip(intervalos, pares):
        inicial, final = par
        resultado.append((final - inicial) / intervalo * escala)
    return resultado


def ejercicio_5():
    print("===== EJERCICIO 5 =====")
    intervalos = [2, 4]
    pares = [(1, 7), (8, 0)]
    opciones = {"escala": 3.6}

    print("\n--- Llamada válida (desempaquetando) ---")
    print(velocidades(intervalos, *pares, **opciones))   # [10.8, -7.2]
    print("Sin escala:", velocidades(intervalos, *pares))  # [3.0, -2.0]
    print("Entradas intactas:", intervalos, pares, opciones)

    print("\n--- Longitudes distintas ---")
    try:
        velocidades([2, 4], (1, 7))
    except ValueError as error:
        print("ValueError:", error)
    print("zip sin verificar daría solo:", list(zip([2, 4], [(1, 7)])))

    print("\n--- Sin pares ---")
    try:
        velocidades([2, 4])
    except ValueError as error:
        print("ValueError:", error)

    print("\n--- Intervalo no positivo ---")
    try:
        velocidades([2, 0], (1, 7), (8, 0))
    except ValueError as error:
        print("ValueError:", error)

    print("\n--- pares SIN * ---")

    def mostrar_pares(intervalos, *pares):
        return pares

    print("Lo que recibe *pares:", mostrar_pares(intervalos, pares))
    try:
        velocidades(intervalos, pares)
    except ValueError as error:
        print("ValueError:", error)

    print("\n--- Opción mal escrita: esacala ---")
    try:
        velocidades(intervalos, *pares, esacala=3.6)
    except ValueError as error:
        print("ValueError:", error)


# =====================================================================
# EJERCICIO 6: Paquetes, importaciones y rutas
# =====================================================================
# Estructura:
#   curso/
#   ├── principal.py
#   ├── datos/mediciones.csv
#   └── biblioteca/Libreria/
#       ├── __init__.py            -> from .cinematica import velocidad
#       └── cinematica/
#           ├── __init__.py        -> from .codigo import velocidad
#           └── codigo.py          (define velocidad y hace print de demo)
#
# PREDICCIÓN (desde curso/, proceso nuevo), líneas impresas en orden:
#   Demostración 5.0
#   4.0
# Por qué: sys.path.insert(0, "biblioteca") agrega la carpeta; import
# Libreria ejecuta Libreria/__init__.py, que importa cinematica, cuyo
# __init__ importa codigo.py y EJECUTA el módulo completo: se define
# velocidad y corre el print de la demostración (10 / 2 = 5.0) DURANTE
# el import. Luego principal.py imprime Libreria.velocidad(12, 3) = 4.0.
#
# ¿Cómo llega velocidad a Libreria.velocidad? Cadena de reexportaciones:
# codigo.py la define; cinematica/__init__.py la importa (queda como
# nombre de Libreria.cinematica); Libreria/__init__.py la importa de
# .cinematica (queda como nombre de Libreria). Los puntos son
# importaciones relativas (dentro del mismo paquete); los tres nombres
# apuntan a la MISMA función.
#
# RESULTADO REAL: coincide.   ¿Coincidió con mi predicción? Sí.
#
# PARTE 2: python curso/principal.py desde la carpeta superior.
# Las rutas relativas "biblioteca" y "datos/mediciones.csv" se resuelven
# respecto al DIRECTORIO DE TRABAJO, no a la ubicación de principal.py.
#   a) "biblioteca" apunta a <superior>/biblioteca, que no existe;
#      Python no se queja al agregarla, y import Libreria falla con
#      ModuleNotFoundError (Libreria está en curso/biblioteca/).
#   b) Path("datos/mediciones.csv") apunta a <superior>/datos/..., que
#      no existe; construir el Path no falla, el error llega al abrirlo
#      (FileNotFoundError): error tardío.
# Reescritura de SOLO la construcción de rutas:
#
#   base = Path(__file__).resolve().parent
#   sys.path.insert(0, str(base / "biblioteca"))
#   import Libreria
#   print(Libreria.velocidad(12, 3))
#   ruta = base / "datos" / "mediciones.csv"
#
# __file__ es la ruta de principal.py; resolve() la hace absoluta y
# parent da curso/. str(...) porque sys.path contiene cadenas.
# Caso: desde la carpeta superior, original -> ModuleNotFoundError;
# corregido -> imprime 4.0 y la ruta apunta al CSV real.
#
# PARTE 3: codigo.py corregido:
#
#   def velocidad(dx, dt):
#       return dx / dt
#
#   if __name__ == "__main__":
#       print("Demostración", velocidad(10, 2))
#
# Ejecutado directamente, __name__ vale "__main__" y la demo corre; al
# importarlo vale "Libreria.cinematica.codigo" y la demo no corre.
# Con la corrección, principal.py imprime solo 4.0.
#
# sys.path vs Libreria.__file__:
#   sys.path = lista de carpetas donde Python BUSCARÁ módulos (anterior
#   al import; explica por qué falla un import o qué carpeta gana).
#   Libreria.__file__ = archivo que Python REALMENTE cargó (existe solo
#   tras un import exitoso; confirma qué copia se cargó si hay varias).
#   Un paquete puede estar en sys.path y aun así no ser el cargado.

def velocidad_original(dx, dt):
    return dx / dt


def velocidad_corregida(dx, dt):
    return dx / dt


def ejercicio_6():
    import sys
    from pathlib import Path

    print("===== EJERCICIO 6 =====")
    print("\n--- Orden de salida del original (simulado) ---")
    print("Demostración", velocidad_original(10, 2))   # 5.0 (ocurre en el import)
    print(velocidad_original(12, 3))                   # 4.0

    print("\n--- Construcción de rutas ---")
    print("Relativa (depende de dónde se ejecute):")
    print("  ", Path("datos/mediciones.csv").resolve())
    base = Path(__file__).resolve().parent
    print("Basada en la ubicación del archivo (siempre igual):")
    print("  ", base / "datos" / "mediciones.csv")

    print("\n--- if __name__ == '__main__' ---")
    print("__name__ en este archivo:", __name__)
    print("Corregido: velocidad(10, 2) =", velocidad_corregida(10, 2))

    print("\n--- sys.path (dónde se BUSCA) vs __file__ (de dónde se CARGÓ) ---")
    for carpeta in sys.path[:3]:
        print("  sys.path:", carpeta)
    print("  __file__:", __file__)


# =====================================================================
# EJERCICIO 7: Revisar un lector que oculta datos defectuosos
# =====================================================================
# Contrato: CSV con encabezado exacto tiempo_s,posicion_m; devolver lista
# de tuplas numéricas; rechazar encabezado incorrecto, filas con otra
# cantidad de campos, campos no numéricos o ausencia de mediciones.
#
# PREDICCIÓN con el archivo del enunciado:
#   tiempo_s,posicion_m
#   0,2
#   1,error
#   2,8,extra
# Línea 1: readline() la descarta, nunca se compara.
# Línea 2: (0.0, 2.0) se agrega.
# Línea 3: float("error") falla y "except Exception: pass" la traga.
# Línea 4: campos = ["2", "8", "extra"]; solo se usan los dos primeros,
#          se agrega (2.0, 8.0) y el tercer campo se ignora.
# Devuelve [(0.0, 2.0), (2.0, 8.0)].
# Se pierde: la fila 3 sin rastro; la fila 4 se ACEPTA aunque tiene 3
# campos; el encabezado nunca se verifica; no se sabe el número de la
# fila dañada; el resultado parece normal.
#
# RESULTADO REAL: [(0.0, 2.0), (2.0, 8.0)].  ¿Coincidió? Sí.
#
# CORRECCIÓN (leer_corregida): compara el encabezado; exige 2 campos
# ANTES de convertir; captura solo ValueError y lo relanza con el número
# de fila; lanza ValueError si no hay mediciones; no captura
# FileNotFoundError; no impone condiciones físicas.
#
# DOS ARCHIVOS QUE DISTINGUEN LAS VERSIONES:
#   A) solo "tiempo_s,posicion_m"
#      original: []   |  corregida: ValueError (sin mediciones)
#   B) "tiempo_s,posicion_m" y "1,error"
#      original: []   |  corregida: ValueError (fila 2: no numérico)
# ¿Por qué no devolver [] ante cualquier problema? Porque mezcla
# situaciones distintas (sin datos, encabezado mal, filas dañadas,
# campos de más): quien llama no puede decidir qué hacer; contradice el
# contrato (la ausencia de mediciones debe rechazarse); se pierde la
# ubicación del fallo; y el programa sigue con datos vacíos o
# incompletos y falla lejos de la causa o da resultados incorrectos.

def leer_original(ruta):
    filas = []
    with ruta.open(encoding="utf-8") as archivo:
        archivo.readline()
        for numero, linea in enumerate(archivo, start=2):
            campos = linea.strip().split(",")
            try:
                filas.append((float(campos[0]), float(campos[1])))
            except Exception:
                pass
    return filas


def leer_corregida(ruta):
    encabezado_esperado = "tiempo_s,posicion_m"
    filas = []
    with ruta.open(encoding="utf-8") as archivo:
        encabezado = archivo.readline().rstrip("\r\n")
        if encabezado != encabezado_esperado:
            raise ValueError("encabezado incorrecto: " + repr(encabezado))

        for numero, linea in enumerate(archivo, start=2):
            contenido = linea.rstrip("\r\n")
            campos = contenido.split(",")

            if len(campos) != 2:
                raise ValueError("fila " + str(numero)
                                 + ": se esperaban 2 campos y hay "
                                 + str(len(campos)))
            try:
                tiempo = float(campos[0])
                posicion = float(campos[1])
            except ValueError as error:
                raise ValueError("fila " + str(numero)
                                 + ": campo no numérico ("
                                 + repr(contenido) + ")") from error
            filas.append((tiempo, posicion))

    if not filas:
        raise ValueError("el archivo no contiene mediciones")
    return filas


def _probar(nombre, funcion, ruta):
    try:
        print(nombre, funcion(ruta))
    except ValueError as error:
        print(nombre, "ValueError:", error)
    except FileNotFoundError:
        print(nombre, "FileNotFoundError (se propaga, no se captura)")


def ejercicio_7():
    import tempfile
    from pathlib import Path

    print("===== EJERCICIO 7 =====")
    casos = [
        ("Archivo del enunciado",
         "tiempo_s,posicion_m\n0,2\n1,error\n2,8,extra\n"),
        ("Archivo A: solo encabezado",
         "tiempo_s,posicion_m\n"),
        ("Archivo B: una fila con texto",
         "tiempo_s,posicion_m\n1,error\n"),
        ("Adicional: campos extra",
         "tiempo_s,posicion_m\n0,2\n2,8,extra\n"),
        ("Adicional: encabezado incorrecto",
         "t,x\n0,2\n"),
        ("Adicional: archivo válido",
         "tiempo_s,posicion_m\n0,2\n1,5\n"),
    ]

    with tempfile.TemporaryDirectory() as carpeta:
        for indice, (titulo, contenido) in enumerate(casos):
            ruta = Path(carpeta) / ("caso" + str(indice) + ".csv")
            ruta.write_text(contenido, encoding="utf-8", newline="\n")
            print("\n--- " + titulo + " ---")
            _probar("original :", leer_original, ruta)
            _probar("corregida:", leer_corregida, ruta)

        print("\n--- Archivo que no existe ---")
        ruta = Path(carpeta) / "no_existe.csv"
        _probar("original :", leer_original, ruta)
        _probar("corregida:", leer_corregida, ruta)


# =====================================================================
# EJERCICIO 8: Algoritmo de puntos medios
# =====================================================================
# Especificación: ancho = (b - a) / n; centro i = a + (i + 0.5) * ancho;
# contribución = centro**2 * ancho; resultado = suma.
#
# PREDICCIÓN con a = 0, b = 2, n = 2 (ancho = 1.0):
#   CÓDIGO ORIGINAL (extremo izquierdo y reemplaza):
#     i = 0: centro = 0.0 | contribución = 0.0 | acumulado = 0.0
#     i = 1: centro = 1.0 | contribución = 1.0 | acumulado = 1.0
#     Devuelve 1.0
#   ALGORITMO ESPECIFICADO:
#     i = 0: centro = 0.5 | contribución = 0.25
#     i = 1: centro = 1.5 | contribución = 2.25
#     Suma = 2.5
# Errores del original: (1) valida DESPUÉS de dividir: con n = 0 sale
# ZeroDivisionError en vez de ValueError; (2) el centro usa a + i*ancho
# (extremo izquierdo), falta + 0.5; (3) "acumulado = ..." reemplaza en
# vez de sumar (+=).
#
# RESULTADO REAL: original 1.0, corregida 2.5.  ¿Coincidió? Sí.
#
# ¿Por qué arreglar solo el centro no basta? Con el centro corregido pero
# "acumulado = ..." se obtiene 2.25 (queda solo el último subintervalo):
# parece razonable pero falta la contribución 0.25. Además n = 0 seguiría
# dando ZeroDivisionError. Son tres defectos independientes.
#
# Caso válido: (0, 2, 2) -> original 1.0, corregida 2.5.
# Caso inválido: (0, 2, 0) -> original ZeroDivisionError, corregida
# ValueError.
# Aproximación vs. exacta: la integral exacta de x² en [0, 2] es 8/3 =
# 2.666...; 2.5 es una APROXIMACIÓN por puntos medios con 2
# subintervalos. La diferencia es propia del método, no un error de
# programación: el código se juzga contra el algoritmo especificado.

def integrar_cuadrado_original(a, b, n):
    ancho = (b - a) / n
    if n <= 0 or b <= a:
        raise ValueError("intervalo o partición inválidos")
    acumulado = 0.0
    for i in range(n):
        centro = a + i * ancho
        acumulado = centro**2 * ancho
    return acumulado


def integrar_cuadrado_corregida(a, b, n):
    """Aproxima la integral de x**2 entre a y b con n puntos medios.

    Contrato: n entero positivo y b > a; si no, lanza ValueError.
    """
    if n <= 0 or b <= a:
        raise ValueError("intervalo o partición inválidos")
    ancho = (b - a) / n
    acumulado = 0.0
    for i in range(n):
        centro = a + (i + 0.5) * ancho
        acumulado += centro**2 * ancho
    return acumulado


def _probar_integral(nombre, funcion, a, b, n):
    try:
        print(nombre, funcion(a, b, n))
    except (ValueError, ZeroDivisionError) as error:
        print(nombre, type(error).__name__ + ":", error)


def ejercicio_8():
    print("===== EJERCICIO 8 =====")
    a, b, n = 0, 2, 2
    ancho = (b - a) / n

    print("\n--- Contribuciones con a=0, b=2, n=2 (ancho =", ancho, ") ---")
    print("Original (extremo izquierdo, reemplaza):")
    for i in range(n):
        centro = a + i * ancho
        print("  i =", i, "| centro =", centro, "| contribución =", centro**2 * ancho)
    print("  Devuelve:", integrar_cuadrado_original(a, b, n))   # 1.0
    print("Especificado (centro real, suma):")
    suma = 0.0
    for i in range(n):
        centro = a + (i + 0.5) * ancho
        contribucion = centro**2 * ancho
        suma += contribucion
        print("  i =", i, "| centro =", centro, "| contribución =", contribucion)
    print("  Suma:", suma)                                      # 2.5

    print("\n--- Solo corregir el centro (sigue sin sumar) ---")
    parcial = 0.0
    for i in range(n):
        centro = a + (i + 0.5) * ancho
        parcial = centro**2 * ancho
    print("Centro corregido pero sin +=:", parcial)             # 2.25 (incorrecto)

    print("\n--- Caso válido (0, 2, 2) ---")
    _probar_integral("original :", integrar_cuadrado_original, 0, 2, 2)
    _probar_integral("corregida:", integrar_cuadrado_corregida, 0, 2, 2)

    print("\n--- Caso inválido (0, 2, 0) ---")
    _probar_integral("original :", integrar_cuadrado_original, 0, 2, 0)
    _probar_integral("corregida:", integrar_cuadrado_corregida, 0, 2, 0)

    print("\n--- Aproximación vs. integral exacta ---")
    exacta = 2**3 / 3
    aproximada = integrar_cuadrado_corregida(0, 2, 2)
    print("Aproximación por puntos medios:", aproximada)
    print("Integral exacta (8/3):         ", exacta)
    print("Diferencia:                    ", exacta - aproximada)


# =====================================================================
# EJERCICIO 9: Entorno, terminal y Git: diagnóstico de una secuencia
# =====================================================================
# Secuencia (Bash en Linux/WSL):
#   python3 -m venv .venv
#   source .venv/bin/activate
#   python programa.py
#
# Línea 1: python3 -m venv .venv  -> CREA la carpeta .venv (copia o
#   enlace al intérprete, site-packages propia y el script de activación).
#   Solo crea: no cambia la terminal ni el python en uso.
# Línea 2: source .venv/bin/activate -> ejecuta el script EN LA SHELL
#   ACTUAL (por eso source): antepone .venv/bin al PATH, define
#   VIRTUAL_ENV y cambia el prompt a (.venv). Desde ahí "python" y "pip"
#   son los del entorno.
# Línea 3: python programa.py -> ejecuta programa.py con el python que
#   resuelve el PATH, o sea el del entorno.
# Crear NO equivale a activar: crear produce archivos en disco; activar
# cambia variables de la sesión de la terminal. Sin activar, "python"
# sigue siendo el del sistema. La activación dura solo en esa terminal.
#
# ¿Borrar .venv borra programa.py? NO. Estructura:
#   proyecto/
#   ├── programa.py   <- junto a .venv, no dentro
#   └── .venv/        <- solo se borra lo que está dentro de esta carpeta
# Se pierden únicamente los paquetes del entorno, que se recrea con los
# mismos comandos.
#
# git add respuestas.md
# (se modifica de nuevo respuestas.md)
# git commit -m "Respuestas"
# Entra SOLO la PRIMERA versión: git add copia al área de preparación
# (staging) el contenido de ese momento, y el commit guarda lo preparado,
# no lo que hay en el directorio de trabajo. La modificación posterior
# queda sin preparar (git status la muestra en "Changes not staged").
# Para incluirla en un NUEVO commit:
#   git add respuestas.md
#   git commit -m "Actualiza respuestas"
#
# Guardar, commit y subir son tres cosas distintas:
#   Guardar un archivo (Ctrl+S): escribe en el disco local.
#   Crear un commit (git add + git commit): registra una instantánea en
#     el historial del repositorio LOCAL.
#   Subir a GitHub (git push): envía los commits locales al remoto.
# Ver cambios pendientes:  git status   (y git diff para las líneas)
# Enviar commits al remoto (rama con seguimiento ya configurado):
#   git push

def ejercicio_9():
    print("===== EJERCICIO 9 =====")
    print("Ejercicio de terminal y Git; las respuestas están en los comentarios.")
    print("\n--- Entorno virtual ---")
    print("python3 -m venv .venv        -> CREA la carpeta .venv")
    print("source .venv/bin/activate    -> ACTIVA el entorno en esta terminal")
    print("python programa.py           -> usa el python del entorno")
    print("Borrar .venv NO borra programa.py (está al lado, no dentro).")
    print("\n--- git add y modificación posterior ---")
    print("Entra en el commit solo la versión que se agregó con git add.")
    print("Para incluir la posterior: git add respuestas.md")
    print('                           git commit -m "Actualiza respuestas"')
    print("\n--- Guardar, commit y subir ---")
    print("Guardar archivo  -> disco local (Ctrl+S)")
    print("Crear commit     -> historial local (git add + git commit)")
    print("Subir a GitHub   -> repositorio remoto (git push)")
    print("Ver pendientes   : git status")
    print("Enviar al remoto : git push")


# =====================================================================
# EJECUCIÓN (único bloque principal, siempre al final del archivo)
# =====================================================================
if __name__ == "__main__":
    opcion = input("¿Qué ejercicio quieres ejecutar? (1 a 9): ")
    if opcion == "1":
        promedio_mediciones()
    elif opcion == "2":
        ejercicio_2()
    elif opcion == "3":
        ejercicio_3()
    elif opcion == "4":
        ejercicio_4()
    elif opcion == "5":
        ejercicio_5()
    elif opcion == "6":
        ejercicio_6()
    elif opcion == "7":
        ejercicio_7()
    elif opcion == "8":
        ejercicio_8()
    elif opcion == "9":
        ejercicio_9()
    else:
        print("Opción no válida.")
        