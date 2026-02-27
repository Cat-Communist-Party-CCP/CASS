/**
 * =============================================================================
 * CASS Frontend - Main Application
 * =============================================================================
 * 
 * Entry point for the CASS frontend. Handles:
 *   - Form submission
 *   - Streaming responses via SSE
 *   - UI updates
 */

import { streamChat, checkHealth } from './utils/sse.js'
import { 
  createUserMessage, 
  createAssistantMessage, 
  createLoadingIndicator 
} from './components/ChatContainer.js'

// =============================================================================
// DOM Elements
// =============================================================================

const chatContainer = document.getElementById('chat-container')
const chatForm = document.getElementById('chat-form')
const messageInput = document.getElementById('message-input')
const sendBtn = document.getElementById('send-btn')
const statusIndicator = document.getElementById('status-indicator')

// =============================================================================
// State
// =============================================================================

let isStreaming = false
let currentEventSource = null

// =============================================================================
// Functions
// =============================================================================

/**
 * Update the connection status indicator
 */
function updateStatus(connected, message = '') {
  const dot = statusIndicator.querySelector('span:first-child')
  const text = statusIndicator.querySelector('span:last-child')
  
  if (connected) {
    dot.className = 'w-2 h-2 bg-green-500 rounded-full'
    text.className = 'text-green-400'
    text.textContent = message || 'Connected'
  } else {
    dot.className = 'w-2 h-2 bg-red-500 rounded-full'
    text.className = 'text-red-400'
    text.textContent = message || 'Disconnected'
  }
}

/**
 * Scroll chat to bottom
 */
function scrollToBottom() {
  chatContainer.scrollTop = chatContainer.scrollHeight
}

/**
 * Set UI to loading/disabled state
 */
function setLoading(loading) {
  isStreaming = loading
  sendBtn.disabled = loading
  messageInput.disabled = loading
  
  if (loading) {
    sendBtn.innerHTML = `
      <svg class="w-5 h-5 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
      </svg>
    `
  } else {
    sendBtn.innerHTML = `
      <span>Send</span>
      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"/>
      </svg>
    `
    messageInput.focus()
  }
}

/**
 * Handle chat form submission
 */
async function handleSubmit(event) {
  event.preventDefault()
  
  const message = messageInput.value.trim()
  if (!message || isStreaming) return
  
  // Clear input
  messageInput.value = ''
  
  // Add user message
  chatContainer.appendChild(createUserMessage(message))
  scrollToBottom()
  
  // Create assistant message container
  const assistant = createAssistantMessage()
  chatContainer.appendChild(assistant.element)
  scrollToBottom()
  
  // Set loading state
  setLoading(true)
  
  // Stream response
  currentEventSource = streamChat(message, {
    onStart() {
      // Stream started
    },
    
    onToken(token) {
      assistant.update(token)
      scrollToBottom()
    },
    
    onSql(sql) {
      assistant.setSQL(sql)
      scrollToBottom()
    },
    
    onData(data) {
      assistant.setData(data)
      scrollToBottom()
    },
    
    onError(error) {
      assistant.setError(error)
      scrollToBottom()
      setLoading(false)
    },
    
    onEnd() {
      setLoading(false)
    }
  })
}

/**
 * Handle suggestion button clicks
 */
function handleSuggestionClick(event) {
  if (event.target.classList.contains('suggestion-btn')) {
    messageInput.value = event.target.textContent.trim()
    messageInput.focus()
  }
}

/**
 * Check backend connectivity
 */
async function checkConnection() {
  try {
    const status = await checkHealth()
    updateStatus(true, status.message || 'Connected')
  } catch (error) {
    console.error('Connection check failed:', error)
    updateStatus(false, 'Backend offline')
  }
}

// =============================================================================
// Event Listeners
// =============================================================================

// Form submission
chatForm.addEventListener('submit', handleSubmit)

// Suggestion buttons
chatContainer.addEventListener('click', handleSuggestionClick)

// Enter key (allow Shift+Enter for newlines in future)
messageInput.addEventListener('keydown', (e) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault()
    chatForm.dispatchEvent(new Event('submit'))
  }
})

// =============================================================================
// Initialize
// =============================================================================

// Check connection on load and periodically
checkConnection()
setInterval(checkConnection, 30000) // Every 30 seconds

// Focus input
messageInput.focus()

console.log('🗃️ CASS Frontend loaded')
