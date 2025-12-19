#!/usr/bin/env node
/**
 * Standalone script to create a memory via the LIAM API
 *
 * Usage: node create-memory.js
 *
 * This script demonstrates creating a memory with proper ECDSA authentication.
 */

const crypto = require('node:crypto');

// =============================================================================
// Configuration
// =============================================================================

const BASE_URL = 'https://api.liam.netxd.com';
const API_KEY = 'Ivt0b0on0BV8ghMhtkQrdKLTi1DWWVTtM5jdGaA';
const USER_KEY = '764f0fb139e37fc010c6094da980615b5e9542a4b9525a5f9d403c1c79bede67';

const PRIVATE_KEY = `-----BEGIN PRIVATE KEY-----
MIGHAgEAMBMGByqGSM49AgEGCCqGSM49AwEHBG0wawIBAQQg0C3EVfhq29fpvxeU
JHP96Qf2iTcATg14W+HsuOC7ueChRANCAAQz6kTluY0JSlo0tnZ7jaWPNoeudS7q
jm3tp4/Md2N5kongspvOEWx50s6JBq5EZcxvxMxssH5GK+cv8tD+M3GZ
-----END PRIVATE KEY-----`;

// =============================================================================
// ECDSA Signature Function
// =============================================================================

function signRequest(data) {
  const sign = crypto.createSign('SHA256');
  sign.update(data);
  sign.end();
  return sign.sign(PRIVATE_KEY, 'base64');
}

// =============================================================================
// API Request Function
// =============================================================================

async function apiRequest(endpoint, payload) {
  const url = `${BASE_URL}${endpoint}`;
  const bodyString = JSON.stringify(payload);
  const signature = signRequest(bodyString);

  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log('REQUEST:');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log(`URL: ${url}`);
  console.log(`Body: ${bodyString}`);
  console.log(`Signature: ${signature}`);
  console.log('');

  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'apiKey': API_KEY,
      'signature': signature
    },
    body: bodyString
  });

  const data = await response.json();

  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log('RESPONSE:');
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log(`HTTP Status: ${response.status}`);
  console.log(`Body: ${JSON.stringify(data, null, 2)}`);
  console.log('');

  return { status: response.status, data };
}

// =============================================================================
// Main
// =============================================================================

async function main() {
  console.log('');
  console.log('╔═══════════════════════════════════════════════════════════╗');
  console.log('║           LIAM Memory API - Create Memory Test            ║');
  console.log('╚═══════════════════════════════════════════════════════════╝');
  console.log('');

  // Generate a unique session ID
  const now = new Date();
  const sessionId = now.toISOString().slice(0, 10).replace(/-/g, '') +
                    String(Math.floor(Math.random() * 100000)).padStart(5, '0');

  // Create a sample memory
  const payload = {
    userKey: USER_KEY,
    content: 'I love hiking in the mountains during summer and prefer coffee without sugar.',
    tag: 'preferences',
    sessionId: sessionId
  };

  try {
    const result = await apiRequest('/api/memory/create', payload);

    if (result.data.status === 'Success') {
      console.log('✅ Memory created successfully!');
    } else {
      console.log('❌ Failed to create memory:', result.data.message);
    }
  } catch (error) {
    console.error('❌ Error:', error.message);
  }
}

main();
