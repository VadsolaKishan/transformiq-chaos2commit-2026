import React, { useState, useEffect, useRef } from 'react';
import { Mic, MicOff, Volume2, AlertCircle } from 'lucide-react';
import { useLanguage } from '../../contexts/LanguageContext';

interface VoiceInputButtonProps {
  onTranscript: (text: string) => void;
  className?: string;
}

export const VoiceInputButton: React.FC<VoiceInputButtonProps> = ({ onTranscript, className = '' }) => {
  const { language } = useLanguage();
  const [isListening, setIsListening] = useState(false);
  const [isSupported, setIsSupported] = useState(true);
  const recognitionRef = useRef<any>(null);

  // Map language codes to speech recognition BCP-47 tags
  const getLangCode = (lang: string): string => {
    const map: Record<string, string> = {
      en: 'en-US',
      hi: 'hi-IN',
      gu: 'gu-IN',
      mr: 'mr-IN',
      ta: 'ta-IN',
      te: 'te-IN',
      bn: 'bn-IN',
      es: 'es-ES',
      fr: 'fr-FR',
      de: 'de-DE',
      ja: 'ja-JP',
      zh: 'zh-CN',
      ar: 'ar-SA',
      pt: 'pt-BR',
      ru: 'ru-RU'
    };
    return map[lang] || 'en-US';
  };

  useEffect(() => {
    const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    if (!SpeechRecognition) {
      setIsSupported(false);
      return;
    }

    const recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = true;
    recognition.lang = getLangCode(language);

    recognition.onresult = (event: any) => {
      let finalTranscript = '';
      for (let i = event.resultIndex; i < event.results.length; ++i) {
        if (event.results[i].isFinal) {
          finalTranscript += event.results[i][0].transcript;
        }
      }
      if (finalTranscript) {
        onTranscript(finalTranscript);
      }
    };

    recognition.onerror = (event: any) => {
      console.warn('Speech recognition error:', event.error);
      setIsListening(false);
    };

    recognition.onend = () => {
      setIsListening(false);
    };

    recognitionRef.current = recognition;

    return () => {
      try {
        recognition.abort();
      } catch (e) {}
    };
  }, [language, onTranscript]);

  const toggleListening = () => {
    if (!isSupported) {
      alert('Voice Speech-to-Text is not supported in this browser. Please use Google Chrome, Edge, or Safari.');
      return;
    }

    if (isListening) {
      recognitionRef.current?.stop();
      setIsListening(false);
    } else {
      try {
        if (recognitionRef.current) {
          recognitionRef.current.lang = getLangCode(language);
          recognitionRef.current.start();
          setIsListening(true);
        }
      } catch (err) {
        console.warn('Could not start recognition:', err);
      }
    }
  };

  if (!isSupported) {
    return null;
  }

  return (
    <div className="relative inline-flex items-center">
      <button
        type="button"
        onClick={toggleListening}
        title={isListening ? 'Stop recording voice prompt' : 'Speak voice prompt (Multilingual Speech-to-Text)'}
        className={`relative p-2.5 rounded-xl transition-all duration-300 flex items-center justify-center ${
          isListening
            ? 'bg-rose-600 text-white shadow-lg shadow-rose-600/50 ring-2 ring-rose-400 scale-105 animate-pulse'
            : 'bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white border border-slate-700'
        } ${className}`}
      >
        {isListening ? (
          <div className="flex items-center space-x-1.5">
            <MicOff className="w-4 h-4 text-white animate-bounce" />
            <span className="text-[10px] font-bold uppercase tracking-wider hidden sm:inline">Listening...</span>
          </div>
        ) : (
          <Mic className="w-4 h-4 text-blue-400 hover:text-blue-300" />
        )}

        {isListening && (
          <span className="absolute -top-1 -right-1 flex h-3 w-3">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-rose-400 opacity-75"></span>
            <span className="relative inline-flex rounded-full h-3 w-3 bg-rose-500"></span>
          </span>
        )}
      </button>
    </div>
  );
};
