// Independent Node.js RFC 8785 + Ed25519 candidate oracle for C Provider Outcome.
import canonicalize from "canonicalize";
import { createHash, createPrivateKey, createPublicKey, sign } from "node:crypto";
import { readFileSync } from "node:fs";

const root = new URL("./", import.meta.url);
const manifest = JSON.parse(readFileSync(new URL("./c_crypto_profile_vector.json", import.meta.url), "utf8"));
const fixtures = JSON.parse(readFileSync(new URL("./c_submit_outcome_1_0_0_vectors.json", import.meta.url), "utf8"));
const byId = Object.fromEntries(fixtures.vectors.map(v => [v.id, v.record]));
const seed = Buffer.from(manifest.seed_hex, "hex");
const prefix = Buffer.from("302e020100300506032b657004220420", "hex");
const privateKey = createPrivateKey({
  key: Buffer.concat([prefix, seed]), format: "der", type: "pkcs8"
});
const publicKey = createPublicKey(privateKey);
const publicDer = publicKey.export({ format: "der", type: "spki" });
const publicRaw = publicDer.subarray(publicDer.length - 32);

const output = manifest.vector_ids.map(id => {
  const record = byId[id];
  const p0 = Object.fromEntries(Object.entries(record).filter(([k]) => !["payload_digest", "signature"].includes(k)));
  const p0Bytes = Buffer.from(canonicalize(p0), "utf8");
  const digest = createHashDigest(Buffer.concat([
    Buffer.from("AIMBA-C-PAYLOAD-v1\0", "ascii"), p0Bytes
  ]));
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
    p0_canonical_utf8: p0Bytes.toString("utf8"),
    digest,
    signed_projection_canonical_utf8: signedBytes.toString("utf8"),
    signature_preimage_hex: preimage.toString("hex"),
    public_key_hex: publicRaw.toString("hex"),
    signature_base64url: signature.toString("base64url"),
    signed_member_count: Object.keys(p0).length
  };
});
function createHashDigest(bytes) {
  return createHash("sha256").update(bytes).digest("hex");
}
process.stdout.write(JSON.stringify(output));
