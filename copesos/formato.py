# copesos/formato.py
from datetime import date, timedelta


# ─── Tablas de referencia ─────────────────────────────────────────────────────

# Salario Mínimo Mensual Legal Vigente (SMMLV) por año
_SMMLV = {
    2021: 908_526,
    2022: 1_000_000,
    2023: 1_160_000,
    2024: 1_300_000,
    2025: 1_423_500,
    2026: 1_750_905,   # Decretos 1469 y 1470 del 29 de diciembre de 2025
}

# Auxilio de transporte por año
_AUXILIO_TRANSPORTE = {
    2021: 106_454,
    2022: 117_172,
    2023: 140_606,
    2024: 162_000,
    2025: 200_000,
    2026: 249_095,     # Decretos 1469 y 1470 del 29 de diciembre de 2025
}

# Unidad de Valor Tributario (UVT) por año
_UVT = {
    2021: 36_308,
    2022: 38_004,
    2023: 42_412,
    2024: 47_065,
    2025: 49_799,
    2026: 52_374,      # Resolución 000238 del 15 de diciembre de 2025 - DIAN
}


# ─── Funciones originales ─────────────────────────────────────────────────────


def formatear_pesos(valor):
    """
    Convierte un número a formato de pesos colombianos.
    Ejemplo: 1250000 -> '$1.250.000'
    """
    return "${:,.0f}".format(valor).replace(",", ".")


def formatear_fecha(fecha):
    """
    Formatea una fecha en español colombiano.
    Recibe un objeto datetime.date
    Ejemplo: date(2026, 3, 27) -> 'viernes 27 de marzo de 2026'
    """
    dias = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
    meses = [
        "enero", "febrero", "marzo", "abril", "mayo", "junio",
        "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
    ]
    dia_semana = dias[fecha.weekday()]
    mes = meses[fecha.month - 1]
    return f"{dia_semana} {fecha.day} de {mes} de {fecha.year}"


def calcular_porcentaje(valor, total):
    """
    Calcula el porcentaje de valor sobre total.
    Ejemplo: calcular_porcentaje(250, 1000) -> 25.0
    """
    if total == 0:
        return 0.0
    return round((valor / total) * 100, 2)


def validar_cedula(cedula):
    """
    Valida si una cédula colombiana tiene formato correcto.
    Debe ser un número entre 6 y 10 dígitos.
    Retorna True o False.
    """
    cedula_str = str(cedula).strip()
    return cedula_str.isdigit() and 6 <= len(cedula_str) <= 10


# ─── Formato y validación ─────────────────────────────────────────────────────


def calcular_iva(valor, porcentaje=19):
    """
    Calcula el IVA sobre un valor base.
    Retorna un diccionario con base, iva y total.
    El porcentaje por defecto es 19% (tarifa general colombiana).
    También existen tarifas del 5% y del 0%.
    Ejemplo: calcular_iva(100000) -> {'base': 100000, 'porcentaje': 19, 'iva': 19000.0, 'total': 119000.0}
    """
    iva = round(valor * porcentaje / 100, 2)
    total = round(valor + iva, 2)
    return {
        "base": valor,
        "porcentaje": porcentaje,
        "iva": iva,
        "total": total
    }


def formatear_celular(numero):
    """
    Formatea un número de celular colombiano al estándar internacional.
    Acepta 10 dígitos que empiecen por 3.
    Ejemplo: 3001234567 -> '+57 300 123 4567'
    Retorna None si el número no tiene formato válido.
    """
    numero_str = str(numero).strip().replace(" ", "").replace("-", "")
    if not numero_str.isdigit():
        return None
    if len(numero_str) == 10 and numero_str.startswith("3"):
        return f"+57 {numero_str[:3]} {numero_str[3:6]} {numero_str[6:]}"
    return None


def validar_nit(nit):
    """
    Valida un NIT colombiano verificando su dígito de verificación.
    Acepta el NIT completo con el dígito al final (con o sin guion).
    Ejemplo: validar_nit('8001972684') -> True
             validar_nit('900123456-0') -> True o False
    """
    nit_str = str(nit).strip().replace(".", "").replace(" ", "").replace("-", "")
    if not nit_str.isdigit() or len(nit_str) < 2:
        return False

    cuerpo = nit_str[:-1]
    digito_esperado = int(nit_str[-1])

    multiplicadores = [3, 7, 13, 17, 19, 23, 29, 37, 41, 43, 47, 53, 59, 67, 71]
    factores = multiplicadores[:len(cuerpo)]

    suma = sum(int(d) * m for d, m in zip(reversed(cuerpo), factores))
    residuo = suma % 11

    digito_calculado = residuo if residuo < 2 else 11 - residuo
    return digito_esperado == digito_calculado


def validar_tarjeta_identidad(ti):
    """
    Valida si una Tarjeta de Identidad colombiana tiene formato correcto.
    Debe ser numérica y entre 8 y 11 dígitos.
    Retorna True o False.
    Ejemplo: validar_tarjeta_identidad('1020304050') -> True
    """
    ti_str = str(ti).strip()
    return ti_str.isdigit() and 8 <= len(ti_str) <= 11


def validar_placa(placa):
    """
    Valida si una placa colombiana tiene formato correcto.
    Carros:  ABC-123  (3 letras + 3 números)
    Motos:   ABC-12D  (3 letras + 2 números + 1 letra)
    Retorna True o False.
    Ejemplo: validar_placa('ABC123') -> True
             validar_placa('ABC12D') -> True
    """
    placa_str = str(placa).strip().upper().replace("-", "").replace(" ", "")
    if len(placa_str) != 6:
        return False
    letras = placa_str[:3]
    medio = placa_str[3:5]
    ultimo = placa_str[5]
    if not letras.isalpha():
        return False
    if not medio.isdigit():
        return False
    # Carro: último es dígito. Moto: último es letra.
    return ultimo.isdigit() or ultimo.isalpha()


def tipo_documento(codigo):
    """
    Traduce el código de tipo de documento colombiano a su nombre completo.
    Retorna None si el código no se reconoce.
    Ejemplo: tipo_documento('CC') -> 'Cédula de Ciudadanía'
    """
    tipos = {
        "CC":  "Cédula de Ciudadanía",
        "TI":  "Tarjeta de Identidad",
        "CE":  "Cédula de Extranjería",
        "NIT": "Número de Identificación Tributaria",
        "PEP": "Permiso Especial de Permanencia",
        "PPT": "Permiso de Protección Temporal",
        "PA":  "Pasaporte",
        "RC":  "Registro Civil",
        "MS":  "Menor sin identificación",
    }
    return tipos.get(str(codigo).strip().upper())


def slugify_colombiano(texto):
    """
    Convierte texto en español (con tildes y caracteres especiales) a slug URL-safe.
    Útil para generar IDs, URLs o nombres de archivo desde texto colombiano.
    Ejemplo: slugify_colombiano('Bogotá D.C.') -> 'bogota-dc'
             slugify_colombiano('Ñoño & Compañía') -> 'nono-compania'
    """
    reemplazos = {
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
        'Á': 'a', 'É': 'e', 'Í': 'i', 'Ó': 'o', 'Ú': 'u',
        'ü': 'u', 'Ü': 'u', 'ñ': 'n', 'Ñ': 'n',
    }
    resultado = texto.lower()
    for car, rep in reemplazos.items():
        resultado = resultado.replace(car, rep)
    slug = ''
    ultimo_guion = False
    for c in resultado:
        if c.isalnum():
            slug += c
            ultimo_guion = False
        elif not ultimo_guion:
            slug += '-'
            ultimo_guion = True
    return slug.strip('-')


# ─── Tributario ───────────────────────────────────────────────────────────────


def calcular_retefuente(valor, tarifa):
    """
    Calcula la retención en la fuente sobre un valor.
    La tarifa se expresa en porcentaje (ej: 3.5 para el 3.5%).
    Las tarifas más comunes: compras 2.5%, servicios 4%, honorarios 10-11%.
    Retorna un diccionario con base, tarifa, retencion y neto a pagar.
    Ejemplo: calcular_retefuente(1000000, 3.5) -> {...}
    """
    retencion = round(valor * tarifa / 100, 2)
    neto = round(valor - retencion, 2)
    return {
        "base": valor,
        "tarifa_pct": tarifa,
        "retencion": retencion,
        "neto": neto
    }


def calcular_reteica(valor, tarifa_por_mil):
    """
    Calcula la retención ICA sobre un valor.
    La tarifa se expresa en pesos por cada mil (‰), varía por municipio y actividad.
    Ejemplos Bogotá: comercio 4.14‰, servicios 9.66‰, industria 4.14‰.
    Retorna un diccionario con base, tarifa, reteica y neto a pagar.
    Ejemplo: calcular_reteica(1000000, 4.14) -> {...}
    """
    reteica = round(valor * tarifa_por_mil / 1000, 2)
    neto = round(valor - reteica, 2)
    return {
        "base": valor,
        "tarifa_por_mil": tarifa_por_mil,
        "reteica": reteica,
        "neto": neto
    }


def uvt_a_pesos(uvts, año=2025):
    """
    Convierte UVTs (Unidades de Valor Tributario) a pesos colombianos.
    La DIAN actualiza el valor de la UVT cada año.
    Retorna None si el año no está en la tabla.
    Ejemplo: uvt_a_pesos(1090, 2025) -> 54,280,910
    """
    valor_uvt = _UVT.get(año)
    if valor_uvt is None:
        return None
    return round(uvts * valor_uvt, 2)


# ─── Laboral / Nómina ─────────────────────────────────────────────────────────


def es_salario_minimo(salario, año=2025):
    """
    Verifica si un salario es mayor o igual al SMMLV del año indicado.
    Retorna True, False, o None si el año no está en la tabla.
    Ejemplo: es_salario_minimo(1300000, 2025) -> False
             es_salario_minimo(1500000, 2025) -> True
    """
    smmlv = _SMMLV.get(año)
    if smmlv is None:
        return None
    return salario >= smmlv


def calcular_subsidio_transporte(salario, año=2025):
    """
    Calcula el auxilio de transporte al que tiene derecho un trabajador.
    Aplica si el salario es menor o igual a 2 SMMLV.
    Retorna el valor del auxilio, o 0 si no aplica.
    Ejemplo: calcular_subsidio_transporte(1423500, 2025) -> 200000
             calcular_subsidio_transporte(3000000, 2025) -> 0
    """
    smmlv = _SMMLV.get(año)
    auxilio = _AUXILIO_TRANSPORTE.get(año)
    if smmlv is None or auxilio is None:
        return None
    return auxilio if salario <= smmlv * 2 else 0


def calcular_prestaciones(salario, dias, año=2025):
    """
    Calcula las prestaciones sociales de un trabajador colombiano.
    Incluye auxilio de transporte si aplica.
    - dias: número de días trabajados (usa 360 para un año completo)
    Retorna un diccionario con cada prestación y el total.
    Ejemplo: calcular_prestaciones(1423500, 360, 2025) -> {...}
    """
    auxilio = calcular_subsidio_transporte(salario, año) or 0
    base_cesantias = salario + auxilio

    cesantias = round(base_cesantias * dias / 360, 2)
    intereses_cesantias = round(cesantias * 0.12 * dias / 360, 2)
    prima = round(base_cesantias * dias / 360, 2)
    vacaciones = round(salario * dias / 720, 2)

    total = round(cesantias + intereses_cesantias + prima + vacaciones, 2)

    return {
        "salario": salario,
        "auxilio_transporte": auxilio,
        "dias": dias,
        "cesantias": cesantias,
        "intereses_cesantias": intereses_cesantias,
        "prima": prima,
        "vacaciones": vacaciones,
        "total": total
    }


# ─── Fechas y festivos ────────────────────────────────────────────────────────


def _calcular_pascua(año):
    """Calcula la fecha del Domingo de Pascua usando el algoritmo de Meeus."""
    a = año % 19
    b = año // 100
    c = año % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    mes = (h + l - 7 * m + 114) // 31
    dia = ((h + l - 7 * m + 114) % 31) + 1
    return date(año, mes, dia)


def _siguiente_lunes(fecha):
    """Si la fecha no es lunes, devuelve el lunes siguiente (Ley Emiliani)."""
    dias_hasta_lunes = (7 - fecha.weekday()) % 7
    if dias_hasta_lunes == 0:
        return fecha
    return fecha + timedelta(days=dias_hasta_lunes)


def festivos_del_año(año):
    """
    Devuelve la lista completa de fechas festivas en Colombia para un año dado.
    Incluye festivos fijos, Ley Emiliani y festivos religiosos móviles.
    Ejemplo: festivos_del_año(2026) -> [date(2026, 1, 1), date(2026, 1, 12), ...]
    """
    pascua = _calcular_pascua(año)

    fijos = [
        date(año, 1, 1),
        date(año, 5, 1),
        date(año, 7, 20),
        date(año, 8, 7),
        date(año, 12, 8),
        date(año, 12, 25),
    ]

    emiliani = [
        date(año, 1, 6),
        date(año, 3, 19),
        date(año, 6, 29),
        date(año, 8, 15),
        date(año, 10, 12),
        date(año, 11, 1),
        date(año, 11, 11),
    ]
    trasladados = [_siguiente_lunes(d) for d in emiliani]

    moviles = [
        pascua - timedelta(days=3),
        pascua - timedelta(days=2),
        _siguiente_lunes(pascua + timedelta(days=39)),
        _siguiente_lunes(pascua + timedelta(days=60)),
        _siguiente_lunes(pascua + timedelta(days=68)),
    ]

    todos = sorted(set(fijos + trasladados + moviles))
    return todos


def es_festivo(fecha):
    """
    Indica si una fecha es festivo en Colombia.
    Retorna True o False.
    Ejemplo: es_festivo(date(2026, 1, 1)) -> True
    """
    return fecha in festivos_del_año(fecha.year)


def dias_habiles(fecha_inicio, fecha_fin):
    """
    Cuenta los días hábiles entre dos fechas (inclusive en ambos extremos).
    Excluye sábados, domingos y festivos colombianos.
    Ejemplo: dias_habiles(date(2026, 4, 1), date(2026, 4, 10)) -> 6
    """
    festivos = set(festivos_del_año(fecha_inicio.year))
    if fecha_fin.year != fecha_inicio.year:
        festivos |= set(festivos_del_año(fecha_fin.year))

    contador = 0
    actual = fecha_inicio
    while actual <= fecha_fin:
        if actual.weekday() < 5 and actual not in festivos:
            contador += 1
        actual += timedelta(days=1)
    return contador


def siguiente_dia_habil(fecha):
    """
    Devuelve el siguiente día hábil después de una fecha dada.
    Útil para calcular vencimientos y plazos.
    Ejemplo: siguiente_dia_habil(date(2026, 4, 3)) -> date(2026, 4, 6)
    """
    siguiente = fecha + timedelta(days=1)
    festivos = set(festivos_del_año(siguiente.year))
    while siguiente.weekday() >= 5 or siguiente in festivos:
        siguiente += timedelta(days=1)
        if siguiente.year != fecha.year:
            festivos |= set(festivos_del_año(siguiente.year))
    return siguiente


# ─── Texto ────────────────────────────────────────────────────────────────────


def numero_a_letras(numero):
    """
    Convierte un número entero a su representación en palabras en español.
    Útil para contratos, cheques y facturas.
    Soporta números hasta 999.999.999.999.
    Ejemplo: numero_a_letras(1500000) -> 'un millón quinientos mil'
    """
    unidades = [
        "", "uno", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho", "nueve",
        "diez", "once", "doce", "trece", "catorce", "quince", "dieciséis",
        "diecisiete", "dieciocho", "diecinueve"
    ]
    decenas = [
        "", "diez", "veinte", "treinta", "cuarenta",
        "cincuenta", "sesenta", "setenta", "ochenta", "noventa"
    ]
    centenas = [
        "", "cien", "doscientos", "trescientos", "cuatrocientos", "quinientos",
        "seiscientos", "setecientos", "ochocientos", "novecientos"
    ]

    def menos_de_mil(n):
        if n == 0:
            return ""
        if n < 20:
            return unidades[n]
        if n < 30:
            return "veinte" if n == 20 else "veinti" + unidades[n - 20]
        if n < 100:
            d, u = divmod(n, 10)
            return decenas[d] if u == 0 else decenas[d] + " y " + unidades[u]
        c, resto = divmod(n, 100)
        if n == 100:
            return "cien"
        return centenas[c] if resto == 0 else centenas[c] + " " + menos_de_mil(resto)

    def convertir(n):
        if n == 0:
            return "cero"
        if n < 1000:
            return menos_de_mil(n)
        if n < 1_000_000:
            miles, resto = divmod(n, 1000)
            prefijo = "mil" if miles == 1 else menos_de_mil(miles) + " mil"
            return prefijo if resto == 0 else prefijo + " " + menos_de_mil(resto)
        if n < 1_000_000_000:
            millones, resto = divmod(n, 1_000_000)
            prefijo = "un millón" if millones == 1 else menos_de_mil(millones) + " millones"
            return prefijo if resto == 0 else prefijo + " " + convertir(resto)
        miles_m, resto = divmod(n, 1_000_000_000)
        prefijo = "mil millones" if miles_m == 1 else menos_de_mil(miles_m) + " mil millones"
        return prefijo if resto == 0 else prefijo + " " + convertir(resto)

    negativo = numero < 0
    resultado = convertir(abs(int(numero)))
    return "menos " + resultado if negativo else resultado


def numero_a_letras_pesos(valor):
    """
    Convierte un valor a letras en formato de contrato colombiano.
    Ejemplo: numero_a_letras_pesos(1500000) -> 'UN MILLÓN QUINIENTOS MIL PESOS M/CTE'
    """
    return f"{numero_a_letras(int(valor))} pesos M/CTE".upper()
