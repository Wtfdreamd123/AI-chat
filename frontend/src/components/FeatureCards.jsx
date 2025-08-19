import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { Code, FileText, CheckCircle, Zap, Brain, MessageSquare } from 'lucide-react';

const FeatureCards = () => {
  const features = [
    {
      icon: <Code className="w-8 h-8" />,
      title: 'Генерация Кода',
      description: 'Создание качественного кода на любом языке программирования с подробными комментариями',
      capabilities: ['JavaScript/TypeScript', 'Python', 'React/Vue', 'API интеграции'],
      gradient: 'from-blue-500 to-cyan-500',
      bgGradient: 'from-blue-50 to-cyan-50'
    },
    {
      icon: <CheckCircle className="w-8 h-8" />,
      title: 'Анализ Кода',
      description: 'Глубокий анализ вашего кода с выявлением ошибок, оптимизацией и рекомендациями',
      capabilities: ['Поиск багов', 'Оптимизация', 'Code Review', 'Безопасность'],
      gradient: 'from-green-500 to-emerald-500',
      bgGradient: 'from-green-50 to-emerald-50'
    },
    {
      icon: <FileText className="w-8 h-8" />,
      title: 'Работа с Текстом',
      description: 'Создание технической документации, статей и любого текстового контента',
      capabilities: ['Документация', 'Статьи', 'README файлы', 'Комментарии'],
      gradient: 'from-purple-500 to-pink-500',
      bgGradient: 'from-purple-50 to-pink-50'
    },
    {
      icon: <Brain className="w-8 h-8" />,
      title: 'ИИ Ассистент',
      description: 'Интеллектуальная помощь в решении сложных задач программирования и разработки',
      capabilities: ['Архитектура', 'Алгоритмы', 'Дизайн паттерны', 'Консультации'],
      gradient: 'from-indigo-500 to-purple-500',
      bgGradient: 'from-indigo-50 to-purple-50'
    },
    {
      icon: <Zap className="w-8 h-8" />,
      title: 'Быстрые Решения',
      description: 'Мгновенные ответы на технические вопросы и быстрое решение проблем',
      capabilities: ['Дебаггинг', 'Рефакторинг', 'Исправления', 'Советы'],
      gradient: 'from-orange-500 to-red-500',
      bgGradient: 'from-orange-50 to-red-50'
    },
    {
      icon: <MessageSquare className="w-8 h-8" />,
      title: 'Интерактивный Чат',
      description: 'Естественное общение с ИИ в удобном чат-интерфейсе с контекстом разговора',
      capabilities: ['Диалог', 'Контекст', 'История', 'Персонализация'],
      gradient: 'from-teal-500 to-cyan-500',
      bgGradient: 'from-teal-50 to-cyan-50'
    }
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
      {features.map((feature, index) => (
        <Card 
          key={index} 
          className={`group hover:shadow-xl transition-all duration-300 hover:-translate-y-2 border-0 bg-gradient-to-br ${feature.bgGradient} hover:shadow-2xl cursor-pointer`}
        >
          <CardHeader className="pb-3">
            <div className="flex items-center gap-3 mb-2">
              <div className={`p-3 bg-gradient-to-r ${feature.gradient} rounded-xl text-white shadow-lg group-hover:scale-110 transition-transform duration-300`}>
                {feature.icon}
              </div>
              <CardTitle className="text-xl font-bold text-gray-800 group-hover:text-gray-900">
                {feature.title}
              </CardTitle>
            </div>
            <p className="text-gray-600 text-sm leading-relaxed">
              {feature.description}
            </p>
          </CardHeader>
          <CardContent className="pt-0">
            <div className="flex flex-wrap gap-2">
              {feature.capabilities.map((capability, capIndex) => (
                <Badge 
                  key={capIndex} 
                  variant="secondary" 
                  className="text-xs bg-white/70 text-gray-700 hover:bg-white hover:shadow-sm transition-all duration-200"
                >
                  {capability}
                </Badge>
              ))}
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  );
};

export default FeatureCards;