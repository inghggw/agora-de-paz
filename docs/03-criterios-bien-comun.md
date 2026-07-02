# 03 — Criterios de Bien Común

El bien común es el criterio de éxito número uno del proyecto (principio innegociable #2, ver [01-problema-y-vision.md](./01-problema-y-vision.md)). Este documento especifica el filtro que aplica la IA sobre cada síntesis de consenso, antes de que llegue a votación ciudadana.

## Objetivo del filtro

Evitar que la plataforma amplifique consensos que, aunque populares o mayoritarios en apariencia, concentren poder o capital en lugar de beneficiar a la mayoría. El filtro no decide qué es correcto ideológicamente: decide si una propuesta **redistribuye o concentra**.

## Preguntas explícitas del filtro

Cada síntesis pasa por estas cuatro preguntas, con criterios **explícitos y públicos**:

1. **¿Mejora la calidad de vida de quienes menos tienen?**
2. **¿Reduce la concentración de poder o de capital?**
3. **¿Es redistributiva o acumulativa?**
4. **¿Beneficia a la comunidad entera o a un grupo privilegiado?**

Si una síntesis no pasa el filtro, la IA la marca como **no alineada** y sugiere ajustes en lugar de descartarla silenciosamente. La propuesta ajustada vuelve a pasar por el filtro antes de ir a votación.

## Auditabilidad

El código del filtro vive en este repositorio (`backend/app/infrastructure/ai/common_good_filter.py`) y es público:

- Cualquiera puede leer exactamente qué prompt, reglas o modelo se usan para evaluar una síntesis.
- Cualquiera puede proponer cambios a los criterios vía Pull Request, siguiendo el proceso de [05-gobernanza-del-proyecto.md](./05-gobernanza-del-proyecto.md#contribuciones-al-nucleo-etico).
- Los cambios al filtro requieren discusión pública previa en un issue, por ser el corazón ético del sistema.

## Evidencia, no ideología

Consistente con el principio #6, las evaluaciones del filtro se contrastan contra:

- Indicadores reales de calidad de vida (educación, salud, desigualdad, seguridad, desarrollo rural).
- Experiencias documentadas de otros países o regiones que hayan mostrado resultados positivos, sin importar de qué corriente política provengan.

## Estado de la implementación

El diseño de los criterios está definido (Etapa 0 de la hoja de ruta). La implementación del motor de síntesis y el filtro como código ejecutable corresponde a la **Etapa 3** de la hoja de ruta (ver README, sección "Hoja de Ruta"). El scaffold inicial del módulo vive en `backend/app/infrastructure/ai/common_good_filter.py`, pendiente de lógica real.

---

Ver también: [02-metodologia.md](./02-metodologia.md) · [04-arquitectura.md](./04-arquitectura.md)
