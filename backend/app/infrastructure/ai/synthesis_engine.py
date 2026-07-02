"""Motor de síntesis: agrupa conversaciones de un ciclo y propone consensos.

Ver docs/02-metodologia.md#3-síntesis-por-ia. Usa el LLM local vía Ollama
para producir una síntesis en una sola oración, en el mismo estilo que el
ejemplo ilustrativo de la metodología.
"""

from app.domain.consensus.interfaces import SynthesisEngine
from app.infrastructure.ai.ollama_client import OllamaClient

SYNTHESIS_PROMPT = (
    "Eres el motor de síntesis de Ágora de Paz. A continuación hay "
    "intervenciones de ciudadanos de Ibagué sobre el tema '{topic}'. "
    "Redacta, en una sola oración y en español, el consenso emergente que "
    "resume la posición mayoritaria. Empieza la oración con 'Consenso "
    "emergente:'.\n\nIntervenciones:\n{texts}\n\nConsenso emergente:"
)


class OllamaSynthesisEngine(SynthesisEngine):
    def __init__(self, client: OllamaClient) -> None:
        self._client = client

    def synthesize(self, topic: str, texts: list[str]) -> str:
        if not texts:
            return f"Sin intervenciones registradas sobre '{topic}' en este ciclo."
        joined = "\n".join(f"- {text}" for text in texts)
        prompt = SYNTHESIS_PROMPT.format(topic=topic, texts=joined)
        response = self._client.generate(prompt).strip()
        return response if response.startswith("Consenso emergente:") else f"Consenso emergente: {response}"
