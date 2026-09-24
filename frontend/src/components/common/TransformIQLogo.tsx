import React from 'react';

interface LogoProps {
  size?: 'sm' | 'md' | 'lg' | 'xl';
  showSubtitle?: boolean;
  className?: string;
}

export const TransformIQLogo: React.FC<LogoProps> = ({
  size = 'md',
  showSubtitle = false,
  className = ''
}) => {
  const iconSizes = {
    sm: 'w-7 h-7',
    md: 'w-9 h-9',
    lg: 'w-12 h-12',
    xl: 'w-16 h-16'
  };

  const textSizes = {
    sm: 'text-base',
    md: 'text-lg',
    lg: 'text-2xl',
    xl: 'text-3xl'
  };

  const badgeSizes = {
    sm: 'text-[8px] px-1 py-0.2',
    md: 'text-[10px] px-1.5 py-0.5',
    lg: 'text-xs px-2 py-0.5',
    xl: 'text-xs px-2.5 py-1'
  };

  return (
    <div className={`flex items-center space-x-2 sm:space-x-3 ${className}`}>
      {/* High-Tech Vector Hexagonal Mark */}
      <div className={`relative ${iconSizes[size]} shrink-0 group`}>
        {/* Ambient Glow */}
        <div className="absolute inset-0 bg-gradient-to-tr from-cyan-500 via-blue-600 to-indigo-600 rounded-xl blur-[6px] opacity-75 group-hover:opacity-100 transition-opacity duration-300 animate-pulse" />
        
        {/* SVG Emblem */}
        <svg
          viewBox="0 0 48 48"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
          className="relative w-full h-full drop-shadow-md transition-transform duration-300 group-hover:scale-105"
        >
          <defs>
            <linearGradient id="tqGrad1" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#38bdf8" />
              <stop offset="50%" stopColor="#6366f1" />
              <stop offset="100%" stopColor="#10b981" />
            </linearGradient>
            <linearGradient id="tqGrad2" x1="100%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stopColor="#a855f7" />
              <stop offset="100%" stopColor="#3b82f6" />
            </linearGradient>
            <linearGradient id="tqCore" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#ffffff" />
              <stop offset="100%" stopColor="#67e8f9" />
            </linearGradient>
          </defs>

          {/* Hexagonal Frame */}
          <rect width="48" height="48" rx="12" fill="#090d16" stroke="url(#tqGrad1)" strokeWidth="1.5" />
          
          {/* Futuristic Transformation Lattice */}
          {/* Top-left node to center */}
          <line x1="14" y1="14" x2="24" y2="24" stroke="url(#tqGrad1)" strokeWidth="2" strokeLinecap="round" strokeDasharray="1 1" />
          {/* Center to bottom-right node */}
          <line x1="24" y1="24" x2="34" y2="34" stroke="url(#tqGrad1)" strokeWidth="2.5" strokeLinecap="round" />
          {/* Top-right to center */}
          <line x1="34" y1="14" x2="24" y2="24" stroke="url(#tqGrad2)" strokeWidth="2" strokeLinecap="round" />
          {/* Bottom-left to center */}
          <line x1="14" y1="34" x2="24" y2="24" stroke="url(#tqGrad2)" strokeWidth="1.5" strokeLinecap="round" />

          {/* Data Nodes */}
          <circle cx="14" cy="14" r="3" fill="#38bdf8" />
          <circle cx="34" cy="14" r="3" fill="#818cf8" />
          <circle cx="14" cy="34" r="2.5" fill="#34d399" />
          <circle cx="34" cy="34" r="3.5" fill="#a855f7" />

          {/* Core Quantum AI Nucleus */}
          <circle cx="24" cy="24" r="5" fill="url(#tqCore)" />
          <circle cx="24" cy="24" r="2" fill="#0f172a" />
        </svg>
      </div>

      {/* Typography & Brand Meta */}
      <div className="flex flex-col text-left">
        <div className="flex items-center space-x-1 sm:space-x-1.5">
          <span className={`font-black ${textSizes[size]} tracking-tight text-white leading-none`}>
            Transform<span className="bg-gradient-to-r from-cyan-400 via-blue-400 to-indigo-300 bg-clip-text text-transparent">IQ</span>
          </span>
          <span className={`uppercase font-extrabold tracking-wider rounded-md bg-cyan-500/10 text-cyan-400 border border-cyan-500/30 shadow-sm ${badgeSizes[size]}`}>
            AI
          </span>
        </div>
        {showSubtitle && (
          <span className="text-[10px] text-slate-400 font-medium tracking-wide mt-0.5 hidden sm:block">
            Chaos → Context → Blueprint
          </span>
        )}
      </div>
    </div>
  );
};
