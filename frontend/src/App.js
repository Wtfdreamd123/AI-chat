import React from "react";
import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import ChatInterface from "./components/ChatInterface";
import FeatureCards from "./components/FeatureCards";
import { Card, CardContent } from "./components/ui/card";
import { Badge } from "./components/ui/badge";
import { Brain, Sparkles, Code2 } from "lucide-react";

const Home = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
      {/* Hero Section */}
      <div className="container mx-auto px-4 py-8">
        <div className="text-center mb-12">
          <div className="flex justify-center items-center gap-3 mb-6">
            <div className="p-4 bg-gradient-to-r from-indigo-600 to-cyan-600 rounded-2xl shadow-xl">
              <Brain className="w-12 h-12 text-white" />
            </div>
            <div className="flex flex-col items-start">
              <h1 className="text-5xl font-bold bg-gradient-to-r from-indigo-600 to-cyan-600 bg-clip-text text-transparent">
                AI Кодер
              </h1>
              <Badge className="mt-2 bg-gradient-to-r from-indigo-500 to-cyan-500 text-white border-0">
                <Sparkles className="w-3 h-3 mr-1" />
                Powered by Advanced AI
              </Badge>
            </div>
          </div>
          
          <p className="text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed mb-8">
            Ваш персональный ИИ-помощник для программирования. Генерируйте код, анализируйте проекты 
            и получайте экспертные советы в режиме реального времени.
          </p>

          <div className="flex justify-center gap-6 text-sm text-gray-500 mb-12">
            <div className="flex items-center gap-2">
              <Code2 className="w-4 h-4 text-indigo-500" />
              <span>Поддержка 15+ языков</span>
            </div>
            <div className="flex items-center gap-2">
              <Brain className="w-4 h-4 text-cyan-500" />
              <span>ИИ анализ кода</span>
            </div>
            <div className="flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-purple-500" />
              <span>Мгновенные ответы</span>
            </div>
          </div>
        </div>

        {/* Feature Cards */}
        <FeatureCards />

        {/* Chat Interface */}
        <Card className="border-0 shadow-2xl bg-white/80 backdrop-blur-sm">
          <CardContent className="p-6">
            <div className="h-[700px]">
              <ChatInterface />
            </div>
          </CardContent>
        </Card>

        {/* Footer */}
        <div className="text-center mt-12 text-gray-500">
          <p className="text-sm">
            🚀 Готов к программированию с ИИ? Задайте первый вопрос выше!
          </p>
          <p className="text-xs mt-2 opacity-70">
            🚀 Настоящая ИИ интеграция активна! Powered by GPT-4o, Claude-3.5 и Gemini-2.0
          </p>
        </div>
      </div>
    </div>
  );
};

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Home />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;