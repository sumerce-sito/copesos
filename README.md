# copesos

Librería Python de utilidades para proyectos colombianos.

Funciones para formato, validación, cálculos tributarios, nómina y fechas — sin dependencias externas.

## Instalación

```bash
pip install copesos
```

## Funciones disponibles

### Formato

```python
from copesos import formatear_pesos, formatear_fecha, formatear_celular

formatear_pesos(1250000)        # '$1.250.000'
formatear_pesos(500)            # '$500'

from datetime import date
formatear_fecha(date(2026, 4, 3))   # 'viernes 3 de abril de 2026'

formatear_celular(3001234567)   # '+57 300 123 4567'
formatear_celular(123)          # None
```

### Cálculos tributarios

```python
from copesos import calcular_iva, calcular_retefuente, calcular_reteica, uvt_a_pesos

calcular_iva(100000)
# {'base': 100000, 'porcentaje': 19, 'iva': 19000.0, 'total': 119000.0}

calcular_iva(50000, 5)
# {'base': 50000, 'porcentaje': 5, 'iva': 2500.0, 'total': 52500.0}

calcular_retefuente(1000000, 3.5)
# {'base': 1000000, 'tarifa_pct': 3.5, 'retencion': 35000.0, 'neto': 965000.0}

calcular_reteica(1000000, 4.14)   # tarifa en por mil (‰)
# {'base': 1000000, 'tarifa_por_mil': 4.14, 'reteica': 4140.0, 'neto': 995860.0}

uvt_a_pesos(1090, 2026)         # 57087660  (UVT 2026 = $52.374)
```

### Validaciones

```python
from copesos import validar_cedula, validar_nit, validar_tarjeta_identidad, validar_placa, tipo_documento

validar_cedula(1234567890)      # True
validar_cedula(123)             # False

validar_nit('8001972684')       # True  (verifica dígito de verificación)
validar_nit('123456789')        # False

validar_tarjeta_identidad('1020304050')  # True

validar_placa('ABC123')         # True  (carro)
validar_placa('ABC12D')         # True  (moto)
validar_placa('12ABC3')         # False

tipo_documento('CC')            # 'Cédula de Ciudadanía'
tipo_documento('NIT')           # 'Número de Identificación Tributaria'
tipo_documento('PEP')           # 'Permiso Especial de Permanencia'
```

### Laboral / Nómina

Tablas de referencia incluidas para 2021–2026 (SMMLV, auxilio de transporte).

```python
from copesos import es_salario_minimo, calcular_subsidio_transporte, calcular_prestaciones

es_salario_minimo(1750905, 2026)        # True
es_salario_minimo(1500000, 2026)        # False

calcular_subsidio_transporte(1750905, 2026)   # 249095
calcular_subsidio_transporte(4000000, 2026)   # 0  (supera 2 SMMLV)

calcular_prestaciones(1750905, 360, 2026)
# {
#   'salario': 1750905,
#   'auxilio_transporte': 249095,
#   'dias': 360,
#   'cesantias': 2000000.0,
#   'intereses_cesantias': 240000.0,
#   'prima': 2000000.0,
#   'vacaciones': 875452.5,
#   'total': 5115452.5
# }
```

### Fechas y festivos colombianos

```python
from copesos import es_festivo, festivos_del_año, dias_habiles, siguiente_dia_habil
from datetime import date

es_festivo(date(2026, 1, 1))    # True  (Año Nuevo)
es_festivo(date(2026, 4, 3))    # True  (Viernes Santo)
es_festivo(date(2026, 3, 27))   # False

festivos_del_año(2026)          # lista con las 18 fechas festivas del año

dias_habiles(date(2026, 4, 1), date(2026, 4, 10))   # 6

siguiente_dia_habil(date(2026, 4, 3))   # date(2026, 4, 6)  (salta Viernes Santo)
```

### Texto

```python
from copesos import numero_a_letras, numero_a_letras_pesos, slugify_colombiano, calcular_porcentaje

numero_a_letras(1500000)        # 'un millón quinientos mil'
numero_a_letras(1000000000)     # 'mil millones'

numero_a_letras_pesos(1500000)  # 'UN MILLÓN QUINIENTOS MIL PESOS M/CTE'

slugify_colombiano('Bogotá D.C.')       # 'bogota-d-c'
slugify_colombiano('Ñoño & Compañía')   # 'nono-compania'

calcular_porcentaje(250, 1000)  # 25.0
```

## Valores de referencia incluidos

| Año | SMMLV | Auxilio transporte | UVT |
|-----|-------|--------------------|-----|
| 2024 | $1.300.000 | $162.000 | $47.065 |
| 2025 | $1.423.500 | $200.000 | $49.799 |
| 2026 | $1.750.905 | $249.095 | $52.374 |

Fuentes: Decretos 1469 y 1470 del 29 de diciembre de 2025 · Resolución DIAN 000238 del 15 de diciembre de 2025.

## Requisitos

Python 3.7 o superior. Sin dependencias externas.

## Autor

Hollman — Fusagasugá, Cundinamarca.
