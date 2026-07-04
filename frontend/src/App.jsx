import { useState, useRef, useEffect } from 'react'

const API_URL = 'http://localhost:5001/api/chat'

const SUGGESTIONS = [
  'What is SellersPoint?',
  'Tell me about EduLite',
  'What tech stack does Assani know?',
  'How does this bot work?',
]

function Message({ role, content, isError }) {
  if (role === 'user') {
    return (
      <div className="line line-user">
        <span className="prompt">assani@bot:~$</span>
        <span className="line-text">{content}</span>
      </div>
    )
  }
  return (
    <div className={`line line-bot ${isError ? 'line-error' : ''}`}>
      <span className="bot-tag">{isError ? 'error' : 'bot'}</span>
      <span className="line-text">{content}</span>
    </div>
  )
}

export default function App() {
  const [messages, setMessages] = useState([
    {
      role: 'bot',
      content:
        "Hi, I'm a small RAG bot. Ask me about Assani's projects — SellersPoint, EduLite, FitLife, or this bot itself.",
    },
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const scrollRef = useRef(null)

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: 'smooth' })
  }, [messages, loading])

  async function sendQuestion(question) {
    if (!question.trim() || loading) return

    setMessages((prev) => [...prev, { role: 'user', content: question }])
    setInput('')
    setLoading(true)

    try {
      const res = await fetch(API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question }),
      })
      const data = await res.json()

      if (!res.ok) {
        throw new Error(data.error || 'Something went wrong.')
      }
      setMessages((prev) => [...prev, { role: 'bot', content: data.answer }])
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          role: 'bot',
          isError: true,
          content: `Could not reach the API — is api_server.py running? (${err.message})`,
        },
      ])
    } finally {
      setLoading(false)
    }
  }

  function handleSubmit(e) {
    e.preventDefault()
    sendQuestion(input)
  }

  return (
    <div className="page">
      <div className="terminal">
        <header className="terminal-header">
          <div className="terminal-title">assani@portfolio-bot</div>
          <div className="terminal-subtitle">
            RAG demo — OpenAI embeddings + retrieval over a small knowledge base
          </div>
        </header>

        <div className="chips">
          {SUGGESTIONS.map((s) => (
            <button
              key={s}
              className="chip"
              onClick={() => sendQuestion(s)}
              disabled={loading}
            >
              {s}
            </button>
          ))}
        </div>

        <div className="log" ref={scrollRef}>
          {messages.map((m, i) => (
            <Message key={i} role={m.role} content={m.content} isError={m.isError} />
          ))}
          {loading && (
            <div className="line line-bot">
              <span className="bot-tag">bot</span>
              <span className="line-text typing">retrieving context, thinking</span>
            </div>
          )}
        </div>

        <form className="input-row" onSubmit={handleSubmit}>
          <span className="prompt">$</span>
          <input
            autoFocus
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="ask about a project, skill, or how this bot works..."
            disabled={loading}
          />
          <button type="submit" disabled={loading || !input.trim()}>
            send
          </button>
        </form>
      </div>
    </div>
  )
}
