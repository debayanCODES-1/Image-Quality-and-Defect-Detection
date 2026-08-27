import { useEffect, useRef, useState } from 'react'
import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || (import.meta.env.DEV ? 'http://localhost:8000' : '/api')

const cards = [
  { title: 'Analyze', subtitle: 'Check blur, light, noise, contrast and defects', icon: 'scan', accent: true },
  { title: 'History', subtitle: 'Review your latest image quality assessments', icon: 'history' },
  { title: 'Features', subtitle: 'Inspect the signals behind every quality score', icon: 'convert' },
  { title: 'Model', subtitle: 'See whether the trained model is available', icon: 'ai' },
]

function Icon({ type }) {
  const commonProps = {
    width: 30,
    height: 30,
    viewBox: '0 0 24 24',
    fill: 'none',
    stroke: 'currentColor',
    strokeWidth: 1.8,
    strokeLinecap: 'round',
    strokeLinejoin: 'round',
  }

  switch (type) {
    case 'scan':
      return (
        <svg {...commonProps}>
          <rect x="3.5" y="4.5" width="17" height="15" rx="3.5" />
          <path d="M7 11.5h10M8 8.5h8M8 15.5h8" />
          <circle cx="12" cy="12" r="4.3" />
        </svg>
      )
    case 'update':
      return (
        <svg {...commonProps}>
          <path d="M5 9.5V6.8A1.8 1.8 0 0 1 6.8 5h10.4A1.8 1.8 0 0 1 19 6.8v10.4a1.8 1.8 0 0 1-1.8 1.8H14" />
          <path d="M8 8h8M8 12h8M8 16h5" />
          <path d="M18.5 6.5 20 5v5h-5l2.2-2.4" />
        </svg>
      )
    case 'convert':
      return (
        <svg {...commonProps}>
          <path d="M7 5.5h8l4 4V18a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V7.5a2 2 0 0 1 2-2Z" />
          <path d="M15 5.5v4h4" />
          <path d="M8 13h8M8 16h6" />
        </svg>
      )
    case 'ai':
      return (
        <svg {...commonProps}>
          <path d="M8 8.5c0-1.7 1.3-3 3-3h2c1.7 0 3 1.3 3 3v1.8c0 1.4-1.1 2.5-2.5 2.5H11A2.5 2.5 0 0 1 8.5 10.3V8.5Z" />
          <path d="M12 12v4.5M9.5 16h5" />
          <path d="M5 18.5c.8-1.5 2.1-2.5 3.8-2.5M19 18.5c-.8-1.5-2.1-2.5-3.8-2.5" />
        </svg>
      )
    case 'history':
      return (
        <svg {...commonProps}>
          <path d="M5 6.5h14M5 12h14M5 17.5h9" />
          <circle cx="18" cy="17.5" r="2.5" />
          <path d="m20 19.5 1.5 1.5" />
        </svg>
      )
    case 'search':
      return (
        <svg {...commonProps}>
          <circle cx="11" cy="11" r="5" />
          <path d="m16 16 3 3" />
        </svg>
      )
    case 'plus':
      return (
        <svg {...commonProps}>
          <path d="M12 5v14M5 12h14" />
        </svg>
      )
    case 'camera':
      return (
        <svg {...commonProps}>
          <path d="M4.5 9.5A2.5 2.5 0 0 1 7 7h1.2l.8-1.4h5l.8 1.4H17a2.5 2.5 0 0 1 2.5 2.5v7A2.5 2.5 0 0 1 17 19H7a2.5 2.5 0 0 1-2.5-2.5v-7Z" />
          <circle cx="12" cy="13" r="3" />
        </svg>
      )
    case 'more':
      return (
        <svg {...commonProps}>
          <circle cx="6" cy="12" r="1.4" fill="currentColor" stroke="none" />
          <circle cx="12" cy="12" r="1.4" fill="currentColor" stroke="none" />
          <circle cx="18" cy="12" r="1.4" fill="currentColor" stroke="none" />
        </svg>
      )
    default:
      return null
  }
}

function FeatureCard({ title, subtitle, icon, accent, onClick }) {
  return (
    <button className={`feature-card ${accent ? 'accent' : ''}`} onClick={onClick}>
      <div className="feature-icon">
        <Icon type={icon} />
      </div>
      <h3>{title}</h3>
      <p>{subtitle}</p>
    </button>
  )
}

function Phone({ dark, history, result, onScan, onHistory, onNotice }) {
  const inputRef = useRef(null)
  const [selectedFile, setSelectedFile] = useState(null)
  const [isUploading, setIsUploading] = useState(false)
  const [error, setError] = useState('')
  const [isFavorite, setIsFavorite] = useState(false)

  const chooseFile = () => inputRef.current?.click()
  const handleFile = (event) => {
    const file = event.target.files?.[0]
    if (!file) return
    setSelectedFile(file)
    setError('')
    onScan(file)
  }

  const upload = async () => {
    if (!selectedFile) return chooseFile()
    setIsUploading(true)
    setError('')
    const body = new FormData()
    body.append('file', selectedFile)
    try {
      const { data } = await axios.post(`${API_BASE_URL}/analyze`, body)
      onScan(selectedFile, true, data)
    } catch (uploadError) {
      setError(uploadError.response?.data?.detail || 'Could not analyze this image.')
    } finally {
      setIsUploading(false)
    }
  }

  return (
    <div className={`phone-shell ${dark ? 'dark' : 'light'}`}>
      <div className="status-bar">
        <span>9:41</span>
        <div className="status-icons">
          <span className="signal"><i /><i /><i /></span>
          <span className="wifi">◔</span>
          <span className="battery">▮</span>
        </div>
      </div>

      <header className="phone-header">
        <div>
          <p className="eyebrow">IMAGE QUALITY</p>
          <h1>{dark ? 'Quality check' : 'Recent scans'}</h1>
        </div>
        <div className="header-actions">
          <button className={`mini-circle ${isFavorite ? 'selected' : ''}`} aria-label="favorite" onClick={() => {
            setIsFavorite((value) => !value)
            onNotice(isFavorite ? 'Removed from favorites' : 'Saved to favorites')
          }}>
            <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3.9 14.6 9l5.7.8-4.1 4 1 5.6-5.2-2.7-5.2 2.7 1-5.6-4.1-4 5.7-.8L12 3.9Z" stroke="currentColor" strokeWidth="1.7" fill="none" strokeLinecap="round" strokeLinejoin="round" /></svg>
          </button>
          <button className="mini-circle" aria-label="notifications" onClick={() => onNotice('Notifications are up to date')}>
            <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 16h12l-1.3-1.8V10a4.7 4.7 0 0 0-9.4 0v4.2L6 16Zm4 4h4" stroke="currentColor" strokeWidth="1.7" fill="none" strokeLinecap="round" strokeLinejoin="round" /></svg>
          </button>
        </div>
      </header>

      <main className="phone-grid">
        {cards.map((card, index) => (
          <FeatureCard key={card.title} {...card} onClick={index === 0 ? chooseFile : index === 1 ? onHistory : () => onNotice(index === 2 ? 'Feature signals appear after an analysis' : 'Model status is shown by the API badge')} />
        ))}
      </main>

      {dark && (
        <div className="upload-panel">
          <input ref={inputRef} type="file" accept="image/png,image/jpeg,image/bmp,image/tiff" onChange={handleFile} />
          <div className="upload-copy">
            <span className="upload-label">{selectedFile ? selectedFile.name : 'Choose an image to inspect'}</span>
            <span className="upload-hint">PNG, JPG, BMP or TIFF</span>
          </div>
          <button className="analyze-button" onClick={upload} disabled={isUploading}>
            {isUploading ? 'Checking...' : 'Analyze'}
          </button>
        </div>
      )}

      {!dark && result && (
        <div className={`result-banner ${result.quality_score >= 70 ? 'good' : 'warning'}`}>
          <div><span className="result-score">{result.quality_score}</span><span>/100 quality score</span></div>
          <div className="result-labels">
            <strong>{result.quality_label}</strong>
            {result.tags?.length > 0 && <span>{result.tags.slice(0, 2).map((tag) => tag.tag?.en || tag.tag).join(' / ')}</span>}
          </div>
        </div>
      )}

      <div className="recent-card">
        <div className="recent-preview">
          <div className="pdf-badge">{result ? result.quality_score : 'IQ'}</div>
          <div className="pdf-meta">
            <strong>{result?.filename || history[0]?.filename || 'No image analyzed yet'}</strong>
            <span>{result ? `${result.quality_label} quality` : history.length ? `${history.length} saved assessment${history.length > 1 ? 's' : ''}` : 'Your results will appear here'}</span>
          </div>
        </div>
        <button className="more-button" aria-label="More actions" onClick={() => onNotice(history.length ? `${history.length} assessment${history.length > 1 ? 's' : ''} saved` : 'No saved assessments yet')}>
          <Icon type="more" />
        </button>
      </div>

      <div className="bottom-actions">
        <button className="floating-action circle" aria-label="Choose an image" onClick={chooseFile}>
          <Icon type="plus" />
        </button>
        <button className="floating-action camera" aria-label="Analyze an image" onClick={chooseFile}>
          <Icon type="camera" />
        </button>
      </div>
    </div>
  )
}

function App() {
  const [history, setHistory] = useState([])
  const [result, setResult] = useState(null)
  const [apiStatus, setApiStatus] = useState('connecting')
  const [notice, setNotice] = useState('')
  const [installPrompt, setInstallPrompt] = useState(null)

  useEffect(() => {
    const handleInstallPrompt = (event) => {
      event.preventDefault()
      setInstallPrompt(event)
    }
    window.addEventListener('beforeinstallprompt', handleInstallPrompt)
    return () => window.removeEventListener('beforeinstallprompt', handleInstallPrompt)
  }, [])

  useEffect(() => {
    const loadHistory = async () => {
      try {
        const [healthResponse, historyResponse] = await Promise.all([
          axios.get(`${API_BASE_URL}/health`),
          axios.get(`${API_BASE_URL}/history`),
        ])
        setApiStatus(healthResponse.data.status === 'ok' ? 'online' : 'offline')
        setHistory(historyResponse.data)
      } catch {
        setApiStatus('offline')
      }
    }
    loadHistory()
  }, [])

  const handleScan = (file, refresh, analysis) => {
    if (!refresh) return
    axios.get(`${API_BASE_URL}/history`).then(({ data }) => {
      setHistory(data)
      setResult(analysis ? { ...analysis, filename: file.name } : data[0] ? { ...data[0], filename: file.name } : null)
    }).catch(() => setApiStatus('offline'))
  }

  const showNotice = (message) => {
    setNotice(message)
    window.setTimeout(() => setNotice(''), 2400)
  }

  const installApp = async () => {
    if (!installPrompt) {
      showNotice('Use your browser menu to add this app to your home screen')
      return
    }
    installPrompt.prompt()
    await installPrompt.userChoice
    setInstallPrompt(null)
  }

  return (
    <div className="page-shell">
      <div className="workspace-label"><span className={`status-dot ${apiStatus}`} /> API {apiStatus}</div>
      <button className="install-button" onClick={installApp} aria-label="Install mobile app">
        <span aria-hidden="true">+</span> Install app
      </button>
      {notice && <div className="notice" role="status">{notice}</div>}
      <div className="phone-stage">
        <Phone dark history={history} result={result} onScan={handleScan} onHistory={() => { setNotice('History refreshed'); }} onNotice={showNotice} />
        <Phone history={history} result={result} onScan={handleScan} onHistory={() => { setNotice('History refreshed'); }} onNotice={showNotice} />
      </div>
    </div>
  )
}

export default App
