import { useEffect, useMemo, useState } from 'react';
import {
  AppShell, Group, Text, Container, Card, Stack, Badge, Button, Switch,
  ActionIcon, Tooltip, Divider, Skeleton, Grid, Table, Modal, Alert, 
  Tabs, Select, Progress, Code, ScrollArea, TextInput, Title, Menu,
  NumberInput
} from '@mantine/core';
import { IconRefresh, IconEye, IconChartBar, IconUsers, IconFlag, IconSettings, IconRuler, IconInfoCircle, IconLogout, IconLogin, IconUser, IconPlus, IconTrash, IconEdit, IconToggleLeft, IconToggleRight, IconRadar, IconShield, IconTrendingUp } from '@tabler/icons-react';
import { 
  LineChart, Line, XAxis, YAxis, CartesianGrid, ResponsiveContainer,
  BarChart, Bar, PieChart, Pie, Cell, AreaChart, Area
} from 'recharts';
import { apiFetch } from './api';
import { getCurrentUser, logout, login, User } from './auth';
import { 
  fetchOverview, fetchTimeline, fetchAccounts, fetchReports, 
  fetchAccountAnalyses, fetchCurrentRules, fetchRulesList, 
  createRule, updateRule, deleteRule, toggleRule, OverviewMetrics, 
  TimelineData, AccountData, ReportData, AnalysisData, RulesData, Rule, RulesList,
  fetchScanningAnalytics, fetchDomainAnalytics, fetchRuleStatistics, fetchRuleDetails,
  triggerFederatedScan, triggerDomainCheck, invalidateScanCache, bulkToggleRules,
  ScanningAnalytics, DomainAnalytics, RuleStatistics, RuleDetails
} from './analytics';

type Health = {
  ok: boolean;
  db_ok: boolean;
  redis_ok: boolean;
  dry_run: boolean;
  panic_stop: boolean;
  batch_size: number;
  version?: string;
  timestamp?: string;
};

const COLORS = ['#8884d8', '#82ca9d', '#ffc658', '#ff7300', '#8dd1e1', '#d084d0'];

export default function App() {
  const [activeTab, setActiveTab] = useState('overview');
  const [health, setHealth] = useState<Health | null>(null);
  const [overview, setOverview] = useState<OverviewMetrics | null>(null);
  const [timeline, setTimeline] = useState<TimelineData | null>(null);
  const [accounts, setAccounts] = useState<AccountData | null>(null);
  const [reports, setReports] = useState<ReportData | null>(null);
  const [rules, setRules] = useState<RulesData | null>(null);
  const [rulesList, setRulesList] = useState<RulesList | null>(null);
  const [selectedAccount, setSelectedAccount] = useState<string | null>(null);
  const [accountAnalyses, setAccountAnalyses] = useState<AnalysisData | null>(null);
  const [timeRange, setTimeRange] = useState('7');
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [refreshing, setRefreshing] = useState(false);
  const [currentUser, setCurrentUser] = useState<User | null>(null);
  const [authLoading, setAuthLoading] = useState(true);
  const [loginLoading, setLoginLoading] = useState(false);
  // Enhanced analytics states
  const [scanningAnalytics, setScanningAnalytics] = useState<ScanningAnalytics | null>(null);
  const [domainAnalytics, setDomainAnalytics] = useState<DomainAnalytics | null>(null);
  const [ruleStatistics, setRuleStatistics] = useState<RuleStatistics | null>(null);
  const [selectedRuleDetails, setSelectedRuleDetails] = useState<RuleDetails | null>(null);
  const [showRuleInfoModal, setShowRuleInfoModal] = useState(false);
  const [selectedRuleForInfo, setSelectedRuleForInfo] = useState<Rule | null>(null);

  const statusBadge = useMemo(() => {
    if (!health) return null;
    const color = health.ok ? 'green' : 'red';
    return <Badge color={color}>{health.ok ? 'Healthy' : 'Degraded'}</Badge>;
  }, [health]);

  async function checkAuth() {
    try {
      const user = await getCurrentUser();
      setCurrentUser(user);
    } catch (error) {
      console.error('Auth check failed:', error);
      setCurrentUser(null);
    } finally {
      setAuthLoading(false);
    }
  }

  async function handleLogin() {
    setLoginLoading(true);
    try {
      const user = await login();
      if (user) {
        setCurrentUser(user);
      }
    } catch (error) {
      console.error('Login failed:', error);
    } finally {
      setLoginLoading(false);
    }
  }

  async function handleLogout() {
    try {
      await logout();
      setCurrentUser(null);
    } catch (error) {
      console.error('Logout failed:', error);
      // Clear user anyway
      setCurrentUser(null);
    }
  }

  async function loadHealth() {
    try {
      const data = await apiFetch<Health>('/healthz');
      setHealth(data);
    } catch (error) {
      console.error('Failed to load health:', error);
    }
  }

  async function loadOverview() {
    try {
      const data = await fetchOverview();
      setOverview(data);
    } catch (error) {
      console.error('Failed to load overview:', error);
    }
  }

  async function loadTimeline() {
    try {
      const data = await fetchTimeline(parseInt(timeRange));
      setTimeline(data);
    } catch (error) {
      console.error('Failed to load timeline:', error);
    }
  }

  async function loadAccounts() {
    try {
      const data = await fetchAccounts();
      setAccounts(data);
    } catch (error) {
      console.error('Failed to load accounts:', error);
    }
  }

  async function loadReports() {
    try {
      const data = await fetchReports();
      setReports(data);
    } catch (error) {
      console.error('Failed to load reports:', error);
    }
  }

  async function loadRules() {
    try {
      const [rulesData, rulesList] = await Promise.all([
        fetchCurrentRules(),
        fetchRulesList()
      ]);
      setRules(rulesData);
      setRulesList(rulesList);
    } catch (error) {
      console.error('Failed to load rules:', error);
    }
  }

  async function loadScanningAnalytics() {
    try {
      const data = await fetchScanningAnalytics();
      setScanningAnalytics(data);
    } catch (error) {
      console.error('Failed to load scanning analytics:', error);
    }
  }

  async function loadDomainAnalytics() {
    try {
      const data = await fetchDomainAnalytics();
      setDomainAnalytics(data);
    } catch (error) {
      console.error('Failed to load domain analytics:', error);
    }
  }

  async function loadRuleStatistics() {
    try {
      const data = await fetchRuleStatistics();
      setRuleStatistics(data);
    } catch (error) {
      console.error('Failed to load rule statistics:', error);
    }
  }

  async function handleTriggerFederatedScan(domains?: string[]) {
    setLoading(true);
    try {
      await triggerFederatedScan(domains);
      // Refresh analytics after triggering scan
      await loadScanningAnalytics();
    } catch (error) {
      console.error('Failed to trigger federated scan:', error);
    } finally {
      setLoading(false);
    }
  }

  async function handleTriggerDomainCheck() {
    setLoading(true);
    try {
      await triggerDomainCheck();
      // Refresh analytics after check
      await loadDomainAnalytics();
    } catch (error) {
      console.error('Failed to trigger domain check:', error);
    } finally {
      setLoading(false);
    }
  }

  async function handleInvalidateCache(rule_changes = false) {
    setLoading(true);
    try {
      await invalidateScanCache(rule_changes);
      // Refresh analytics after cache invalidation
      await loadScanningAnalytics();
    } catch (error) {
      console.error('Failed to invalidate cache:', error);
    } finally {
      setLoading(false);
    }
  }

  async function loadAccountAnalyses(accountId: string) {
    try {
      const data = await fetchAccountAnalyses(accountId);
      setAccountAnalyses(data);
    } catch (error) {
      console.error('Failed to load account analyses:', error);
    }
  }

  async function refreshAllData() {
    setRefreshing(true);
    try {
      await Promise.all([
        loadHealth(),
        loadOverview(),
        loadTimeline(),
        loadAccounts(),
        loadReports(),
        loadRules(),
        loadScanningAnalytics(),
        loadDomainAnalytics(),
        loadRuleStatistics()
      ]);
    } finally {
      setRefreshing(false);
    }
  }

  useEffect(() => {
    checkAuth();
  }, []);

  useEffect(() => {
    if (currentUser && !authLoading) {
      refreshAllData();
    }
  }, [currentUser, authLoading]);

  useEffect(() => {
    loadTimeline();
  }, [timeRange]);

  async function updateDryRun(next: boolean) {
    setSaving(true);
    try {
      await apiFetch('/config/dry_run', {
        method: 'POST',
        body: JSON.stringify({ dry_run: next, updated_by: 'dashboard' })
      });
      setHealth((h) => (h ? { ...h, dry_run: next } : h));
    } finally {
      setSaving(false);
    }
  }

  async function updatePanic(next: boolean) {
    setSaving(true);
    try {
      await apiFetch('/config/panic_stop', {
        method: 'POST',
        body: JSON.stringify({ panic_stop: next, updated_by: 'dashboard' })
      });
      setHealth((h) => (h ? { ...h, panic_stop: next } : h));
    } finally {
      setSaving(false);
    }
  }


  // Show login screen if not authenticated
  if (authLoading) {
    return (
      <Container size="sm" mt="xl">
        <Card withBorder padding="xl" ta="center">
          <Skeleton height={20} width="60%" mx="auto" mb="sm" />
          <Skeleton height={16} width="40%" mx="auto" />
        </Card>
      </Container>
    );
  }

  if (!currentUser) {
    return (
      <Container size="sm" mt="xl">
        <Card withBorder padding="xl" ta="center">
          <Stack gap="lg">
            <div>
              <Title order={2} mb="sm">MastoWatch Analytics</Title>
              <Text c="dimmed">
                Please sign in with your Mastodon admin account to access the dashboard.
              </Text>
            </div>
            <Button 
              leftSection={<IconLogin size={16} />}
              onClick={handleLogin}
              loading={loginLoading}
              size="lg"
            >
              Sign In with Mastodon
            </Button>
          </Stack>
        </Card>
      </Container>
    );
  }

  return (
    <AppShell
      header={{ height: 56 }}
      padding="md"
      withBorder={false}
    >
      <AppShell.Header>
        <Container size="xl" h="100%">
          <Group h="100%" justify="space-between">
            <Group gap="xs">
              <Text fw={700} size="lg">MastoWatch Analytics</Text>
              {statusBadge}
            </Group>
            <Group>
              <Menu shadow="md" width={200}>
                <Menu.Target>
                  <Button variant="light" leftSection={<IconUser size={16} />}>
                    {currentUser.display_name}
                  </Button>
                </Menu.Target>
                <Menu.Dropdown>
                  <Menu.Item 
                    leftSection={<IconLogout size={16} />}
                    onClick={handleLogout}
                  >
                    Logout
                  </Menu.Item>
                </Menu.Dropdown>
              </Menu>
              
              <Select
                placeholder="Time Range"
                value={timeRange}
                onChange={(value) => setTimeRange(value || '7')}
                data={[
                  { value: '1', label: '24 Hours' },
                  { value: '7', label: '7 Days' },
                  { value: '30', label: '30 Days' },
                  { value: '90', label: '90 Days' }
                ]}
                w={120}
              />
              <Tooltip label="Refresh all data">
                <ActionIcon 
                  variant="light" 
                  onClick={refreshAllData} 
                  loading={refreshing}
                  aria-label="Refresh"
                >
                  <IconRefresh size={16} />
                </ActionIcon>
              </Tooltip>
            </Group>
          </Group>
        </Container>
      </AppShell.Header>

      <AppShell.Main>
        <Container size="xl">
          <Tabs value={activeTab} onChange={(value) => setActiveTab(value || 'overview')}>
            <Tabs.List>
              <Tabs.Tab value="overview" leftSection={<IconChartBar size={16} />}>
                Overview
              </Tabs.Tab>
              <Tabs.Tab value="accounts" leftSection={<IconUsers size={16} />}>
                Accounts
              </Tabs.Tab>
              <Tabs.Tab value="reports" leftSection={<IconFlag size={16} />}>
                Reports
              </Tabs.Tab>
              <Tabs.Tab value="rules" leftSection={<IconRuler size={16} />}>
                Rules
              </Tabs.Tab>
              <Tabs.Tab value="scanning" leftSection={<IconRadar size={16} />}>
                Scanning
              </Tabs.Tab>
              <Tabs.Tab value="domains" leftSection={<IconShield size={16} />}>
                Domains
              </Tabs.Tab>
              <Tabs.Tab value="settings" leftSection={<IconSettings size={16} />}>
                Settings
              </Tabs.Tab>
            </Tabs.List>

            <Tabs.Panel value="overview" pt="md">
              <OverviewTab overview={overview} timeline={timeline} />
            </Tabs.Panel>

            <Tabs.Panel value="accounts" pt="md">
              <AccountsTab 
                accounts={accounts} 
                onViewAccount={(accountId) => {
                  setSelectedAccount(accountId);
                  loadAccountAnalyses(accountId);
                }}
              />
            </Tabs.Panel>

            <Tabs.Panel value="reports" pt="md">
              <ReportsTab reports={reports} />
            </Tabs.Panel>

            <Tabs.Panel value="rules" pt="md">
              <RulesTab rules={rules} saving={saving} />
            </Tabs.Panel>

            <Tabs.Panel value="scanning" pt="md">
              <ScanningTab 
                scanningAnalytics={scanningAnalytics} 
                ruleStatistics={ruleStatistics}
                onTriggerFederatedScan={handleTriggerFederatedScan}
                onTriggerDomainCheck={handleTriggerDomainCheck}
                onInvalidateCache={handleInvalidateCache}
                loading={loading}
              />
            </Tabs.Panel>

            <Tabs.Panel value="domains" pt="md">
              <DomainsTab 
                domainAnalytics={domainAnalytics}
                onRefresh={loadDomainAnalytics}
                loading={loading}
              />
            </Tabs.Panel>

            <Tabs.Panel value="settings" pt="md">
              <SettingsTab
                health={health}
                onUpdateDryRun={updateDryRun}
                onUpdatePanic={updatePanic}
                saving={saving}
              />
            </Tabs.Panel>
          </Tabs>
        </Container>
      </AppShell.Main>

      {/* Account Detail Modal */}
      <Modal
        opened={!!selectedAccount}
        onClose={() => {
          setSelectedAccount(null);
          setAccountAnalyses(null);
        }}
        title={`Account Details: ${selectedAccount}`}
        size="xl"
      >
        {selectedAccount && (
          <AccountDetailModal 
            accountId={selectedAccount}
            analyses={accountAnalyses}
          />
        )}
      </Modal>
    </AppShell>
  );
}

// Tab Components
function OverviewTab({ overview, timeline }: { overview: OverviewMetrics | null, timeline: TimelineData | null }) {
  if (!overview) {
    return <Skeleton height={400} />;
  }

  const timelineData = timeline ? 
    timeline.analyses.map((item, idx) => ({
      date: item.date,
      analyses: item.count,
      reports: timeline.reports[idx]?.count || 0
    })) : [];

  const ruleData = overview.rules.map((rule, idx) => ({
    ...rule,
    fill: COLORS[idx % COLORS.length]
  }));

  const domainData = overview.top_domains.map((domain, idx) => ({
    ...domain,
    fill: COLORS[idx % COLORS.length]
  }));

  return (
    <Stack gap="md">
      {/* Summary Cards */}
      <Grid>
        <Grid.Col span={3}>
          <Card withBorder padding="md">
            <Stack gap="xs">
              <Text size="sm" c="dimmed">Total Accounts</Text>
              <Text size="xl" fw={700}>{overview.totals.accounts.toLocaleString()}</Text>
            </Stack>
          </Card>
        </Grid.Col>
        <Grid.Col span={3}>
          <Card withBorder padding="md">
            <Stack gap="xs">
              <Text size="sm" c="dimmed">Total Analyses</Text>
              <Text size="xl" fw={700}>{overview.totals.analyses.toLocaleString()}</Text>
              <Text size="xs" c="dimmed">+{overview.recent_24h.analyses} last 24h</Text>
            </Stack>
          </Card>
        </Grid.Col>
        <Grid.Col span={3}>
          <Card withBorder padding="md">
            <Stack gap="xs">
              <Text size="sm" c="dimmed">Total Reports</Text>
              <Text size="xl" fw={700}>{overview.totals.reports.toLocaleString()}</Text>
              <Text size="xs" c="dimmed">+{overview.recent_24h.reports} last 24h</Text>
            </Stack>
          </Card>
        </Grid.Col>
        <Grid.Col span={3}>
          <Card withBorder padding="md">
            <Stack gap="xs">
              <Text size="sm" c="dimmed">Report Rate</Text>
              <Text size="xl" fw={700}>
                {overview.totals.analyses > 0 
                  ? ((overview.totals.reports / overview.totals.analyses) * 100).toFixed(1)
                  : '0'}%
              </Text>
            </Stack>
          </Card>
        </Grid.Col>
      </Grid>

      {/* Charts */}
      <Grid>
        <Grid.Col span={8}>
          <Card withBorder padding="md">
            <Title order={4} mb="md">Activity Timeline</Title>
            <ResponsiveContainer width="100%" height={300}>
              <AreaChart data={timelineData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Area 
                  type="monotone" 
                  dataKey="analyses" 
                  stackId="1"
                  stroke="#8884d8" 
                  fill="#8884d8" 
                  fillOpacity={0.6}
                />
                <Area 
                  type="monotone" 
                  dataKey="reports" 
                  stackId="1"
                  stroke="#82ca9d" 
                  fill="#82ca9d" 
                  fillOpacity={0.6}
                />
              </AreaChart>
            </ResponsiveContainer>
          </Card>
        </Grid.Col>
        <Grid.Col span={4}>
          <Card withBorder padding="md">
            <Title order={4} mb="md">Rule Effectiveness</Title>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={ruleData}
                  dataKey="count"
                  nameKey="rule_key"
                  cx="50%"
                  cy="50%"
                  outerRadius={80}
                  label={(entry) => `${entry.rule_key}: ${entry.count}`}
                >
                  {ruleData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.fill} />
                  ))}
                </Pie>
              </PieChart>
            </ResponsiveContainer>
          </Card>
        </Grid.Col>
      </Grid>

      <Card withBorder padding="md">
        <Title order={4} mb="md">Top Domains by Activity</Title>
        <ResponsiveContainer width="100%" height={200}>
          <BarChart data={domainData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="domain" />
            <YAxis />
            <Bar dataKey="analysis_count" fill="#8884d8" />
          </BarChart>
        </ResponsiveContainer>
      </Card>
    </Stack>
  );
}

function AccountsTab({ accounts, onViewAccount }: { 
  accounts: AccountData | null, 
  onViewAccount: (accountId: string) => void 
}) {
  if (!accounts) {
    return <Skeleton height={400} />;
  }

  return (
    <Card withBorder padding="md">
      <Title order={4} mb="md">Account Activity</Title>
      <ScrollArea>
        <Table striped highlightOnHover>
          <Table.Thead>
            <Table.Tr>
              <Table.Th>Account</Table.Th>
              <Table.Th>Domain</Table.Th>
              <Table.Th>Analyses</Table.Th>
              <Table.Th>Reports</Table.Th>
              <Table.Th>Last Activity</Table.Th>
              <Table.Th>Actions</Table.Th>
            </Table.Tr>
          </Table.Thead>
          <Table.Tbody>
            {accounts.accounts.map((account) => (
              <Table.Tr key={account.id}>
                <Table.Td>
                  <Text fw={500}>{account.acct}</Text>
                </Table.Td>
                <Table.Td>
                  <Badge variant="light">{account.domain}</Badge>
                </Table.Td>
                <Table.Td>
                  <Badge color="blue" variant="light">
                    {account.analysis_count}
                  </Badge>
                </Table.Td>
                <Table.Td>
                  <Badge color={account.report_count > 0 ? "red" : "gray"} variant="light">
                    {account.report_count}
                  </Badge>
                </Table.Td>
                <Table.Td>
                  <Text size="sm" c="dimmed">
                    {account.last_analysis 
                      ? new Date(account.last_analysis).toLocaleDateString()
                      : 'Never'
                    }
                  </Text>
                </Table.Td>
                <Table.Td>
                  <Button
                    size="xs"
                    variant="light"
                    leftSection={<IconEye size={14} />}
                    onClick={() => onViewAccount(account.mastodon_account_id)}
                  >
                    View Details
                  </Button>
                </Table.Td>
              </Table.Tr>
            ))}
          </Table.Tbody>
        </Table>
      </ScrollArea>
    </Card>
  );
}

function ReportsTab({ reports }: { reports: ReportData | null }) {
  if (!reports) {
    return <Skeleton height={400} />;
  }

  return (
    <Card withBorder padding="md">
      <Title order={4} mb="md">Recent Reports</Title>
      <ScrollArea>
        <Table striped highlightOnHover>
          <Table.Thead>
            <Table.Tr>
              <Table.Th>Account</Table.Th>
              <Table.Th>Report ID</Table.Th>
              <Table.Th>Comment</Table.Th>
              <Table.Th>Created</Table.Th>
            </Table.Tr>
          </Table.Thead>
          <Table.Tbody>
            {reports.reports.map((report) => (
              <Table.Tr key={report.id}>
                <Table.Td>
                  <Text fw={500}>{report.account}</Text>
                </Table.Td>
                <Table.Td>
                  <Code>{report.mastodon_report_id || 'Pending'}</Code>
                </Table.Td>
                <Table.Td>
                  <Text size="sm" lineClamp={2}>
                    {report.comment}
                  </Text>
                </Table.Td>
                <Table.Td>
                  <Text size="sm" c="dimmed">
                    {new Date(report.created_at).toLocaleString()}
                  </Text>
                </Table.Td>
              </Table.Tr>
            ))}
          </Table.Tbody>
        </Table>
      </ScrollArea>
    </Card>
  );
}

function RulesTab({ rules, saving }: {
  rules: RulesData | null,
  saving: boolean
}) {
  const [rulesList, setRulesList] = useState<Rule[]>([]);
  const [loading, setLoading] = useState(false);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [editingRule, setEditingRule] = useState<Rule | null>(null);
  const [showRuleInfoModal, setShowRuleInfoModal] = useState(false);
  const [selectedRuleForInfo, setSelectedRuleForInfo] = useState<Rule | null>(null);
  const [newRule, setNewRule] = useState({
    name: '',
    rule_type: 'username_regex' as Rule['rule_type'],
    pattern: '',
    weight: 0.5
  });

  useEffect(() => {
    loadRulesList();
  }, []);

  async function loadRulesList() {
    try {
      const data = await fetchRulesList();
      setRulesList(data.rules);
    } catch (error) {
      console.error('Failed to load rules list:', error);
    }
  }

  async function handleCreateRule() {
    try {
      setLoading(true);
      await createRule({
        name: newRule.name,
        rule_type: newRule.rule_type,
        pattern: newRule.pattern,
        weight: newRule.weight,
        enabled: true
      });
      setNewRule({ name: '', rule_type: 'username_regex', pattern: '', weight: 0.5 });
      setShowCreateModal(false);
      await loadRulesList();
    } catch (error) {
      console.error('Failed to create rule:', error);
    } finally {
      setLoading(false);
    }
  }

  async function handleToggleRule(rule: Rule) {
    if (rule.is_default || !rule.id) return;
    
    try {
      setLoading(true);
      await toggleRule(rule.id);
      await loadRulesList();
    } catch (error) {
      console.error('Failed to toggle rule:', error);
    } finally {
      setLoading(false);
    }
  }

  async function handleDeleteRule(rule: Rule) {
    if (rule.is_default || !rule.id) return;
    
    try {
      setLoading(true);
      await deleteRule(rule.id);
      await loadRulesList();
    } catch (error) {
      console.error('Failed to delete rule:', error);
    } finally {
      setLoading(false);
    }
  }

  async function handleUpdateRule() {
    if (!editingRule?.id) return;
    
    try {
      setLoading(true);
      await updateRule(editingRule.id, {
        name: editingRule.name,
        pattern: editingRule.pattern,
        weight: editingRule.weight
      });
      setEditingRule(null);
      await loadRulesList();
    } catch (error) {
      console.error('Failed to update rule:', error);
    } finally {
      setLoading(false);
    }
  }

  if (!rules) {
    return <Skeleton height={400} />;
  }

  const groupedRules = rulesList.reduce((acc, rule) => {
    if (!acc[rule.rule_type]) acc[rule.rule_type] = [];
    acc[rule.rule_type].push(rule);
    return acc;
  }, {} as Record<string, Rule[]>);

  return (
    <Stack gap="md">
      <Card withBorder padding="md">
        <Group justify="space-between" align="flex-start">
          <Stack gap="xs">
            <Title order={4}>Rules Management</Title>
            <Text c="dimmed" size="sm">
              Report threshold: {rules.report_threshold}
            </Text>
          </Stack>
          <Group>
            <Button
              variant="light"
              leftSection={<IconPlus size={16} />}
              onClick={() => setShowCreateModal(true)}
            >
              Add Rule
            </Button>
          </Group>
        </Group>
        
        <Divider my="md" />
        
        <Grid>
          {['username_regex', 'display_name_regex', 'content_regex'].map((ruleType) => (
            <Grid.Col span={4} key={ruleType}>
              <Card withBorder padding="sm">
                <Title order={5} mb="sm">
                  {ruleType === 'username_regex' ? 'Username Rules' :
                   ruleType === 'display_name_regex' ? 'Display Name Rules' :
                   'Content Rules'}
                </Title>
                <Stack gap="xs">
                  {(groupedRules[ruleType] || []).map((rule) => (
                    <Card key={rule.id || rule.name} withBorder padding="xs" bg={rule.enabled ? undefined : 'gray.0'}>
                      <Group justify="space-between" align="flex-start">
                        <Stack gap={2} style={{ flex: 1 }}>
                          <Group gap="xs" align="center">
                            <Text size="sm" fw={500} c={rule.enabled ? undefined : 'dimmed'}>
                              {rule.name}
                            </Text>
                            {rule.is_default && (
                              <Badge size="xs" color="blue" variant="light">Default</Badge>
                            )}
                            <Badge size="xs" variant="light" color={rule.enabled ? 'green' : 'gray'}>
                              {rule.enabled ? 'On' : 'Off'}
                            </Badge>
                            <ActionIcon
                              size="xs"
                              variant="subtle"
                              color="blue"
                              onClick={() => {
                                setSelectedRuleForInfo(rule);
                                setShowRuleInfoModal(true);
                              }}
                              title="View rule information and examples"
                            >
                              <IconInfoCircle size={12} />
                            </ActionIcon>
                          </Group>
                          <Code c={rule.enabled ? undefined : 'dimmed'}>{rule.pattern}</Code>
                          <Text size="xs" c="dimmed">Weight: {rule.weight}</Text>
                        </Stack>
                        <Group gap={4}>
                          {!rule.is_default && rule.id && (
                            <>
                              <ActionIcon
                                size="sm"
                                variant="subtle"
                                color={rule.enabled ? 'orange' : 'green'}
                                onClick={() => handleToggleRule(rule)}
                                loading={loading}
                              >
                                {rule.enabled ? <IconToggleRight size={14} /> : <IconToggleLeft size={14} />}
                              </ActionIcon>
                              <ActionIcon
                                size="sm"
                                variant="subtle"
                                color="blue"
                                onClick={() => setEditingRule(rule)}
                              >
                                <IconEdit size={14} />
                              </ActionIcon>
                              <ActionIcon
                                size="sm"
                                variant="subtle"
                                color="red"
                                onClick={() => handleDeleteRule(rule)}
                                loading={loading}
                              >
                                <IconTrash size={14} />
                              </ActionIcon>
                            </>
                          )}
                        </Group>
                      </Group>
                    </Card>
                  ))}
                  {(!groupedRules[ruleType] || groupedRules[ruleType].length === 0) && (
                    <Text c="dimmed" size="sm">No rules defined</Text>
                  )}
                </Stack>
              </Card>
            </Grid.Col>
          ))}
        </Grid>
      </Card>

      {/* Create Rule Modal */}
      <Modal
        opened={showCreateModal}
        onClose={() => setShowCreateModal(false)}
        title="Create New Rule"
      >
        <Stack gap="md">
          <TextInput
            label="Rule Name"
            value={newRule.name}
            onChange={(e) => setNewRule({...newRule, name: e.target.value})}
            placeholder="Enter rule name"
          />
          <Select
            label="Rule Type"
            value={newRule.rule_type}
            onChange={(value) => setNewRule({...newRule, rule_type: value as Rule['rule_type']})}
            data={[
              { value: 'username_regex', label: 'Username Regex' },
              { value: 'display_name_regex', label: 'Display Name Regex' },
              { value: 'content_regex', label: 'Content Regex' }
            ]}
          />
          <TextInput
            label="Pattern (Regex)"
            value={newRule.pattern}
            onChange={(e) => setNewRule({...newRule, pattern: e.target.value})}
            placeholder="Enter regex pattern"
          />
          <NumberInput
            label="Weight"
            value={newRule.weight}
            onChange={(value) => setNewRule({...newRule, weight: Number(value) || 0})}
            min={0}
            max={2}
            step={0.1}
          />
          <Group justify="flex-end">
            <Button variant="subtle" onClick={() => setShowCreateModal(false)}>
              Cancel
            </Button>
            <Button 
              onClick={handleCreateRule}
              loading={loading}
              disabled={!newRule.name || !newRule.pattern}
            >
              Create Rule
            </Button>
          </Group>
        </Stack>
      </Modal>

      {/* Edit Rule Modal */}
      <Modal
        opened={!!editingRule}
        onClose={() => setEditingRule(null)}
        title="Edit Rule"
      >
        {editingRule && (
          <Stack gap="md">
            <TextInput
              label="Rule Name"
              value={editingRule.name}
              onChange={(e) => setEditingRule({...editingRule, name: e.target.value})}
              placeholder="Enter rule name"
            />
            <TextInput
              label="Pattern (Regex)"
              value={editingRule.pattern}
              onChange={(e) => setEditingRule({...editingRule, pattern: e.target.value})}
              placeholder="Enter regex pattern"
            />
            <NumberInput
              label="Weight"
              value={editingRule.weight}
              onChange={(value) => setEditingRule({...editingRule, weight: Number(value) || 0})}
              min={0}
              max={2}
              step={0.1}
            />
            <Group justify="flex-end">
              <Button variant="subtle" onClick={() => setEditingRule(null)}>
                Cancel
              </Button>
              <Button 
                onClick={handleUpdateRule}
                loading={loading}
                disabled={!editingRule.name || !editingRule.pattern}
              >
                Update Rule
              </Button>
            </Group>
          </Stack>
        )}
      </Modal>

      {/* Rule Info Modal */}
      <Modal
        opened={showRuleInfoModal}
        onClose={() => setShowRuleInfoModal(false)}
        title="Rule Information"
        size="lg"
      >
        {selectedRuleForInfo && (
          <Stack gap="md">
            <Group justify="space-between">
              <div>
                <Text fw={500} size="lg">{selectedRuleForInfo.name}</Text>
                <Badge color={selectedRuleForInfo.enabled ? 'green' : 'gray'}>
                  {selectedRuleForInfo.enabled ? 'Enabled' : 'Disabled'}
                </Badge>
              </div>
              <Group>
                <Badge variant="light">{selectedRuleForInfo.rule_type}</Badge>
                {selectedRuleForInfo.is_default && (
                  <Badge color="blue">Default Rule</Badge>
                )}
              </Group>
            </Group>
            
            {selectedRuleForInfo.description && (
              <Alert>
                <Text size="sm">{selectedRuleForInfo.description}</Text>
              </Alert>
            )}
            
            <Divider />
            
            <div>
              <Text fw={500} mb="xs">Pattern</Text>
              <Code block>{selectedRuleForInfo.pattern}</Code>
            </div>
            
            <div>
              <Text fw={500} mb="xs">Weight</Text>
              <Text size="sm">
                {selectedRuleForInfo.weight} 
                <Text span c="dimmed" size="xs" ml="xs">
                  (Higher values increase likelihood of reporting)
                </Text>
              </Text>
            </div>
            
            {selectedRuleForInfo.rule_type === 'username_regex' && (
              <div>
                <Text fw={500} mb="xs">Username Pattern Examples</Text>
                <Stack gap="xs">
                  <Text size="sm" c="dimmed">This pattern matches usernames. Examples:</Text>
                  <div><Code>^spam.*</Code> <Text size="xs" c="dimmed" ml="sm">- Matches usernames starting with "spam"</Text></div>
                  <div><Code>.*bot$</Code> <Text size="xs" c="dimmed" ml="sm">- Matches usernames ending with "bot"</Text></div>
                  <div><Code>{'\\\\d{8,}'}</Code> <Text size="xs" c="dimmed" ml="sm">- Matches usernames with 8+ consecutive digits</Text></div>
                </Stack>
              </div>
            )}
            
            {selectedRuleForInfo.rule_type === 'display_name_regex' && (
              <div>
                <Text fw={500} mb="xs">Display Name Pattern Examples</Text>
                <Stack gap="xs">
                  <Text size="sm" c="dimmed">This pattern matches display names. Examples:</Text>
                  <div><Code>.*[🔥💰🚀].*</Code> <Text size="xs" c="dimmed" ml="sm">- Matches names with specific emojis</Text></div>
                  <div><Code>{'[A-Z]{3,}'}</Code> <Text size="xs" c="dimmed" ml="sm">- Matches all-caps names (3+ chars)</Text></div>
                  <div><Code>.*(crypto|nft|trading).*</Code> <Text size="xs" c="dimmed" ml="sm">- Matches names containing specific terms</Text></div>
                </Stack>
              </div>
            )}
            
            {selectedRuleForInfo.rule_type === 'content_regex' && (
              <div>
                <Text fw={500} mb="xs">Content Pattern Examples</Text>
                <Stack gap="xs">
                  <Text size="sm" c="dimmed">This pattern matches post content. Examples:</Text>
                  <div><Code>.*buy.*crypto.*</Code> <Text size="xs" c="dimmed" ml="sm">- Matches posts about buying crypto</Text></div>
                  <div><Code>{'https?://[^\\\\s]*\\\\.tk'}</Code> <Text size="xs" c="dimmed" ml="sm">- Matches posts with .tk domain links</Text></div>
                  <div><Code>.*(earn|money|profit).*home.*</Code> <Text size="xs" c="dimmed" ml="sm">- Matches work-from-home scams</Text></div>
                </Stack>
              </div>
            )}
            
            {selectedRuleForInfo.trigger_count !== undefined && (
              <div>
                <Text fw={500} mb="xs">Statistics</Text>
                <Grid>
                  <Grid.Col span={6}>
                    <Text size="sm" c="dimmed">Times Triggered</Text>
                    <Text fw={500}>{selectedRuleForInfo.trigger_count}</Text>
                  </Grid.Col>
                  <Grid.Col span={6}>
                    <Text size="sm" c="dimmed">Last Triggered</Text>
                    <Text fw={500}>
                      {selectedRuleForInfo.last_triggered_at 
                        ? new Date(selectedRuleForInfo.last_triggered_at).toLocaleDateString()
                        : 'Never'
                      }
                    </Text>
                  </Grid.Col>
                </Grid>
              </div>
            )}
            
            <Button 
              variant="subtle" 
              onClick={() => setShowRuleInfoModal(false)}
              fullWidth
            >
              Close
            </Button>
          </Stack>
        )}
      </Modal>
    </Stack>
  );
}

function SettingsTab({ health, onUpdateDryRun, onUpdatePanic, saving }: {
  health: Health | null,
  onUpdateDryRun: (next: boolean) => void,
  onUpdatePanic: (next: boolean) => void,
  saving: boolean
}) {
  const [configError, setConfigError] = useState<string | null>(null);
  const [configSuccess, setConfigSuccess] = useState<string | null>(null);

  const handleConfigUpdate = async (updateFn: () => Promise<void>, successMessage: string) => {
    try {
      setConfigError(null);
      setConfigSuccess(null);
      await updateFn();
      setConfigSuccess(successMessage);
      setTimeout(() => setConfigSuccess(null), 3000);
    } catch (error: any) {
      setConfigError(error.message || 'Configuration update failed');
      setTimeout(() => setConfigError(null), 5000);
    }
  };

  return (
    <Stack gap="md">
      {/* Error/Success alerts */}
      {configError && (
        <Alert color="red" withCloseButton onClose={() => setConfigError(null)}>
          <Text size="sm">{configError}</Text>
        </Alert>
      )}
      
      {configSuccess && (
        <Alert color="green" withCloseButton onClose={() => setConfigSuccess(null)}>
          <Text size="sm">{configSuccess}</Text>
        </Alert>
      )}

      {/* System Status Card */}
      <Card withBorder padding="md">
        <Title order={4} mb="md">System Status</Title>
        {!health ? (
          <Skeleton height={90} />
        ) : (
          <Grid>
            <Grid.Col span={6}>
              <Group gap="lg">
                <Stat label="Database" ok={health.db_ok} />
                <Stat label="Redis" ok={health.redis_ok} />
                <Stat label="Overall Status" ok={health.ok} />
              </Group>
            </Grid.Col>
            <Grid.Col span={6}>
              <Group gap="lg">
                <Stat label="Version" value={health.version || 'Unknown'} />
                <Stat label="Batch Size" value={String(health.batch_size)} />
                <Text size="xs" c="dimmed">
                  Last updated: {health.timestamp ? new Date(health.timestamp).toLocaleString() : 'Unknown'}
                </Text>
              </Group>
            </Grid.Col>
          </Grid>
        )}
      </Card>

      {/* Runtime Controls Card */}
      <Card withBorder padding="md">
        <Title order={4} mb="md">Runtime Controls</Title>
        <Stack gap="md">
          <Group justify="space-between" align="flex-start">
            <div>
              <Group gap="xs" align="center">
                <Text fw={500}>Dry Run Mode</Text>
                <Tooltip 
                  label="When enabled, no reports are sent; use this to test your rules safely."
                  withArrow
                  position="top"
                  multiline
                  w={300}
                  aria-label="Dry Run Mode information"
                >
                  <IconInfoCircle size={16} style={{ color: 'var(--mantine-color-dimmed)', cursor: 'help' }} />
                </Tooltip>
              </Group>
              <Text size="sm" c="dimmed">
                When enabled, analyses will run but no reports will be submitted to Mastodon.
                Use this for testing rules and configurations safely.
              </Text>
              <Badge 
                color={health?.dry_run ? "blue" : "gray"} 
                variant="light" 
                size="sm" 
                mt="xs"
              >
                {health?.dry_run ? "ENABLED - Testing Mode" : "DISABLED - Live Mode"}
              </Badge>
            </div>
            <Switch
              size="lg"
              checked={!!health?.dry_run}
              onChange={(e) => handleConfigUpdate(
                async () => onUpdateDryRun(e.currentTarget.checked),
                `Dry run mode ${e.currentTarget.checked ? 'enabled' : 'disabled'}`
              )}
              disabled={!health || saving}
              color="blue"
            />
          </Group>
          
          <Divider />
          
          <Group justify="space-between" align="flex-start">
            <div>
              <Group gap="xs" align="center">
                <Text fw={500}>Panic Stop</Text>
                <Tooltip 
                  label="When active, all polling and reporting pauses immediately."
                  withArrow
                  position="top"
                  multiline
                  w={300}
                  aria-label="Panic Stop information"
                >
                  <IconInfoCircle size={16} style={{ color: 'var(--mantine-color-dimmed)', cursor: 'help' }} />
                </Tooltip>
              </Group>
              <Text size="sm" c="dimmed">
                Emergency stop for all polling and reporting operations. 
                Use this to immediately halt all automated moderation activities.
              </Text>
              <Badge 
                color={health?.panic_stop ? "red" : "gray"} 
                variant="light" 
                size="sm" 
                mt="xs"
              >
                {health?.panic_stop ? "ACTIVE - All Operations Stopped" : "INACTIVE - Normal Operations"}
              </Badge>
            </div>
            <Switch
              size="lg"
              checked={!!health?.panic_stop}
              onChange={(e) => handleConfigUpdate(
                async () => onUpdatePanic(e.currentTarget.checked),
                `Panic stop ${e.currentTarget.checked ? 'activated' : 'deactivated'}`
              )}
              disabled={!health || saving}
              color="red"
            />
          </Group>
          
        </Stack>
      </Card>

      {/* Configuration Information Card */}
      <Card withBorder padding="md">
        <Title order={4} mb="md">Current Configuration</Title>
        <Grid>
          <Grid.Col span={6}>
            <Stack gap="xs">
              <Group justify="space-between">
                <Text size="sm" c="dimmed">Dry Run:</Text>
                <Badge color={health?.dry_run ? "blue" : "gray"} variant="light" size="sm">
                  {health?.dry_run ? "Enabled" : "Disabled"}
                </Badge>
              </Group>
              <Group justify="space-between">
                <Text size="sm" c="dimmed">Panic Stop:</Text>
                <Badge color={health?.panic_stop ? "red" : "gray"} variant="light" size="sm">
                  {health?.panic_stop ? "Active" : "Inactive"}
                </Badge>
              </Group>
              <Group justify="space-between">
                <Text size="sm" c="dimmed">Batch Size:</Text>
                <Text size="sm" fw={500}>{health?.batch_size || 'Unknown'}</Text>
              </Group>
            </Stack>
          </Grid.Col>
          <Grid.Col span={6}>
            <Stack gap="xs">
              <Group justify="space-between">
                <Text size="sm" c="dimmed">Database:</Text>
                <Badge color={health?.db_ok ? "green" : "red"} variant="light" size="sm">
                  {health?.db_ok ? "Connected" : "Error"}
                </Badge>
              </Group>
              <Group justify="space-between">
                <Text size="sm" c="dimmed">Redis:</Text>
                <Badge color={health?.redis_ok ? "green" : "red"} variant="light" size="sm">
                  {health?.redis_ok ? "Connected" : "Error"}
                </Badge>
              </Group>
              <Group justify="space-between">
                <Text size="sm" c="dimmed">Version:</Text>
                <Text size="sm" fw={500}>{health?.version || 'Unknown'}</Text>
              </Group>
            </Stack>
          </Grid.Col>
        </Grid>
      </Card>

      {/* Help and Documentation Card */}
      <Card withBorder padding="md">
        <Title order={4} mb="md">Help & Documentation</Title>
        <Stack gap="md">
          <Text size="sm" c="dimmed">
            For more information about configuration options and troubleshooting, 
            refer to the project documentation.
          </Text>
          <Group>
            <Button variant="light" size="sm" component="a" href="/docs" target="_blank">
              View Documentation
            </Button>
            <Button variant="light" size="sm" component="a" href="/metrics" target="_blank">
              View Metrics
            </Button>
          </Group>
        </Stack>
      </Card>
    </Stack>
  );
}

function AccountDetailModal({ accountId, analyses }: { 
  accountId: string, 
  analyses: AnalysisData | null 
}) {
  if (!analyses) {
    return <Skeleton height={300} />;
  }

  return (
    <Stack gap="md">
      <Alert>
        <Text size="sm">
          Showing recent analysis results for account: <Code>{accountId}</Code>
        </Text>
      </Alert>
      
      <ScrollArea h={400}>
        <Table striped>
          <Table.Thead>
            <Table.Tr>
              <Table.Th>Type</Table.Th>
              <Table.Th>Rule/Scan</Table.Th>
              <Table.Th>Score</Table.Th>
              <Table.Th>Evidence/Result</Table.Th>
              <Table.Th>Date</Table.Th>
            </Table.Tr>
          </Table.Thead>
          <Table.Tbody>
            {analyses.analyses.map((analysis) => (
              <Table.Tr key={`${analysis.id}-${analysis.scan_type || 'traditional'}`}>
                <Table.Td>
                  <Badge 
                    color={analysis.scan_type === 'enhanced_scan' ? 'blue' : 'gray'}
                    variant="light"
                  >
                    {analysis.scan_type === 'enhanced_scan' ? 'Enhanced' : 'Traditional'}
                  </Badge>
                </Table.Td>
                <Table.Td>
                  <Badge variant="light">{analysis.rule_key}</Badge>
                  {analysis.content_hash && (
                    <Text size="xs" c="dimmed" mt="xs">
                      Hash: {analysis.content_hash.slice(0, 8)}...
                    </Text>
                  )}
                </Table.Td>
                <Table.Td>
                  <Badge 
                    color={analysis.score >= 1.0 ? "red" : analysis.score >= 0.5 ? "yellow" : "green"}
                    variant="light"
                  >
                    {analysis.score.toFixed(2)}
                  </Badge>
                </Table.Td>
                <Table.Td>
                  {analysis.scan_type === 'enhanced_scan' ? (
                    <div>
                      {analysis.scan_result && (
                        <Stack gap="xs">
                          <Text size="xs" c="dimmed">
                            Rules triggered: {Object.keys(analysis.scan_result.rule_results || {}).length}
                          </Text>
                          {analysis.needs_rescan && (
                            <Badge size="xs" color="orange">Needs Rescan</Badge>
                          )}
                          <Code>{JSON.stringify(analysis.scan_result, null, 2).slice(0, 100)}...</Code>
                        </Stack>
                      )}
                    </div>
                  ) : (
                    <Code>{JSON.stringify(analysis.evidence, null, 2).slice(0, 100)}...</Code>
                  )}
                </Table.Td>
                <Table.Td>
                  <Text size="sm" c="dimmed">
                    {analysis.created_at ? new Date(analysis.created_at).toLocaleString() : 'Unknown'}
                  </Text>
                </Table.Td>
              </Table.Tr>
            ))}
          </Table.Tbody>
        </Table>
      </ScrollArea>
    </Stack>
  );
}

function Stat({ label, ok, onColor, value }: { label: string; ok?: boolean; onColor?: string; value?: string }) {
  if (value != null) {
    return (
      <Stack gap={2}>
        <Text size="sm" c="dimmed">{label}</Text>
        <Text fw={600}>{value}</Text>
      </Stack>
    );
  }
  const color = ok ? (onColor ?? 'green') : 'gray';
  const text = ok ? 'OK' : 'Down';
  return (
    <Stack gap={2}>
      <Text size="sm" c="dimmed">{label}</Text>
      <Badge color={color} variant="light">{text}</Badge>
    </Stack>
  );
}

function ScanningTab({ 
  scanningAnalytics, 
  ruleStatistics, 
  onTriggerFederatedScan, 
  onTriggerDomainCheck, 
  onInvalidateCache, 
  loading 
}: { 
  scanningAnalytics: ScanningAnalytics | null;
  ruleStatistics: RuleStatistics | null;
  onTriggerFederatedScan: (domains?: string[]) => void;
  onTriggerDomainCheck: () => void;
  onInvalidateCache: (rule_changes?: boolean) => void;
  loading: boolean;
}) {
  if (!scanningAnalytics) {
    return <Skeleton height={400} />;
  }

  return (
    <Stack gap="md">
      {/* Active Scanning Sessions */}
      <Card withBorder padding="md">
        <Title order={4} mb="md">Active Scanning Sessions</Title>
        {scanningAnalytics.active_sessions.length === 0 ? (
          <Text c="dimmed">No active scanning sessions</Text>
        ) : (
          <Table>
            <Table.Thead>
              <Table.Tr>
                <Table.Th>Type</Table.Th>
                <Table.Th>Progress</Table.Th>
                <Table.Th>Started</Table.Th>
                <Table.Th>Status</Table.Th>
              </Table.Tr>
            </Table.Thead>
            <Table.Tbody>
              {scanningAnalytics.active_sessions.map((session) => (
                <Table.Tr key={session.id}>
                  <Table.Td>
                    <Badge variant="light">{session.session_type}</Badge>
                  </Table.Td>
                  <Table.Td>
                    <Stack gap="xs">
                      <Text size="sm">{session.accounts_processed} accounts processed</Text>
                      {session.total_accounts && (
                        <Progress 
                          value={(session.accounts_processed / session.total_accounts) * 100} 
                          size="sm" 
                        />
                      )}
                    </Stack>
                  </Table.Td>
                  <Table.Td>
                    <Text size="sm">{new Date(session.started_at).toLocaleString()}</Text>
                  </Table.Td>
                  <Table.Td>
                    <Badge color="green">Active</Badge>
                  </Table.Td>
                </Table.Tr>
              ))}
            </Table.Tbody>
          </Table>
        )}
      </Card>

      {/* Scanning Controls */}
      <Card withBorder padding="md">
        <Title order={4} mb="md">Scanning Controls</Title>
        <Group>
          <Button 
            leftSection={<IconRadar size={16} />}
            onClick={() => onTriggerFederatedScan()}
            loading={loading}
            variant="light"
          >
            Trigger Federated Scan
          </Button>
          <Button 
            leftSection={<IconShield size={16} />}
            onClick={onTriggerDomainCheck}
            loading={loading}
            variant="light"
          >
            Check Domain Violations
          </Button>
          <Button 
            leftSection={<IconRefresh size={16} />}
            onClick={() => onInvalidateCache(false)}
            loading={loading}
            variant="light"
          >
            Invalidate Cache
          </Button>
          <Button 
            leftSection={<IconTrendingUp size={16} />}
            onClick={() => onInvalidateCache(true)}
            loading={loading}
            variant="light"
            color="orange"
          >
            Force Re-scan (Rules Changed)
          </Button>
        </Group>
      </Card>

      {/* Recent Sessions */}
      <Card withBorder padding="md">
        <Title order={4} mb="md">Recent Scan Sessions</Title>
        <Table>
          <Table.Thead>
            <Table.Tr>
              <Table.Th>Type</Table.Th>
              <Table.Th>Accounts</Table.Th>
              <Table.Th>Duration</Table.Th>
              <Table.Th>Status</Table.Th>
            </Table.Tr>
          </Table.Thead>
          <Table.Tbody>
            {scanningAnalytics.recent_sessions.map((session) => (
              <Table.Tr key={session.id}>
                <Table.Td>
                  <Badge variant="light">{session.session_type}</Badge>
                </Table.Td>
                <Table.Td>{session.accounts_processed}</Table.Td>
                <Table.Td>
                  {session.completed_at && (
                    <Text size="sm">
                      {Math.round((new Date(session.completed_at).getTime() - new Date(session.started_at).getTime()) / 1000 / 60)} min
                    </Text>
                  )}
                </Table.Td>
                <Table.Td>
                  <Badge color={session.status === 'completed' ? 'green' : session.status === 'failed' ? 'red' : 'blue'}>
                    {session.status}
                  </Badge>
                </Table.Td>
              </Table.Tr>
            ))}
          </Table.Tbody>
        </Table>
      </Card>

      {/* Content Scan Statistics */}
      <Card withBorder padding="md">
        <Title order={4} mb="md">Content Scan Statistics</Title>
        <Grid>
          <Grid.Col span={4}>
            <Stat label="Total Scans" value={scanningAnalytics.content_scan_stats.total_scans.toLocaleString()} />
          </Grid.Col>
          <Grid.Col span={4}>
            <Stat label="Needs Re-scan" value={scanningAnalytics.content_scan_stats.needs_rescan.toLocaleString()} />
          </Grid.Col>
          <Grid.Col span={4}>
            <Stat 
              label="Last Scan" 
              value={scanningAnalytics.content_scan_stats.last_scan 
                ? new Date(scanningAnalytics.content_scan_stats.last_scan).toLocaleDateString()
                : 'Never'
              } 
            />
          </Grid.Col>
        </Grid>
      </Card>

      {/* Rule Statistics */}
      {ruleStatistics && (
        <Card withBorder padding="md">
          <Title order={4} mb="md">Rule Performance</Title>
          <Grid>
            <Grid.Col span={6}>
              <Title order={5} mb="sm">Most Triggered Rules</Title>
              <Stack gap="xs">
                {ruleStatistics.top_triggered_rules.slice(0, 5).map((rule) => (
                  <Card key={rule.name} withBorder padding="xs">
                    <Group justify="space-between">
                      <div>
                        <Text size="sm" fw={500}>{rule.name}</Text>
                        <Text size="xs" c="dimmed">{rule.rule_type}</Text>
                      </div>
                      <Badge>{rule.trigger_count} triggers</Badge>
                    </Group>
                  </Card>
                ))}
              </Stack>
            </Grid.Col>
            <Grid.Col span={6}>
              <Title order={5} mb="sm">Rule Summary</Title>
              <Grid>
                <Grid.Col span={6}>
                  <Stat label="Total Rules" value={ruleStatistics.total_rules.toString()} />
                </Grid.Col>
                <Grid.Col span={6}>
                  <Stat label="Enabled Rules" value={ruleStatistics.enabled_rules.toString()} />
                </Grid.Col>
                <Grid.Col span={6}>
                  <Stat label="Custom Rules" value={ruleStatistics.custom_rules.toString()} />
                </Grid.Col>
                <Grid.Col span={6}>
                  <Stat label="File Rules" value={ruleStatistics.file_rules.toString()} />
                </Grid.Col>
              </Grid>
            </Grid.Col>
          </Grid>
        </Card>
      )}
    </Stack>
  );
}

function DomainsTab({ 
  domainAnalytics, 
  onRefresh, 
  loading 
}: { 
  domainAnalytics: DomainAnalytics | null;
  onRefresh: () => void;
  loading: boolean;
}) {
  if (!domainAnalytics) {
    return <Skeleton height={400} />;
  }

  return (
    <Stack gap="md">
      {/* Domain Summary */}
      <Card withBorder padding="md">
        <Group justify="space-between" align="flex-start">
          <Title order={4}>Domain Monitoring Overview</Title>
          <Button 
            leftSection={<IconRefresh size={16} />}
            onClick={onRefresh}
            loading={loading}
            variant="light"
          >
            Refresh
          </Button>
        </Group>
        
        <Grid mt="md">
          <Grid.Col span={3}>
            <Card withBorder padding="sm" bg="blue.0">
              <Text size="sm" c="dimmed">Total Domains</Text>
              <Text size="xl" fw={700}>{domainAnalytics.summary.total_domains}</Text>
            </Card>
          </Grid.Col>
          <Grid.Col span={3}>
            <Card withBorder padding="sm" bg="green.0">
              <Text size="sm" c="dimmed">Monitored</Text>
              <Text size="xl" fw={700}>{domainAnalytics.summary.monitored_domains}</Text>
            </Card>
          </Grid.Col>
          <Grid.Col span={3}>
            <Card withBorder padding="sm" bg="orange.0">
              <Text size="sm" c="dimmed">High Risk</Text>
              <Text size="xl" fw={700}>{domainAnalytics.summary.high_risk_domains}</Text>
            </Card>
          </Grid.Col>
          <Grid.Col span={3}>
            <Card withBorder padding="sm" bg="red.0">
              <Text size="sm" c="dimmed">Defederated</Text>
              <Text size="xl" fw={700}>{domainAnalytics.summary.defederated_domains}</Text>
            </Card>
          </Grid.Col>
        </Grid>
      </Card>

      {/* Domain Alerts */}
      <Card withBorder padding="md">
        <Title order={4} mb="md">Domain Alerts</Title>
        <ScrollArea>
          <Table striped highlightOnHover>
            <Table.Thead>
              <Table.Tr>
                <Table.Th>Domain</Table.Th>
                <Table.Th>Violations</Table.Th>
                <Table.Th>Threshold</Table.Th>
                <Table.Th>Last Violation</Table.Th>
                <Table.Th>Status</Table.Th>
              </Table.Tr>
            </Table.Thead>
            <Table.Tbody>
              {domainAnalytics.domain_alerts.map((alert) => (
                <Table.Tr key={alert.domain}>
                  <Table.Td>
                    <Text fw={500}>{alert.domain}</Text>
                  </Table.Td>
                  <Table.Td>
                    <Badge 
                      color={alert.violation_count >= alert.defederation_threshold ? 'red' : 
                             alert.violation_count >= alert.defederation_threshold * 0.8 ? 'orange' : 'blue'}
                      variant="light"
                    >
                      {alert.violation_count}
                    </Badge>
                  </Table.Td>
                  <Table.Td>
                    <Text size="sm">{alert.defederation_threshold}</Text>
                  </Table.Td>
                  <Table.Td>
                    <Text size="sm" c="dimmed">
                      {alert.last_violation_at 
                        ? new Date(alert.last_violation_at).toLocaleDateString()
                        : 'Never'
                      }
                    </Text>
                  </Table.Td>
                  <Table.Td>
                    {alert.is_defederated ? (
                      <Badge color="red">Defederated</Badge>
                    ) : alert.violation_count >= alert.defederation_threshold * 0.8 ? (
                      <Badge color="orange">High Risk</Badge>
                    ) : (
                      <Badge color="green">Monitored</Badge>
                    )}
                  </Table.Td>
                </Table.Tr>
              ))}
            </Table.Tbody>
          </Table>
        </ScrollArea>
      </Card>

      {/* Help Information */}
      <Card withBorder padding="md">
        <Title order={5} mb="sm">About Domain Monitoring</Title>
        <Text size="sm" c="dimmed">
          Domain monitoring tracks violations across federated instances. When a domain accumulates 
          violations above the threshold, it can be automatically marked for defederation. High-risk 
          domains (80% of threshold) are highlighted for manual review.
        </Text>
      </Card>
    </Stack>
  );
}