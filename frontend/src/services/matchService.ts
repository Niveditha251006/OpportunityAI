export interface TextMatchResponse {
  student_profile: StudentProfileInput
  matches: MatchResult[]
}
export interface StudentProfileInput {
  education_level: string | null
  field: string | null
  annual_income: number | null
  state: string | null
  rural: boolean | null
  first_generation: boolean | null
  interests: string[]
}

export interface MatchResult {
  id: number
  title: string
  organization: string
  eligible: boolean
  eligibility_status?: 'ELIGIBLE' | 'INELIGIBLE' | 'NEEDS_INFORMATION'
  reasons: string[]
  semantic_similarity: number
  interest_match: number
  matched_interests: string[]
  explanation: string[]
  match_score: number
}



export interface MatchResponse {
  student_profile: StudentProfileInput
  matches: MatchResult[]
}

const API_BASE_URL = 'http://127.0.0.1:5000/api/v1'

export async function matchOpportunities(
  profile: StudentProfileInput
): Promise<MatchResponse> {
  const response = await fetch(`${API_BASE_URL}/match`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(profile),
  })

  if (!response.ok) {
    throw new Error('Failed to match opportunities')
  }

  return response.json()
}
export async function matchOpportunitiesFromText(
  profileText: string
): Promise<TextMatchResponse> {
  const response = await fetch(`${API_BASE_URL}/match-from-text`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      profile_text: profileText,
    }),
  })

  if (!response.ok) {
    throw new Error('Failed to match opportunities from profile text')
  }

  return response.json()
}