import { apiFetch } from './api';

export type OverviewMetrics = {
  totals: {
    accounts: number;
    analyses: number;
    reports: number;
  };
  recent_24h: {
    analyses: number;
    reports: number;
  };
  rules: Array<{
    rule_key: string;
    count: number;
    avg_score: number;
  }>;
  top_domains: Array<{
    domain: string;
    analysis_count: number;
  }>;
};

export type TimelineData = {
  analyses: Array<{
    date: string;
    count: number;
  }>;
  reports: Array<{
    date: string;
    count: number;
  }>;
};

export type AccountData = {
  accounts: Array<{
    id: number;
    mastodon_account_id: string;
    acct: string;
    domain: string;
    last_checked_at: string | null;
    analysis_count: number;
    report_count: number;
    last_analysis: string | null;
  }>;
};

export type ReportData = {
  reports: Array<{
    id: number;
    mastodon_account_id: string;
    account: string;
    status_id: string | null;
    mastodon_report_id: string | null;
    comment: string;
    created_at: string;
  }>;
};

export type AnalysisData = {
  analyses: Array<{
    id: number;
    status_id: string | null;
    rule_key: string;
    score: number;
    evidence: any;
    created_at: string;
  }>;
};

export type RulesData = {
  rules: {
    report_threshold: number;
    username_regex?: Array<{name: string; pattern: string; weight: number}>;
    display_name_regex?: Array<{name: string; pattern: string; weight: number}>;
    content_regex?: Array<{name: string; pattern: string; weight: number}>;
  };
  report_threshold: number;
};

export async function fetchOverview(): Promise<OverviewMetrics> {
  return apiFetch<OverviewMetrics>('/analytics/overview');
}

export async function fetchTimeline(days: number = 7): Promise<TimelineData> {
  return apiFetch<TimelineData>(`/analytics/timeline?days=${days}`);
}

export async function fetchAccounts(limit: number = 50, offset: number = 0): Promise<AccountData> {
  return apiFetch<AccountData>(`/analytics/accounts?limit=${limit}&offset=${offset}`);
}

export async function fetchReports(limit: number = 50, offset: number = 0): Promise<ReportData> {
  return apiFetch<ReportData>(`/analytics/reports?limit=${limit}&offset=${offset}`);
}

export async function fetchAccountAnalyses(accountId: string, limit: number = 50, offset: number = 0): Promise<AnalysisData> {
  return apiFetch<AnalysisData>(`/analytics/analyses/${accountId}?limit=${limit}&offset=${offset}`);
}

export async function fetchCurrentRules(): Promise<RulesData> {
  return apiFetch<RulesData>('/rules/current');
}
