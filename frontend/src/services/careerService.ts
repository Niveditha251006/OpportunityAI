
const API_BASE_URL = 'http://127.0.0.1:5000/api/v1'

export interface CareerGoal {
  id: number
  student_name: string
  career_path: string
  current_skill_level: string
  daily_minutes: number
  status: string
}

export interface RoadmapTask {
  id: number
  week_number: number
  day_number: number
  title: string
  description: string
  estimated_minutes: number
  status: string
  completed_at: string | null
  resources?: {
  title: string
  url: string
  type: string
}[]
}

export interface RoadmapResponse {
  career_goal_id: number
  career_path: string
  tasks: RoadmapTask[]
}
export interface LearningAchievement {
  code: string
  title: string
  description: string
  unlocked_at: string
}

export interface LearningProgress {
  goal_id: number
  current_streak: number
  best_streak: number
  activity_days: number
  achievements: LearningAchievement[]
}

export async function getLearningProgress(
  goalId: number
): Promise<LearningProgress> {
  const response = await fetch(
    `${API_BASE_URL}/career/goals/${goalId}/learning-progress`
  )

  if (!response.ok) {
    throw new Error('Failed to load learning progress')
  }

  return response.json()
}
export async function getCareerGoals(): Promise<CareerGoal[]> {
  const response = await fetch(`${API_BASE_URL}/career/goals`)

  if (!response.ok) {
    throw new Error('Failed to load career goals')
  }

  const data = await response.json()
  return data.goals
}

export async function generateRoadmap(
  goalId: number
): Promise<RoadmapResponse> {
  const response = await fetch(
    `${API_BASE_URL}/career/goals/${goalId}/roadmap/generate`,
    { method: 'POST' }
  )

  if (!response.ok) {
    const data = await response.json()
    throw new Error(data.error || 'Failed to generate roadmap')
  }

  return response.json()
}

export async function getRoadmap(
  goalId: number
): Promise<RoadmapResponse> {
  const response = await fetch(
    `${API_BASE_URL}/career/goals/${goalId}/roadmap`
  )

  if (!response.ok) {
    throw new Error('Failed to load roadmap')
  }

  return response.json()
}

export async function completeRoadmapTask(
  taskId: number
): Promise<void> {
  const response = await fetch(
    `${API_BASE_URL}/roadmap/tasks/${taskId}/complete`,
    { method: 'PATCH' }
  )

  if (!response.ok) {
    throw new Error('Failed to complete task')
  }
}

export interface CareerChatRecommendation {
  career_path: string
  description: string
  first_step: string
  match_count: number
  matched_interests: string[]
  skill_level: string
}

export interface CareerChatResponse {
  reply: string
  needs_more_information: boolean
  recommendations: CareerChatRecommendation[]
  suggested_interests: string[]
}


export interface CareerChatMessage {
  role: 'user' | 'assistant'
  content: string
}

export async function sendCareerChatMessage(
  message: string,
  conversationHistory: CareerChatMessage[] = []
): Promise<CareerChatResponse> {
  const response = await fetch(
    `${API_BASE_URL}/career-guidance/chat`,
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message,
        conversation_history: conversationHistory,
      }),
    }
  )

  if (!response.ok) {
    const data = await response.json().catch(() => ({}))
    throw new Error(data.error || 'Failed to get career guidance')
  }

  return response.json()
}
