/**
 * =============================================================================
 * SSE (Server-Sent Events) Utility
 * =============================================================================
 * 
 * Handles streaming responses from the backend /chat/stream endpoint.
 * 
 * Event Types:
 *   - start: Stream has begun
 *   - token: Individual token from LLM
 *   - sql: Extracted SQL query
 *   - data: Query results (JSON array)
 *   - error: Error message
 *   - end: Stream complete
 */

/**
 * Configuration for the SSE client
 */
const config = {
  // In development, Vite proxy handles this. In production, use full URL.
  baseUrl: import.meta.env.DEV ? '/api' : 'http://localhost:8001'
}

/**
 * Create an SSE connection to stream chat responses
 * 
 * @param {string} message - The user's question
 * @param {Object} callbacks - Event callbacks
 * @param {Function} callbacks.onStart - Called when stream starts
 * @param {Function} callbacks.onToken - Called for each token
 * @param {Function} callbacks.onSql - Called with extracted SQL
 * @param {Function} callbacks.onData - Called with query results
 * @param {Function} callbacks.onError - Called on error
 * @param {Function} callbacks.onEnd - Called when stream ends
 * @returns {EventSource} The EventSource instance (for cleanup)
 */
export function streamChat(message, callbacks = {}) {
  const encodedMessage = encodeURIComponent(message)
  const url = `${config.baseUrl}/chat/stream?message=${encodedMessage}`
  
  const eventSource = new EventSource(url)
  
  eventSource.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data)
      
      switch (data.type) {
        case 'start':
          callbacks.onStart?.()
          break
        case 'token':
          callbacks.onToken?.(data.content)
          break
        case 'sql':
          callbacks.onSql?.(data.content)
          break
        case 'data':
          callbacks.onData?.(data.content)
          break
        case 'error':
          callbacks.onError?.(data.content)
          break
        case 'end':
          callbacks.onEnd?.()
          eventSource.close()
          break
      }
    } catch (e) {
      console.error('Failed to parse SSE event:', e)
      callbacks.onError?.('Failed to parse response')
    }
  }
  
  eventSource.onerror = (error) => {
    console.error('SSE connection error:', error)
    callbacks.onError?.('Connection lost')
    eventSource.close()
  }
  
  return eventSource
}

/**
 * Non-streaming chat request (uses POST /chat)
 * 
 * @param {string} message - The user's question
 * @returns {Promise<Object>} Response with answer, sql, data
 */
export async function sendChat(message) {
  const response = await fetch(`${config.baseUrl}/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message })
  })
  
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}: ${response.statusText}`)
  }
  
  return response.json()
}

/**
 * Check API health and get status
 * 
 * @returns {Promise<Object>} Status object
 */
export async function checkHealth() {
  const response = await fetch(`${config.baseUrl}/`)
  return response.json()
}

/**
 * Get database schema
 * 
 * @returns {Promise<string>} Database schema
 */
export async function getSchema() {
  const response = await fetch(`${config.baseUrl}/schema`)
  const data = await response.json()
  return data.schema
}

/**
 * Get list of tables
 * 
 * @returns {Promise<string[]>} Array of table names
 */
export async function getTables() {
  const response = await fetch(`${config.baseUrl}/tables`)
  const data = await response.json()
  return data.tables
}

export default {
  streamChat,
  sendChat,
  checkHealth,
  getSchema,
  getTables
}
