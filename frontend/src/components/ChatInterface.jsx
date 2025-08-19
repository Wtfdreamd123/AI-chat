import React, { useState, useRef, useEffect } from 'react';
import { Button } from './ui/button';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Textarea } from './ui/textarea';
import { ScrollArea } from './ui/scroll-area';
import { Avatar, AvatarFallback } from './ui/avatar';
import { Badge } from './ui/badge';
import { Separator } from './ui/separator';
import { Send, Bot, User, Code, FileText, CheckCircle, AlertCircle } from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

const ChatInterface = () => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'ai',
      content: 'Привет! Я ваш AI помощник для работы с текстом и кодом. Я могу генерировать код, анализировать его и помочь с программированием. Что вас интересует?',
      timestamp: new Date(Date.now() - 60000),
      category: 'text'
    }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const [error, setError] = useState(null);
  const messagesEndRef = useRef(null);
  const textareaRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!inputValue.trim() || isTyping) return;

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: inputValue,
      timestamp: new Date(),
      category: detectCategory(inputValue)
    };

    setMessages(prev => [...prev, userMessage]);
    const messageContent = inputValue;
    setInputValue('');
    setIsTyping(true);
    setError(null);

    try {
      const response = await fetch(`${BACKEND_URL}/api/chat/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: messageContent,
          category: userMessage.category,
          session_id: sessionId
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const aiResponseData = await response.json();
      
      // Update session ID if this is the first message
      if (!sessionId) {
        setSessionId(aiResponseData.session_id);
      }

      const aiMessage = {
        id: aiResponseData.id,
        type: 'ai',
        content: aiResponseData.response,
        timestamp: new Date(aiResponseData.timestamp),
        category: aiResponseData.category
      };

      setMessages(prev => [...prev, aiMessage]);
      
    } catch (error) {
      console.error('Error sending message:', error);
      setError('Ошибка подключения к ИИ. Попробуйте еще раз.');
      
      // Add error message to chat
      const errorMessage = {
        id: Date.now() + 1,
        type: 'ai',
        content: 'Извините, произошла ошибка при обращении к ИИ. Проверьте подключение к интернету и попробуйте еще раз.',
        timestamp: new Date(),
        category: 'error'
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsTyping(false);
    }
  };

  const detectCategory = (text) => {
    const lowerText = text.toLowerCase();
    if (lowerText.includes('код') || lowerText.includes('программ') || lowerText.includes('function') || lowerText.includes('class')) {
      return 'code';
    } else if (lowerText.includes('анализ') || lowerText.includes('проверь') || lowerText.includes('ошибк')) {
      return 'analysis';
    } else {
      return 'text';
    }
  };

  const getMockResponse = (userInput, category) => {
    const responses = mockResponses[category] || mockResponses.text;
    return responses[Math.floor(Math.random() * responses.length)];
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const getCategoryIcon = (category) => {
    switch (category) {
      case 'code':
        return <Code className="w-4 h-4" />;
      case 'analysis':
        return <CheckCircle className="w-4 h-4" />;
      default:
        return <FileText className="w-4 h-4" />;
    }
  };

  const getCategoryColor = (category) => {
    switch (category) {
      case 'code':
        return 'bg-blue-100 text-blue-800 hover:bg-blue-200';
      case 'analysis':
        return 'bg-green-100 text-green-800 hover:bg-green-200';
      default:
        return 'bg-purple-100 text-purple-800 hover:bg-purple-200';
    }
  };

  return (
    <div className="flex flex-col h-full max-w-4xl mx-auto">
      {/* Header */}
      <Card className="mb-4 border-0 shadow-sm bg-gradient-to-r from-slate-50 to-gray-50">
        <CardHeader className="pb-4">
          <CardTitle className="flex items-center gap-3 text-2xl font-bold text-gray-800">
            <div className="p-2 bg-gradient-to-r from-indigo-500 to-cyan-500 rounded-lg">
              <Bot className="w-6 h-6 text-white" />
            </div>
            AI Помощник по Коду и Тексту
          </CardTitle>
          <p className="text-gray-600 mt-2">
            Генерация, анализ и помощь с программированием в реальном времени
          </p>
        </CardHeader>
      </Card>

      {/* Messages */}
      <Card className="flex-1 flex flex-col border-0 shadow-sm">
        <CardContent className="flex-1 p-0">
          <ScrollArea className="h-[500px] p-4">
            {messages.map((message) => (
              <div key={message.id} className="mb-6 animate-in fade-in-50 duration-500">
                <div className={`flex gap-3 ${message.type === 'user' ? 'flex-row-reverse' : ''}`}>
                  <Avatar className="w-8 h-8 border-2 border-white shadow-sm">
                    <AvatarFallback className={message.type === 'ai' ? 'bg-gradient-to-r from-indigo-500 to-cyan-500 text-white' : 'bg-gray-100'}>
                      {message.type === 'ai' ? <Bot className="w-4 h-4" /> : <User className="w-4 h-4" />}
                    </AvatarFallback>
                  </Avatar>
                  
                  <div className={`flex-1 max-w-[80%] ${message.type === 'user' ? 'flex flex-col items-end' : ''}`}>
                    <div className="flex items-center gap-2 mb-1">
                      <Badge variant="secondary" className={`text-xs ${getCategoryColor(message.category)}`}>
                        {getCategoryIcon(message.category)}
                        <span className="ml-1 capitalize">{message.category === 'code' ? 'Код' : message.category === 'analysis' ? 'Анализ' : 'Текст'}</span>
                      </Badge>
                      <span className="text-xs text-gray-500">
                        {message.timestamp.toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' })}
                      </span>
                    </div>
                    
                    <div className={`p-4 rounded-2xl shadow-sm transition-all duration-200 hover:shadow-md ${
                      message.type === 'ai' 
                        ? 'bg-white border border-gray-100' 
                        : 'bg-gradient-to-r from-indigo-500 to-cyan-500 text-white'
                    }`}>
                      <div className="whitespace-pre-wrap text-sm leading-relaxed">
                        {message.content}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            ))}
            
            {isTyping && (
              <div className="mb-6 animate-in fade-in-50 duration-300">
                <div className="flex gap-3">
                  <Avatar className="w-8 h-8 border-2 border-white shadow-sm">
                    <AvatarFallback className="bg-gradient-to-r from-indigo-500 to-cyan-500 text-white">
                      <Bot className="w-4 h-4" />
                    </AvatarFallback>
                  </Avatar>
                  <div className="bg-white border border-gray-100 p-4 rounded-2xl shadow-sm">
                    <div className="flex gap-1">
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                    </div>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </ScrollArea>
        </CardContent>

        <Separator />

        {/* Input */}
        <CardContent className="p-4">
          <div className="flex gap-3 items-end">
            <div className="flex-1">
              <Textarea
                ref={textareaRef}
                placeholder="Задайте вопрос, попросите написать код или проанализировать его..."
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyPress={handleKeyPress}
                rows={3}
                className="resize-none border-gray-200 focus:border-indigo-500 focus:ring-indigo-500/20 transition-colors duration-200"
              />
            </div>
            <Button 
              onClick={handleSend}
              disabled={!inputValue.trim() || isTyping}
              className="px-6 py-3 bg-gradient-to-r from-indigo-500 to-cyan-500 hover:from-indigo-600 hover:to-cyan-600 transition-all duration-200 transform hover:scale-105 shadow-lg hover:shadow-xl"
            >
              <Send className="w-4 h-4" />
            </Button>
          </div>
          <div className="mt-2 text-xs text-gray-500 text-center">
            Нажмите Enter для отправки, Shift+Enter для новой строки
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default ChatInterface;