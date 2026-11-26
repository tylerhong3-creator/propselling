// Shared math for the record page, the story generator and the CLI.
export const GRADED = ["win", "loss", "push"];

export function toWin(odds, units) {
  return odds > 0 ? (units * odds) / 100 : (units * 100) / Math.abs(odds);
}

export function profit(p) {
  if (p.result === "win") return toWin(p.odds, p.units);
  if (p.result === "loss") return -p.units;
  return 0;
}

export function summarize(picks) {
  const graded = picks.filter((p) => GRADED.includes(p.result));
  const wins = graded.filter((p) => p.result === "win").length;
  const losses = graded.filter((p) => p.result === "loss").length;
  const pushes = graded.filter((p) => p.result === "push").length;
  const units = graded.reduce((s, p) => s + profit(p), 0);
  const risked = graded.filter((p) => p.result !== "push").reduce((s, p) => s + p.units, 0);
  // Current streak, newest first.
  const decided = graded.filter((p) => p.result !== "push").sort(byNewest);
  let streak = "";
  if (decided.length) {
    const r = decided[0].result;
    let n = 0;
    while (n < decided.length && decided[n].result === r) n++;
    streak = `${r === "win" ? "W" : "L"}${n}`;
  }
  return {
    wins, losses, pushes, units, risked, streak,
    pending: picks.filter((p) => p.result === "pending").length,
    winPct: wins + losses ? wins / (wins + losses) : 0,
    roi: risked ? units / risked : 0,
  };
}

export function byNewest(a, b) {
  return (b.date + b.postedAt).localeCompare(a.date + a.postedAt) || b.id - a.id;
}

export const fmtOdds = (o) => (o > 0 ? `+${o}` : `${o}`);
export const fmtUnits = (u) => `${u >= 0 ? "+" : ""}${u.toFixed(2)}u`;
export const fmtRecord = (s) => `${s.wins}-${s.losses}${s.pushes ? `-${s.pushes}` : ""}`;
export const fmtPct = (x) => `${(x * 100).toFixed(1)}%`;
