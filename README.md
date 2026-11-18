# Modelo de planta Power-to-Gas en Python

Modelo en Python de una planta de depuración de aguas residuales de matadero
porcino (5000 m³/d) con valorización del biogás mediante Power-to-Gas, basado
en mi Trabajo de Fin de Grado en Ingeniería Química (Universidad de Valladolid, 2026).

## Módulos

| Módulo | Etapa | Estado |
|---|---|---|
| `src/reactor_ic.py` | Reactor anaerobio de circulación interna (IC) | ✅ Validado con los resultados del TFG |

## Cómo usarlo

Requiere Python 3. Desde la carpeta del proyecto:

```
python src/reactor_ic.py
```

Ejecuta el caso de prueba del TFG y muestra los resultados del reactor
(volumen, tiempo de retención, producción de metano y biogás, purga de fango).

## Metodología

Cada módulo se desarrolla en cuatro pasos:

1. **Especificación:** ecuaciones, supuestos y casos de prueba extraídos del TFG.
2. **Borrador con IA:** el código se genera a partir de esa especificación (ver `docs/`).
3. **Revisión y validación:** el código se revisa línea a línea y se valida contra los resultados del TFG.
4. **Documentación:** se publica el módulo con su especificación.

## Datos

Todos los datos proceden del TFG (bibliografía y cálculos de diseño propios).
