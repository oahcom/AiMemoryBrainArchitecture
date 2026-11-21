// Independent JavaScript implementation of HRC-TEST-v1 only.
// This is a differential test oracle, not a production canonicalization profile.
import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";

const vectors = JSON.parse(readFileSync(new URL("./wire_interop_vectors.json", import.meta.url), "utf8"));

function canonical(value) {
  if (value === null) return "null";
  if (typeof value === "string" || typeof value === "boolean") return JSON.stringify(value);
  if (typeof value === "number") {
    if (!Number.isFinite(value)) throw new Error("non-finite number");
    return JSON.stringify(value);
  }
  if (Array.isArray(value)) return "[" + value.map(canonical).join(",") + "]";
  if (typeof value === "object") {
    const keys = Object.keys(value).sort();
    return "{" + keys.map(k => JSON.stringify(k) + ":" + canonical(value[k])).join(",") + "}";
  }
  throw new Error("unsupported value");
}

const output = vectors.map(v => {
  const bytes = Buffer.from(canonical(v.value), "utf8");
  const digest = createHash("sha256")
    .update(Buffer.from(v.domain + "\0", "utf8"))
    .update(bytes)
    .digest("hex");
  return { id: v.id, canonical_utf8: bytes.toString("utf8"), digest_sha256: digest };
});
process.stdout.write(JSON.stringify(output));
