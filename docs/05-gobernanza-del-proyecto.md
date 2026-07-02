# 05 — Gobernanza del Proyecto

Este documento cubre cómo se gobierna el propio proyecto Ágora de Paz: quién puede contribuir, cómo se formaliza como investigación, y bajo qué licencia se libera.

## Rotación del poder (aplicada también al proyecto)

El principio innegociable #5 — rotación del poder, custodia temporal en vez de propiedad — aplica igual a la gobernanza del código y del proyecto de investigación como a las candidaturas que eventualmente produzca la plataforma. Ninguna persona o institución es dueña permanente de Ágora de Paz: es una donación a la humanidad, liberada bajo licencias que garantizan que siga siendo libre (ver [Licencias](#licencias)).

## Proyecto de Investigación

Este proyecto se documenta desde el día uno como **investigación aplicada** en:

- Gobernanza digital y democracia participativa mediada por IA.
- Transparencia algorítmica en procesos políticos.
- Construcción de consensos ciudadanos asistida por modelos de lenguaje locales.

### Formalización en Colombia

- **GitHub** como registro público, versionado y auditable de metodología, código y resultados.
- **ORCID** para el registro del investigador y sus productos (gratuito, internacional).
- **Minciencias** (CvLAC / GrupLAC) para el registro nacional del proyecto y sus productos de investigación.
- Posible aval institucional (SENA, universidades) mediante convocatorias, sin que el proyecto dependa de ello.

### Estructura documental del repositorio

```
docs/
├── 01-problema-y-vision.md
├── 02-metodologia.md            # Cómo funciona el motor de consenso
├── 03-criterios-bien-comun.md   # Filtro explícito y auditable
├── 04-arquitectura.md
├── 05-gobernanza-del-proyecto.md
└── paper/                        # Reporte de investigación
data/                             # Datos anonimizados de consensos (públicos)
results/                          # Resultados por ciclo de votación
```

## Cómo Contribuir

1. Lee el [README](../README.md) y la documentación en `docs/`.
2. Revisa los issues abiertos o propone uno nuevo.
3. Haz fork, crea una rama (`feat/...`, `fix/...`) siguiendo Conventional Commits.
4. Abre un Pull Request describiendo el cambio y su relación con los principios del proyecto.

### Contribuciones al núcleo ético

Las contribuciones al **filtro de bien común** (`docs/03-criterios-bien-comun.md` y su implementación) y al **motor de síntesis** requieren discusión pública previa en un issue, por ser el corazón ético del sistema. No se aceptan cambios directos vía PR sin ese debate previo.

## Licencias

- **Código**: [AGPL-3.0](https://www.gnu.org/licenses/agpl-3.0.html). Garantiza que el proyecto y todos sus derivados sigan siendo libres **incluso cuando se ofrecen como servicio en línea**: nadie puede tomar esta plataforma, modificarla y desplegarla como servicio cerrado sin publicar su código. Es la protección más fuerte para un bien común digital.
- **Documentación, metodología y datos de consenso**: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/deed.es).

---

*Este proyecto es una donación a la humanidad: cualquier comunidad, en cualquier lugar del mundo, puede tomarlo, adaptarlo y usarlo para construir gobernanza basada en consensos ciudadanos reales.*

---

Ver también: [01-problema-y-vision.md](./01-problema-y-vision.md) · [04-arquitectura.md](./04-arquitectura.md)
