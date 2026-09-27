# POO en limpieza y validación

**Herencia.** `ReglaValidacion` define el contrato común de las validaciones. Las
reglas concretas, como `ReglaFechas` y `ReglaVariablesDerivadas`, heredan de ella
y desarrollan su propio nombre y su método `validar`.

**Polimorfismo.** `ValidadorDatasetProcesado` recorre todas las reglas y llama a
`validar` de la misma forma, sin necesitar saber qué revisa cada una. Por ejemplo,
se puede incorporar una nueva regla que herede de `ReglaValidacion` sin modificar
el validador.

**Encapsulamiento.** `LimpiadorLicitaciones` mantiene el resumen de su última
ejecución en `_ultima_ejecucion`. Este estado no se entrega directamente: la
propiedad `ultima_ejecucion` devuelve una copia, de modo que cambiar el resumen
recibido desde fuera no altera la información guardada por el limpiador.
