# CLAUDE.md — Proyecto `copesos`

## Qué es este proyecto

`copesos` es una librería Python de utilidades para proyectos colombianos.
Nació como ejercicio de aprendizaje para entender cómo se construye y empaqueta
una librería desde cero, con casos de uso reales.

## Quién lo desarrolla

Hollman — Diseñador Industrial y Data Scientist, Fusagasugá, Cundinamarca.
Nivel Python: básico-intermedio. Prefiere explicaciones directas sin rodeos.

## Qué hace la librería

Cuatro funciones en `copesos/formato.py`:

- `formatear_pesos(valor)` → convierte 1250000 en '$1.250.000'
- `formatear_fecha(fecha)` → convierte date(2026,3,27) en 'viernes 27 de marzo de 2026'
- `calcular_porcentaje(valor, total)` → retorna porcentaje con dos decimales
- `validar_cedula(cedula)` → valida que sea numérica y entre 6 y 10 dígitos

## Estructura del proyecto

```
copesos/
├── copesos/
│   ├── __init__.py       ← expone las funciones al importar
│   └── formato.py        ← toda la lógica actual vive aquí
├── tests/
│   └── test_copesos.py   ← pruebas manuales por consola
├── setup.py              ← configuración para pip install
└── README.md
```

## Estado actual

- [x] Estructura creada
- [x] Cuatro funciones implementadas
- [x] Archivo de pruebas listo
- [ ] Pendiente: revisar y correr pruebas en PC
- [ ] Pendiente: agregar más funciones
- [ ] Pendiente: publicar en PyPI

## Hoja de ruta de ideas (no urgente)

Proyectos futuros inspirados en esta librería:

- `fichatec` — generador de fichas técnicas en PDF
- `normatec` — validador de normas ICONTEC/ISO
- `parametrik` — costeo paramétrico para diseño industrial
- `habilitacion` — validador de cumplimiento Resolución 3100
- `ips_utils` — utilidades para datos clínicos colombianos (CUPS, RIPS, CIE-10)
- `liturgia` — tiempo litúrgico y lecturas por día
- `pymes_col` — análisis financiero para pequeños negocios colombianos
- `formapy` — geometría 3D paramétrica exportable a STL
- `evaluador_ergonomico` — validación ergonómica para población colombiana

## Instrucciones para el agente

- El usuario aprende construyendo, no leyendo teoría
- Explicar antes de escribir código
- Nivel de explicación: sin asumir conocimiento previo
- Prioridad actual: terminar y entender `copesos` antes de arrancar otro proyecto
- No sugerir librerías externas innecesarias en esta etapa
