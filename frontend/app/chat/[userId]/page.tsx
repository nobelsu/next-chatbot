'use client'

import { useState, useEffect } from 'react'
import { useParams } from 'next/navigation'
import axios from 'axios'

// Create an axios instance with the base URL
const api = axios.create({
  baseURL: 'https://next-chatbot-production.up.railway.app/',  // FastAPI backend URL
  headers: {
    'Content-Type': 'application/json',
  },
})

export default function ChatPage() {
  const params = useParams()
  const userId = params.userId as string
  const [messages, setMessages] = useState<{ text: string; isUser: boolean }[]>([])
  const [input, setInput] = useState('')
  const [error, setError] = useState<string | null>(null)

  const clearHistory = async () => {
    try {
      await api.delete(`/api/history/${userId}`)
      setMessages([])
      setError(null)
    } catch (error: any) {
      console.error('Error clearing chat history:', error)
      setError(`Failed to clear chat history: ${error.message}`)
    }
  }

  // Load chat history on component mount
  useEffect(() => {
    const loadHistory = async () => {
      try {
        console.log('Attempting to load chat history...')
        const response = await api.get(`/api/history/${userId}`)
        console.log('Chat history response:', response.data)
        const history = response.data.history

        const formattedMessages = history.map((msg: any) => ({
          text: msg.content,
          isUser: msg.role === 'user'
        }))
        setMessages(formattedMessages)
        setError(null)
      } catch (error: any) {
        console.error('Error loading chat history:', error)
        setError(`Failed to load chat history: ${error.message}`)
        if (error.response) {
          console.error('Error response:', error.response.data)
          console.error('Error status:', error.response.status)
        }
      }
    }
    loadHistory()
  }, [userId])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim()) return

    // Add user message to UI immediately
    setMessages(prev => [...prev, { text: input, isUser: true }])
    setInput('')
    setError(null)

    try {
      console.log('Sending message to backend:', input)
      // Send message to backend
      const response = await api.post('/api/chat', {
        message: input,
        userId: userId
      })
      console.log('Backend response:', response.data)

      // Add bot response to UI
      setMessages(prev => [...prev, { text: response.data.response, isUser: false }])
    } catch (error: any) {
      console.error('Error sending message:', error)
      if (error.response) {
        console.error('Error response:', error.response.data)
        console.error('Error status:', error.response.status)
      }
      // Add error message to UI
      setError(`Failed to send message: ${error.message}`)
      setMessages(prev => [...prev, { 
        text: 'Sorry, there was an error processing your message. Please try again.',
        isUser: false 
      }])
    }
  }

  return (
    <main className="flex min-h-screen flex-col items-center p-4">
      <div className="w-full max-w-2xl">
        <h1 className="text-3xl font-bold text-center mb-8">Chat with User: {userId}</h1>
        
        <div className="flex justify-between items-center mb-4">
          <button
            onClick={clearHistory}
            className="bg-red-500 text-white px-4 py-2 rounded-lg hover:bg-red-600 transition-colors"
          >
            Clear History
          </button>
        </div>

        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-4" role="alert">
            <span className="block sm:inline">{error}</span>
          </div>
        )}

        <div className="bg-white rounded-lg shadow-lg p-4 mb-4 h-[60vh] overflow-y-auto">
          {messages.map((message, index) => (
            <div
              key={index}
              className={`mb-4 ${
                message.isUser ? 'text-right' : 'text-left'
              }`}
            >
              <div
                className={`inline-block p-3 rounded-lg whitespace-pre-wrap ${
                  message.isUser
                    ? 'bg-blue-500 text-white'
                    : 'bg-gray-200 text-gray-800'
                }`}
              >
                {message.text}
              </div>
            </div>
          ))}
        </div>

        <form onSubmit={handleSubmit} className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your message..."
            className="flex-1 p-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500"
          />
          <button
            type="submit"
            className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 transition-colors"
          >
            Send
          </button>
        </form>
      </div>
    </main>
  )
} 