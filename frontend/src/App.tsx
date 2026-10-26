import { useEffect, useMemo, useState } from 'react'
import './App.css'
import type { Opportunity } from './types/opportunity'
import {
  matchOpportunities,
  matchOpportunitiesFromText,
  type MatchResult,
  type StudentProfileInput,
} from './services/matchService'
import { getOpportunities } from './services/opportunityService'
import {
  getCareerGoals,
  generateRoadmap,
  getRoadmap,
  completeRoadmapTask,
  getLearningProgress,
  sendCareerChatMessage,
  type CareerGoal,
  type RoadmapTask,
  type LearningProgress,
  type CareerChatResponse,
  type CareerChatMessage,
} from './services/careerService'

const exampleStudentProfile = `I am an undergraduate BTech student studying Computer Science and Engineering in Andhra Pradesh, India. My annual family income is ₹250000. I live in a rural area and I am the first person in my family to attend college. My interests include Python, artificial intelligence, machine learning, and software development. I am looking for scholarships and internships related to technology.`

function App() {
  const [profile, setProfile] = useState('')
  const [searched, setSearched] = useState(false)
  const [opportunities, setOpportunities] = useState<Opportunity[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [filter, setFilter] = useState('All')
  const [saved, setSaved] = useState<number[]>([])
  const [matches, setMatches] = useState<MatchResult[]>([])
  const [matching, setMatching] = useState(false)
  const [chatMessage, setChatMessage] = useState('')
  const [chatReplies, setChatReplies] = useState<CareerChatResponse[]>([])
  const [chatHistory, setChatHistory] = useState<CareerChatMessage[]>([])
  const [chatLoading, setChatLoading] = useState(false)
  const [chatError, setChatError] = useState('')
  const [careerGoals, setCareerGoals] = useState<CareerGoal[]>([])
  const [selectedGoalId, setSelectedGoalId] = useState<number | null>(null)
  const [roadmapTasks, setRoadmapTasks] = useState<RoadmapTask[]>([])
  const [roadmapLoading, setRoadmapLoading] = useState(false)
  const [roadmapMessage, setRoadmapMessage] = useState('')
  const [extractedProfile, setExtractedProfile] =
    useState<StudentProfileInput | null>(null)
    const [eligibilityDraft, setEligibilityDraft] =
  useState<StudentProfileInput | null>(null)

const [eligibilityUpdating, setEligibilityUpdating] = useState(false)
const [eligibilityMessage, setEligibilityMessage] = useState('')
  const [learningProgress, setLearningProgress] =
    useState<LearningProgress | null>(null)
  const [progressError, setProgressError] = useState('')
  // Load opportunities.
  useEffect(() => {
    const loadOpportunities = async () => {
      try {
        setLoading(true)
        setError('')
        const data = await getOpportunities()
        setOpportunities(data)
      } catch (err) {
        console.error('Error loading opportunities:', err)
        setError('Unable to load opportunities.')
      } finally {
        setLoading(false)
      }
    }

    loadOpportunities()
  }, [])


  // Load career goals and automatically load the selected goal's roadmap.
  useEffect(() => {
    const loadCareerGoals = async () => {
      try {
        const goals = await getCareerGoals()
        setCareerGoals(goals)

        if (goals.length > 0) {
          const firstGoalId = goals[0].id
          setSelectedGoalId(firstGoalId)

          try {
            const roadmap = await getRoadmap(firstGoalId)
            setRoadmapTasks(roadmap.tasks)
            setRoadmapMessage('')
          } catch (err) {
            console.error('Error loading existing roadmap:', err)
            setRoadmapTasks([])
            setRoadmapMessage(
              'No roadmap loaded yet. Generate one to begin.'
            )
          }
        }
      } catch (err) {
        console.error('Error loading career goals:', err)
        setRoadmapMessage('Unable to load career goals.')
      }
    }

    loadCareerGoals()
  }, [])

  // Load learning progress whenever the selected career goal changes.
  useEffect(() => {
    if (selectedGoalId === null) {
      setLearningProgress(null)
      setProgressError('')
      return
    }

    let cancelled = false

    const loadLearningProgress = async () => {
      try {
        setProgressError('')
        const progress = await getLearningProgress(selectedGoalId)
        if (!cancelled) {
          setLearningProgress(progress)
        }
      } catch (err) {
        console.error('Error loading learning progress:', err)
        if (!cancelled) {
          setLearningProgress(null)
          setProgressError('Unable to load learning progress.')
        }
      }
    }

    loadLearningProgress()
    return () => {
      cancelled = true
    }
  }, [selectedGoalId])

  // Filter opportunities.
  const filtered = useMemo(() => {
    if (!searched) {
      if (filter === 'All') {
        return opportunities
      }

      return opportunities.filter(
        (opportunity) =>
          opportunity.type.toLowerCase() === filter.toLowerCase()
      )
    }


const matchedIds = new Set(
  matches
    .filter(
      (match) =>
        match.eligible ||
        match.eligibility_status === 'NEEDS_INFORMATION'
    )
    .map((match) => match.id)
)


    const matchedOpportunities = opportunities.filter((opportunity) =>
      matchedIds.has(opportunity.id)
    )

    if (filter === 'All') {
      return matchedOpportunities
    }

    return matchedOpportunities.filter(
      (opportunity) =>
        opportunity.type.toLowerCase() === filter.toLowerCase()
    )
  }, [filter, matches, opportunities, searched])

  // Match a student profile to opportunities.
  const runMatch = async () => {
    if (!profile.trim()) return

    try {
      setMatching(true)
      setError('')

    const result = await matchOpportunitiesFromText(profile)
setExtractedProfile(result.student_profile)
setEligibilityDraft({ ...result.student_profile })
setMatches(result.matches)
setEligibilityMessage('')
setSearched(true)

      setTimeout(() => {
        document
          .getElementById('opportunities')
          ?.scrollIntoView({ behavior: 'smooth' })
      }, 100)
    } catch (err) {
      console.error('Error matching opportunities:', err)
      setError('Unable to find matching opportunities.')
    } finally {
      setMatching(false)
    }
  }
  const updateEligibility = async () => {
  if (!eligibilityDraft) return

  try {
    setEligibilityUpdating(true)
    setEligibilityMessage('')
    setError('')

    const result = await matchOpportunities(eligibilityDraft)

    setExtractedProfile(result.student_profile)
    setEligibilityDraft({ ...result.student_profile })
    setMatches(result.matches)
    setSearched(true)

    setEligibilityMessage(
      'Eligibility updated successfully. Your opportunity matches have been refreshed.'
    )
  } catch (err) {
    console.error('Error updating eligibility:', err)
    setEligibilityMessage(
      'Unable to update eligibility. Please check that the backend is running and try again.'
    )
  } finally {
    setEligibilityUpdating(false)
  }
}
  const toggleSaved = (id: number) => {
    setSaved((current) =>
      current.includes(id)
        ? current.filter((savedId) => savedId !== id)
        : [...current, id]
    )
  }

  // Load an existing roadmap.
  const loadRoadmap = async (goalId: number) => {
    try {
      setRoadmapLoading(true)
      setRoadmapMessage('')

      const roadmap = await getRoadmap(goalId)
      setRoadmapTasks(roadmap.tasks)
    } catch {
      setRoadmapTasks([])
      setRoadmapMessage('No roadmap loaded yet. Generate one to begin.')
    } finally {
      setRoadmapLoading(false)
    }
  }

  // Generate a roadmap for the selected career goal.
  const handleGenerateRoadmap = async () => {
    if (selectedGoalId === null) return

    try {
      setRoadmapLoading(true)
      setRoadmapMessage('')

      await generateRoadmap(selectedGoalId)
      const roadmap = await getRoadmap(selectedGoalId)
      setRoadmapTasks(roadmap.tasks)
      setRoadmapMessage('Your learning roadmap is ready!')
    } catch (err) {
      setRoadmapMessage(
        err instanceof Error ? err.message : 'Unable to generate roadmap.'
      )
    } finally {
      setRoadmapLoading(false)
    }
  }

  // Save task completion and refresh the roadmap.
  const handleCompleteTask = async (taskId: number) => {
    try {
      setRoadmapLoading(true)
      await completeRoadmapTask(taskId)

      if (selectedGoalId !== null) {
        const roadmap = await getRoadmap(selectedGoalId)
        setRoadmapTasks(roadmap.tasks)

        try {
          const progress = await getLearningProgress(selectedGoalId)
          setLearningProgress(progress)
          setProgressError('')
        } catch (progressErr) {
          console.error('Error refreshing learning progress:', progressErr)
        }
      }

      setRoadmapMessage('Task completion saved.')
    } catch {
      setRoadmapMessage('Unable to save task completion.')
    } finally {
      setRoadmapLoading(false)
    }
  }
const handleSendCareerMessage = async (
  event: React.FormEvent<HTMLFormElement>
) => {
  event.preventDefault()

  const message = chatMessage.trim()
  if (!message || chatLoading) return

  setChatLoading(true)
  setChatError('')

  try {
    const result = await sendCareerChatMessage(message, chatHistory)
    setChatReplies((previous) => [...previous, result])

setChatHistory((previous) => [
  ...previous,
  { role: 'user', content: message },
  { role: 'assistant', content: result.reply },
])
    setChatMessage('')
  } catch (err) {
    setChatError(
      err instanceof Error
        ? err.message
        : 'Unable to get career guidance right now.'
    )
  } finally {
    setChatLoading(false)
  }
}
  const selectedGoal = careerGoals.find(
    (goal) => goal.id === selectedGoalId
  )

  const completedTasks = roadmapTasks.filter(
    (task) => task.status === 'COMPLETED'
  ).length

  return (
    <div className="app">
      <header className="navbar">
        <div className="logo">OpportunityAI</div>

        <nav>
          <a href="#discover">Discover</a>
          <a href="#opportunities">Opportunities</a>
          <a href="#roadmap">Career Roadmap</a>
          <a href="#impact">Impact</a>
          <a href="#career-chat">Career Chat</a>
        </nav>
      </header>

      <main>
        <section id="discover" className="hero">
          <div className="heroContent">
            <p className="eyebrow">AI-POWERED OPPORTUNITY DISCOVERY</p>

            <h1>
              Find opportunities
              <br />
              meant for you.
            </h1>

            <p className="heroText">
              OpportunityAI helps students discover scholarships,
              internships, grants and competitions that match their
              unique background and goals.
            </p>

            <div className="featureRow">
              <span>✓ Personalized matching</span>
              <span>✓ Eligibility-aware</span>
              <span>✓ Student-first</span>
            </div>
          </div>
        </section>

        <section className="profileSection">
          <div className="sectionHeader">
            <p className="eyebrow">Tell us about yourself</p>
            <p className="sectionSubtitle">
              The more you share, the better we can match.
            </p>
          </div>

          <div className="profileCard">
            <div className="aiBadge">✦ AI</div>


<label className="profileInputLabel" htmlFor="student-profile">
  Your student profile
</label>

<p className="profileHelpText">
  Tell us about your education, family income, location,
  background, interests, and goals. Share only details you
  are comfortable providing.
</p>

<textarea
  id="student-profile"
  value={profile}
  onChange={(event) => setProfile(event.target.value)}
  placeholder="Example: I am an undergraduate BTech student studying CSE in Andhra Pradesh..."
  aria-describedby="profile-guidance"
  rows={7}
/>

<p id="profile-guidance" className="profileGuidance">
  Include any details you know. Leave unknown information out;
  OpportunityAI should not guess it.
</p>

<div className="profileHints">
  <span>🎓 Education</span>
  <span>💰 Family income</span>
  <span>📍 State</span>
  <span>💻 Interests</span>
  <span>🌍 Background</span>
</div>

<button
  type="button"
  className="profileExampleBtn"
  onClick={() => setProfile(exampleStudentProfile)}
>
  Use example profile
</button>


            <button
              type="button"
              className="matchBtn"
              onClick={runMatch}
              disabled={!profile.trim() || matching}
            >
              {matching ? 'Finding...' : 'Find My Opportunities ✦'}
            </button>

            {error && <p className="errorMessage">{error}</p>}
          </div>

        </section>

        {extractedProfile && searched && (
          <section className="extractedProfileSection">
            <div className="sectionHeader">
              <p className="eyebrow">PROFILE REVIEW</p>
              <h2>What OpportunityAI understood</h2>
              <p className="sectionSubtitle">
                Review the details extracted from your description.
                Unknown information is shown as not provided.
              </p>
            </div>

            <div className="extractedProfileGrid">
              <div className="extractedProfileItem">
                <span>Education level</span>
                <strong>{extractedProfile.education_level || 'Not provided'}</strong>
              </div>
               <div className="eligibilityEditor">
  <h3>Update your eligibility details</h3>

  <p>
    Correct any extracted information or provide missing details.
    Choose "Not provided" if you don't know the answer.
  </p>

  <div className="eligibilityFormGrid">
    <label className="eligibilityField">
      <span>Annual family income (₹)</span>

      <input
        type="number"
        min="0"
        step="1"
        value={eligibilityDraft?.annual_income ?? ''}
        onChange={(event) => {
          const value = event.target.value

          setEligibilityDraft((current) =>
            current
              ? {
                  ...current,
                  annual_income:
                    value === '' ? null : Number(value),
                }
              : current
          )
        }}
        placeholder="Enter annual income"
      />
    </label>

    <label className="eligibilityField">
      <span>Rural background</span>

      <select
        value={
          eligibilityDraft?.rural == null
            ? ''
            : String(eligibilityDraft.rural)
        }
        onChange={(event) => {
          const value = event.target.value

          setEligibilityDraft((current) =>
            current
              ? {
                  ...current,
                  rural:
                    value === '' ? null : value === 'true',
                }
              : current
          )
        }}
      >
        <option value="">Not provided</option>
        <option value="true">Yes — rural</option>
        <option value="false">No — urban</option>
      </select>
    </label>

    <label className="eligibilityField">
      <span>First-generation college student</span>

      <select
        value={
          eligibilityDraft?.first_generation == null
            ? ''
            : String(eligibilityDraft.first_generation)
        }
        onChange={(event) => {
          const value = event.target.value

          setEligibilityDraft((current) =>
            current
              ? {
                  ...current,
                  first_generation:
                    value === '' ? null : value === 'true',
                }
              : current
          )
        }}
      >
        <option value="">Not provided</option>
        <option value="true">Yes</option>
        <option value="false">No</option>
      </select>
    </label>
  </div>

  <button
    type="button"
    className="matchBtn"
    onClick={updateEligibility}
    disabled={!eligibilityDraft || eligibilityUpdating}
  >
    {eligibilityUpdating
      ? 'Updating...'
      : 'Update Eligibility ✓'}
  </button>

  {eligibilityMessage && (
    <p role="status" aria-live="polite">
      {eligibilityMessage}
    </p>
  )}
</div>
              <div className="extractedProfileItem">
                <span>Field of study</span>
                <strong>{extractedProfile.field || 'Not provided'}</strong>
              </div>

              <div className="extractedProfileItem">
                <span>Annual family income</span>
                <strong>
                  {extractedProfile.annual_income == null
                    ? 'Not provided'
                    : `₹${Number(extractedProfile.annual_income).toLocaleString('en-IN')}`}
                </strong>
              </div>

              <div className="extractedProfileItem">
                <span>State</span>
                <strong>{extractedProfile.state || 'Not provided'}</strong>
              </div>

              <div className="extractedProfileItem">
                <span>Rural background</span>
                <strong>
                  {extractedProfile.rural == null
                    ? 'Not provided'
                    : extractedProfile.rural ? 'Yes' : 'No'}
                </strong>
              </div>

              <div className="extractedProfileItem">
                <span>First-generation student</span>
                <strong>
                  {extractedProfile.first_generation == null
                    ? 'Not provided'
                    : extractedProfile.first_generation ? 'Yes' : 'No'}
                </strong>
              </div>

              <div className="extractedProfileItem">
                <span>Interests</span>
                <strong>
                  {extractedProfile.interests.length
                    ? extractedProfile.interests.join(', ')
                    : 'Not provided'}
                </strong>
              </div>
            </div>
          </section>
        )}

        <section id="opportunities" className="opportunitiesSection">

          <div className="sectionHeader">
            <p className="eyebrow">DISCOVER</p>
            <h2>Opportunities for you</h2>
            <p className="sectionSubtitle">
              Explore opportunities available in our database.
            </p>
          </div>

          <div className="opportunityToolbar">
            <span>{filtered.length} opportunities</span>

            <div className="filters">
              {['All', 'Scholarship', 'Internship', 'Grant', 'Competition'].map(
                (option) => (
                  <button
                    key={option}
                    type="button"
                    className={filter === option ? 'active' : ''}
                    onClick={() => setFilter(option)}
                  >
                    {option}
                  </button>
                )
              )}
            </div>
          </div>

          {loading && (
            <p className="loadingMessage">Loading opportunities...</p>
          )}

          {!loading && filtered.length === 0 && (
            <p className="emptyMessage">
              No matching opportunities found.
            </p>
          )}

          <div className="opportunityGrid">
            {filtered.map((opportunity) => {
              const match = matches.find(
                (item) => item.id === opportunity.id
              )
              const score = match?.match_score ?? 0

              return (
                <article className="opportunityCard" key={opportunity.id}>
                  <div className="cardTop">
                    <span className="opportunityType">
                      {opportunity.type}
                    </span>

                    <button
                      type="button"
                      className="saveBtn"
                      onClick={() => toggleSaved(opportunity.id)}
                      aria-label={
                        saved.includes(opportunity.id)
                          ? 'Remove saved opportunity'
                          : 'Save opportunity'
                      }
                    >
                      {saved.includes(opportunity.id) ? '♥' : '♡'}
                    </button>
                  </div>

                  <h3>{opportunity.title}</h3>
                  <p className="organization">{opportunity.organization}</p>
                  <p className="description">{opportunity.description}</p>

                  <div className="details">
                    <div>
                      <span>Amount</span>
                      <strong>
                        ₹
                        {Number(opportunity.amount).toLocaleString('en-IN')}
                      </strong>
                    </div>

                    <div>
                      <span>Education</span>
                      <strong>
                        {opportunity.education_level || 'Not specified'}
                      </strong>
                    </div>
                  </div>

                  <div className="matchInfo">
                    <div className="matchLabel">
                      <span>AI match score</span>
                      <span>{searched ? `${score}%` : '—'}</span>
                    </div>

                    <div className="matchBar">
                      <div
                        className="matchFill"
                        style={{ width: `${searched ? score : 0}%` }}
                      />
                    </div>
                  </div>

                  {searched && match && (
                    <div className="matchExplanation">

               <p
                  className={
                  match.eligibility_status === 'ELIGIBLE' ||
                 (!match.eligibility_status && match.eligible)
                   ? 'eligibleStatus'
                  : match.eligibility_status === 'NEEDS_INFORMATION'
                  ? 'needsInformationStatus'
                  : 'ineligibleStatus'
                   }
                 >
                {match.eligibility_status === 'NEEDS_INFORMATION'
                ? 'ℹ More information needed to confirm eligibility'
            : match.eligibility_status === 'INELIGIBLE' || !match.eligible
             ? '⚠ Eligibility requirements are not met'
            : '✓ Eligible based on current checks'}
              </p>


                      {match.matched_interests.length > 0 && (
                        <div>
                          <strong>Matched interests</strong>
                          <p>{match.matched_interests.join(', ')}</p>
                        </div>
                      )}

                      {match.explanation.length > 0 && (
                        <div>
                          <strong>Why this result?</strong>
                          <ul>
                            {match.explanation.map((reason, index) => (
                              <li key={index}>{reason}</li>
                            ))}
                          </ul>
                        </div>
                      )}
                    </div>
                  )}

                  <div className="cardActions">
                    <a
                      href={opportunity.application_url || '#'}
                      target="_blank"
                      rel="noreferrer"
                    >
                      Apply Now →
                    </a>

                    <a
                      href={opportunity.source_url || '#'}
                      target="_blank"
                      rel="noreferrer"
                    >
                      View Source
                    </a>
                  </div>
                </article>
              )
            })}
          </div>
        </section>

        <section id="roadmap" className="opportunitiesSection">
          <div className="sectionHeader">
            <p className="eyebrow">YOUR LEARNING JOURNEY</p>
            <h2>Career Roadmap</h2>
            <p className="sectionSubtitle">
              Turn your career goal into small, trackable daily steps.
            </p>
          </div>

          {careerGoals.length === 0 ? (
            <p className="emptyMessage">
              No career goals are available yet. Create a career goal first.
            </p>
          ) : (
            <div className="profileCard">
              <label htmlFor="careerGoal">Choose your career goal</label>

              <select
                id="careerGoal"
                value={selectedGoalId ?? ''}
                onChange={(event) => {
                  const goalId = Number(event.target.value)
                  setSelectedGoalId(goalId)
                  setRoadmapTasks([])
                  setRoadmapMessage('')
                }}
              >
                {careerGoals.map((goal) => (
                  <option key={goal.id} value={goal.id}>
                    {goal.career_path} — {goal.current_skill_level}
                  </option>
                ))}
              </select>

              {selectedGoal && (
                <div className="roadmapGoalInfo">
                  <p>
                    <strong>Career:</strong> {selectedGoal.career_path}
                  </p>
                  <p>
                    <strong>Current level:</strong>{' '}
                    {selectedGoal.current_skill_level}
                  </p>
                  <p>
                    <strong>Daily study time:</strong>{' '}
                    {selectedGoal.daily_minutes} minutes
                  </p>
                </div>
              )}

              <button
                type="button"
                className="matchBtn"
                onClick={handleGenerateRoadmap}
                disabled={roadmapLoading || selectedGoalId === null}
              >
                {roadmapLoading ? 'Please wait...' : 'Generate My Roadmap'}
              </button>

              <button
                type="button"
                className="roadmapLoadBtn"
                onClick={() =>
                  selectedGoalId !== null && loadRoadmap(selectedGoalId)
                }
                disabled={roadmapLoading || selectedGoalId === null}
              >
                Load Existing Roadmap
              </button>

              {roadmapMessage && (
                <p role="status" className="roadmapMessage">
                  {roadmapMessage}
                </p>
              )}

              {roadmapTasks.length > 0 && (
                <div className="roadmapContent">
                  <div className="roadmapProgress">
                    <strong>
                      {completedTasks} of {roadmapTasks.length} tasks completed
                    </strong>

                    <div className="matchBar">
                      <div
                        className="matchFill"
                        style={{
                          width: `${
                            (completedTasks / roadmapTasks.length) * 100
                          }%`,
                        }}
                      />
                    </div>
                  </div>

                  {progressError && (
                    <p className="errorMessage" role="alert">
                      {progressError}
                    </p>
                  )}

                  {learningProgress && (
                    <section className="learningProgressCard" aria-label="Learning progress">
                      <div className="learningProgressHeader">
                        <p className="eyebrow">CONSISTENCY & ACHIEVEMENTS</p>
                        <h3>Your learning progress</h3>
                      </div>

                      <div className="learningStatsGrid">
                        <div className="learningStat">
                          <span>🔥 Current streak</span>
                          <strong>{learningProgress.current_streak} day(s)</strong>
                        </div>
                        <div className="learningStat">
                          <span>🏅 Best streak</span>
                          <strong>{learningProgress.best_streak} day(s)</strong>
                        </div>
                        <div className="learningStat">
                          <span>📅 Active days</span>
                          <strong>{learningProgress.activity_days}</strong>
                        </div>
                      </div>

                      <div className="achievementSection">
                        <h4>Achievements</h4>
                        {learningProgress.achievements.length > 0 ? (
                          <div className="achievementList">
                            {learningProgress.achievements.map((achievement) => (
                              <article className="achievementBadge" key={achievement.code}>
                                <span className="achievementIcon" aria-hidden="true">🏆</span>
                                <div>
                                  <strong>{achievement.title}</strong>
                                  <p>{achievement.description}</p>
                                </div>
                              </article>
                            ))}
                          </div>
                        ) : (
                          <p className="achievementEmpty">
                            Complete a roadmap task to unlock your first achievement.
                          </p>
                        )}
                      </div>
                    </section>
                  )}

                  <div className="roadmapTaskList">
                    {roadmapTasks.map((task) => {
                      const completed = task.status === 'COMPLETED'

                      return (
                        <article
                          className="roadmapTask"
                          key={task.id}
                        >
                          <div className="roadmapTaskHeader">
                            <span className="opportunityType">
                              Day {task.day_number}
                            </span>

                            <span
                              className={
                                completed
                                  ? 'eligibleStatus'
                                  : 'taskPending'
                              }
                            >
                              {completed ? '✓ Completed' : 'Pending'}
                            </span>
                          </div>

                          <h3>{task.title}</h3>
                          <p>{task.description}</p>
                          <p className="roadmapTaskTime">
                            Estimated time: {task.estimated_minutes} minutes
                          </p>

{task.resources && task.resources.length > 0 && (
  <div className="roadmapResources">
    <h4>Learning resources</h4>
    <ul>
      {task.resources.map((resource) => (
        <li key={resource.url}>
          <a
            href={resource.url}
            target="_blank"
            rel="noopener noreferrer"
          >
            {resource.title}
          </a>
          <span> — {resource.type}</span>
        </li>
      ))}
    </ul>
  </div>
)}

                          {completed && task.completed_at && (
                            <p className="roadmapTaskTime">
                              Completed at:{' '}
                              {new Date(task.completed_at).toLocaleString()}
                            </p>
                          )}

                          <button
                            type="button"
                            className="roadmapCompleteBtn"
                            onClick={() => handleCompleteTask(task.id)}
                            disabled={roadmapLoading || completed}
                          >
                            {completed ? 'Completed ✓' : 'Mark Complete'}
                          </button>
                        </article>
                      )
                    })}
                  </div>

                </div>
              )}
            </div>
          )}
        </section>

        <section id="career-chat" className="opportunitiesSection">
          <div className="sectionHeader">
            <p className="eyebrow">YOUR PERSONAL CAREER GUIDE</p>
            <h2>Not sure which career to choose?</h2>
            <p className="sectionSubtitle">
              Tell OpportunityAI what you enjoy, explore possible career
              paths, and discover a practical first step.
            </p>
          </div>

          <div className="careerChatPanel">
            <div className="careerChatWelcome">
              <strong>OpportunityAI Career Guide</strong>
              <p>
                Are you interested in building software, analysing data,
                or exploring artificial intelligence? You can ask in your
                own words.
              </p>
            </div>

            <div className="careerChatMessages" aria-live="polite">
              {chatReplies.map((reply, index) => (
                <article className="careerChatReply" key={index}>
                  <p className="careerChatLabel">Career Guide</p>
                  <p>{reply.reply}</p>

                  {reply.recommendations.length > 0 && (
                    <div className="careerChatRecommendations">
                      {reply.recommendations
                        .filter((item) => item.match_count > 0)
                        .map((item) => (
                          <div
                            className="careerChatRecommendation"
                            key={item.career_path}
                          >
                            <h4>{item.career_path}</h4>
                            <p>{item.description}</p>
                            <p>
                              <strong>Your first step:</strong>{' '}
                              {item.first_step}
                            </p>
                          </div>
                        ))}
                    </div>
                  )}
                </article>
              ))}
            </div>

            <form
              className="careerChatForm"
              onSubmit={handleSendCareerMessage}
            >
              <label htmlFor="career-chat-input">
                What would you like help with?
              </label>

              <textarea
                id="career-chat-input"
                value={chatMessage}
                onChange={(event) => setChatMessage(event.target.value)}
                placeholder="Example: I enjoy Python and want to explore AI careers..."
                rows={3}
                maxLength={1000}
                disabled={chatLoading}
              />

              {chatError && (
                <p className="careerChatError" role="alert">
                  {chatError}
                </p>
              )}

              <button
                type="submit"
                className="careerChatSendBtn"
                disabled={chatLoading || !chatMessage.trim()}
              >
                {chatLoading ? 'Thinking...' : 'Explore my career →'}
              </button>
            </form>
          </div>
        </section>

        <section id="impact" className="impactSection">
          <p className="eyebrow">OUR IMPACT</p>
          <h2>Helping students discover more.</h2>
          <p>
            OpportunityAI brings opportunities and personalized learning
            into one simple experience.
          </p>

          <div className="impactGrid">
            <div>
              <strong>{opportunities.length}</strong>
              <span>Opportunities</span>
            </div>
            <div>
              <strong>AI</strong>
              <span>Powered discovery</span>
            </div>
            <div>
              <strong>{completedTasks}/{roadmapTasks.length}</strong>
              <span>Roadmap tasks completed</span>
            </div>
          </div>
                    <div className="heroPreview">
            <div className="previewHeader">
              <div>
                <span className="previewDot"></span>
                <span>Opportunity matching</span>
              </div>
              <span className="previewLabel">AI PREVIEW</span>
            </div>

            <div className="previewProfile">
              <div className="previewAvatar">✦</div>
              <div>
                <strong>Your next opportunity</strong>
                <p>Personalized around your goals</p>
              </div>
            </div>

            <div className="previewMatch">
              <div>
                <span>Scholarship match</span>
                <strong>92%</strong>
              </div>
              <div className="previewTrack">
                <span></span>
              </div>
              <p>Illustrative match score · Actual results depend on your profile</p>
            </div>

            <div className="previewOpportunity">
              <div className="previewIcon">🎓</div>
              <div>
                <strong>Education opportunity</strong>
                <p>Eligibility-aware discovery</p>
              </div>
              <span className="previewCheck">✓</span>
            </div>

            <div className="previewOpportunity">
              <div className="previewIcon">💻</div>
              <div>
                <strong>Career opportunity</strong>
                <p>Explore paths that fit your goals</p>
              </div>
              <span className="previewCheck">✓</span>
            </div>
          </div>
        </section>
      </main>

      <footer>
        <strong>OpportunityAI</strong>
        <span>Discover opportunities that fit your journey.</span>
      </footer>
    </div>
  )

}
export default App
