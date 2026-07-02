# 02 — Metodología: el Motor de Consenso

## Flujo general

```
Conversación abierta en chat
          ↓
   Corte temporal (semanal / quincenal)
          ↓
   Síntesis de temas por IA
          ↓
   Filtro de bien común (público y auditable)
          ↓
   Propuesta de consensos
          ↓
   Votación ciudadana abierta (con fechas definidas)
          ↓
   Resultados guardados y documentados
          ↓
   Siguiente ciclo (la conversación evoluciona)
```

## 1. Conversación abierta

La interfaz es un **chat simple y conversacional**, sin formularios complejos ni fricción. La IA abre con preguntas del tipo:

- "¿Cuál es el mayor desafío que ves en Ibagué hoy?"
- "¿Qué necesita cambiar en educación?"
- "¿Cómo debería ser la seguridad en tu barrio?"

El ciudadano puede elegir temáticas sugeridas al inicio o hablar abiertamente. Conforme conversa, la IA sugiere temáticas relacionadas para profundizar.

## 2. Cortes temporales

Las opiniones políticas **evolucionan** con la información y los resultados de las políticas. Por eso la conversación corre de forma continua, pero en momentos definidos (cada semana o quincena) la plataforma **congela y procesa** todo lo dicho hasta ese punto. Cada ciclo tiene fechas claras de apertura y cierre de votación.

## 3. Síntesis por IA

La IA lee las conversaciones del período, identifica temas comunes, agrupa por dominio (seguridad, educación, economía, salud, ruralidad, etc.) y sintetiza posiciones emergentes.

**Ejemplo ilustrativo:**
- 340 ciudadanos hablaron de educación.
- Mayoría señala baja calidad y falta de recursos docentes.
- Alta recurrencia de la prioridad en educación rural.

Síntesis propuesta: *"Consenso emergente: Ibagué necesita inversión urgente en educación rural, con recursos para docentes e infraestructura."*

## 4. Filtro de bien común

Cada síntesis pasa por un filtro con criterios explícitos y públicos antes de convertirse en propuesta de consenso. Ver el detalle completo en [03-criterios-bien-comun.md](./03-criterios-bien-comun.md).

## 5. Votación ciudadana

Cada consenso propuesto va a **votación abierta en un período con fecha definida**.

Ponderación sugerida (ajustable y documentada):
- Participante con identidad verificada: **1.0 voto**.
- Participante anónimo: **0.5 votos**.

Reglas:
- Consenso **aprobado** si supera el umbral definido (p. ej. >50%).
- Consenso **rechazado** si no lo alcanza.
- La comunidad puede proponer ajustes dentro del mismo período.

## 6. Registro histórico

Todos los consensos (aprobados y rechazados) se documentan públicamente con timestamp, número de votos y evolución en el tiempo. Este registro permite:

- Ver **cómo pensó la ciudad a lo largo del tiempo**.
- Ejercer **rendición de cuentas**: contrastar lo que prometen y hacen los elegidos contra los consensos que la ciudadanía pidió.

Los resultados de cada ciclo se publican en [`results/`](../results/) y los datos anonimizados de consenso en [`data/`](../data/).

## 7. Selección de candidaturas

Sobre los consensos validados:

1. Personas interesadas **suben su hoja de vida** a la plataforma.
2. La IA calcula un **score de alineación** entre el perfil/propuestas de cada persona y los consensos aprobados.
3. Filtros de integridad: sin investigaciones ni antecedentes relevantes, sin historial de enriquecimiento con lo público, favoreciendo rotación y renovación.
4. La comunidad valida mediante **recolección de firmas** (mecanismo legal colombiano de grupos significativos de ciudadanos).
5. Las candidaturas resultantes representan el proyecto político construido colectivamente, con **mandato temporal** y rendición de cuentas contra el registro histórico de consensos.

---

Ver también: [01-problema-y-vision.md](./01-problema-y-vision.md) · [03-criterios-bien-comun.md](./03-criterios-bien-comun.md) · [04-arquitectura.md](./04-arquitectura.md)
