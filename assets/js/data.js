// Lazy-loading data layer. All JSON lives under ./data/.
const cache = { problems: null, days: null, byId: new Map(), patterns: null };

const BASE = "./data";

export async function getProblems() {
  if (cache.problems) return cache.problems;
  const r = await fetch(`${BASE}/problems.json`);
  cache.problems = await r.json();
  return cache.problems;
}

export async function getDays() {
  if (cache.days) return cache.days;
  const r = await fetch(`${BASE}/days.json`);
  cache.days = await r.json();
  return cache.days;
}

export async function getProblem(id) {
  if (cache.byId.has(id)) return cache.byId.get(id);
  const padded = String(id).padStart(4, "0");
  const r = await fetch(`${BASE}/problems/p${padded}.json`);
  if (!r.ok) throw new Error(`Problem ${id} not found`);
  const data = await r.json();
  cache.byId.set(id, data);
  return data;
}

export async function getPattern(filename) {
  const r = await fetch(`${BASE}/patterns/${filename}`);
  if (!r.ok) throw new Error(`Pattern ${filename} not found`);
  return await r.text();
}
