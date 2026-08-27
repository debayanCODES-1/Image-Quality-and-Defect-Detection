const darkCards = [
  { title: 'Scan', subtitle: 'Records, ID Card, Measure, Count, Passport..', icon: 'scan', accent: true },
  { title: 'Update', subtitle: 'Sign, Write, Insert Images, Highlight, Hide, Scan..', icon: 'update' },
  { title: 'Convert', subtitle: 'PDF, Image, Word, Text, Excel, Presentation', icon: 'convert' },
  { title: 'Ask AI', subtitle: 'Recap, Complete Writing, Make Brief, Simplify...', icon: 'ai' },
]

const lightCards = [
  { title: 'Scan', subtitle: 'Records, ID Card, Measure, Count, Passport..', icon: 'scan', accent: true },
  { title: 'Update', subtitle: 'Sign, Write, Insert Images, Highlight, Hide, Scan..', icon: 'update' },
  { title: 'Convert', subtitle: 'PDF, Image, Word, Text, Excel, Presentation', icon: 'convert' },
  { title: 'Ask AI', subtitle: 'Recap, Complete Writing, Make Brief, Simplify...', icon: 'ai' },
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

function FeatureCard({ title, subtitle, icon, accent }) {
  return (
    <div className={`feature-card ${accent ? 'accent' : ''}`}>
      <div className="feature-icon">
        <Icon type={icon} />
      </div>
      <h3>{title}</h3>
      <p>{subtitle}</p>
    </div>
  )
}

function Phone({ dark }) {
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
        <h1>PDF Scanner</h1>
        <div className="header-actions">
          <button className="mini-circle" aria-label="favorite">
            <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3.9 14.6 9l5.7.8-4.1 4 1 5.6-5.2-2.7-5.2 2.7 1-5.6-4.1-4 5.7-.8L12 3.9Z" stroke="currentColor" strokeWidth="1.7" fill="none" strokeLinecap="round" strokeLinejoin="round" /></svg>
          </button>
          <button className="mini-circle" aria-label="notifications">
            <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 16h12l-1.3-1.8V10a4.7 4.7 0 0 0-9.4 0v4.2L6 16Zm4 4h4" stroke="currentColor" strokeWidth="1.7" fill="none" strokeLinecap="round" strokeLinejoin="round" /></svg>
          </button>
        </div>
      </header>

      <main className="phone-grid">
        {(dark ? darkCards : lightCards).map((card) => (
          <FeatureCard key={card.title} {...card} />
        ))}
      </main>

      <div className="recent-card">
        <div className="recent-preview">
          <div className="pdf-badge">PDF</div>
          <div className="pdf-meta">
            <strong>PDF Scanner 131225</strong>
            <span>13 Dec, 2025 • 11:23PM</span>
          </div>
        </div>
        <button className="more-button" aria-label="More actions">
          <Icon type="more" />
        </button>
      </div>

      <div className="bottom-actions">
        <button className="floating-action circle">
          <Icon type="plus" />
        </button>
        <button className="floating-action camera">
          <Icon type="camera" />
        </button>
      </div>
    </div>
  )
}

function App() {
  return (
    <div className="page-shell">
      <div className="phone-stage">
        <Phone dark />
        <Phone />
      </div>
    </div>
  )
}

export default App
