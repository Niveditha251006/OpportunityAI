import type {
  Opportunity,
  OpportunitiesResponse,
} from '../types/opportunity'

const API_BASE_URL = 'http://127.0.0.1:5000/api/v1'

export async function getOpportunities(): Promise<Opportunity[]> {
  const response = await fetch(`${API_BASE_URL}/opportunities`)

  if (!response.ok) {
    throw new Error('Failed to fetch opportunities')
  }

  const data: OpportunitiesResponse = await response.json()

  return data.opportunities
}