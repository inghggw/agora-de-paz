"""Filtro de bien común: núcleo ético y auditable del sistema.

Ver docs/03-criterios-bien-comun.md para las cuatro preguntas explícitas
que debe responder este filtro. Cambios a este archivo requieren discusión
pública previa en un issue (docs/05-gobernanza-del-proyecto.md#contribuciones-al-nucleo-etico).
"""

from app.domain.consensus.interfaces import CommonGoodFilter
from app.infrastructure.ai.ollama_client import OllamaClient

FILTER_PROMPT = (
    "Evalúa la siguiente síntesis de consenso ciudadano contra estos cuatro "
    "criterios de bien común:\n"
    "1. ¿Mejora la calidad de vida de quienes menos tienen?\n"
    "2. ¿Reduce la concentración de poder o de capital?\n"
    "3. ¿Es redistributiva o acumulativa?\n"
    "4. ¿Beneficia a la comunidad entera o a un grupo privilegiado?\n\n"
    "Síntesis: \"{summary}\"\n\n"
    "Responde únicamente con la palabra ALINEADO si la síntesis pasa estos "
    "criterios, o NO_ALINEADO si no los pasa. No expliques tu respuesta."
)


class OllamaCommonGoodFilter(CommonGoodFilter):
    def __init__(self, client: OllamaClient) -> None:
        self._client = client

    def is_aligned(self, summary: str) -> bool:
        response = self._client.generate(FILTER_PROMPT.format(summary=summary))
        return "NO_ALINEADO" not in response.upper() and "ALINEADO" in response.upper()
