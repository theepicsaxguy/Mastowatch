import { useEffect, useMemo, useState } from 'react';
import {
  AppShell, Group, Text, Container, Card, Stack, Badge, Button, Switch,
  TextInput, ActionIcon, Tooltip, Divider, Skeleton
} from '@mantine/core';
import { IconRefresh, IconKey } from '@tabler/icons-react';
import { apiFetch, getStoredApiKey, setStoredApiKey } from './api';

type Health = {
  ok: boolean;
  db_ok: boolean;
  redis_ok: boolean;
  dry_run: boolean;
  panic_stop: boolean;
  batch_size: number;
};

export default function App() {
  const [apiKey, setApiKey] = useState<string>(getStoredApiKey() ?? '');
  const [health, setHealth] = useState<Health | null>(null);
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);

  const statusBadge = useMemo(() => {
    if (!health) return null;
    const color = health.ok ? 'green' : 'red';
    return <Badge color={color}>{health.ok ? 'Healthy' : 'Degraded'}</Badge>;
  }, [health]);

  async function loadHealth() {
    setLoading(true);
    try {
      const data = await apiFetch<Health>('/healthz');
      setHealth(data);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadHealth();
  }, []);

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
    } finally {
      setSaving(false);
    }
  }

  function persistKey(v: string) {
    setApiKey(v);
    setStoredApiKey(v);
  }

  return (
    <AppShell
      header={{ height: 56 }}
      padding="md"
      withBorder={false}
    >
      <AppShell.Header>
        <Container size="lg" h="100%">
          <Group h="100%" justify="space-between">
            <Group gap="xs">
              <Text fw={700}>MastoWatch</Text>
              {statusBadge}
            </Group>
            <Group>
              <TextInput
                leftSection={<IconKey size={16} />}
                placeholder="API key"
                value={apiKey}
                onChange={(e) => persistKey(e.currentTarget.value)}
                w={280}
                aria-label="API key"
              />
              <Tooltip label="Refresh health">
                <ActionIcon variant="light" onClick={loadHealth} aria-label="Refresh health">
                  <IconRefresh size={16} />
                </ActionIcon>
              </Tooltip>
            </Group>
          </Group>
        </Container>
      </AppShell.Header>

      <AppShell.Main>
        <Container size="lg">
          <Stack gap="md">
            <Card withBorder radius="md" padding="md">
              <Group justify="space-between" align="flex-start">
                <Stack gap={4}>
                  <Text fw={600}>Instance status</Text>
                  <Text c="dimmed" size="sm">Quick overview of service health.</Text>
                </Stack>
                <Button variant="light" onClick={loadHealth} leftSection={<IconRefresh size={16} />} loading={loading}>
                  Reload
                </Button>
              </Group>
              <Divider my="md" />
              {!health ? (
                <Skeleton height={90} />
              ) : (
                <Group gap="lg">
                  <Stat label="Database" ok={health.db_ok} />
                  <Stat label="Redis" ok={health.redis_ok} />
                  <Stat label="Dry run" ok={health.dry_run} onColor="blue" />
                  <Stat label="Panic stop" ok={health.panic_stop} onColor="red" />
                  <Stat label="Batch size" value={String(health.batch_size)} />
                </Group>
              )}
            </Card>

            <Card withBorder radius="md" padding="md">
              <Stack gap="xs">
                <Text fw={600}>Controls</Text>
                <Text c="dimmed" size="sm">Toggle runtime behavior (requires API key).</Text>
              </Stack>
              <Divider my="md" />
              <Stack gap="md">
                <Group justify="space-between">
                  <Text>Dry run (no reports submitted)</Text>
                  <Switch
                    checked={!!health?.dry_run}
                    onChange={(e) => updateDryRun(e.currentTarget.checked)}
                    disabled={!health || saving}
                  />
                </Group>
                <Group justify="space-between">
                  <Text>Panic stop (pause polling & reporting)</Text>
                  <Switch
                    checked={!!health?.panic_stop}
                    onChange={(e) => updatePanic(e.currentTarget.checked)}
                    disabled={!health || saving}
                    color="red"
                  />
                </Group>
                <Group justify="space-between">
                  <Text>Rules</Text>
                  <Button variant="light" onClick={reloadRules} disabled={saving}>
                    Reload rules
                  </Button>
                </Group>
              </Stack>
            </Card>
          </Stack>
        </Container>
      </AppShell.Main>
    </AppShell>
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