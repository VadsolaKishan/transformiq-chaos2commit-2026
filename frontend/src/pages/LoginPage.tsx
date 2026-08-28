import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Mail, Lock, AlertCircle, ArrowRight, Eye, EyeOff, Sparkles, ShieldCheck } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';
import { TransformIQLogo } from '../components/common/TransformIQLogo';

export const LoginPage: React.FC = () => {
  const navigate = useNavigate();
  const { login, isLoading } = useAuth();

  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    try {
      await login(email, password);
      navigate('/dashboard');
    } catch (err: any) {
      setError(err?.detail || err?.message || 'Invalid credentials. Please check your corporate email and password.');
    }
  };

  return (

    <div className="min-h-screen bg-slate-950 flex flex-col items-center justify-center p-6 relative overflow-hidden font-sans text-slate-100 selection:bg-blue-600 selection:text-white">
      {/* High-Tech Ambient Glowing Backdrops */}
      <div className="absolute top-1/3 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[700px] h-[700px] bg-gradient-to-tr from-blue-600/15 via-cyan-500/10 to-indigo-600/15 blur-3xl pointer-events-none rounded-full" />
      <div className="absolute bottom-10 left-10 w-96 h-96 bg-purple-600/10 blur-3xl pointer-events-none rounded-full" />

      <div className="w-full max-w-md bg-slate-900/85 border border-slate-800 rounded-3xl p-8 backdrop-blur-2xl shadow-2xl relative z-10">
        {/* Header with New Logo */}
        <div className="flex flex-col items-center text-center mb-8">
          <Link to="/" className="mb-4 hover:opacity-95 transition-opacity">
            <TransformIQLogo size="lg" showSubtitle />
          </Link>
          <h2 className="text-xl font-black text-white tracking-tight">Sign In to Your Workspace</h2>
          <p className="text-xs text-slate-400 mt-1">Enterprise Business Transformation AI Platform</p>
        </div>

        {error && (
          <div className="mb-5 p-3 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-300 text-xs flex items-center space-x-2.5 animate-fadeIn">
            <AlertCircle className="w-4 h-4 shrink-0 text-rose-400" />
            <span>{error}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4" autoComplete="off">
          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1.5">
              Corporate Email Address
            </label>
            <div className="relative">
              <Mail className="w-4 h-4 text-slate-500 absolute left-3.5 top-3.5" />
              <input
                type="email"
                required
                autoComplete="off"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="you@company.com"
                className="w-full pl-10 pr-4 py-3 bg-slate-950/70 border border-slate-700/80 rounded-xl text-xs text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500/80 focus:border-blue-500 transition shadow-inner"
              />
            </div>
          </div>

          <div>
            <div className="flex items-center justify-between mb-1.5">
              <label className="block text-xs font-semibold text-slate-300">Password</label>
              <Link
                to="/forgot-password"
                className="text-[11px] text-blue-400 hover:text-blue-300 transition font-medium"
              >
                Forgot password?
              </Link>
            </div>
            <div className="relative">
              <Lock className="w-4 h-4 text-slate-500 absolute left-3.5 top-3.5" />
              <input
                type={showPassword ? 'text' : 'password'}
                required
                autoComplete="new-password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••••••"
                className="w-full pl-10 pr-10 py-3 bg-slate-950/70 border border-slate-700/80 rounded-xl text-xs text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500/80 focus:border-blue-500 transition shadow-inner"
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute right-3.5 top-3.5 text-slate-500 hover:text-slate-300 cursor-pointer"
              >
                {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
              </button>
            </div>
          </div>

          <button
            type="submit"
            disabled={isLoading}
            className="w-full py-3 bg-gradient-to-r from-blue-600 via-indigo-600 to-cyan-600 hover:from-blue-500 hover:to-cyan-500 text-white font-bold text-xs rounded-xl transition-all shadow-lg shadow-blue-500/25 disabled:opacity-50 mt-2 flex items-center justify-center space-x-2 cursor-pointer"
          >
            <span>{isLoading ? 'Authenticating...' : 'Sign In to Platform'}</span>
            <ArrowRight className="w-4 h-4" />
          </button>
        </form>

        <p className="text-center text-xs text-slate-400 mt-6">
          Need a new workspace?{' '}
          <Link to="/register" className="text-cyan-400 hover:text-cyan-300 hover:underline font-semibold">
            Register Organization
          </Link>
        </p>
      </div>
    </div>
  );
};

