#!/usr/bin/env node
/**
 * LIAM API Signature Generator
 *
 * Generates ECDSA signatures for the LIAM Memory API
 * Algorithm: ECDSA | Curve: P-256 | Hash: SHA-256 | Output: DER-encoded Base64
 */

const crypto = require('node:crypto');

// =============================================================================
// Configuration
// =============================================================================

const PRIVATE_KEY = `-----BEGIN PRIVATE KEY-----
MIGHAgEAMBMGByqGSM49AgEGCCqGSM49AwEHBG0wawIBAQQg0C3EVfhq29fpvxeU
JHP96Qf2iTcATg14W+HsuOC7ueChRANCAAQz6kTluY0JSlo0tnZ7jaWPNoeudS7q
jm3tp4/Md2N5kongspvOEWx50s6JBq5EZcxvxMxssH5GK+cv8tD+M3GZ
-----END PRIVATE KEY-----`;

const API_KEY = 'Ivt0b0on0BV8ghMhtkQrdKLTi1DWWVTtM5jdGaA';
const USER_KEY = '764f0fb139e37fc010c6094da980615b5e9542a4b9525a5f9d403c1c79bede67';

// =============================================================================
// Signature Generation (Node.js crypto - produces DER format by default)
// =============================================================================

function signRequest(data) {
  const sign = crypto.createSign('SHA256');
  sign.update(data);
  sign.end();
  // Node.js crypto.sign with ECDSA keys produces DER-encoded signatures by default
  return sign.sign(PRIVATE_KEY, 'base64');
}

// =============================================================================
// Generate Signature for Sample Payload
// =============================================================================

// Sample payload for creating a memory
const payload = {
  userKey: USER_KEY,
  content: 'I love hiking in the mountains during summer and prefer coffee without sugar.',
  tag: 'preferences',
  sessionId: '2025121900001'
};

const bodyString = JSON.stringify(payload);
const signature = signRequest(bodyString);

console.log('');
console.log('╔═══════════════════════════════════════════════════════════════════╗');
console.log('║               LIAM API - Signature Generator                      ║');
console.log('╚═══════════════════════════════════════════════════════════════════╝');
console.log('');
console.log('REQUEST DETAILS:');
console.log('────────────────────────────────────────────────────────────────────');
console.log('Endpoint: POST https://api.liam.netxd.com/api/memory/create');
console.log('');
console.log('HEADERS:');
console.log('────────────────────────────────────────────────────────────────────');
console.log(`Content-Type: application/json`);
console.log(`apiKey: ${API_KEY}`);
console.log(`signature: ${signature}`);
console.log('');
console.log('BODY (JSON):');
console.log('────────────────────────────────────────────────────────────────────');
console.log(JSON.stringify(payload, null, 2));
console.log('');
console.log('BODY (raw string for signing):');
console.log('────────────────────────────────────────────────────────────────────');
console.log(bodyString);
console.log('');
console.log('════════════════════════════════════════════════════════════════════');
console.log('CURL COMMAND:');
console.log('════════════════════════════════════════════════════════════════════');
console.log(`curl -X POST 'https://api.liam.netxd.com/api/memory/create' \\
  -H 'Content-Type: application/json' \\
  -H 'apiKey: ${API_KEY}' \\
  -H 'signature: ${signature}' \\
  -d '${bodyString}'`);
console.log('');
