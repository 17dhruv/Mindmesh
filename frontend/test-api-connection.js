/**
 * Quick API connection test script
 * Tests: Health endpoint, CORS, basic connectivity
 * 
 * Usage: node test-api-connection.js
 */

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

console.log('🧪 Testing Mindmesh API Connection...');
console.log('📍 API URL:', API_URL);
console.log('');

// Test 1: Health Check
async function testHealthEndpoint() {
  console.log('Test 1: Health Endpoint');
  try {
    const response = await fetch(`${API_URL}/api/health`);
    const data = await response.json();
    
    if (response.ok && data.status === 'healthy') {
      console.log('✅ Health check passed:', data);
      return true;
    } else {
      console.log('❌ Health check failed:', response.status, data);
      return false;
    }
  } catch (error) {
    console.log('❌ Health check error:', error.message);
    return false;
  }
}

// Test 2: CORS Check
async function testCORS() {
  console.log('\nTest 2: CORS Headers');
  try {
    const response = await fetch(`${API_URL}/api/health`);
    const corsHeader = response.headers.get('access-control-allow-origin');
    
    if (corsHeader) {
      console.log('✅ CORS enabled:', corsHeader);
      return true;
    } else {
      console.log('⚠️  No CORS header found (might be an issue in browser)');
      return false;
    }
  } catch (error) {
    console.log('❌ CORS check error:', error.message);
    return false;
  }
}

// Test 3: Authentication Error (should return 401 without token)
async function testAuthRequired() {
  console.log('\nTest 3: Auth Required (401 without token)');
  try {
    const response = await fetch(`${API_URL}/api/plans`);
    
    if (response.status === 401 || response.status === 403) {
      console.log('✅ Auth properly required:', response.status);
      return true;
    } else {
      console.log('⚠️  Unexpected status:', response.status);
      return false;
    }
  } catch (error) {
    console.log('❌ Auth check error:', error.message);
    return false;
  }
}

// Run all tests
async function runTests() {
  const results = {
    health: await testHealthEndpoint(),
    cors: await testCORS(),
    auth: await testAuthRequired(),
  };
  
  console.log('\n' + '='.repeat(50));
  console.log('📊 Test Results:');
  console.log('  Health Check:', results.health ? '✅ PASS' : '❌ FAIL');
  console.log('  CORS:', results.cors ? '✅ PASS' : '⚠️  WARN');
  console.log('  Auth Required:', results.auth ? '✅ PASS' : '❌ FAIL');
  console.log('='.repeat(50));
  
  const allPassed = results.health && results.auth;
  if (allPassed) {
    console.log('\n🎉 All critical tests passed!');
    console.log('💡 Your backend is ready for integration.');
  } else {
    console.log('\n⚠️  Some tests failed.');
    console.log('💡 Make sure the backend server is running:');
    console.log('   cd backend && python -m uvicorn app.main:app --reload');
  }
  
  process.exit(allPassed ? 0 : 1);
}

runTests();
