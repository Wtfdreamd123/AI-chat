#!/usr/bin/env python3
"""
AI Coder Backend Test Suite
Tests the AI Coder backend with real AI integration
"""

import asyncio
import aiohttp
import json
import os
import sys
from datetime import datetime
from typing import Dict, Any, Optional

# Load environment variables
sys.path.append('/app/backend')
from dotenv import load_dotenv
load_dotenv('/app/frontend/.env')

# Get backend URL from frontend environment
BACKEND_URL = os.environ.get('REACT_APP_BACKEND_URL', 'http://localhost:8001')
API_BASE = f"{BACKEND_URL}/api"

class AICoderTester:
    def __init__(self):
        self.session = None
        self.test_session_id = None
        self.results = {
            'total_tests': 0,
            'passed': 0,
            'failed': 0,
            'errors': []
        }
    
    async def setup(self):
        """Setup test session"""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30)
        )
        print(f"🔧 Testing backend at: {API_BASE}")
    
    async def cleanup(self):
        """Cleanup test session"""
        if self.session:
            await self.session.close()
    
    def log_test(self, test_name: str, passed: bool, message: str = ""):
        """Log test result"""
        self.results['total_tests'] += 1
        if passed:
            self.results['passed'] += 1
            print(f"✅ {test_name}: PASSED {message}")
        else:
            self.results['failed'] += 1
            self.results['errors'].append(f"{test_name}: {message}")
            print(f"❌ {test_name}: FAILED {message}")
    
    async def test_health_endpoints(self):
        """Test health check endpoints"""
        print("\n🏥 Testing Health Endpoints...")
        
        # Test root endpoint
        try:
            async with self.session.get(f"{API_BASE}/") as response:
                if response.status == 200:
                    data = await response.json()
                    if "AI Coder Backend is running" in data.get('message', ''):
                        self.log_test("Root endpoint", True, f"Status: {response.status}")
                    else:
                        self.log_test("Root endpoint", False, f"Unexpected message: {data}")
                else:
                    self.log_test("Root endpoint", False, f"Status: {response.status}")
        except Exception as e:
            self.log_test("Root endpoint", False, f"Exception: {str(e)}")
        
        # Test health endpoint
        try:
            async with self.session.get(f"{API_BASE}/health") as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get('status') == 'healthy':
                        self.log_test("Health endpoint", True, 
                                    f"DB: {data.get('database')}, AI: {data.get('ai_service')}")
                    else:
                        self.log_test("Health endpoint", False, f"Unhealthy: {data}")
                else:
                    self.log_test("Health endpoint", False, f"Status: {response.status}")
        except Exception as e:
            self.log_test("Health endpoint", False, f"Exception: {str(e)}")
    
    async def test_chat_code_generation(self):
        """Test chat with code generation request"""
        print("\n💻 Testing Code Generation...")
        
        payload = {
            "message": "Напиши функцию сортировки массива на JavaScript",
            "category": "code"
        }
        
        try:
            async with self.session.post(
                f"{API_BASE}/chat/",
                json=payload,
                headers={'Content-Type': 'application/json'}
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    # Check response structure
                    required_fields = ['id', 'response', 'category', 'timestamp', 'session_id']
                    missing_fields = [field for field in required_fields if field not in data]
                    
                    if missing_fields:
                        self.log_test("Code generation structure", False, 
                                    f"Missing fields: {missing_fields}")
                    else:
                        self.log_test("Code generation structure", True, "All fields present")
                    
                    # Check category detection
                    if data.get('category') == 'code':
                        self.log_test("Code category detection", True)
                    else:
                        self.log_test("Code category detection", False, 
                                    f"Expected 'code', got '{data.get('category')}'")
                    
                    # Check AI response quality
                    response_text = data.get('response', '').lower()
                    if any(keyword in response_text for keyword in ['function', 'sort', 'javascript', 'array']):
                        self.log_test("Code generation quality", True, "Contains relevant keywords")
                    else:
                        self.log_test("Code generation quality", False, "Response doesn't seem code-related")
                    
                    # Store session ID for later tests
                    self.test_session_id = data.get('session_id')
                    
                else:
                    self.log_test("Code generation request", False, f"Status: {response.status}")
                    
        except Exception as e:
            self.log_test("Code generation request", False, f"Exception: {str(e)}")
    
    async def test_chat_code_analysis(self):
        """Test chat with code analysis request"""
        print("\n🔍 Testing Code Analysis...")
        
        payload = {
            "message": "Анализируй этот код: const arr = [3,1,4,1,5]; arr.sort();",
            "category": "analysis"
        }
        
        try:
            async with self.session.post(
                f"{API_BASE}/chat/",
                json=payload,
                headers={'Content-Type': 'application/json'}
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    # Check category
                    if data.get('category') == 'analysis':
                        self.log_test("Analysis category", True)
                    else:
                        self.log_test("Analysis category", False, 
                                    f"Expected 'analysis', got '{data.get('category')}'")
                    
                    # Check response quality
                    response_text = data.get('response', '').lower()
                    analysis_keywords = ['анализ', 'код', 'sort', 'массив', 'array']
                    if any(keyword in response_text for keyword in analysis_keywords):
                        self.log_test("Analysis quality", True, "Contains analysis keywords")
                    else:
                        self.log_test("Analysis quality", False, "Response doesn't seem analysis-related")
                        
                else:
                    self.log_test("Code analysis request", False, f"Status: {response.status}")
                    
        except Exception as e:
            self.log_test("Code analysis request", False, f"Exception: {str(e)}")
    
    async def test_chat_text_documentation(self):
        """Test chat with text/documentation request"""
        print("\n📝 Testing Text/Documentation Generation...")
        
        payload = {
            "message": "Создай README файл для проекта веб-приложения на React",
            "category": "text"
        }
        
        try:
            async with self.session.post(
                f"{API_BASE}/chat/",
                json=payload,
                headers={'Content-Type': 'application/json'}
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    # Check category
                    if data.get('category') == 'text':
                        self.log_test("Text category", True)
                    else:
                        self.log_test("Text category", False, 
                                    f"Expected 'text', got '{data.get('category')}'")
                    
                    # Check response quality
                    response_text = data.get('response', '').lower()
                    text_keywords = ['readme', 'react', 'проект', 'установка', 'запуск']
                    if any(keyword in response_text for keyword in text_keywords):
                        self.log_test("Documentation quality", True, "Contains documentation keywords")
                    else:
                        self.log_test("Documentation quality", False, "Response doesn't seem documentation-related")
                        
                else:
                    self.log_test("Text generation request", False, f"Status: {response.status}")
                    
        except Exception as e:
            self.log_test("Text generation request", False, f"Exception: {str(e)}")
    
    async def test_category_auto_detection(self):
        """Test automatic category detection"""
        print("\n🤖 Testing Category Auto-Detection...")
        
        test_cases = [
            {
                "message": "Напиши функцию для валидации email",
                "expected_category": "code",
                "test_name": "Auto-detect code"
            },
            {
                "message": "Проверь этот код на ошибки: function test() { return; }",
                "expected_category": "analysis", 
                "test_name": "Auto-detect analysis"
            },
            {
                "message": "Расскажи о принципах SOLID в программировании",
                "expected_category": "text",
                "test_name": "Auto-detect text"
            }
        ]
        
        for test_case in test_cases:
            payload = {
                "message": test_case["message"],
                # Don't specify category to test auto-detection
            }
            
            try:
                async with self.session.post(
                    f"{API_BASE}/chat/",
                    json=payload,
                    headers={'Content-Type': 'application/json'}
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        detected_category = data.get('category')
                        
                        if detected_category == test_case["expected_category"]:
                            self.log_test(test_case["test_name"], True, 
                                        f"Detected: {detected_category}")
                        else:
                            self.log_test(test_case["test_name"], False, 
                                        f"Expected: {test_case['expected_category']}, Got: {detected_category}")
                    else:
                        self.log_test(test_case["test_name"], False, f"Status: {response.status}")
                        
            except Exception as e:
                self.log_test(test_case["test_name"], False, f"Exception: {str(e)}")
    
    async def test_session_management(self):
        """Test session creation and persistence"""
        print("\n🔐 Testing Session Management...")
        
        if not self.test_session_id:
            self.log_test("Session ID availability", False, "No session ID from previous tests")
            return
        
        # Test getting chat history
        try:
            async with self.session.get(f"{API_BASE}/chat/history/{self.test_session_id}") as response:
                if response.status == 200:
                    data = await response.json()
                    messages = data.get('messages', [])
                    
                    if len(messages) > 0:
                        self.log_test("Chat history retrieval", True, f"Found {len(messages)} messages")
                        
                        # Check message structure
                        first_message = messages[0]
                        required_fields = ['id', 'session_id', 'type', 'content', 'category', 'timestamp']
                        missing_fields = [field for field in required_fields if field not in first_message]
                        
                        if missing_fields:
                            self.log_test("Message structure", False, f"Missing fields: {missing_fields}")
                        else:
                            self.log_test("Message structure", True, "All fields present")
                    else:
                        self.log_test("Chat history retrieval", False, "No messages found")
                        
                elif response.status == 404:
                    self.log_test("Chat history retrieval", False, "Session not found")
                else:
                    self.log_test("Chat history retrieval", False, f"Status: {response.status}")
                    
        except Exception as e:
            self.log_test("Chat history retrieval", False, f"Exception: {str(e)}")
        
        # Test getting sessions list
        try:
            async with self.session.get(f"{API_BASE}/chat/sessions") as response:
                if response.status == 200:
                    data = await response.json()
                    sessions = data.get('sessions', [])
                    
                    if len(sessions) > 0:
                        self.log_test("Sessions list", True, f"Found {len(sessions)} sessions")
                    else:
                        self.log_test("Sessions list", False, "No sessions found")
                else:
                    self.log_test("Sessions list", False, f"Status: {response.status}")
                    
        except Exception as e:
            self.log_test("Sessions list", False, f"Exception: {str(e)}")
    
    async def test_error_handling(self):
        """Test error handling with invalid requests"""
        print("\n⚠️ Testing Error Handling...")
        
        # Test empty message
        try:
            payload = {"message": ""}
            async with self.session.post(
                f"{API_BASE}/chat/",
                json=payload,
                headers={'Content-Type': 'application/json'}
            ) as response:
                if response.status in [400, 422]:  # Bad request or validation error
                    self.log_test("Empty message handling", True, f"Status: {response.status}")
                else:
                    self.log_test("Empty message handling", False, 
                                f"Expected 400/422, got {response.status}")
        except Exception as e:
            self.log_test("Empty message handling", False, f"Exception: {str(e)}")
        
        # Test invalid session ID in history
        try:
            invalid_session_id = "invalid-session-id-12345"
            async with self.session.get(f"{API_BASE}/chat/history/{invalid_session_id}") as response:
                if response.status == 404:
                    self.log_test("Invalid session handling", True, "Returns 404 for invalid session")
                else:
                    self.log_test("Invalid session handling", False, 
                                f"Expected 404, got {response.status}")
        except Exception as e:
            self.log_test("Invalid session handling", False, f"Exception: {str(e)}")
        
        # Test malformed JSON
        try:
            async with self.session.post(
                f"{API_BASE}/chat/",
                data="invalid json",
                headers={'Content-Type': 'application/json'}
            ) as response:
                if response.status in [400, 422]:
                    self.log_test("Malformed JSON handling", True, f"Status: {response.status}")
                else:
                    self.log_test("Malformed JSON handling", False, 
                                f"Expected 400/422, got {response.status}")
        except Exception as e:
            self.log_test("Malformed JSON handling", False, f"Exception: {str(e)}")
    
    async def test_database_integration(self):
        """Test database integration by verifying data persistence"""
        print("\n🗄️ Testing Database Integration...")
        
        # Send a message and verify it's saved
        test_message = f"Test message for database verification - {datetime.now().isoformat()}"
        payload = {
            "message": test_message,
            "category": "text"
        }
        
        try:
            # Send message
            async with self.session.post(
                f"{API_BASE}/chat/",
                json=payload,
                headers={'Content-Type': 'application/json'}
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    session_id = data.get('session_id')
                    
                    # Wait a moment for database write
                    await asyncio.sleep(1)
                    
                    # Retrieve history and verify message is saved
                    async with self.session.get(f"{API_BASE}/chat/history/{session_id}") as hist_response:
                        if hist_response.status == 200:
                            hist_data = await hist_response.json()
                            messages = hist_data.get('messages', [])
                            
                            # Look for our test message
                            found_message = False
                            for msg in messages:
                                if msg.get('content') == test_message and msg.get('type') == 'user':
                                    found_message = True
                                    break
                            
                            if found_message:
                                self.log_test("Database persistence", True, "Message saved and retrieved")
                            else:
                                self.log_test("Database persistence", False, "Message not found in history")
                        else:
                            self.log_test("Database persistence", False, 
                                        f"Failed to retrieve history: {hist_response.status}")
                else:
                    self.log_test("Database persistence", False, 
                                f"Failed to send message: {response.status}")
                    
        except Exception as e:
            self.log_test("Database persistence", False, f"Exception: {str(e)}")
    
    async def run_all_tests(self):
        """Run all tests"""
        print("🚀 Starting AI Coder Backend Tests")
        print("=" * 50)
        
        await self.setup()
        
        try:
            await self.test_health_endpoints()
            await self.test_chat_code_generation()
            await self.test_chat_code_analysis()
            await self.test_chat_text_documentation()
            await self.test_category_auto_detection()
            await self.test_session_management()
            await self.test_error_handling()
            await self.test_database_integration()
            
        finally:
            await self.cleanup()
        
        # Print summary
        print("\n" + "=" * 50)
        print("🏁 Test Summary")
        print("=" * 50)
        print(f"Total Tests: {self.results['total_tests']}")
        print(f"Passed: {self.results['passed']} ✅")
        print(f"Failed: {self.results['failed']} ❌")
        
        if self.results['errors']:
            print("\n❌ Failed Tests:")
            for error in self.results['errors']:
                print(f"  - {error}")
        
        success_rate = (self.results['passed'] / self.results['total_tests']) * 100 if self.results['total_tests'] > 0 else 0
        print(f"\nSuccess Rate: {success_rate:.1f}%")
        
        if success_rate >= 80:
            print("🎉 Backend tests mostly successful!")
        elif success_rate >= 60:
            print("⚠️ Backend has some issues but core functionality works")
        else:
            print("🚨 Backend has significant issues")
        
        return self.results

async def main():
    """Main test runner"""
    tester = AICoderTester()
    results = await tester.run_all_tests()
    
    # Exit with appropriate code
    if results['failed'] == 0:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())