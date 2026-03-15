import { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import './App.css'; 

function App() {
  const [text, setText] = useState('');
  const [mode, setMode] = useState('business');
  const [feedback, setFeedback] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isDarkMode, setIsDarkMode] = useState(true);

  const theme = {
    bg: isDarkMode ? '#0f172a' : '#f8fafc',
    card: isDarkMode ? '#1e293b' : '#ffffff',
    text: isDarkMode ? '#f8fafc' : '#0f172a',
    border: isDarkMode ? '#334155' : '#e2e8f0',
    input: isDarkMode ? '#1e293b' : '#ffffff',
    accent: '#38bdf8'
  };

  const handleSubmit = async () => {
    if (!text.trim()) return;
    setIsLoading(true);
    setFeedback(''); 
    try {
      const response = await fetch('https://ai-writing-coach-api.onrender.com/api/analyze-text', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text, mode })
      });
      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      while (true) {
        const { value, done } = await reader.read();
        if (done) break;
        setFeedback((prev) => prev + decoder.decode(value, { stream: true }));
      }
    } catch (error) {
      setFeedback("⚠️ **Error:** Backend connection failed or quota exceeded.");
    } finally { setIsLoading(false); }
  };

  return (
    <div className="app-container" style={{ 
      height: '100vh', 
      width: '100%', 
      display: 'flex', 
      flexDirection: 'column',
      backgroundColor: theme.bg, 
      color: theme.text,
      overflow: 'hidden', 
      fontFamily: 'Inter, system-ui, sans-serif',
      transition: 'background-color 0.3s ease'
    }}>
      
      {/* 1. Header Row */}
      <header className="app-header" style={{ 
        height: '60px', 
        padding: '0 2rem', 
        display: 'flex', 
        justifyContent: 'space-between', 
        alignItems: 'center',
        borderBottom: `1px solid ${theme.border}`,
        backgroundColor: theme.card
      }}>
        <div className="header-controls" style={{ display: 'flex', alignItems: 'center', gap: '15px' }}>
          <h2 style={{ margin: 0, color: theme.accent, letterSpacing: '1px' }}>COACH.AI</h2>
          <select 
            value={mode} 
            onChange={(e) => setMode(e.target.value)}
            style={{ padding: '5px 10px', borderRadius: '6px', backgroundColor: theme.bg, color: theme.text, border: `1px solid ${theme.border}` }}
          >
            <option value="academic">Academic Mode</option>
            <option value="business">Business Mode</option>
            <option value="creative">Creative Mode</option>
          </select>
        </div>
        <button 
          onClick={() => setIsDarkMode(!isDarkMode)}
          style={{ background: 'none', border: `1px solid ${theme.border}`, color: theme.text, padding: '5px 15px', borderRadius: '20px', cursor: 'pointer' }}
        >
          {isDarkMode ? '🌙 Dark' : '☀️ Light'}
        </button>
      </header>

      {/* 2. Main Workspace */}
      <main className="main-workspace" style={{ display: 'flex', flex: 1, padding: '2rem', gap: '2rem', overflow: 'hidden' }}>
        
        {/* Left Pane: Editor */}
        <div style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: '15px', minHeight: 0 }}>
          <textarea 
            className="editor-textarea"
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Type your content here..."
            style={{ 
              flex: 1, 
              padding: '2rem', 
              fontSize: '1.1rem',
              lineHeight: '1.6',
              borderRadius: '12px', 
              backgroundColor: theme.input, 
              color: theme.text, 
              border: `1px solid ${theme.border}`,
              outline: 'none',
              resize: 'none',
              boxShadow: 'inset 0 2px 10px rgba(0,0,0,0.1)',
              overflowY: 'auto' /* ADDED THIS: Forces the scrollbar on the left input box */
            }}
          />
          <button 
            onClick={handleSubmit} 
            disabled={isLoading}
            style={{ 
              height: '50px',
              minHeight: '50px',
              backgroundColor: isLoading ? '#475569' : theme.accent, 
              color: '#0f172a', 
              fontWeight: 'bold', 
              border: 'none', 
              borderRadius: '8px', 
              cursor: 'pointer',
              fontSize: '1rem',
              transition: 'transform 0.1s'
            }}
          >
            {isLoading ? 'ANALYZING...' : 'RUN COACH ANALYSIS'}
          </button>
        </div>

        {/* Right Pane: Feedback Area */}
        <div className="feedback-pane" style={{ 
          flex: 1,
          display: 'flex', 
          flexDirection: 'column', 
          backgroundColor: theme.card, 
          borderRadius: '12px', 
          border: `1px solid ${theme.border}`,
          overflow: 'hidden',
          minHeight: 0 /* ADDED THIS: Prevents the flex container from stretching off-screen */
        }}>
          <div style={{ padding: '15px 20px', borderBottom: `1px solid ${theme.border}`, fontWeight: 'bold', color: theme.accent }}>
            COACH'S FEEDBACK
          </div>
          
          <div className="feedback-content" style={{ 
            flex: 1, 
            padding: '20px', 
            overflowY: 'auto' /* ALREADY HERE: Forces the scrollbar on the right feedback box */
          }}>
            {feedback ? (
              <ReactMarkdown>{feedback}</ReactMarkdown>
            ) : (
              <div style={{ opacity: 0.5, textAlign: 'center', marginTop: '20%' }}>
                <p>No analysis yet.</p>
                <small>Write something on the left and click Run.</small>
              </div>
            )}
          </div>
        </div>

      </main>

      {/* 3. Footer */}
      <footer style={{ 
        padding: '10px 2rem', 
        fontSize: '0.8rem', 
        display: 'flex', 
        alignItems: 'center', 
        justifyContent: 'space-between',
        borderTop: `1px solid ${theme.border}`,
        opacity: 0.6,
        backgroundColor: theme.bg
      }}>
        <span>Status: {isLoading ? 'Processing via Groq/Llama 3...' : 'Ready'}</span>
        <span>Word Count: {text.trim().split(/\s+/).filter(Boolean).length}</span>
      </footer>

    </div>
  );
}

export default App;