"""Motor de síntesis: agrupa conversaciones de un ciclo y propone consensos.

Implementación real (LLM local vía Ollama) pendiente para la Etapa 3 de la
hoja de ruta (ver docs/02-metodologia.md#3-síntesis-por-ia). Esta clase base
define el contrato y un comportamiento mínimo determinista para poder probar
el resto del flujo end-to-end sin un modelo cargado.
"""

from typing import Protocol


class SynthesisEngine(Protocol):
    def synthesize(self, topic: str, texts: list[str]) -> str: ...


class NaiveSynthesisEngine:
    """Concatena y resume de forma trivial. Placeholder hasta integrar Ollama."""

    def synthesize(self, topic: str, texts: list[str]) -> str:
        if not texts:
            return f"Sin intervenciones registradas sobre '{topic}' en este ciclo."
        return f"Consenso emergente sobre '{topic}' a partir de {len(texts)} intervenciones ciudadanas."
