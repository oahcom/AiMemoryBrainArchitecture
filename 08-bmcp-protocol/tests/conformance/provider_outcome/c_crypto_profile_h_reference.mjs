// H-authored Node.js JCS/Ed25519 verifier for C candidate vectors.
import canonicalize from "canonicalize";
import { createHash, createPrivateKey, createPublicKey, sign } from "node:crypto";
import { readFileSync } from "node:fs";

const fixtureDir = new URL("./fixtures/", import.meta.url);
const manifest = JSON.parse(readFileSync(new URL("c_crypto_profile_vector.json", fixtureDir), "utf8"));
const recordsFile = JSON.parse(readFileSync(new URL("c_submit_outcome_1_0_0_vectors.json", fixtureDir), "utf8"));
const byId = Object.fromEntries(recordsFile.vectors.map(v => [v.id, v.record]));
const seed = Buffer.from(manifest.seed_hex, "hex");
const pkcs8Prefix = Buffer.from("302e020100300506032b657004220420", "hex");
const privateKey = createPrivateKey({ key: Buffer.concat([pkcs8Prefix, seed]), format: "der", type: "pkcs8" });
const publicKey = createPublicKey(privateKey);
const publicDer = publicKey.export({ format: "der", type: "spki" });
const publicRaw = publicDer.subarray(publicDer.length - 32);

const results = manifest.vector_ids.map(id => {
  const record = byId[id];
  const p0 = Object.fromEntries(Object.entries(record).filter(([key]) => key !== "payload_digest" && key !== "signature"));
  const p0Bytes = Buffer.from(canonicalize(p0), "utf8");
  const digest = createHash("sha256").update(Buffer.concat([
    Buffer.from("AIMBA-C-PAYLOAD-v1\0", "ascii"), p0Bytes
  ])).digest("hex");
  const signed = { ...p0, payload_digest: digest };
  const signedBytes = Buffer.from(canonicalize(signed), "utf8");
  const preimage = Buffer.concat([
    Buffer.from("AIMBA-C-SIGNATURE-v1\0AIMBA-C-CRYPTO-1.0\0", "ascii"),
    Buffer.from(record.message_type, "ascii"),
    Buffer.from("\0", "ascii"),
    signedBytes
  ]);
  const signature = sign(null, preimage, privateKey);
  return {
    id: record.record_id,
    p0_sha256: createHash("sha256").update(p0Bytes).digest("hex"),
    payload_digest: digest,
    signed_projection_sha256: createHash("sha256").update(signedBytes).digest("hex"),
    signature_preimage_sha256: createHash("sha256").update(preimage).digest("hex"),
    public_key_hex: publicRaw.toString("hex"),
    signature_base64url: signature.toString("base64url")
  };
});
process.stdout.write(JSON.stringify(results));
