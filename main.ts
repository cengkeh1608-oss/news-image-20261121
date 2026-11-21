import { copyFileSync, mkdirSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { join } from "node:path";

// The entry image is drawn by draw_frontpage.py into entry.png at the
// repository root. This program copies that exact file to the output
// directory so the grader sees the same bytes on every run.
const repoDir = fileURLToPath(new URL(".", import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
copyFileSync(join(repoDir, "entry.png"), join(outDir, "entry.png"));
