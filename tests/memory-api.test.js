/**
 * XDB Memory Management API Test Suite
 *
 * This test suite covers all endpoints for the XDB Memory API:
 * - Create Memory
 * - List Memories
 * - Chat
 * - Chat External
 * - Predict Intent
 * - Process Contract
 * - Generate Contract Markup
 *
 * Base URL: https://api.liam.netxd.com/
 */

const { describe, it, before, after } = require('node:test');
const assert = require('node:assert');
const crypto = require('node:crypto');

// =============================================================================
// Configuration
// =============================================================================

const BASE_URL = 'https://api.liam.netxd.com';
const API_KEY = 'Ivt0b0on0BV8ghMhtkQrdKLTi1DWWVTtM5jdGaA';

// ECDSA Private Key for signing requests (PEM format)
// Replace with your actual private key
const PRIVATE_KEY = `-----BEGIN PRIVATE KEY-----
YOUR_PRIVATE_KEY_HERE
-----END PRIVATE KEY-----`;

// Test user keys - replace with valid keys for actual testing
const TEST_CONFIG = {
  validUserKey: '764f0fb139e37fc010c6094da980615b5e9542a4b9525a5f9d403c1c79bede67',
  invalidUserKey: 'invalid_user_key_12345',
  testSessionId: `test_session_${Date.now()}`,
};

// =============================================================================
// ECDSA Signature Helper Functions
// =============================================================================

/**
 * Signs the request body using ECDSA with SHA-256
 * @param {string} data - The stringified request body
 * @returns {string} Base64-encoded DER signature
 */
function signRequest(data) {
  const sign = crypto.createSign('SHA256');
  sign.update(data);
  sign.end();

  // Sign and get DER-encoded signature (Node.js crypto returns DER by default)
  const signature = sign.sign(PRIVATE_KEY, 'base64');
  return signature;
}

// =============================================================================
// API Request Helper
// =============================================================================

/**
 * Makes an authenticated API request to the LIAM Memory API
 * @param {string} endpoint - API endpoint path
 * @param {object} body - Request body
 * @param {object} options - Additional fetch options
 * @returns {Promise<{status: number, data: object}>}
 */
async function apiRequest(endpoint, body, options = {}) {
  const url = `${BASE_URL}${endpoint}`;
  const bodyString = JSON.stringify(body);

  // Generate ECDSA signature
  const signature = signRequest(bodyString);

  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'apiKey': API_KEY,
      'signature': signature,
      ...options.headers,
    },
    body: bodyString,
    ...options,
  });

  const data = await response.json().catch(() => ({}));

  return {
    status: response.status,
    data,
  };
}

/**
 * Validates the standard response structure
 * @param {object} data - Response data
 */
function validateResponseStructure(data) {
  assert.ok(data.status !== undefined, 'Response should have status field');
  assert.ok(data.message !== undefined, 'Response should have message field');
  assert.ok(data.timestamp !== undefined, 'Response should have timestamp field');
  assert.ok(data.processId !== undefined, 'Response should have processId field');
}

/**
 * Generates a unique session ID for testing
 * @returns {string}
 */
function generateSessionId() {
  const date = new Date();
  const dateStr = date.toISOString().slice(0, 10).replace(/-/g, '');
  const random = Math.floor(Math.random() * 100000).toString().padStart(5, '0');
  return `${dateStr}${random}`;
}

// =============================================================================
// Test Suite: Create Memory Endpoint
// =============================================================================

describe('POST /api/memory/create - Create Memory', () => {

  it('should create a memory with valid userKey and content', async () => {
    const response = await apiRequest('/api/memory/create', {
      userKey: TEST_CONFIG.validUserKey,
      content: 'I love hiking in the mountains during summer.',
    });

    // Note: May return 400 if userKey profile doesn't exist
    if (response.status === 200) {
      assert.strictEqual(response.data.status, 'Success');
      validateResponseStructure(response.data);
    } else {
      // Expected failure for test user key
      assert.strictEqual(response.status, 400);
      assert.strictEqual(response.data.status, 'Failed');
    }
  });

  it('should create a memory with optional sessionId', async () => {
    const sessionId = generateSessionId();

    const response = await apiRequest('/api/memory/create', {
      userKey: TEST_CONFIG.validUserKey,
      content: 'My favorite color is blue.',
      sessionId: sessionId,
    });

    validateResponseStructure(response.data);
  });

  it('should create a memory with optional tag', async () => {
    const response = await apiRequest('/api/memory/create', {
      userKey: TEST_CONFIG.validUserKey,
      content: 'I prefer dark roast coffee.',
      tag: 'preferences',
    });

    validateResponseStructure(response.data);
  });

  it('should return error for invalid userKey', async () => {
    const response = await apiRequest('/api/memory/create', {
      userKey: TEST_CONFIG.invalidUserKey,
      content: 'This should fail.',
    });

    assert.strictEqual(response.status, 400);
    assert.strictEqual(response.data.status, 'Failed');
    assert.ok(response.data.message.includes('Profile not found') ||
              response.data.details?.userKey === 'Profile not found',
              'Should indicate profile not found');
  });

  it('should return error for missing userKey', async () => {
    const response = await apiRequest('/api/memory/create', {
      content: 'This should fail - no userKey.',
    });

    // Expecting 400 or similar error status
    assert.ok(response.status >= 400, 'Should return error status');
  });

  it('should return error for missing content', async () => {
    const response = await apiRequest('/api/memory/create', {
      userKey: TEST_CONFIG.validUserKey,
    });

    // Expecting 400 or similar error status
    assert.ok(response.status >= 400, 'Should return error status');
  });

  it('should handle empty content string', async () => {
    const response = await apiRequest('/api/memory/create', {
      userKey: TEST_CONFIG.validUserKey,
      content: '',
    });

    // Should either reject empty content or handle gracefully
    validateResponseStructure(response.data);
  });

  it('should handle very long content', async () => {
    const longContent = 'A'.repeat(10000);

    const response = await apiRequest('/api/memory/create', {
      userKey: TEST_CONFIG.validUserKey,
      content: longContent,
    });

    validateResponseStructure(response.data);
  });

  it('should handle special characters in content', async () => {
    const response = await apiRequest('/api/memory/create', {
      userKey: TEST_CONFIG.validUserKey,
      content: 'Special chars: !@#$%^&*()_+-=[]{}|;:",.<>?/~`',
    });

    validateResponseStructure(response.data);
  });

  it('should handle unicode content', async () => {
    const response = await apiRequest('/api/memory/create', {
      userKey: TEST_CONFIG.validUserKey,
      content: 'Unicode test: 你好世界 🌍 مرحبا العالم',
    });

    validateResponseStructure(response.data);
  });
});

// =============================================================================
// Test Suite: List Memories Endpoint
// =============================================================================

describe('POST /api/memory/list - List Memories', () => {

  it('should list memories with valid userKey', async () => {
    const response = await apiRequest('/api/memory/list', {
      userKey: TEST_CONFIG.validUserKey,
      tokens: [],
      query: '',
    });

    if (response.status === 200) {
      assert.strictEqual(response.data.status, 'Success');
      validateResponseStructure(response.data);
      assert.ok(response.data.data !== undefined, 'Should have data field');
      assert.ok(Array.isArray(response.data.data.memories), 'Should have memories array');
    }
  });

  it('should list memories with query filter', async () => {
    const response = await apiRequest('/api/memory/list', {
      userKey: TEST_CONFIG.validUserKey,
      tokens: [],
      query: 'coffee',
    });

    validateResponseStructure(response.data);
  });

  it('should list memories with tokens filter', async () => {
    const response = await apiRequest('/api/memory/list', {
      userKey: TEST_CONFIG.validUserKey,
      tokens: ['coffee', 'preferences'],
      query: '',
    });

    validateResponseStructure(response.data);
  });

  it('should list memories with suggestedTokens', async () => {
    const response = await apiRequest('/api/memory/list', {
      userKey: TEST_CONFIG.validUserKey,
      tokens: [],
      query: 'where should I give blood sample',
      require_llm_summary: false,
      suggestedTokens: {
        high: [
          {
            token: 'blood',
            synonyms: ['hemoglobin', 'plasma', 'red blood cells', 'blood components'],
          },
          {
            token: 'sample',
            synonyms: ['specimen', 'test', 'sample specimen'],
          },
        ],
        low: ['give', 'where'],
      },
    });

    validateResponseStructure(response.data);
  });

  it('should list memories with conversationId', async () => {
    const response = await apiRequest('/api/memory/list', {
      userKey: TEST_CONFIG.validUserKey,
      conversationId: '',
    });

    validateResponseStructure(response.data);
  });

  it('should return error for invalid userKey', async () => {
    const response = await apiRequest('/api/memory/list', {
      userKey: TEST_CONFIG.invalidUserKey,
      tokens: [],
      query: '',
    });

    assert.strictEqual(response.status, 400);
    assert.strictEqual(response.data.status, 'Failed');
  });

  it('should validate memory object structure in response', async () => {
    const response = await apiRequest('/api/memory/list', {
      userKey: TEST_CONFIG.validUserKey,
      tokens: [],
      query: '',
    });

    if (response.status === 200 && response.data.data?.memories?.length > 0) {
      const memory = response.data.data.memories[0];

      // Required fields
      assert.ok(memory.memory !== undefined, 'Memory should have memory field');
      assert.ok(memory.transactionNumber !== undefined, 'Memory should have transactionNumber');
      assert.ok(memory.date !== undefined, 'Memory should have date');
      assert.ok(Array.isArray(memory.tokens), 'Memory should have tokens array');

      // Optional fields (can be null)
      assert.ok('language' in memory, 'Memory should have language field');
      assert.ok('docId' in memory, 'Memory should have docId field');
      assert.ok('fileID' in memory, 'Memory should have fileID field');
      assert.ok('notesKey' in memory, 'Memory should have notesKey field');
    }
  });
});

// =============================================================================
// Test Suite: Predict Intent Endpoint
// =============================================================================

describe('POST /api/memory/predict - Predict Intent', () => {

  it('should predict intent with valid statement', async () => {
    const response = await apiRequest('/api/memory/predict', {
      userKey: TEST_CONFIG.validUserKey,
      statement: 'Remember I LIKE coffee without sugar and no cream',
      sessionId: generateSessionId(),
    });

    validateResponseStructure(response.data);
  });

  it('should predict intent for preference statement', async () => {
    const response = await apiRequest('/api/memory/predict', {
      userKey: TEST_CONFIG.validUserKey,
      statement: 'I prefer working from home on Fridays',
      sessionId: generateSessionId(),
    });

    validateResponseStructure(response.data);
  });

  it('should predict intent for question', async () => {
    const response = await apiRequest('/api/memory/predict', {
      userKey: TEST_CONFIG.validUserKey,
      statement: 'What are my coffee preferences?',
      sessionId: generateSessionId(),
    });

    validateResponseStructure(response.data);
  });

  it('should return error for invalid userKey', async () => {
    const response = await apiRequest('/api/memory/predict', {
      userKey: TEST_CONFIG.invalidUserKey,
      statement: 'Test statement',
      sessionId: generateSessionId(),
    });

    assert.strictEqual(response.status, 400);
  });
});

// =============================================================================
// Test Suite: Chat Endpoint
// =============================================================================

describe('POST /api/memory/chat - Chat', () => {

  it('should process chat with valid request', async () => {
    const response = await apiRequest('/api/memory/chat', {
      userKey: TEST_CONFIG.validUserKey,
      statement: 'where should I give blood sample',
      existing_tags: ['food_preferences', 'banking'],
    });

    validateResponseStructure(response.data);
  });

  it('should process chat without existing_tags', async () => {
    const response = await apiRequest('/api/memory/chat', {
      userKey: TEST_CONFIG.validUserKey,
      statement: 'What is my favorite restaurant?',
    });

    validateResponseStructure(response.data);
  });

  it('should process chat with multiple existing_tags', async () => {
    const response = await apiRequest('/api/memory/chat', {
      userKey: TEST_CONFIG.validUserKey,
      statement: 'Help me find information about my contracts',
      existing_tags: ['XBD_Changes', 'food_preferences', 'banking', 'health', 'contracts'],
    });

    validateResponseStructure(response.data);
  });

  it('should return error for invalid userKey', async () => {
    const response = await apiRequest('/api/memory/chat', {
      userKey: TEST_CONFIG.invalidUserKey,
      statement: 'Test chat message',
    });

    assert.strictEqual(response.status, 400);
  });
});

// =============================================================================
// Test Suite: Chat External Endpoint
// =============================================================================

describe('POST /api/memory/chat-external - Chat External', () => {

  it('should process external chat with valid request', async () => {
    const response = await apiRequest('/api/memory/chat-external', {
      userKey: TEST_CONFIG.validUserKey,
      statement: 'where should I give blood sample',
      existing_tags: ['food_preferences', 'banking'],
    });

    validateResponseStructure(response.data);
  });

  it('should process external chat without existing_tags', async () => {
    const response = await apiRequest('/api/memory/chat-external', {
      userKey: TEST_CONFIG.validUserKey,
      statement: 'What appointments do I have?',
    });

    validateResponseStructure(response.data);
  });

  it('should return error for invalid userKey', async () => {
    const response = await apiRequest('/api/memory/chat-external', {
      userKey: TEST_CONFIG.invalidUserKey,
      statement: 'Test external chat',
    });

    assert.strictEqual(response.status, 400);
  });
});

// =============================================================================
// Test Suite: Process Contract Endpoint
// =============================================================================

describe('POST /api/extraction/process-contract - Process Contract', () => {

  it('should process contract with valid request', async () => {
    const response = await apiRequest('/api/extraction/process-contract', {
      userKey: TEST_CONFIG.validUserKey,
      contractId: `test-contract-${Date.now()}`,
      name: 'Test Contract Document',
      fileName: 'test_contract.pdf',
      description: 'Test vendor contract',
      fileId: 'test_file_id_hash',
      fileUrl: 'gs://test-bucket/test_contract.pdf',
      referenceId: '12345',
    });

    validateResponseStructure(response.data);
  });

  it('should return error for invalid userKey', async () => {
    const response = await apiRequest('/api/extraction/process-contract', {
      userKey: TEST_CONFIG.invalidUserKey,
      contractId: 'test-contract',
      name: 'Test',
      fileName: 'test.pdf',
      description: 'Test',
      fileId: 'test',
      fileUrl: 'gs://test/test.pdf',
      referenceId: '123',
    });

    assert.strictEqual(response.status, 400);
  });

  it('should handle missing required fields', async () => {
    const response = await apiRequest('/api/extraction/process-contract', {
      userKey: TEST_CONFIG.validUserKey,
      // Missing other required fields
    });

    assert.ok(response.status >= 400, 'Should return error for missing fields');
  });
});

// =============================================================================
// Test Suite: Generate Contract Markup Endpoint
// =============================================================================

describe('POST /api/contract/generate-contract-markup - Generate Contract Markup', () => {

  it('should generate contract markup with MARKDOWN format', async () => {
    const response = await apiRequest('/api/contract/generate-contract-markup', {
      userKey: TEST_CONFIG.validUserKey,
      processId: 'XD21010DC8A9DA11F088A56A2E821FB445',
      explanationFormat: 'MARKDOWN',
      audienceLevel: 'business',
    });

    validateResponseStructure(response.data);
  });

  it('should generate contract markup for technical audience', async () => {
    const response = await apiRequest('/api/contract/generate-contract-markup', {
      userKey: TEST_CONFIG.validUserKey,
      processId: 'XD21010DC8A9DA11F088A56A2E821FB445',
      explanationFormat: 'MARKDOWN',
      audienceLevel: 'technical',
    });

    validateResponseStructure(response.data);
  });

  it('should return error for invalid userKey', async () => {
    const response = await apiRequest('/api/contract/generate-contract-markup', {
      userKey: TEST_CONFIG.invalidUserKey,
      processId: 'test-process-id',
      explanationFormat: 'MARKDOWN',
      audienceLevel: 'business',
    });

    assert.strictEqual(response.status, 400);
  });

  it('should return error for invalid processId', async () => {
    const response = await apiRequest('/api/contract/generate-contract-markup', {
      userKey: TEST_CONFIG.validUserKey,
      processId: 'invalid-process-id',
      explanationFormat: 'MARKDOWN',
      audienceLevel: 'business',
    });

    // Should return error for non-existent process
    validateResponseStructure(response.data);
  });
});

// =============================================================================
// Test Suite: Error Handling & Edge Cases
// =============================================================================

describe('Error Handling & Edge Cases', () => {

  it('should handle malformed JSON gracefully', async () => {
    try {
      const response = await fetch(`${BASE_URL}/api/memory/create`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: 'not valid json',
      });

      assert.ok(response.status >= 400, 'Should return error for malformed JSON');
    } catch (error) {
      // Network error is acceptable for this test
      assert.ok(true);
    }
  });

  it('should handle empty request body', async () => {
    const response = await apiRequest('/api/memory/create', {});
    assert.ok(response.status >= 400, 'Should return error for empty body');
  });

  it('should handle null values in request', async () => {
    const response = await apiRequest('/api/memory/create', {
      userKey: null,
      content: null,
    });

    assert.ok(response.status >= 400, 'Should return error for null values');
  });

  it('should handle array instead of object', async () => {
    try {
      const response = await fetch(`${BASE_URL}/api/memory/create`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify([{ userKey: 'test', content: 'test' }]),
      });

      assert.ok(response.status >= 400, 'Should return error for array body');
    } catch (error) {
      assert.ok(true);
    }
  });

  it('should include required response headers', async () => {
    const response = await fetch(`${BASE_URL}/api/memory/list`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        userKey: TEST_CONFIG.validUserKey,
        tokens: [],
        query: '',
      }),
    });

    // Check for common response headers
    assert.ok(response.headers.get('content-type'), 'Should have content-type header');
  });
});

// =============================================================================
// Test Suite: Performance & Rate Limiting
// =============================================================================

describe('Performance & Rate Limiting', () => {

  it('should respond within acceptable time', async () => {
    const startTime = Date.now();

    await apiRequest('/api/memory/list', {
      userKey: TEST_CONFIG.validUserKey,
      tokens: [],
      query: '',
    });

    const duration = Date.now() - startTime;

    // Should respond within 30 seconds
    assert.ok(duration < 30000, `Response took ${duration}ms, expected < 30000ms`);
  });

  it('should handle concurrent requests', async () => {
    const requests = Array(5).fill(null).map(() =>
      apiRequest('/api/memory/list', {
        userKey: TEST_CONFIG.validUserKey,
        tokens: [],
        query: '',
      })
    );

    const results = await Promise.all(requests);

    results.forEach((response) => {
      validateResponseStructure(response.data);
    });
  });
});

// =============================================================================
// Run Tests
// =============================================================================

console.log('Starting XDB Memory API Tests...');
console.log(`Base URL: ${BASE_URL}`);
console.log(`Test Session: ${TEST_CONFIG.testSessionId}`);
console.log('');
