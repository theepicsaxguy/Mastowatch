import { useEffect, useMemo, useState } from 'react';
import {
  AppShell, Group, Text, Container, Card, Stack, Badge, Button, Switch,
  ActionIcon, Tooltip, Divider, Skeleton, Grid, Table, Modal, Alert, 
  Tabs, Select, Progress, Code, ScrollArea, TextInput, Title
} from '@mantine/core';
import { IconRefresh, IconEye, IconChartBar, IconUsers, IconFlag, IconSettings, IconRuler } from '@tabler/icons-react';
import { 
  LineChart, Line, XAxis, YAxis, CartesianGrid, ResponsiveContainer,
  BarChart, Bar, PieChart, Pie, Cell, AreaChart, Area
} from 'recharts';
import { apiFetch } from './api';
import { 
  fetchOverview, fetchTimeline, fetchAccounts, fetchReports, 
  fetchAccountAnalyses, fetchCurrentRules, OverviewMetrics, 
  TimelineData, AccountData, ReportData, AnalysisData, RulesData 
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
  const [selectedAccount, setSelectedAccount] = useState<string | null>(null);
  const [accountAnalyses, setAccountAnalyses] = useState<AnalysisData | null>(null);
  const [timeRange, setTimeRange] = useState('7');
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [refreshing, setRefreshing] = useState(false);

  const statusBadge = useMemo(() => {
    if (!health) return null;
    const color = health.ok ? 'green' : 'red';
    return <Badge color={color}>{health.ok ? 'Healthy' : 'Degraded'}</Badge>;
  }, [health]);

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
      const data = await fetchCurrentRules();
      setRules(data);
    } catch (error) {
      console.error('Failed to load rules:', error);
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
        loadRules()
      ]);
    } finally {
      setRefreshing(false);
    }
  }

  useEffect(() => {
    refreshAllData();
  }, []);

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

  async function reloadRules() {
    setSaving(true);
    try {
      await apiFetch('/config/rules/reload', { method: 'POST' });
      await loadRules();
    } finally {
      setSaving(false);
    }
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
              <RulesTab rules={rules} onReload={reloadRules} saving={saving} />
            </Tabs.Panel>

            <Tabs.Panel value="settings" pt="md">
              <SettingsTab 
                health={health}
                onUpdateDryRun={updateDryRun}
                onUpdatePanic={updatePanic}
                onReloadRules={reloadRules}
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

function RulesTab({ rules, onReload, saving }: { 
  rules: RulesData | null, 
  onReload: () => void,
  saving: boolean 
}) {
  if (!rules) {
    return <Skeleton height={400} />;
  }

  return (
    <Stack gap="md">
      <Card withBorder padding="md">
        <Group justify="space-between" align="flex-start">
          <Stack gap="xs">
            <Title order={4}>Current Rules Configuration</Title>
            <Text c="dimmed" size="sm">
              Report threshold: {rules.report_threshold}
            </Text>
          </Stack>
          <Button 
            variant="light" 
            leftSection={<IconRefresh size={16} />}
            onClick={onReload}
            loading={saving}
          >
            Reload Rules
          </Button>
        </Group>
        
        <Divider my="md" />
        
        <Grid>
          <Grid.Col span={4}>
            <Card withBorder padding="sm">
              <Title order={5} mb="sm">Username Rules</Title>
              {rules.rules.username_regex?.map((rule, idx) => (
                <Group key={idx} justify="space-between" mb="xs">
                  <div>
                    <Text size="sm" fw={500}>{rule.name}</Text>
                    <Code>{rule.pattern}</Code>
                  </div>
                  <Badge variant="light">Weight: {rule.weight}</Badge>
                </Group>
              )) || <Text c="dimmed" size="sm">No rules defined</Text>}
            </Card>
          </Grid.Col>
          
          <Grid.Col span={4}>
            <Card withBorder padding="sm">
              <Title order={5} mb="sm">Display Name Rules</Title>
              {rules.rules.display_name_regex?.map((rule, idx) => (
                <Group key={idx} justify="space-between" mb="xs">
                  <div>
                    <Text size="sm" fw={500}>{rule.name}</Text>
                    <Code>{rule.pattern}</Code>
                  </div>
                  <Badge variant="light">Weight: {rule.weight}</Badge>
                </Group>
              )) || <Text c="dimmed" size="sm">No rules defined</Text>}
            </Card>
          </Grid.Col>
          
          <Grid.Col span={4}>
            <Card withBorder padding="sm">
              <Title order={5} mb="sm">Content Rules</Title>
              {rules.rules.content_regex?.map((rule, idx) => (
                <Group key={idx} justify="space-between" mb="xs">
                  <div>
                    <Text size="sm" fw={500}>{rule.name}</Text>
                    <Code>{rule.pattern}</Code>
                  </div>
                  <Badge variant="light">Weight: {rule.weight}</Badge>
                </Group>
              )) || <Text c="dimmed" size="sm">No rules defined</Text>}
            </Card>
          </Grid.Col>
        </Grid>
      </Card>
    </Stack>
  );
}

function SettingsTab({ health, onUpdateDryRun, onUpdatePanic, onReloadRules, saving }: {
  health: Health | null,
  onUpdateDryRun: (next: boolean) => void,
  onUpdatePanic: (next: boolean) => void,
  onReloadRules: () => void,
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
              <Text fw={500}>Dry Run Mode</Text>
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
              <Text fw={500}>Panic Stop</Text>
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
          
          <Divider />
          
          <Group justify="space-between" align="flex-start">
            <div>
              <Text fw={500}>Rules Configuration</Text>
              <Text size="sm" c="dimmed">
                Reload moderation rules from the configuration file. 
                This will apply any changes made to rules.yml without restarting the service.
              </Text>
            </div>
            <Button 
              variant="light" 
              leftSection={<IconRefresh size={16} />}
              onClick={() => handleConfigUpdate(
                async () => onReloadRules(),
                'Rules configuration reloaded successfully'
              )} 
              disabled={saving}
              loading={saving}
            >
              Reload Rules
            </Button>
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
              <Table.Th>Rule</Table.Th>
              <Table.Th>Score</Table.Th>
              <Table.Th>Evidence</Table.Th>
              <Table.Th>Date</Table.Th>
            </Table.Tr>
          </Table.Thead>
          <Table.Tbody>
            {analyses.analyses.map((analysis) => (
              <Table.Tr key={analysis.id}>
                <Table.Td>
                  <Badge variant="light">{analysis.rule_key}</Badge>
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
                  <Code>{JSON.stringify(analysis.evidence)}</Code>
                </Table.Td>
                <Table.Td>
                  <Text size="sm" c="dimmed">
                    {new Date(analysis.created_at).toLocaleString()}
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