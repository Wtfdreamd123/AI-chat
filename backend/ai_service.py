import os
import asyncio
from dotenv import load_dotenv
from emergentintegrations.llm.chat import LlmChat, UserMessage
from typing import Dict, Any
import logging

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        self.api_key = os.environ.get('EMERGENT_LLM_KEY')
        if not self.api_key:
            raise ValueError("EMERGENT_LLM_KEY not found in environment variables")
    
    def _get_system_message(self, category: str) -> str:
        """Get specialized system message based on category"""
        system_messages = {
            "code": """Ты - экспертный программист и ИИ-помощник. Специализируешься на:
- Генерации качественного кода на любых языках программирования
- Создании архитектурных решений
- Объяснении сложных концепций программирования
- Написании чистого, оптимизированного кода с комментариями

Всегда предоставляй рабочий код с объяснениями. Используй современные практики и паттерны.""",
            
            "analysis": """Ты - эксперт по анализу кода и code review. Специализируешься на:
- Поиске багов и уязвимостей в коде
- Оптимизации производительности
- Проверке соответствия best practices
- Рекомендациях по улучшению архитектуры
- Анализе безопасности кода

Предоставляй детальный анализ с конкретными рекомендациями и примерами исправлений.""",
            
            "text": """Ты - эксперт по техническому письму и документации. Специализируешься на:
- Создании технической документации
- Написании README файлов
- Создании руководств и инструкций
- Написании технических статей
- Создании комментариев к коду

Пиши ясно, структурированно и информативно. Используй примеры и конкретные рекомендации."""
        }
        
        return system_messages.get(category, system_messages["text"])
    
    def _get_model_by_category(self, category: str) -> tuple[str, str]:
        """Select optimal model based on task category"""
        model_mapping = {
            "code": ("openai", "gpt-4o"),  # Best for code generation
            "analysis": ("anthropic", "claude-3-5-sonnet-20241022"),  # Best for analysis
            "text": ("openai", "gpt-4o-mini")  # Fast for text generation
        }
        
        return model_mapping.get(category, ("openai", "gpt-4o-mini"))
    
    async def generate_response(self, message: str, category: str, session_id: str) -> str:
        """Generate AI response based on message and category"""
        try:
            # Get system message and model for category
            system_message = self._get_system_message(category)
            provider, model = self._get_model_by_category(category)
            
            # Initialize chat with appropriate settings
            chat = LlmChat(
                api_key=self.api_key,
                session_id=session_id,
                system_message=system_message
            ).with_model(provider, model)
            
            # Create user message
            user_message = UserMessage(text=message)
            
            # Generate response
            logger.info(f"Sending message to {provider}/{model} for category: {category}")
            response = await chat.send_message(user_message)
            
            return response
            
        except Exception as e:
            logger.error(f"Error generating AI response: {str(e)}")
            # Fallback response
            return self._get_fallback_response(category, str(e))
    
    def _get_fallback_response(self, category: str, error: str) -> str:
        """Provide fallback response when AI is unavailable"""
        fallbacks = {
            "code": "Извините, сервис ИИ временно недоступен. Попробуйте позже или задайте более конкретный вопрос по программированию.",
            "analysis": "Извините, сервис анализа кода временно недоступен. Пожалуйста, попробуйте позже.",
            "text": "Извините, сервис генерации текста временно недоступен. Попробуйте повторить запрос через несколько минут."
        }
        
        logger.warning(f"Using fallback response for category {category} due to error: {error}")
        return fallbacks.get(category, "Извините, сервис временно недоступен. Попробуйте позже.")
    
    def detect_category(self, message: str) -> str:
        """Automatically detect message category"""
        message_lower = message.lower()
        
        # Code-related keywords
        code_keywords = [
            'код', 'программ', 'function', 'class', 'def', 'var', 'const', 'let',
            'import', 'export', 'if', 'else', 'for', 'while', 'try', 'catch',
            'javascript', 'python', 'react', 'html', 'css', 'sql', 'api',
            'алгоритм', 'функц', 'класс', 'метод', 'переменная'
        ]
        
        # Analysis-related keywords  
        analysis_keywords = [
            'анализ', 'проверь', 'ошибк', 'баг', 'оптимиз', 'производительность',
            'безопасность', 'review', 'рефактор', 'улучш', 'исправ'
        ]
        
        # Check for analysis first (more specific)
        if any(keyword in message_lower for keyword in analysis_keywords):
            return "analysis"
        
        # Then check for code
        if any(keyword in message_lower for keyword in code_keywords):
            return "code"
        
        # Default to text
        return "text"