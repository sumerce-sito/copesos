# tests/test_formato.py
import pytest
from datetime import date
from copesos import (
    formatear_pesos, formatear_fecha, formatear_celular,
    calcular_porcentaje, calcular_iva, calcular_retefuente, calcular_reteica, uvt_a_pesos,
    validar_cedula, validar_nit, validar_tarjeta_identidad, validar_placa, tipo_documento,
    es_salario_minimo, calcular_subsidio_transporte, calcular_prestaciones,
    festivos_del_año, es_festivo, dias_habiles, siguiente_dia_habil,
    numero_a_letras, numero_a_letras_pesos, slugify_colombiano,
)


# ── formatear_pesos ───────────────────────────────────────────────────────────

def test_formatear_pesos_millon():
    assert formatear_pesos(1250000) == "$1.250.000"

def test_formatear_pesos_pequeno():
    assert formatear_pesos(500) == "$500"

def test_formatear_pesos_cero():
    assert formatear_pesos(0) == "$0"


# ── formatear_fecha ───────────────────────────────────────────────────────────

def test_formatear_fecha_viernes():
    assert formatear_fecha(date(2026, 3, 27)) == "viernes 27 de marzo de 2026"

def test_formatear_fecha_lunes():
    assert formatear_fecha(date(2026, 1, 1)) == "jueves 1 de enero de 2026"


# ── formatear_celular ─────────────────────────────────────────────────────────

def test_formatear_celular_valido():
    assert formatear_celular(3001234567) == "+57 300 123 4567"

def test_formatear_celular_corto():
    assert formatear_celular(123) is None

def test_formatear_celular_no_empieza_en_3():
    assert formatear_celular(1234567890) is None

def test_formatear_celular_texto():
    assert formatear_celular("abc") is None


# ── calcular_porcentaje ───────────────────────────────────────────────────────

def test_calcular_porcentaje_normal():
    assert calcular_porcentaje(250, 1000) == 25.0

def test_calcular_porcentaje_total_cero():
    assert calcular_porcentaje(100, 0) == 0.0

def test_calcular_porcentaje_decimales():
    assert calcular_porcentaje(1, 3) == 33.33


# ── calcular_iva ──────────────────────────────────────────────────────────────

def test_calcular_iva_19():
    resultado = calcular_iva(100000)
    assert resultado["iva"] == 19000.0
    assert resultado["total"] == 119000.0

def test_calcular_iva_5():
    resultado = calcular_iva(50000, 5)
    assert resultado["iva"] == 2500.0
    assert resultado["total"] == 52500.0

def test_calcular_iva_0():
    resultado = calcular_iva(100000, 0)
    assert resultado["iva"] == 0.0
    assert resultado["total"] == 100000.0


# ── calcular_retefuente ───────────────────────────────────────────────────────

def test_calcular_retefuente():
    resultado = calcular_retefuente(1000000, 3.5)
    assert resultado["retencion"] == 35000.0
    assert resultado["neto"] == 965000.0


# ── calcular_reteica ──────────────────────────────────────────────────────────

def test_calcular_reteica():
    resultado = calcular_reteica(1000000, 4.14)
    assert resultado["reteica"] == 4140.0
    assert resultado["neto"] == 995860.0


# ── uvt_a_pesos ───────────────────────────────────────────────────────────────

def test_uvt_a_pesos_2026():
    assert uvt_a_pesos(1, 2026) == 52374.0

def test_uvt_a_pesos_año_invalido():
    assert uvt_a_pesos(100, 1990) is None


# ── validar_cedula ────────────────────────────────────────────────────────────

def test_validar_cedula_valida():
    assert validar_cedula(1234567890) is True

def test_validar_cedula_corta():
    assert validar_cedula(123) is False

def test_validar_cedula_texto():
    assert validar_cedula("abc") is False

def test_validar_cedula_limite_inferior():
    assert validar_cedula(123456) is True   # 6 dígitos: mínimo válido

def test_validar_cedula_limite_superior():
    assert validar_cedula(12345678901) is False  # 11 dígitos: fuera de rango


# ── validar_nit ───────────────────────────────────────────────────────────────

def test_validar_nit_valido():
    assert validar_nit("8001972684") is True   # NIT de la DIAN

def test_validar_nit_invalido():
    assert validar_nit("123456789") is False

def test_validar_nit_con_guion():
    assert validar_nit("800197268-4") is True


# ── validar_tarjeta_identidad ─────────────────────────────────────────────────

def test_validar_ti_valida():
    assert validar_tarjeta_identidad("1020304050") is True

def test_validar_ti_corta():
    assert validar_tarjeta_identidad("123") is False

def test_validar_ti_texto():
    assert validar_tarjeta_identidad("abcdefgh") is False


# ── validar_placa ─────────────────────────────────────────────────────────────

def test_validar_placa_carro():
    assert validar_placa("ABC123") is True

def test_validar_placa_moto():
    assert validar_placa("ABC12D") is True

def test_validar_placa_con_guion():
    assert validar_placa("ABC-123") is True

def test_validar_placa_invalida():
    assert validar_placa("12ABC3") is False

def test_validar_placa_corta():
    assert validar_placa("AB12") is False


# ── tipo_documento ────────────────────────────────────────────────────────────

def test_tipo_documento_cc():
    assert tipo_documento("CC") == "Cédula de Ciudadanía"

def test_tipo_documento_nit():
    assert tipo_documento("NIT") == "Número de Identificación Tributaria"

def test_tipo_documento_minuscula():
    assert tipo_documento("cc") == "Cédula de Ciudadanía"

def test_tipo_documento_desconocido():
    assert tipo_documento("XX") is None


# ── es_salario_minimo ─────────────────────────────────────────────────────────

def test_es_salario_minimo_exacto():
    assert es_salario_minimo(1750905, 2026) is True

def test_es_salario_minimo_bajo():
    assert es_salario_minimo(1500000, 2026) is False

def test_es_salario_minimo_año_invalido():
    assert es_salario_minimo(2000000, 1990) is None


# ── calcular_subsidio_transporte ──────────────────────────────────────────────

def test_subsidio_aplica():
    assert calcular_subsidio_transporte(1750905, 2026) == 249095

def test_subsidio_no_aplica():
    assert calcular_subsidio_transporte(4000000, 2026) == 0

def test_subsidio_año_invalido():
    assert calcular_subsidio_transporte(1750905, 1990) is None


# ── calcular_prestaciones ─────────────────────────────────────────────────────

def test_calcular_prestaciones_salario_minimo():
    resultado = calcular_prestaciones(1750905, 360, 2026)
    assert resultado["cesantias"] == 2000000.0
    assert resultado["prima"] == 2000000.0
    assert resultado["auxilio_transporte"] == 249095

def test_calcular_prestaciones_sin_auxilio():
    resultado = calcular_prestaciones(5000000, 360, 2026)
    assert resultado["auxilio_transporte"] == 0


# ── es_festivo ────────────────────────────────────────────────────────────────

def test_es_festivo_año_nuevo():
    assert es_festivo(date(2026, 1, 1)) is True

def test_es_festivo_viernes_santo():
    assert es_festivo(date(2026, 4, 3)) is True   # Viernes Santo 2026

def test_es_festivo_dia_normal():
    assert es_festivo(date(2026, 3, 27)) is False

def test_es_festivo_independencia():
    assert es_festivo(date(2026, 7, 20)) is True

def test_es_festivo_navidad():
    assert es_festivo(date(2026, 12, 25)) is True


# ── festivos_del_año ──────────────────────────────────────────────────────────

def test_festivos_del_año_cantidad():
    assert len(festivos_del_año(2026)) == 18

def test_festivos_del_año_es_lista_de_fechas():
    festivos = festivos_del_año(2026)
    assert all(isinstance(f, date) for f in festivos)

def test_festivos_del_año_ordenados():
    festivos = festivos_del_año(2026)
    assert festivos == sorted(festivos)


# ── dias_habiles ──────────────────────────────────────────────────────────────

def test_dias_habiles_semana_normal():
    # Lunes a viernes sin festivos
    assert dias_habiles(date(2026, 3, 2), date(2026, 3, 6)) == 5

def test_dias_habiles_con_festivo():
    # Del 1 al 10 de abril: incluye Jueves Santo (2) y Viernes Santo (3)
    assert dias_habiles(date(2026, 4, 1), date(2026, 4, 10)) == 6


# ── siguiente_dia_habil ───────────────────────────────────────────────────────

def test_siguiente_dia_habil_desde_festivo():
    # Viernes Santo -> lunes siguiente
    assert siguiente_dia_habil(date(2026, 4, 3)) == date(2026, 4, 6)

def test_siguiente_dia_habil_desde_viernes():
    # Viernes normal -> lunes (semana sin festivos)
    assert siguiente_dia_habil(date(2026, 3, 13)) == date(2026, 3, 16)


# ── numero_a_letras ───────────────────────────────────────────────────────────

def test_numero_a_letras_cero():
    assert numero_a_letras(0) == "cero"

def test_numero_a_letras_simple():
    assert numero_a_letras(15) == "quince"

def test_numero_a_letras_cien():
    assert numero_a_letras(100) == "cien"

def test_numero_a_letras_miles():
    assert numero_a_letras(1500) == "mil quinientos"

def test_numero_a_letras_millones():
    assert numero_a_letras(1500000) == "un millón quinientos mil"

def test_numero_a_letras_negativo():
    assert numero_a_letras(-5) == "menos cinco"


# ── numero_a_letras_pesos ─────────────────────────────────────────────────────

def test_numero_a_letras_pesos():
    assert numero_a_letras_pesos(1500000) == "UN MILLÓN QUINIENTOS MIL PESOS M/CTE"


# ── slugify_colombiano ────────────────────────────────────────────────────────

def test_slugify_con_tildes():
    assert slugify_colombiano("Bogotá") == "bogota"

def test_slugify_con_enie():
    assert slugify_colombiano("Compañía") == "compania"

def test_slugify_con_espacios_y_simbolos():
    assert slugify_colombiano("Ñoño & Compañía") == "nono-compania"
