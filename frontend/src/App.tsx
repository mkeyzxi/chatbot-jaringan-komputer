import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, AlertCircle, BookOpen } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import { sendChatMessage } from './services/api';
import type { ChatResponse } from './services/api';

interface Message {
  id: string;
  type: 'user' | 'bot' | 'error';
  content: string;
  retrieval?: ChatResponse['retrieval'];
  latency_ms?: number;
}

function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      type: 'user',
      content: input.trim(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await sendChatMessage(userMessage.content);
      
      const botMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: 'bot',
        content: response.answer,
        retrieval: response.retrieval,
        latency_ms: response.latency_ms,
      };
      
      setMessages((prev) => [...prev, botMessage]);
    } catch (error: any) {
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: 'error',
        content: error.message || 'Terjadi kesalahan saat menghubungi server.',
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app-shell">
      <main className="chat-shell">
        <header className="chat-header">
          <BookOpen size={22} className="logo-icon" color="var(--color-primary)" />
          <div>
            <h1>Chatbot Jaringan Komputer</h1>
            <p>Asisten Belajar Mahasiswa Teknik Informatika</p>
          </div>
        </header>

        <section className="chat-content">
          <div className="chat-content-inner">
            {messages.length === 0 ? (
              <div className="empty-state">
                <div className="empty-state-icon">
                  <Bot size={32} />
                </div>
                <div className="empty-state-title">Halo! Saya asisten<br/>Jaringan Komputer Anda.</div>
                <div className="empty-state-subtitle">
                  Saya dapat membantu Anda memahami materi kuliah berdasarkan dokumen yang telah dipelajari.
                </div>
                
                <div className="suggestions">
                  <button onClick={() => setInput("Apa itu model OSI dan sebutkan lapisannya?")}>
                    Apa itu model OSI dan sebutkan lapisannya?
                  </button>
                  <button onClick={() => setInput("Jelaskan cara kerja subnet mask pada IPv4.")}>
                    Jelaskan cara kerja subnet mask pada IPv4.
                  </button>
                  <button onClick={() => setInput("Apa perbedaan antara routing statis dan dinamis?")}>
                    Apa perbedaan antara routing statis dan dinamis?
                  </button>
                </div>
              </div>
            ) : (
              <>
                {messages.map((msg) => (
                  <div key={msg.id} className={`message ${msg.type}`}>
                    {msg.type !== 'user' && (
                      <div className={msg.type === 'error' ? "error-avatar" : "assistant-avatar"}>
                        {msg.type === 'error' ? <AlertCircle size={20} /> : <Bot size={20} />}
                      </div>
                    )}
                    
                    <div className={msg.type === 'user' ? "message-bubble" : "message-body prose"}>
                      {msg.type === 'user' ? (
                        msg.content
                      ) : (
                        <ReactMarkdown>{msg.content || ''}</ReactMarkdown>
                      )}
                      
                      {msg.retrieval?.sources?.length > 0 && (
                        <div className="sources-container">
                          <div className="sources-title">
                            <span>Sumber Konteks</span>
                          </div>
                          <ul className="sources-list">
                            {msg.retrieval.sources.map((src, idx) => (
                              <li key={idx} className="source-card">
                                <span>📄 {src.source} (Hal. {src.page})</span>
                                {src.score && (
                                  <span className="relevance-badge">
                                    {(src.score).toFixed(3)}
                                  </span>
                                )}
                              </li>
                            ))}
                          </ul>
                        </div>
                      )}
                    </div>
                  </div>
                ))}
                
                {isLoading && (
                  <div className="message bot">
                    <div className="assistant-avatar">
                      <Bot size={20} />
                    </div>
                    <div className="message-body">
                      <div className="loading-indicator">
                        <span></span>
                        <span></span>
                        <span></span>
                      </div>
                    </div>
                  </div>
                )}
                <div ref={messagesEndRef} />
              </>
            )}
          </div>
        </section>

        <footer className="composer-area">
          <div className="composer-wrapper">
            <form onSubmit={handleSubmit} className="composer">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Tanyakan materi Jaringan Komputer..."
                disabled={isLoading}
              />
              <button 
                type="submit" 
                disabled={!input.trim() || isLoading}
                className="send-button"
              >
                <Send size={18} />
              </button>
            </form>
            <div className="disclaimer">
              Chatbot dapat membuat kesalahan. Jadikan sebagai pendamping belajar, bukan sumber tunggal.
            </div>
          </div>
        </footer>
      </main>
    </div>
  );
}

export default App;
