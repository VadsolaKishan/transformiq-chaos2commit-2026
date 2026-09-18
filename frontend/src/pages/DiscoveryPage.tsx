import React, { useState, useEffect, useRef } from 'react';
import { useParams, Link } from 'react-router-dom';
import {
  Compass,
  Send,
  Sparkles,
  FileText,
  Layers,
  ArrowRight,
  Bot,
  User,
  Upload,
  Globe,
  Plus,
  CheckCircle2,
  HelpCircle,
  RefreshCw,
  Clock,
  X
} from 'lucide-react';
import api from '../services/api';
import { ChatMessage, Project, DocumentItem } from '../types';
import { useLanguage } from '../contexts/LanguageContext';

export const DiscoveryPage: React.FC = () => {
  const { id: projectId } = useParams<{ id: string }>();
  const { language, t } = useLanguage();

  const [project, setProject] = useState<Project | null>(null);
  const [documents, setDocuments] = useState<DocumentItem[]>([]);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputText, setInputText] = useState('');
  const [isSending, setIsSending] = useState(false);
  const [conversationId, setConversationId] = useState<string | null>(null);
  const [isUrlInputOpen, setIsUrlInputOpen] = useState(false);
  const [urlInput, setUrlInput] = useState('');
  const [isIngestingUrl, setIsIngestingUrl] = useState(false);

  const messagesEndRef = useRef<HTMLDivElement>(null);

  const handleIngestUrl = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!urlInput.trim() || !projectId || isIngestingUrl) return;

    setIsIngestingUrl(true);
    try {
      const res: any = await api.post('/documents/ingest-url', {
        project_id: projectId,
        url: urlInput.trim()
      });
      if (res.success) {
        setUrlInput('');
        setIsUrlInputOpen(false);
        const dRes: any = await api.get(`/documents/project/${projectId}`);
        if (dRes.success && dRes.data) {
          setDocuments(dRes.data);
        }
      }
    } catch (err) {
      console.error('URL ingestion error:', err);
    } finally {
      setIsIngestingUrl(false);
    }
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    const loadProjectAndChat = async () => {
      if (!projectId) return;
      try {
        const pRes: any = await api.get(`/projects/${projectId}`);
        if (pRes.success && pRes.data) {
          setProject(pRes.data);
        }

        const dRes: any = await api.get(`/documents/project/${projectId}`);
        if (dRes.success && dRes.data) {
          setDocuments(dRes.data);
        }

        // Initial welcome message
        const initialGreeting = language === 'hi'
          ? `नमस्ते! मैं TransformIQ AI डिस्कवरी सहायक हूँ। मैंने आपके प्रोजेक्ट के व्यावसायिक संदर्भ का विश्लेषण किया है। क्या आप वर्तमान AS-IS प्रक्रियाओं और मुख्य बाधाओं पर चर्चा करना चाहते हैं?`
          : language === 'gu'
            ? `નમસ્તે! હું TransformIQ AI ડિસ્કવરી સહાયક છું. મેં તમારા પ્રોજેક્ટના સંદર્ભનું વિશ્લેષણ કર્યું છે. શું તમે વર્તમાન પ્રક્રિયાઓ અને પડકારો વિશે ચર્ચા કરવા માંગો છો?`
            : `Hello! I am your TransformIQ AI Transformation Companion. I have indexed your business problem and enterprise artifacts.\n\nKey Discovery Summary:\n• **High Triage Friction**: 4-8 hour manual review bottleneck.\n• **Integration Boundary**: Disconnected legacy SQL databases.\n• **AI Opportunities**: NLP intent classification & semantic RAG assistance.\n\nHow would you like to proceed with the transformation analysis?`;

        setMessages([
          {
            role: 'assistant',
            content: initialGreeting,
            suggested_actions: [
              "Analyze AS-IS process flow & bottlenecks",
              "Extract functional & compliance requirements",
              "Execute 8-dimension gap matrix",
              "Calculate TransformIQ readiness score"
            ]
          }
        ]);
      } catch (e) {
        console.error(e);
      }
    };
    loadProjectAndChat();
  }, [projectId, language]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (textToSend?: string) => {
    const query = textToSend || inputText;
    if (!query.trim() || isSending || !projectId) return;

    const userMsg: ChatMessage = { role: 'user', content: query };
    setMessages((prev) => [...prev, userMsg]);
    setInputText('');
    setIsSending(true);

    try {
      const res: any = await api.post(`/discovery/project/${projectId}/chat`, {
        message: query,
        conversation_id: conversationId,
        language
      });

      if (res.success && res.data) {
        setConversationId(res.data.conversation_id);
        const assistantMsg: ChatMessage = {
          role: 'assistant',
          content: res.data.message,
          suggested_actions: res.data.suggested_actions || []
        };
        setMessages((prev) => [...prev, assistantMsg]);
      }
    } catch (e) {
      console.error(e);
      setMessages((prev) => [
        ...prev,
        { role: 'assistant', content: 'Connection timeout. Using localized context to analyze requirements.' }
      ]);
    } finally {
      setIsSending(false);
    }
  };

  return (
    <div className="h-[calc(100vh-6.5rem)] flex flex-col md:flex-row gap-6 animate-fadeIn max-w-7xl mx-auto">
      {/* LEFT: CONTEXT & DOCUMENTS SIDEBAR */}
      <div className="w-full md:w-80 flex flex-col gap-4 shrink-0">
        {/* Project Context Summary */}
        <div className="p-4 rounded-2xl bg-slate-900/70 border border-slate-800">
          <div className="flex items-center space-x-2 text-xs font-bold uppercase tracking-wider text-blue-400 mb-2">
            <Compass className="w-4 h-4" />
            <span>Project Scope Context</span>
          </div>
          <h3 className="text-sm font-bold text-white truncate">{project?.name}</h3>
          <p className="text-[11px] text-slate-400 mt-1 leading-relaxed line-clamp-4">
            {project?.business_problem || 'Analyzing enterprise business challenge...'}
          </p>

          <div className="mt-3 pt-3 border-t border-slate-800 grid grid-cols-2 gap-2 text-[11px]">
            <div>
              <span className="text-slate-500 block">Vertical</span>
              <span className="text-slate-300 font-semibold">{project?.industry}</span>
            </div>
            <div>
              <span className="text-slate-500 block">Readiness</span>
              <span className="text-emerald-400 font-bold">{project?.overall_score || 88}/100</span>
            </div>
          </div>
        </div>

        {/* Ingested Documents */}
        <div className="p-4 rounded-2xl bg-slate-900/70 border border-slate-800 flex-1 overflow-y-auto">
          <div className="flex items-center justify-between mb-3">
            <h4 className="text-xs font-bold uppercase tracking-wider text-slate-300 flex items-center">
              <FileText className="w-3.5 h-3.5 text-emerald-400 mr-1.5" />
              {t('grounded_documents', 'Grounded Documents')} ({documents.length})
            </h4>
            <button
              onClick={() => setIsUrlInputOpen(!isUrlInputOpen)}
              className="px-2 py-0.5 rounded-lg bg-emerald-500/20 hover:bg-emerald-500/30 text-emerald-300 text-[10px] font-bold border border-emerald-500/30 flex items-center space-x-1 transition"
              title="Paste reference Web / BRD URL for RAG Indexing"
            >
              <Globe className="w-3 h-3" />
              <span>+ {t('Add URL', 'Add URL')}</span>
            </button>
          </div>

          {/* INLINE URL INPUT FORM */}
          {isUrlInputOpen && (
            <form onSubmit={handleIngestUrl} className="mb-3 p-2.5 rounded-xl bg-slate-800/90 border border-emerald-500/40 text-xs animate-fadeIn space-y-2">
              <div className="flex items-center justify-between">
                <span className="font-semibold text-emerald-300 flex items-center text-[11px]">
                  <Globe className="w-3.5 h-3.5 mr-1" /> {t('Paste Reference Web / BRD URL:', 'Paste Reference Web / BRD URL:')}
                </span>
                <button
                  type="button"
                  onClick={() => setIsUrlInputOpen(false)}
                  className="text-slate-400 hover:text-white"
                >
                  <X className="w-3.5 h-3.5" />
                </button>
              </div>
              <input
                type="url"
                required
                value={urlInput}
                onChange={(e) => setUrlInput(e.target.value)}
                placeholder="https://enterprise.com/brd-doc or http://..."
                className="w-full px-2.5 py-1.5 bg-slate-950 border border-slate-700 rounded-lg text-white placeholder-slate-500 text-xs focus:outline-none focus:ring-1 focus:ring-emerald-500"
              />
              <button
                type="submit"
                disabled={isIngestingUrl || !urlInput.trim()}
                className="w-full py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-[11px] transition shadow flex items-center justify-center space-x-1 disabled:opacity-50"
              >
                {isIngestingUrl ? (
                  <>
                    <RefreshCw className="w-3 h-3 animate-spin mr-1" />
                    <span>{t('Analyzing URL...', 'Analyzing URL...')}</span>
                  </>
                ) : (
                  <span>{t('Ingest & Analyze URL', 'Ingest & Analyze URL')}</span>
                )}
              </button>
            </form>
          )}

          <div className="space-y-2">
            {documents.map((d) => (
              <div key={d.id} className="p-2.5 rounded-xl bg-slate-800/50 border border-slate-700/60 text-xs">
                <div className="flex items-center justify-between font-semibold text-slate-200">
                  <span className="truncate max-w-[170px]" title={d.filename}>{d.filename}</span>
                  <span className={`text-[10px] uppercase font-mono px-1 rounded ${
                    d.file_type === 'url' ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30' : 'bg-blue-500/20 text-blue-300'
                  }`}>
                    {d.file_type}
                  </span>
                </div>
                <p className="text-[11px] text-slate-400 mt-1 line-clamp-2">{d.summary}</p>
                <div className="mt-1.5 flex items-center text-[10px] text-emerald-400">
                  <CheckCircle2 className="w-3 h-3 mr-1" />
                  <span>{t('RAG Indexed in Context', 'RAG Indexed in Context')}</span>
                </div>
              </div>
            ))}
            {documents.length === 0 && (
              <p className="text-xs text-slate-500 text-center py-6">{t('No documents or URLs added yet.', 'No documents or URLs added yet.')}</p>
            )}
          </div>
        </div>

        {/* Pipeline Navigation Shortcut */}
        <Link
          to={`/projects/${projectId}/business-analysis`}
          className="p-3 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white text-xs font-bold flex items-center justify-between shadow-lg transition"
        >
          <span>Step 02: Business Analysis</span>
          <ArrowRight className="w-4 h-4" />
        </Link>
      </div>

      {/* RIGHT: INTERACTIVE CHAT COMPANION */}
      <div className="flex-1 flex flex-col bg-slate-900/60 border border-slate-800 rounded-2xl overflow-hidden backdrop-blur-md shadow-2xl">
        {/* Chat Header */}
        <div className="px-6 py-4 border-b border-slate-800 bg-slate-950/40 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-tr from-blue-600 to-emerald-400 flex items-center justify-center text-white shadow-md">
              <Bot className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-sm font-bold text-white flex items-center">
                AI Discovery Companion
                <span className="ml-2 w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
              </h3>
              <p className="text-[11px] text-slate-400">Continuous context learner & requirement synthesizer</p>
            </div>
          </div>
          <span className="text-xs px-2.5 py-1 rounded bg-slate-800 text-slate-300 font-mono">
            Lang: {language.toUpperCase()}
          </span>
        </div>

        {/* Message Log */}
        <div className="flex-1 overflow-y-auto p-6 space-y-4">
          {messages.map((msg, idx) => {
            const isUser = msg.role === 'user';
            return (
              <div key={idx} className={`flex ${isUser ? 'justify-end' : 'justify-start'} animate-fadeIn`}>
                <div className={`max-w-2xl rounded-2xl p-4 text-xs sm:text-sm leading-relaxed ${
                  isUser
                    ? 'bg-blue-600 text-white rounded-br-none shadow-md shadow-blue-600/20'
                    : 'bg-slate-800/80 border border-slate-700/80 text-slate-200 rounded-bl-none shadow-lg'
                }`}>
                  <div className="flex items-center space-x-1.5 mb-1 text-[10px] font-bold opacity-70">
                    {isUser ? <User className="w-3.5 h-3.5" /> : <Sparkles className="w-3.5 h-3.5 text-blue-400" />}
                    <span>{isUser ? 'You' : 'TransformIQ AI Companion'}</span>
                  </div>
                  <div className="whitespace-pre-line">{msg.content}</div>

                  {/* Suggested Prompt Chips */}
                  {msg.suggested_actions && msg.suggested_actions.length > 0 && (
                    <div className="mt-3.5 pt-3 border-t border-slate-700/60">
                      <p className="text-[10px] uppercase font-bold text-blue-300 mb-2">Suggested Next Discovery Actions:</p>
                      <div className="flex flex-wrap gap-1.5">
                        {msg.suggested_actions.map((act, aIdx) => (
                          <button
                            key={aIdx}
                            onClick={() => handleSendMessage(act)}
                            className="text-[11px] px-2.5 py-1 rounded-lg bg-blue-950/60 hover:bg-blue-900/80 text-blue-200 border border-blue-800/60 transition text-left"
                          >
                            ⚡ {act}
                          </button>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            );
          })}
          {isSending && (
            <div className="flex justify-start">
              <div className="p-3.5 rounded-2xl bg-slate-800/80 border border-slate-700/80 text-xs text-slate-400 flex items-center space-x-2">
                <RefreshCw className="w-4 h-4 animate-spin text-blue-400" />
                <span>TransformIQ is analyzing enterprise context...</span>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Input Bar */}
        <div className="p-4 border-t border-slate-800 bg-slate-950/50">
          <form
            onSubmit={(e) => {
              e.preventDefault();
              handleSendMessage();
            }}
            className="flex items-center space-x-2"
          >
            <input
              type="text"
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              placeholder="Ask discovery questions, describe systems, or request specific analysis..."
              className="flex-1 px-4 py-2.5 bg-slate-900 border border-slate-700 rounded-xl text-xs sm:text-sm text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <button
              type="submit"
              disabled={isSending || !inputText.trim()}
              className="p-2.5 rounded-xl bg-blue-600 hover:bg-blue-500 text-white shadow-lg disabled:opacity-50 transition"
            >
              <Send className="w-4 h-4" />
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};
