<script setup>
import { ref } from 'vue'

const API_BASE = '/api/v1'

const conversationId = ref(null)
const messages = ref([])
const draft = ref('')
const participantMode = ref('anonymous')
const loading = ref(false)
const error = ref(null)

async function startConversation() {
  loading.value = true
  error.value = null
  try {
    const response = await fetch(`${API_BASE}/chat/conversations`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ participant_mode: participantMode.value }),
    })
    if (!response.ok) throw new Error(`Error ${response.status}`)
    const conversation = await response.json()
    conversationId.value = conversation.id
    messages.value = conversation.messages
  } catch (err) {
    error.value = 'No se pudo conectar con el backend. ¿Está corriendo en http://localhost:8000?'
  } finally {
    loading.value = false
  }
}

async function sendMessage() {
  if (!draft.value.trim() || !conversationId.value) return
  loading.value = true
  error.value = null
  try {
    const response = await fetch(
      `${API_BASE}/chat/conversations/${conversationId.value}/messages`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content: draft.value }),
      },
    )
    if (!response.ok) throw new Error(`Error ${response.status}`)
    const conversation = await response.json()
    messages.value = conversation.messages
    draft.value = ''
  } catch (err) {
    error.value = 'No se pudo enviar el mensaje.'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <main class="app">
    <h1>Ágora de Paz</h1>
    <p class="subtitle">Conversación ciudadana — prueba piloto Ibagué</p>

    <div v-if="!conversationId" class="starter">
      <label>
        Modo de participación:
        <select v-model="participantMode">
          <option value="anonymous">Anónimo</option>
          <option value="verified">Identidad verificada</option>
        </select>
      </label>
      <button :disabled="loading" @click="startConversation">Iniciar conversación</button>
    </div>

    <div v-else class="chat">
      <ul class="messages">
        <li v-for="m in messages" :key="m.id" :class="m.author">
          <strong>{{ m.author === 'assistant' ? 'Ágora' : 'Tú' }}:</strong> {{ m.content }}
        </li>
      </ul>
      <form class="composer" @submit.prevent="sendMessage">
        <input v-model="draft" placeholder="Escribe tu opinión..." :disabled="loading" />
        <button type="submit" :disabled="loading">Enviar</button>
      </form>
    </div>

    <p v-if="error" class="error">{{ error }}</p>
  </main>
</template>

<style scoped>
.app {
  max-width: 640px;
  margin: 2rem auto;
  font-family: system-ui, sans-serif;
}
.subtitle {
  color: #555;
}
.messages {
  list-style: none;
  padding: 0;
}
.messages li {
  margin-bottom: 0.75rem;
}
.composer {
  display: flex;
  gap: 0.5rem;
}
.composer input {
  flex: 1;
}
.error {
  color: #b00020;
}
</style>
