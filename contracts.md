# API Contracts - AI Coder Backend

## 1. API Endpoints

### POST /api/chat
**Описание**: Отправка сообщения в чат с ИИ
**Request Body**:
```json
{
  "message": "string",
  "category": "code" | "analysis" | "text",
  "session_id": "string (optional)"
}
```

**Response**:
```json
{
  "id": "string",
  "response": "string", 
  "category": "string",
  "timestamp": "datetime",
  "session_id": "string"
}
```

### GET /api/chat/history/{session_id}
**Описание**: Получение истории чата
**Response**:
```json
{
  "messages": [
    {
      "id": "string",
      "type": "user" | "ai",
      "content": "string",
      "category": "string",
      "timestamp": "datetime"
    }
  ]
}
```

## 2. Mock Data Integration

**Файл**: `/app/frontend/src/data/mock.js`
- Содержит mock ответы для разных категорий: code, analysis, text
- Нужно удалить после интеграции с backend
- Заменить в ChatInterface.jsx на реальные API вызовы

## 3. Backend Implementation Plan

### Models (MongoDB)
```python
class ChatMessage:
    id: str
    session_id: str  
    type: str  # "user" | "ai"
    content: str
    category: str  # "code" | "analysis" | "text"
    timestamp: datetime

class ChatSession:
    id: str
    created_at: datetime
    updated_at: datetime
```

### ИИ Integration
- Использовать Emergent LLM Key для универсального доступа к LLM
- Поддержка OpenAI, Claude, Google models
- Категоризация запросов для выбора оптимальной модели
- Streaming responses для real-time ответов

### Business Logic
1. **Детекция категории** - анализ пользовательского ввода
2. **Выбор модели** - в зависимости от категории задачи
3. **Генерация промптов** - специализированные промпты для кода/анализа/текста
4. **Сохранение истории** - все сообщения в MongoDB
5. **Session management** - управление сессиями чата

## 4. Frontend Integration Changes

### ChatInterface.jsx
- Заменить `getMockResponse()` на `fetch('/api/chat')`
- Добавить обработку ошибок API
- Добавить индикатор загрузки для реальных запросов
- Интегрировать session management

### Changes needed:
```javascript
// Заменить это:
const aiResponse = {
  content: getMockResponse(userMessage.content, userMessage.category)
};

// На это:
const response = await fetch(`${BACKEND_URL}/api/chat`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    message: userMessage.content,
    category: userMessage.category,
    session_id: sessionId
  })
});
const aiResponse = await response.json();
```

## 5. Error Handling
- API timeouts (30s for LLM requests)
- Rate limiting (10 requests/minute per session)
- Fallback responses при недоступности ИИ
- Валидация входных данных

## 6. Security
- Input sanitization
- Rate limiting
- Session validation
- API key protection в environment variables

## 7. Testing Protocol
1. Backend API тестирование с curl
2. Frontend интеграция тестирование
3. End-to-end тестирование чата
4. Performance тестирование с реальными LLM запросами