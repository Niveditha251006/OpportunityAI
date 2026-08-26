import { useMemo, useState } from 'react'
import './App.css'

type Opportunity = {
  title: string
  type: string
  provider: string
  amount: string
  match: number
  deadline: string
  tags: string[]
  reason: string
}

const opportunities: Opportunity[] = [
  {
    title: 'National Merit Scholarship',
    type: 'Scholarship',
    provider: 'Education Support Foundation',
    amount: '₹50,000',
    match: 96,
    deadline: '30 Sep 2026',
    tags: ['Scholarship', 'Engineering', 'Financial Aid'],
    reason: 'Strong match for your education needs, academic background and financial-support requirement.'
  },
  {
    title: 'FutureTech Student Internship',
    type: 'Internship',
    provider: 'FutureTech Labs',
    amount: '₹15,000/month',
    match: 91,
    deadline: '15 Sep 2026',
    tags: ['Python', 'Backend', 'Internship'],
    reason: 'Matches your technical interests and gives practical software-development experience.'
  },
  {
    title: 'AI for Social Good Challenge',
    type: 'Competition',
    provider: 'Innovation Network',
    amount: '₹1,00,000 prize',
    match: 88,
    deadline: '10 Oct 2026',
    tags: ['AI', 'Innovation', 'Social Impact'],
    reason: 'Your problem-solving interests align strongly with an AI solution focused on social impact.'
  },
  {
    title: 'Women in Technology Grant',
    type: 'Grant',
    provider: 'Digital Futures Initiative',
    amount: '₹75,000',
    match: 84,
    deadline: '22 Oct 2026',
    tags: ['Technology', 'Education', 'Grant'],
    reason: 'A strong educational-support opportunity for students pursuing technology careers.'
  },
  {
    title: 'Open Source Fellowship',
    type: 'Fellowship',
    provider: 'Open Innovation Community',
    amount: '₹40,000',
    match: 79,
    deadline: '5 Nov 2026',
    tags: ['GitHub', 'Open Source', 'Development'],
    reason: 'Useful for building industry experience and strengthening your developer portfolio.'
  },
  {
    title: 'Emerging Developer Scholarship',
    type: 'Scholarship',
    provider: 'CodeForward',
    amount: '₹30,000',
    match: 76,
    deadline: '18 Nov 2026',
    tags: ['Coding', 'Engineering', 'Scholarship'],
    reason: 'Relevant to engineering students developing software and programming skills.'
  }
]

function App() {
  const [profile, setProfile] = useState('')
  const [searched, setSearched] = useState(false)
  const [filter, setFilter] = useState('All')
  const [saved, setSaved] = useState<string[]>([])

  const filtered = useMemo(() => {
    if (filter === 'All') return opportunities
    return opportunities.filter(o => o.type === filter)
  }, [filter])

  const runMatch = () => {
    if (profile.trim()) setSearched(true)
  }

  const toggleSaved = (title: string) => {
    setSaved(prev =>
      prev.includes(title) ? prev.filter(x => x !== title) : [...prev, title]
    )
  }

  return (
    <div className="app">
      <nav className="nav">
        <div className="brand">
          <div className="brandIcon">✦</div>
          <div>
            <strong>Opportunity<span>AI</span></strong>
            <small>Discover your next opportunity</small>
          </div>
        </div>
        <div className="navLinks">
          <a href="#discover">Discover</a>
          <a href="#opportunities">Opportunities</a>
          <a href="#impact">Impact</a>
        </div>
        <button className="profileBtn">Student Profile</button>
      </nav>

      <main>
        <section className="hero" id="discover">
          <div className="heroText">
            <div className="eyebrow">AI-POWERED OPPORTUNITY DISCOVERY</div>
            <h1>Find opportunities<br /><span>meant for you.</span></h1>
            <p>
              OpportunityAI helps students discover scholarships, internships,
              grants and competitions that match their unique background and goals.
            </p>
            <div className="trust">
              <span>✓ Personalized matching</span>
              <span>✓ Eligibility-aware</span>
              <span>✓ Student-first</span>
            </div>
          </div>

          <div className="profileCard">
            <div className="cardTop">
              <div>
                <h2>Tell us about yourself</h2>
                <p>The more you share, the better we can match.</p>
              </div>
              <div className="aiBadge">✦ AI</div>
            </div>

            <textarea
              value={profile}
              onChange={e => setProfile(e.target.value)}
              placeholder="Example: I'm a first-generation engineering student from a rural family. My annual family income is ₹2.5 lakh and I need financial support for my education. I'm interested in Python and AI..."
            />

            <div className="chips">
              <button onClick={() => setProfile('I am an engineering student looking for scholarships and financial support for my education.')}>🎓 Education</button>
              <button onClick={() => setProfile('I am a Python developer interested in internships and software engineering opportunities.')}>💻 Technology</button>
              <button onClick={() => setProfile('I want opportunities that help me build solutions with meaningful social impact.')}>🌱 Social Impact</button>
            </div>

            <button className="matchBtn" onClick={runMatch}>
              Find My Opportunities <span>→</span>
            </button>
          </div>
        </section>

        {searched && (
          <section className="results" id="opportunities">
            <div className="resultHeader">
              <div>
                <div className="eyebrow">PERSONALIZED FOR YOU</div>
                <h2>Your Opportunity Matches</h2>
                <p>AI-ranked opportunities based on your profile.</p>
              </div>
              <div className="stat">
                <strong>{opportunities.length}</strong>
                <span>matches found</span>
              </div>
            </div>

            <div className="filters">
              {['All', 'Scholarship', 'Internship', 'Competition', 'Grant', 'Fellowship'].map(f => (
                <button
                  key={f}
                  className={filter === f ? 'active' : ''}
                  onClick={() => setFilter(f)}
                >
                  {f}
                </button>
              ))}
            </div>

            <div className="opportunityGrid">
              {filtered.map(op => (
                <article className="opportunity" key={op.title}>
                  <div className="opTop">
                    <div className="type">{op.type}</div>
                    <button className="save" onClick={() => toggleSaved(op.title)}>
                      {saved.includes(op.title) ? '♥' : '♡'}
                    </button>
                  </div>

                  <h3>{op.title}</h3>
                  <p className="provider">{op.provider}</p>

                  <div className="matchRow">
                    <div className="score">{op.match}%</div>
                    <div>
                      <strong>Match score</strong>
                      <div className="bar"><i style={{ width: `${op.match}%` }} /></div>
                    </div>
                  </div>

                  <div className="details">
                    <span>💰 {op.amount}</span>
                    <span>📅 {op.deadline}</span>
                  </div>

                  <div className="tags">
                    {op.tags.map(tag => <span key={tag}>{tag}</span>)}
                  </div>

                  <div className="why">
                    <strong>✦ Why this matches</strong>
                    <p>{op.reason}</p>
                  </div>

                  <button className="viewBtn">View Opportunity →</button>
                </article>
              ))}
            </div>
          </section>
        )}

        <section className="impact" id="impact">
          <div>
            <div className="eyebrow">THE PROBLEM WE SOLVE</div>
            <h2>Opportunity shouldn't depend on <span>who you know.</span></h2>
            <p>
              Thousands of students miss scholarships, internships and programs
              simply because relevant opportunities are scattered across the internet.
              OpportunityAI turns that search into a personalized discovery experience.
            </p>
          </div>
          <div className="impactStats">
            <div><strong>12+</strong><span>Opportunities indexed</span></div>
            <div><strong>96%</strong><span>Top match score</span></div>
            <div><strong>1</strong><span>Personalized dashboard</span></div>
          </div>
        </section>
      </main>

      <footer>
        <strong>OpportunityAI</strong>
        <span>AI-powered opportunity discovery for every student.</span>
        <span>Built for Hackathon 2026 • © 2026</span>
      </footer>
    </div>
  )
}

export default App
