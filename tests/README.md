# XDB Memory API Test Suite

This test suite provides comprehensive testing for the XDB Memory Management API.

## API Endpoints Covered

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/memory/create` | POST | Create a new memory |
| `/api/memory/list` | POST | List/search memories |
| `/api/memory/predict` | POST | Predict intent from statement |
| `/api/memory/chat` | POST | Chat with memory context |
| `/api/memory/chat-external` | POST | External chat integration |
| `/api/extraction/process-contract` | POST | Process contract documents |
| `/api/contract/generate-contract-markup` | POST | Generate contract markup |

## Prerequisites

- Node.js 18+ (uses built-in test runner and fetch)

## Running Tests

```bash
# Run all tests
npm test

# Run with verbose output
npm run test:verbose
```

## Configuration

Edit `memory-api.test.js` to update the test configuration:

```javascript
const TEST_CONFIG = {
  validUserKey: 'your-valid-user-key-here',
  invalidUserKey: 'invalid_user_key_12345',
  testSessionId: `test_session_${Date.now()}`,
};
```

## Test Categories

### Create Memory Tests
- Valid memory creation with content
- Memory with optional sessionId and tag
- Error handling for invalid/missing userKey
- Edge cases: empty content, long content, special characters, unicode

### List Memories Tests
- Basic listing with valid userKey
- Filtering with query and tokens
- Advanced filtering with suggestedTokens
- Filtering by conversationId
- Response structure validation

### Chat Tests
- Chat with existing_tags
- Chat without tags
- External chat integration

### Contract Tests
- Process contract documents
- Generate contract markup with different formats and audience levels

### Error Handling Tests
- Malformed JSON handling
- Empty/null request bodies
- Missing required fields
- Response header validation

### Performance Tests
- Response time validation
- Concurrent request handling

## API Base URL

```
https://postman-rest-api-learner.glitch.me/
```

## Request Body Examples

### Create Memory
```json
{
  "userKey": "your-user-key-hash",
  "content": "I love hiking in the mountains during summer.",
  "tag": "preferences",
  "sessionId": "2025121700001"
}
```

### List Memories
```json
{
  "userKey": "your-user-key-hash",
  "tokens": [],
  "query": "coffee preferences",
  "require_llm_summary": false
}
```

### Chat
```json
{
  "userKey": "your-user-key-hash",
  "statement": "What are my coffee preferences?",
  "existing_tags": ["food_preferences", "banking"]
}
```

## Response Structure

All API responses follow this structure:

```json
{
  "status": "Success" | "Failed",
  "message": "Request processed successfully.",
  "data": { ... },
  "timestamp": "2025-12-17T12:00:00.000000+00:00",
  "processId": "abc123..."
}
```
