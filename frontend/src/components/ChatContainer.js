/**
 * =============================================================================
 * ChatContainer Component
 * =============================================================================
 * 
 * Manages the chat UI - rendering messages, handling streaming, displaying
 * SQL and data results.
 */

/**
 * Message types for rendering
 */
export const MessageType = {
  USER: 'user',
  ASSISTANT: 'assistant',
  ERROR: 'error'
}

/**
 * Create a user message element
 * 
 * @param {string} content - The message text
 * @returns {HTMLElement} Message element
 */
export function createUserMessage(content) {
  const div = document.createElement('div')
  div.className = 'flex justify-end fade-in'
  div.innerHTML = `<div class="msg-user">${escapeHtml(content)}</div>`
  return div
}

/**
 * Create an assistant message container (for streaming)
 * 
 * @returns {Object} { element, tokensContainer, sqlContainer, dataContainer, update, setSQL, setData, setError }
 */
export function createAssistantMessage() {
  const div = document.createElement('div')
  div.className = 'flex justify-start fade-in'
  
  const wrapper = document.createElement('div')
  wrapper.className = 'msg-assistant'
  
  // Tokens (streaming text)
  const tokensContainer = document.createElement('div')
  tokensContainer.className = 'tokens whitespace-pre-wrap'
  
  // SQL block (hidden initially)
  const sqlContainer = document.createElement('div')
  sqlContainer.className = 'sql-container hidden mt-3'
  sqlContainer.innerHTML = `
    <div class="flex items-center gap-2 text-xs text-gray-400 mb-2">
      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"/>
      </svg>
      Generated SQL
    </div>
    <div class="sql-block"><code></code></div>
  `
  
  // Data table (hidden initially)
  const dataContainer = document.createElement('div')
  dataContainer.className = 'data-container hidden mt-3'
  
  wrapper.appendChild(tokensContainer)
  wrapper.appendChild(sqlContainer)
  wrapper.appendChild(dataContainer)
  div.appendChild(wrapper)
  
  return {
    element: div,
    tokensContainer,
    sqlContainer,
    dataContainer,
    
    // Add token to streaming text
    update(token) {
      tokensContainer.textContent += token
    },
    
    // Set the SQL code
    setSQL(sql) {
      const code = sqlContainer.querySelector('code')
      code.textContent = sql
      sqlContainer.classList.remove('hidden')
    },
    
    // Set the data table
    setData(data) {
      if (!data || data.length === 0) {
        dataContainer.innerHTML = '<p class="text-gray-400 text-sm">No results</p>'
        dataContainer.classList.remove('hidden')
        return
      }
      
      const table = createDataTable(data)
      dataContainer.innerHTML = `
        <div class="flex items-center gap-2 text-xs text-gray-400 mb-2">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h18M3 14h18m-9-4v8m-7 0h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"/>
          </svg>
          Results (${data.length} row${data.length > 1 ? 's' : ''})
        </div>
      `
      dataContainer.appendChild(table)
      dataContainer.classList.remove('hidden')
    },
    
    // Show error
    setError(error) {
      tokensContainer.innerHTML = `<div class="error-msg">${escapeHtml(error)}</div>`
    }
  }
}

/**
 * Create a loading indicator (typing dots)
 * 
 * @returns {HTMLElement} Loading element
 */
export function createLoadingIndicator() {
  const div = document.createElement('div')
  div.className = 'flex justify-start fade-in'
  div.innerHTML = `
    <div class="msg-assistant typing-indicator">
      <span></span>
      <span></span>
      <span></span>
    </div>
  `
  return div
}

/**
 * Create a data table from query results
 * 
 * @param {Array<Object>} data - Array of row objects
 * @returns {HTMLElement} Table element
 */
function createDataTable(data) {
  if (!data || data.length === 0) {
    const p = document.createElement('p')
    p.className = 'text-gray-400 text-sm'
    p.textContent = 'No data'
    return p
  }
  
  const columns = Object.keys(data[0])
  
  const table = document.createElement('table')
  table.className = 'data-table'
  
  // Header
  const thead = document.createElement('thead')
  thead.innerHTML = `<tr>${columns.map(col => `<th>${escapeHtml(col)}</th>`).join('')}</tr>`
  table.appendChild(thead)
  
  // Body
  const tbody = document.createElement('tbody')
  data.forEach(row => {
    const tr = document.createElement('tr')
    tr.innerHTML = columns.map(col => `<td>${formatCell(row[col])}</td>`).join('')
    tbody.appendChild(tr)
  })
  table.appendChild(tbody)
  
  return table
}

/**
 * Format a table cell value
 * 
 * @param {any} value - Cell value
 * @returns {string} Formatted HTML string
 */
function formatCell(value) {
  if (value === null || value === undefined) {
    return '<span class="text-gray-500">NULL</span>'
  }
  if (typeof value === 'object') {
    return escapeHtml(JSON.stringify(value))
  }
  if (typeof value === 'number') {
    return `<span class="text-blue-400">${value.toLocaleString()}</span>`
  }
  return escapeHtml(String(value))
}

/**
 * Escape HTML to prevent XSS
 * 
 * @param {string} str - String to escape
 * @returns {string} Escaped string
 */
function escapeHtml(str) {
  const div = document.createElement('div')
  div.textContent = str
  return div.innerHTML
}

export default {
  MessageType,
  createUserMessage,
  createAssistantMessage,
  createLoadingIndicator
}
