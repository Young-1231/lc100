// Lazy-loading data layer. All JSON lives under ./data/.
const cache = {
  problems: null, days: null, byId: new Map(), patterns: null,
  algos: null, algoFamilies: null, algoById: new Map(),
};

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

// ===== 算法基础 / 经典算法 =====
export async function getAlgos() {
  if (cache.algos) return cache.algos;
  const r = await fetch(`${BASE}/algos.json`);
  cache.algos = await r.json();
  return cache.algos;
}

export async function getAlgoFamilies() {
  if (cache.algoFamilies) return cache.algoFamilies;
  const r = await fetch(`${BASE}/algo_families.json`);
  cache.algoFamilies = await r.json();
  return cache.algoFamilies;
}

export async function getAlgo(id) {
  if (cache.algoById.has(id)) return cache.algoById.get(id);
  const r = await fetch(`${BASE}/algos/${id}.json`);
  if (!r.ok) throw new Error(`Algo ${id} not found`);
  const data = await r.json();
  cache.algoById.set(id, data);
  return data;
}
