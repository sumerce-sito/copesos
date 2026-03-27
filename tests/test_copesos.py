# tests/test_copesos.py
from datetime import date
from copesos import (
    formatear_pesos, formatear_fecha, formatear_celular,
    calcular_porcentaje, calcular_iva, calcular_retefuente, calcular_reteica, uvt_a_pesos,
    validar_cedula, validar_nit, validar_tarjeta_identidad, validar_placa, tipo_documento,
    es_salario_minimo, calcular_subsidio_transporte, calcular_prestaciones,
    festivos_del_año, es_festivo, dias_habiles, siguiente_dia_habil,
    numero_a_letras, numero_a_letras_pesos, slugify_colombiano,
)

print("=== Probando copesos ===\n")

# ── Formato ───────────────────────────────────────────────────────────────────
print("--- Formato ---")
print("formatear_pesos(1250000)      ->", formatear_pesos(1250000))
print("formatear_fecha(hoy)          ->", formatear_fecha(date.today()))
print("formatear_celular(3001234567) ->", formatear_celular(3001234567))
print("formatear_celular(123)        ->", formatear_celular(123))

# ── Cálculos ──────────────────────────────────────────────────────────────────
print("\n--- Cálculos ---")
print("calcular_porcentaje(250, 1000)       ->", calcular_porcentaje(250, 1000))
print("calcular_iva(100000)                 ->", calcular_iva(100000))
print("calcular_iva(50000, 5)               ->", calcular_iva(50000, 5))
print("calcular_retefuente(1000000, 3.5)    ->", calcular_retefuente(1000000, 3.5))
print("calcular_reteica(1000000, 4.14)      ->", calcular_reteica(1000000, 4.14))
print("uvt_a_pesos(1090, 2025)              ->", uvt_a_pesos(1090, 2025))

# ── Validaciones ──────────────────────────────────────────────────────────────
print("\n--- Validaciones ---")
print("validar_cedula(1234567890)    ->", validar_cedula(1234567890))
print("validar_cedula(123)           ->", validar_cedula(123))
print("validar_nit('8001972684')     ->", validar_nit('8001972684'))   # DIAN -> True
print("validar_nit('123456789')      ->", validar_nit('123456789'))    # invalido -> False
print("validar_tarjeta_identidad('1020304050') ->", validar_tarjeta_identidad('1020304050'))
print("validar_tarjeta_identidad('123')        ->", validar_tarjeta_identidad('123'))
print("validar_placa('ABC123')       ->", validar_placa('ABC123'))     # carro -> True
print("validar_placa('ABC12D')       ->", validar_placa('ABC12D'))     # moto  -> True
print("validar_placa('12ABC3')       ->", validar_placa('12ABC3'))     # invalida -> False
print("tipo_documento('CC')          ->", tipo_documento('CC'))
print("tipo_documento('NIT')         ->", tipo_documento('NIT'))
print("tipo_documento('XX')          ->", tipo_documento('XX'))

# ── Laboral ───────────────────────────────────────────────────────────────────
print("\n--- Laboral ---")
print("es_salario_minimo(1423500, 2025)           ->", es_salario_minimo(1423500, 2025))
print("es_salario_minimo(1000000, 2025)           ->", es_salario_minimo(1000000, 2025))
print("calcular_subsidio_transporte(1423500, 2025)->", calcular_subsidio_transporte(1423500, 2025))
print("calcular_subsidio_transporte(3000000, 2025)->", calcular_subsidio_transporte(3000000, 2025))
print("calcular_prestaciones(1423500, 360, 2025)  ->")
for k, v in calcular_prestaciones(1423500, 360, 2025).items():
    print(f"   {k}: {v}")

# ── Fechas y festivos ─────────────────────────────────────────────────────────
print("\n--- Fechas y festivos ---")
print("festivos_del_año(2026) ->")
for f in festivos_del_año(2026):
    print(f"   {f}  ({formatear_fecha(f)})")
print("es_festivo(date(2026, 1, 1))  ->", es_festivo(date(2026, 1, 1)))   # Año Nuevo -> True
print("es_festivo(date(2026, 4, 3))  ->", es_festivo(date(2026, 4, 3)))   # Viernes Santo -> True
print("es_festivo(date(2026, 3, 27)) ->", es_festivo(date(2026, 3, 27)))  # dia normal -> False
print("dias_habiles(date(2026,4,1), date(2026,4,10)) ->", dias_habiles(date(2026, 4, 1), date(2026, 4, 10)))
print("siguiente_dia_habil(date(2026,4,3)) ->", siguiente_dia_habil(date(2026, 4, 3)))  # Viernes Santo

# ── Texto ─────────────────────────────────────────────────────────────────────
print("\n--- Texto ---")
print("numero_a_letras(0)             ->", numero_a_letras(0))
print("numero_a_letras(1500000)       ->", numero_a_letras(1500000))
print("numero_a_letras(1000000000)    ->", numero_a_letras(1000000000))
print("numero_a_letras_pesos(1500000) ->", numero_a_letras_pesos(1500000))
print("slugify_colombiano('Bogotá D.C.')       ->", slugify_colombiano('Bogotá D.C.'))
print("slugify_colombiano('Ñoño & Compañía')   ->", slugify_colombiano('Ñoño & Compañía'))
