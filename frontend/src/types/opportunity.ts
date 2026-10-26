export interface Opportunity {
  id: number;
  title: string;
  organization: string;
  description: string;
  type: string;
  education_level: string | null;
  fields: string | null;
  states: string | null;
  max_income: number | null;
  amount: number | null;
  application_url: string | null;
  source_url: string | null;
}

export interface OpportunitiesResponse {
  count: number;
  opportunities: Opportunity[];
}
