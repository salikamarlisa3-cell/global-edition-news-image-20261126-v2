// Entry for news-image-20261126: "The World in One Day — 26 Nov 2026".
//
// One image sums up Thursday 26 November 2026: 56 verified stories in
// 7 regions, a dot-matrix world map with 7 pins, 16 front-page leads,
// a weather strip and a "left out & why" date-check box. Every story
// is cited in SOURCES.md. The page is authored as poster.svg (built by
// build_poster.py) and rendered to entry.png by generate.mjs.
//
// This program's whole job is delivery: hand the judge the rendered
// page byte for byte. It reads entry.png from beside itself, writes it
// to the output directory ($MAKEFUN_OUTPUT_DIR, or /output in the
// grader's container), then verifies the copy landed at full size.

import { readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';

// Resolve paths from this file's own URL so the program works from
// any working directory the grader chooses to start it in.
const here = fileURLToPath(new URL('.', import.meta.url));
const page = readFileSync(join(here, 'entry.png'));
const target = join(process.env.MAKEFUN_OUTPUT_DIR ?? '/output', 'entry.png');
writeFileSync(target, page);

const landed = readFileSync(target);
if (landed.length !== page.length) {
  throw new Error(
    `entry.png copy is ${landed.length} bytes, expected ${page.length}`);
}
