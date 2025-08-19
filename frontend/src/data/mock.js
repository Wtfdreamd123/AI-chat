// Mock responses for different categories
export const mockResponses = {
  code: [
    `Вот пример функции на JavaScript для сортировки массива:

\`\`\`javascript
function quickSort(arr) {
  if (arr.length <= 1) {
    return arr;
  }
  
  const pivot = arr[Math.floor(arr.length / 2)];
  const left = arr.filter(x => x < pivot);
  const middle = arr.filter(x => x === pivot);
  const right = arr.filter(x => x > pivot);
  
  return [...quickSort(left), ...middle, ...quickSort(right)];
}

// Использование:
const numbers = [3, 6, 8, 10, 1, 2, 1];
console.log(quickSort(numbers));
\`\`\`

Эта функция использует алгоритм быстрой сортировки с временной сложностью O(n log n) в среднем случае.`,

    `Вот класс для работы с API на Python:

\`\`\`python
import requests
from typing import Dict, Any, Optional

class APIClient:
    def __init__(self, base_url: str, api_key: Optional[str] = None):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        
        if api_key:
            self.session.headers.update({
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            })
    
    def get(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        response = self.session.get(f"{self.base_url}/{endpoint}", params=params)
        response.raise_for_status()
        return response.json()
    
    def post(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        response = self.session.post(f"{self.base_url}/{endpoint}", json=data)
        response.raise_for_status()
        return response.json()

# Использование:
client = APIClient("https://api.example.com", "your-api-key")
result = client.get("users", {"page": 1})
\`\`\``,

    `Создам для вас React компонент с хуками:

\`\`\`jsx
import React, { useState, useEffect, useCallback } from 'react';

const DataFetcher = ({ url }) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchData = useCallback(async () => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error(\`HTTP error! status: \${response.status}\`);
      }
      const result = await response.json();
      setData(result);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [url]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  if (loading) return <div>Загрузка...</div>;
  if (error) return <div>Ошибка: {error}</div>;
  if (!data) return <div>Нет данных</div>;

  return (
    <div>
      <pre>{JSON.stringify(data, null, 2)}</pre>
      <button onClick={fetchData}>Обновить</button>
    </div>
  );
};

export default DataFetcher;
\`\`\``
  ],

  analysis: [
    `Анализ вашего кода показывает несколько проблем:

🔍 **Найденные проблемы:**
1. **Утечка памяти**: useEffect без cleanup функции
2. **Производительность**: Отсутствует мемоизация дорогих вычислений  
3. **Безопасность**: Нет валидации входных данных

💡 **Рекомендации по исправлению:**

\`\`\`javascript
// Добавьте cleanup в useEffect
useEffect(() => {
  const timer = setInterval(() => {
    // ваш код
  }, 1000);
  
  return () => clearInterval(timer); // cleanup!
}, []);

// Используйте useMemo для дорогих вычислений
const expensiveValue = useMemo(() => {
  return heavyCalculation(data);
}, [data]);

// Добавьте валидацию
const validateInput = (input) => {
  if (!input || typeof input !== 'string') {
    throw new Error('Некорректный ввод');
  }
  return input.trim();
};
\`\`\`

Исправление этих проблем значительно улучшит качество и надёжность кода.`,

    `Проверил ваш код на соответствие лучшим практикам:

✅ **Хорошо:**
- Правильное использование TypeScript типов
- Читаемые названия переменных
- Модульная архитектура

⚠️ **Можно улучшить:**
- Добавить обработку ошибок в async функциях
- Использовать более строгие TypeScript настройки
- Добавить unit тесты

\`\`\`typescript
// Улучшенная версия с обработкой ошибок
async function fetchUserData(userId: string): Promise<User | null> {
  try {
    const response = await api.get(\`/users/\${userId}\`);
    
    if (!response.ok) {
      console.error(\`Failed to fetch user: \${response.status}\`);
      return null;
    }
    
    return response.data;
  } catch (error) {
    console.error('Error fetching user:', error);
    throw new Error(\`Failed to fetch user data: \${error.message}\`);
  }
}
\`\`\`

Рекомендую также настроить ESLint и Prettier для автоматической проверки кода.`,

    `Анализ производительности вашего React приложения:

📊 **Метрики производительности:**
- First Contentful Paint: 1.2s (хорошо)
- Largest Contentful Paint: 2.8s (требует оптимизации)
- Time to Interactive: 3.1s (медленно)

🚀 **Рекомендации по оптимизации:**

1. **Lazy loading компонентов:**
\`\`\`jsx
const LazyComponent = React.lazy(() => import('./HeavyComponent'));

function App() {
  return (
    <Suspense fallback={<div>Загрузка...</div>}>
      <LazyComponent />
    </Suspense>
  );
}
\`\`\`

2. **Мемоизация дорогих компонентов:**
\`\`\`jsx
const ExpensiveComponent = React.memo(({ data }) => {
  // дорогие вычисления
});
\`\`\`

3. **Виртуализация длинных списков:**
\`\`\`jsx
import { FixedSizeList as List } from 'react-window';

const VirtualizedList = ({ items }) => (
  <List height={600} itemCount={items.length} itemSize={50}>
    {({ index, style }) => (
      <div style={style}>{items[index]}</div>
    )}
  </List>
);
\`\`\`

Эти изменения должны улучшить производительность на 40-60%.`
  ],

  text: [
    `Конечно! Помогу вам с написанием текста. Вот несколько советов для эффективного технического письма:

📝 **Принципы хорошего технического текста:**

1. **Ясность и простота** - используйте простые предложения
2. **Структурированность** - разбивайте на логические блоки  
3. **Конкретность** - избегайте расплывчатых формулировок
4. **Примеры** - подкрепляйте теорию практикой

💡 **Пример структуры документации:**

\`\`\`markdown
# Заголовок функции

## Описание
Краткое описание того, что делает функция.

## Параметры
- \`param1\` (string) - описание параметра
- \`param2\` (number) - описание параметра

## Возвращаемое значение
Описание того, что возвращает функция.

## Пример использования
\`\`\`javascript
const result = myFunction('example', 42);
\`\`\`

Хотите, чтобы я помог с конкретным текстом или документацией?`,

    `Отлично! Вот шаблон для написания качественной технической статьи:

📖 **Структура технической статьи:**

**1. Введение (hook + проблема)**
- Зацепите читателя интересным фактом
- Четко сформулируйте проблему
- Покажите, почему это важно

**2. Основная часть**
- Разделите на 3-5 логических блоков
- Каждый блок = одна ключевая идея
- Используйте подзаголовки и списки

**3. Примеры и код (если применимо)**
- Показывайте, а не только рассказывайте
- Комментируйте сложные моменты
- Проверяйте работоспособность кода

**4. Заключение**
- Резюмируйте ключевые моменты
- Дайте практические рекомендации
- Предложите дальнейшие шаги

✍️ **Советы по стилю:**
- Пишите активным залогом
- Используйте "вы" вместо "пользователь"  
- Добавляйте эмодзи для визуального разделения
- Проверяйте текст на читаемость

Какую именно статью или документацию хотите написать?`,

    `Помогу создать эффективный контент! Вот универсальный подход:

🎯 **Определение цели:**
- Кто ваша аудитория?
- Какую проблему решаете?
- Какое действие должен совершить читатель?

📋 **План создания контента:**

**Этап 1: Исследование**
- Изучите потребности аудитории
- Проанализируйте конкурентов
- Соберите ключевые факты и данные

**Этап 2: Структура**
- Создайте outline (план)
- Определите ключевые разделы
- Подготовьте примеры и иллюстрации

**Этап 3: Написание**
- Начните с самого важного
- Используйте принцип пирамиды (главное сверху)
- Добавляйте конкретные детали и примеры

**Этап 4: Редактирование**
- Проверьте логику изложения
- Упростите сложные предложения
- Добавьте призывы к действию

🔥 **Секрет хорошего контента:**
Пишите так, будто объясняете другу. Будьте полезны, конкретны и искренни.

О чем именно хотите написать? Помогу создать контент под вашу задачу!`
  ],

  greeting: [
    'Привет! Я готов помочь вам с кодом, текстом и анализом. Что вас интересует?'
  ]
};