import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import {
  Layout,
  Users,
  Compass,
  ArrowRight,
  RefreshCw,
  Eye,
  CheckCircle2,
  AlertTriangle,
  Sparkles
} from 'lucide-react';
import api from '../services/api';
import { UxData } from '../types';
import { LoadingScreen } from '../components/common/LoadingScreen';

export const UxPage: React.FC = () => {
  const { id: projectId } = useParams<{ id: string }>();
  const [data, setData] = useState<UxData | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isRegenerating, setIsRegenerating] = useState(false);
  const [activeWireframeTab, setActiveWireframeTab] = useState(0);

  const fetchData = async () => {
    if (!projectId) return;
    setIsLoading(true);
    try {
      const res: any = await api.get(`/ux/project/${projectId}`);
      if (res.success && res.data) {
        setData(res.data);
      }
    } catch (e) {
      console.error(e);
    } finally {
      setIsLoading(false);
    }
  };

  const handleRegenerate = async () => {
    if (!projectId) return;
    setIsRegenerating(true);
    try {
      const res: any = await api.post(`/ux/project/${projectId}/generate`);
      if (res.success && res.data) {
        setData(res.data);
      }
    } catch (e) {
      console.error(e);
    } finally {
      setIsRegenerating(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, [projectId]);

  if (isLoading) {
    return <LoadingScreen message="Designing user personas, journey stages, and wireframes..." />;
  }

  const activeWireframe = data?.wireframes?.[activeWireframeTab];

  return (
    <div className="space-y-8 animate-fadeIn max-w-7xl mx-auto">
      {/* HEADER */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-slate-800">
        <div>
          <div className="flex items-center space-x-2">
            <span className="text-xs font-mono font-bold px-2 py-0.5 rounded bg-indigo-500/20 text-indigo-300">
              STEP 09
            </span>
            <h1 className="text-2xl font-extrabold text-white">AI UX Designer & Interactive Wireframes</h1>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Enterprise user personas, end-to-end journey maps, and interactive wireframe concepts.
          </p>
        </div>

        <div className="flex items-center space-x-3">
          <button
            onClick={handleRegenerate}
            disabled={isRegenerating}
            className="px-3.5 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold border border-slate-700 transition flex items-center space-x-2"
          >
            <RefreshCw className={`w-3.5 h-3.5 text-indigo-400 ${isRegenerating ? 'animate-spin' : ''}`} />
            <span>{isRegenerating ? 'Designing...' : 'Regenerate'}</span>
          </button>
          <Link
            to={`/projects/${projectId}/planning`}
            className="px-4 py-2 rounded-xl bg-gradient-to-r from-indigo-600 to-blue-600 hover:from-indigo-500 hover:to-blue-500 text-white text-xs font-bold transition flex items-center space-x-1.5 shadow-lg"
          >
            <span>Next: Roadmap & Costs</span>
            <ArrowRight className="w-4 h-4" />
          </Link>
        </div>
      </div>

      {/* USER PERSONAS */}
      <div>
        <h3 className="text-sm font-bold uppercase tracking-wider text-slate-400 mb-3 flex items-center">
          <Users className="w-4 h-4 text-indigo-400 mr-2" /> Target User Personas
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {data?.personas.map((p, idx) => (
            <div key={idx} className="p-6 rounded-2xl bg-slate-900/60 border border-slate-800 backdrop-blur-md">
              <div className="flex items-center space-x-3 mb-4">
                <div className="w-10 h-10 rounded-full bg-indigo-600/30 border border-indigo-500/40 flex items-center justify-center font-bold text-sm text-indigo-300">
                  {p.name.charAt(0)}
                </div>
                <div>
                  <h4 className="text-sm font-bold text-white">{p.name}</h4>
                  <p className="text-xs text-indigo-400 font-medium">{p.role}</p>
                </div>
              </div>

              <div className="space-y-3 text-xs">
                <div>
                  <span className="font-bold text-slate-300 block mb-1 text-[11px] uppercase text-emerald-400">Goals</span>
                  <ul className="list-disc list-inside text-slate-400 space-y-0.5">
                    {p.goals.map((g, i) => (
                      <li key={i}>{g}</li>
                    ))}
                  </ul>
                </div>
                <div>
                  <span className="font-bold text-slate-300 block mb-1 text-[11px] uppercase text-rose-400">Pain Points</span>
                  <ul className="list-disc list-inside text-slate-400 space-y-0.5">
                    {p.pain_points.map((pt, i) => (
                      <li key={i}>{pt}</li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* INTERACTIVE WIREFRAME RENDERER */}
      <div className="p-6 rounded-2xl bg-slate-900/80 border border-slate-800 backdrop-blur-md">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-6 pb-4 border-b border-slate-800">
          <div>
            <h3 className="text-base font-bold text-white flex items-center">
              <Layout className="w-4 h-4 text-blue-400 mr-2" /> Interactive Wireframe Mockup
            </h3>
            <p className="text-xs text-slate-400">Rendered UI component layout generated by AI UX Designer.</p>
          </div>

          {/* Wireframe Tabs */}
          <div className="flex items-center space-x-2 bg-slate-950 p-1 rounded-xl border border-slate-800">
            {data?.wireframes.map((wf, idx) => (
              <button
                key={idx}
                onClick={() => setActiveWireframeTab(idx)}
                className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition ${
                  activeWireframeTab === idx
                    ? 'bg-blue-600 text-white shadow'
                    : 'text-slate-400 hover:text-white'
                }`}
              >
                {wf.screen_name}
              </button>
            ))}
          </div>
        </div>

        {/* MOCKUP CONTAINER */}
        {activeWireframe && (
          <div className="p-6 rounded-2xl bg-slate-950 border border-slate-800 shadow-inner">
            <div className="flex items-center justify-between mb-4 pb-3 border-b border-slate-800">
              <div>
                <span className="text-[10px] uppercase font-bold text-blue-400 px-2 py-0.5 rounded bg-blue-500/10">
                  {activeWireframe.layout_type}
                </span>
                <h4 className="text-sm font-bold text-white mt-1">{activeWireframe.screen_name}</h4>
                <p className="text-xs text-slate-400">{activeWireframe.purpose}</p>
              </div>
              <div className="flex items-center space-x-2">
                {activeWireframe.user_actions.map((act, idx) => (
                  <button
                    key={idx}
                    className="px-3 py-1 rounded-lg text-xs font-semibold bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 transition"
                  >
                    {act}
                  </button>
                ))}
              </div>
            </div>

            {/* Rendered Mockup Components */}
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              {activeWireframe.components.map((comp, idx) => {
                if (comp.type === 'stat_card') {
                  return (
                    <div key={idx} className="p-4 rounded-xl bg-slate-900 border border-slate-800">
                      <span className="text-[11px] font-semibold text-slate-400 block">{comp.label}</span>
                      <span className="text-xl font-bold text-white mt-1 block">{comp.props?.value || '88%'}</span>
                      <span className="text-[10px] text-emerald-400">{comp.props?.trend}</span>
                    </div>
                  );
                }
                if (comp.type === 'alert') {
                  return (
                    <div key={idx} className="sm:col-span-3 p-4 rounded-xl bg-amber-950/30 border border-amber-500/40 text-amber-200 text-xs flex items-center space-x-2">
                      <AlertTriangle className="w-4 h-4 text-amber-400 shrink-0" />
                      <span>{comp.label}</span>
                    </div>
                  );
                }
                return (
                  <div key={idx} className="p-4 rounded-xl bg-slate-900 border border-slate-800 text-xs text-slate-300">
                    <span className="font-bold text-white block mb-1">{comp.label}</span>
                    <span className="text-[10px] text-slate-500">Component: {comp.type}</span>
                  </div>
                );
              })}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
