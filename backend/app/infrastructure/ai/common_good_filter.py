"""Filtro de bien común: núcleo ético y auditable del sistema.

Ver docs/03-criterios-bien-comun.md para las cuatro preguntas explícitas
que debe responder este filtro. Cambios a este archivo requieren discusión
pública previa en un issue (docs/05-gobernanza-del-proyecto.md#contribuciones-al-nucleo-etico).

Esta es una implementación placeholder (siempre aprueba) hasta que la
Etapa 3 de la hoja de ruta conecte la evaluación real vía LLM local.
"""

from typing import Protocol


class CommonGoodFilter(Protocol):
    def is_aligned(self, summary: str) -> bool: ...


class PermissiveCommonGoodFilter:
    """Placeholder: no rechaza nada. Reemplazar por la evaluación real."""

    def is_aligned(self, summary: str) -> bool:
        return True
