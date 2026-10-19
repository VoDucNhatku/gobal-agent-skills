// Grade one case from its raw dsh --json event stream.
export function gradeEvents(c, raw, { armDir, capMap }) {
  const events = raw.split('\n').filter(Boolean).map((l) => { try { return JSON.parse(l); } catch { return null; } }).filter(Boolean);
  const final = events.filter((e) => e.type === 'final').map((e) => e.text).join('\n')
    || events.filter((e) => e.type === 'text').map((e) => e.text).join('');
  const calls = events.filter((e) => e.type === 'tool_call');
  const loaded = calls.filter((e) => e.tool === 'skill').map((e) => e.input?.name).filter(Boolean);
  // v2 registry route: SKILL.md read from the arm directory counts as engaging that skill.
  const armNorm = armDir.replace(/\\/g, '/').toLowerCase();
  for (const e of calls) {
    if (e.tool === 'skill') continue;
    const s = JSON.stringify(e.input ?? {}).replace(/\\\\/g, '/').toLowerCase();
    const m = s.match(/([a-z0-9-]+)\/skill\.md/);
    if (m && s.includes(armNorm.slice(-30))) loaded.push(m[1]);
  }
  let input = 0; let output = 0; let steps = 0;
  for (const e of events) {
    if (e.type === 'status' && e.phase === 'step_end' && e.usage) {
      steps++;
      input += (e.usage.inputTokens ?? 0) + (e.usage.cacheReadTokens ?? 0);
      output += e.usage.outputTokens ?? 0;
    }
  }
  const checks = [];
  const has = (cap) => (capMap[cap] ?? []).some((s) => loaded.includes(s));
  for (const cap of c.expect ?? []) checks.push({ check: `expect:${cap}`, pass: has(cap) });
  for (const cap of c.forbid ?? []) checks.push({ check: `forbid:${cap}`, pass: !has(cap) });
  if (c.forbidAnySkill) checks.push({ check: 'forbid:any-skill', pass: loaded.length === 0 });
  for (const re of c.must ?? []) checks.push({ check: `must:${re.source}`, pass: new RegExp(re.source, 'iu').test(final) });
  for (const re of c.mustNot ?? []) checks.push({ check: `mustNot:${re.source}`, pass: !new RegExp(re.source, 'iu').test(final) });
  const completed = events.some((e) => e.type === 'final');
  if (!completed) checks.push({ check: 'completed', pass: false });
  return {
    id: c.id, kind: c.kind,
    pass: checks.every((x) => x.pass), score: checks.filter((x) => x.pass).length / Math.max(1, checks.length),
    checks, skills: [...new Set(loaded)], toolCalls: calls.length, steps, inputTokens: input, outputTokens: output,
    finalChars: final.length,
  };
}
