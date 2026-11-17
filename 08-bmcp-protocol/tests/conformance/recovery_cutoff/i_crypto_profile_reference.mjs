// Independent Node.js RFC 8785 + Ed25519 oracle. TEST-ONLY deterministic seed.
import canonicalize from "canonicalize";
import { createHash, createPrivateKey, createPublicKey, sign } from "node:crypto";
import { readFileSync } from "node:fs";

const vector = JSON.parse(readFileSync(new URL("./i_crypto_profile_vector.json", import.meta.url), "utf8"));
const seed = Buffer.from(vector.seed_hex, "hex");
const pkcs8Prefix = Buffer.from("302e020100300506032b657004220420", "hex");
const privateKey = createPrivateKey({ key: Buffer.concat([pkcs8Prefix, seed]), format: "der", type: "pkcs8" });
const publicKey = createPublicKey(privateKey);
const publicDer = publicKey.export({ format: "der", type: "spki" });
const publicRaw = publicDer.subarray(publicDer.length - 32);

const output = vector.vectors.map(v => {
  const p0Bytes = Buffer.from(canonicalize(v.p0), "utf8");
  const digest = createHash("sha256")
    .update(Buffer.concat([Buffer.from("AIMBA-I-PAYLOAD-v1\0", "ascii"), p0Bytes]))
    .digest("hex");
  const signedProjection = { ...v.p0, [v.digest_field]: digest };
  const signedBytes = Buffer.from(canonicalize(signedProjection), "utf8");
  const preimage = Buffer.concat([
    Buffer.from("AIMBA-I-SIGNATURE-v1\0AIMBA-I-CRYPTO-1.0\0", "ascii"),
    Buffer.from(v.message_type, "ascii"),
    Buffer.from("\0", "ascii"),
    signedBytes,
  ]);
  const signature = sign(null, preimage, privateKey);
  return {
    id: v.id,
    p0_canonical_utf8: p0Bytes.toString("utf8"),
    digest,
    signed_projection_canonical_utf8: signedBytes.toString("utf8"),
    signature_preimage_hex: preimage.toString("hex"),
    public_key_hex: publicRaw.toString("hex"),
    signature_base64url: signature.toString("base64url"),
  };
});
process.stdout.write(JSON.stringify(output));
