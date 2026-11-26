#!/usr/bin/env node
// Manage data/picks.json from the terminal.
//
//   node scripts/picks.mjs add --sport NBA --game "Lakers @ Celtics" --pick "Lakers +4.5" --odds -110 --units 1 [--date 2026-11-26] [--note "..."]
//   node scripts/picks.mjs grade <id> win|loss|push|void
//   node scripts/picks.mjs list [--pending]
//   node scripts/picks.mjs record
import { readFileSync, writeFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { summarize, profit, byNewest, fmtOdds, fmtUnits, fmtRecord, fmtPct } from "../js/stats.js";

const FILE = fileURLToPath(new URL("../data/picks.json", import.meta.url));
const load = () => JSON.parse(readFileSync(FILE, "utf8"));
const save = (picks) => writeFileSync(FILE, JSON.stringify(picks, null, 2) + "\n");

function flags(args) {
  const out = { _: [] };
  for (let i = 0; i < args.length; i++) {
    if (args[i].startsWith("--")) {
      const key = args[i].slice(2);
      const next = args[i + 1];
      if (next === undefined || next.startsWith("--")) out[key] = true;
      else { out[key] = next; i++; }
    } else out._.push(args[i]);
  }
  return out;
}

const die = (msg) => { console.error(msg); process.exit(1); };
const today = () => new Date().toLocaleDateString("en-CA"); // YYYY-MM-DD, local time
const line = (p) =>
  `#${String(p.id).padEnd(4)} ${p.date}  ${p.sport.padEnd(5)} ${p.pick} (${fmtOdds(p.odds)}, ${p.units}u)  — ${p.game}  [${p.result}${p.result !== "pending" && p.result !== "void" ? " " + fmtUnits(profit(p)) : ""}]`;

const [cmd, ...rest] = process.argv.slice(2);
const f = flags(rest);
const picks = load();

switch (cmd) {
  case "add": {
    for (const k of ["sport", "game", "pick", "odds"]) if (!f[k] || f[k] === true) die(`Missing --${k}`);
    const odds = Number(f.odds);
    const units = f.units ? Number(f.units) : 1;
    if (!Number.isFinite(odds) || Math.abs(odds) < 100) die("--odds must be American odds like -110 or +150");
    if (!(units > 0)) die("--units must be a positive number");
    const pick = {
      id: picks.reduce((m, p) => Math.max(m, p.id), 0) + 1,
      date: f.date || today(),
      postedAt: new Date().toISOString(),
      sport: String(f.sport).toUpperCase(),
      game: f.game,
      pick: f.pick,
      odds,
      units,
      result: "pending",
      ...(f.note && f.note !== true ? { note: f.note } : {}),
    };
    picks.push(pick);
    save(picks);
    console.log("Added " + line(pick));
    break;
  }
  case "grade": {
    const [id, result] = f._;
    if (!["win", "loss", "push", "void"].includes(result)) die("Result must be win, loss, push or void");
    const p = picks.find((x) => x.id === Number(id));
    if (!p) die(`No pick #${id}`);
    p.result = result;
    p.gradedAt = new Date().toISOString();
    save(picks);
    console.log("Graded " + line(p));
    break;
  }
  case "list": {
    const shown = picks.filter((p) => !f.pending || p.result === "pending").sort(byNewest);
    console.log(shown.length ? shown.map(line).join("\n") : "No picks.");
    break;
  }
  case "record": {
    const s = summarize(picks);
    console.log(`Record ${fmtRecord(s)} | ${fmtUnits(s.units)} | Win ${fmtPct(s.winPct)} | ROI ${fmtPct(s.roi)} | Streak ${s.streak || "-"} | Pending ${s.pending}`);
    break;
  }
  default:
    console.log(readFileSync(fileURLToPath(import.meta.url), "utf8").split("\n").slice(1, 8).join("\n").replace(/^\/\/ ?/gm, ""));
}
