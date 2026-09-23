import React, { useState, useEffect, useRef } from 'react';
import { Outlet, Link, useLocation, useNavigate, useParams, Navigate } from 'react-router-dom';
import {
  LayoutDashboard,
  Building2,
  Users,
  Lock,
  Layers,
  FolderKanban,
  Cpu,
  Activity,
  ShieldCheck,
  Key,
  Sliders,
  Globe,
  Bell,
  LogOut,
  ChevronDown,
  Menu,
  X,
  User as UserIcon,
  Mail,
  Shield,
  Plus,
  UserCheck,
  RefreshCw,
  FileCheck
} from 'lucide-react';
import { useAuth } from '../../contexts/AuthContext';
import { useLanguage } from '../../contexts/LanguageContext';
import api from '../../services/api';
import { Project } from '../../types';
import {
  getSidebarItemsForRole,
  ROLE_DEFINITIONS,
  SidebarItemConfig
} from '../../config/navigation';
import { VALID_ROLES } from '../../utils/permissions';
import { TransformIQLogo } from '../common/TransformIQLogo';
import { CreditBalanceBadge } from '../common/CreditBalanceBadge';


export const AppLayout: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const params = useParams();
  const {
    user,
    token,
    role,
    actualRole,
    evaluationRole,
    isEvaluationMode,
    isRealAdmin,
    isAuthenticated,
    isLoading,
    isReadOnly,
    hasPermission,
    setEvaluationRole,
    exitEvaluationMode,
    logout
  } = useAuth();
  const { language, setLanguage, t } = useLanguage();

  const [projects, setProjects] = useState<Project[]>([]);
  const [selectedProjectId, setSelectedProjectId] = useState<string>('');
  const [isSidebarOpen, setIsSidebarOpen] = useState<boolean>(true);
  const [notificationsOpen, setNotificationsOpen] = useState<boolean>(false);
  const [notifications, setNotifications] = useState<any[]>([]);
  const [isProfileOpen, setIsProfileOpen] = useState<boolean>(false);
  const [isRoleMenuOpen, setIsRoleMenuOpen] = useState<boolean>(false);

  const roleMenuRef = useRef<HTMLDivElement>(null);

  // Close dropdown on outside click
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (roleMenuRef.current && !roleMenuRef.current.contains(event.target as Node)) {
        setIsRoleMenuOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  // Fetch projects for switcher
  useEffect(() => {
    const fetchProjects = async () => {
      try {
        const res: any = await api.get('/projects');
        if (res.success && res.data) {
          const uniqueProjects: Project[] = [];
          const seenIds = new Set<string>();
          const seenNames = new Set<string>();
          for (const p of res.data) {
            if (!seenIds.has(p.id) && !seenNames.has(p.name)) {
              seenIds.add(p.id);
              seenNames.add(p.name);
              uniqueProjects.push(p);
            }
          }
          setProjects(uniqueProjects);
          const hasValidParam = params.id && params.id !== 'default' && uniqueProjects.some((p: Project) => p.id === params.id);
          if (hasValidParam) {
            setSelectedProjectId(params.id!);
          } else if (uniqueProjects.length > 0) {
            setSelectedProjectId(uniqueProjects[0].id);
            if (params.id === 'default' && location.pathname.includes('/projects/default')) {
              navigate(location.pathname.replace('/projects/default', `/projects/${uniqueProjects[0].id}`), { replace: true });
            }
          }
        }
      } catch (e) {
        console.error('Failed to load projects:', e);
      }
    };
    fetchProjects();
  }, [params.id, location.pathname, navigate]);

  // Auto-redirect if on /projects/default/* once projects are loaded
  useEffect(() => {
    if (projects.length > 0 && params.id === 'default' && location.pathname.includes('/projects/default')) {
      navigate(location.pathname.replace('/projects/default', `/projects/${projects[0].id}`), { replace: true });
    }
  }, [projects, params.id, location.pathname, navigate]);

  // Fetch notifications
  useEffect(() => {
    const fetchNotifications = async () => {
      try {
        const res: any = await api.get('/collaboration/notifications');
        if (res.success && res.data) {
          setNotifications(res.data);
        }
      } catch (e) {}
    };
    fetchNotifications();
  }, []);

  const handleLogout = () => {
    setIsProfileOpen(false);
    logout();
    navigate('/login', { replace: true });
  };

  const handleRoleSelect = async (targetRole: string) => {
    setIsRoleMenuOpen(false);
    await setEvaluationRole(targetRole);

    if (targetRole === 'ADMIN') {
      navigate('/admin');
    } else if (location.pathname.startsWith('/admin')) {
      navigate('/dashboard');
    }
  };

  const handleExitEvaluation = async () => {
    await exitEvaluationMode();
    setIsRoleMenuOpen(false);
    navigate('/admin');
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-slate-950 flex flex-col items-center justify-center space-y-4">
        <div className="w-10 h-10 border-3 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
        <p className="text-xs text-slate-400 font-medium">Validating session...</p>
      </div>
    );
  }

  if (!token || !user) {
    return <Navigate to="/login" replace />;
  }

  const activeProject = projects.find(p => p.id === selectedProjectId) || projects[0];
  const activeProjectId = activeProject?.id || '';

  const roleDef = ROLE_DEFINITIONS[role] || ROLE_DEFINITIONS.VIEWER;
  const actualRoleDef = ROLE_DEFINITIONS[actualRole] || ROLE_DEFINITIONS.ADMIN;

  // Get dynamic sidebar items
  const sidebarItems = getSidebarItemsForRole(role, activeProjectId);

  // Group items by section
  const adminItems = sidebarItems.filter(item => item.section === 'admin');
  const mainItems = sidebarItems.filter(item => item.section === 'main');
  const transformationItems = sidebarItems.filter(item => item.section === 'transformation');
  const collaborationItems = sidebarItems.filter(item => item.section === 'collaboration');

  const isAdminRole = role === 'ADMIN';

  // Precision active state checker
  const isItemActive = (route: string) => {
    const [basePath, query] = route.split('?');
    if (query) {
      return location.pathname === basePath && location.search.includes(query);
    }
    return location.pathname === basePath;
  };

  return (
    <div className="min-h-screen bg-slate-950 flex flex-col font-sans text-slate-100 selection:bg-blue-600 selection:text-white">
      {/* EVALUATION MODE STICKY BANNER */}
      {isEvaluationMode && (
        <div className="bg-gradient-to-r from-amber-600 via-orange-600 to-amber-700 px-4 py-1.5 text-xs font-semibold text-white shadow-md z-50 flex items-center justify-between">
          <div className="flex items-center space-x-2 truncate">
            <span className="flex h-2 w-2 relative">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-white opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-white"></span>
            </span>
            <span className="font-extrabold uppercase tracking-wider text-[11px] bg-black/25 px-2 py-0.5 rounded">
              ROLE EVALUATION MODE ACTIVE
            </span>
            <span className="hidden sm:inline">
              Previewing UI as <strong className="underline underline-offset-2">{roleDef.displayName}</strong>. Real account role remains <strong className="font-mono bg-black/30 px-1.5 py-0.5 rounded">{actualRole}</strong>.
            </span>
          </div>

          <div className="flex items-center space-x-2 shrink-0">
            <button
              onClick={handleExitEvaluation}
              className="px-2.5 py-1 rounded bg-black/30 hover:bg-black/50 text-white text-[11px] font-bold transition flex items-center space-x-1 border border-white/20 shadow-sm"
              title="Exit Evaluation Mode and return to full Admin view"
            >
              <RefreshCw className="w-3 h-3" />
              <span>Exit Evaluation Mode</span>
            </button>
          </div>
        </div>
      )}

      {/* TOP NAVBAR */}
      <header className="h-16 border-b border-slate-800 bg-slate-950/90 backdrop-blur-md sticky top-0 z-40 px-4 md:px-6 flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <button
            onClick={() => setIsSidebarOpen(!isSidebarOpen)}
            className="md:hidden p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800"
          >
            {isSidebarOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
          </button>

          <Link to={isAdminRole ? '/admin' : '/dashboard'} className="flex items-center hover:opacity-95 transition-opacity">
            <TransformIQLogo size="md" showSubtitle />
          </Link>


          {/* ROLE EVALUATION SWITCHER DROPDOWN */}
          {isRealAdmin ? (
            <div className="relative" ref={roleMenuRef}>
              <button
                type="button"
                onClick={() => setIsRoleMenuOpen(!isRoleMenuOpen)}
                className={`flex items-center space-x-2 px-3 py-1.5 rounded-xl border text-xs font-bold transition shadow-sm ${
                  isEvaluationMode
                    ? 'bg-amber-500/15 text-amber-300 border-amber-500/40 hover:bg-amber-500/25 ring-1 ring-amber-500/30'
                    : `${roleDef.color.bg} ${roleDef.color.text} ${roleDef.color.border} hover:opacity-95`
                }`}
                title="Click to select evaluation role preview"
              >
                <UserCheck className="w-3.5 h-3.5" />
                <div className="flex flex-col text-left">
                  <div className="flex items-center space-x-1">
                    <span>ROLE: {role}</span>
                    <ChevronDown className="w-3 h-3 opacity-70" />
                  </div>
                  {isEvaluationMode && (
                    <span className="text-[9px] uppercase tracking-wider font-extrabold text-amber-400 leading-none">
                      EVALUATION MODE (Real: ADMIN)
                    </span>
                  )}
                </div>
              </button>

              {isRoleMenuOpen && (
                <div className="absolute left-0 mt-2 w-72 bg-slate-900 border border-slate-700 rounded-2xl shadow-2xl p-2.5 z-50 animate-fadeIn space-y-1.5 text-xs">
                  <div className="px-3 py-2 border-b border-slate-800">
                    <div className="flex items-center justify-between">
                      <span className="text-[11px] font-extrabold text-white uppercase tracking-wider">
                        SELECT EVALUATION ROLE
                      </span>
                      <span className="text-[9px] font-bold px-1.5 py-0.5 rounded bg-blue-500/20 text-blue-300">
                        Admin Preview
                      </span>
                    </div>
                    <p className="text-[10px] text-slate-400 mt-0.5">
                      Preview UI, sidebar & permissions without altering real Admin account or DB roles.
                    </p>
                  </div>

                  <div className="space-y-1 max-h-80 overflow-y-auto py-1">
                    {VALID_ROLES.map((roleKey) => {
                      const itemDef = ROLE_DEFINITIONS[roleKey];
                      const isSelected = role === roleKey;

                      return (
                        <button
                          key={roleKey}
                          type="button"
                          onClick={() => handleRoleSelect(roleKey)}
                          className={`w-full text-left px-3 py-2 rounded-xl transition flex items-start justify-between group ${
                            isSelected
                              ? 'bg-blue-600 text-white shadow-md'
                              : 'text-slate-300 hover:bg-slate-800 hover:text-white'
                          }`}
                        >
                          <div className="space-y-0.5">
                            <div className="flex items-center space-x-2">
                              <span className="font-bold text-xs">{itemDef.displayName}</span>
                              <span className={`text-[10px] font-medium opacity-80 ${isSelected ? 'text-blue-100' : 'text-slate-400'}`}>
                                ({itemDef.subtitle})
                              </span>
                            </div>
                            <p className={`text-[10px] ${isSelected ? 'text-blue-100' : 'text-slate-400'}`}>
                              {itemDef.description}
                            </p>
                          </div>

                          {isSelected && (
                            <span className="w-2 h-2 rounded-full bg-emerald-400 shrink-0 mt-1.5 shadow-sm"></span>
                          )}
                        </button>
                      );
                    })}
                  </div>

                  {isEvaluationMode && (
                    <div className="pt-2 border-t border-slate-800">
                      <button
                        type="button"
                        onClick={handleExitEvaluation}
                        className="w-full py-2 px-3 rounded-xl bg-rose-600/20 hover:bg-rose-600/30 text-rose-300 border border-rose-500/30 text-xs font-bold transition flex items-center justify-center space-x-1.5"
                      >
                        <RefreshCw className="w-3.5 h-3.5" />
                        <span>Exit Evaluation Mode (Restore ADMIN)</span>
                      </button>
                    </div>
                  )}
                </div>
              )}
            </div>
          ) : (
            <div
              className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-xl border text-xs font-bold ${roleDef.color.bg} ${roleDef.color.text} ${roleDef.color.border}`}
              title={`Authenticated as ${actualRole}`}
            >
              <UserCheck className="w-3.5 h-3.5" />
              <span>ROLE: {actualRoleDef.displayName}</span>
            </div>
          )}
        </div>

        {/* Project Selector & Actions */}
        <div className="flex items-center space-x-3">
          {!isAdminRole && projects.length > 0 ? (
            <div className="relative">
              <select
                value={selectedProjectId}
                onChange={(e) => {
                  const newId = e.target.value;
                  setSelectedProjectId(newId);
                  if (location.pathname.includes('/projects/')) {
                    const parts = location.pathname.split('/');
                    const subpage = parts.slice(3).join('/');
                    navigate(`/projects/${newId}/${subpage || 'discovery'}`);
                  } else {
                    navigate(`/projects/${newId}/discovery`);
                  }
                }}
                className="bg-slate-900 border border-slate-700 hover:border-slate-600 text-xs font-semibold text-slate-200 rounded-lg px-3 py-1.5 focus:outline-none focus:ring-1 focus:ring-blue-500 cursor-pointer pr-7 max-w-[180px] sm:max-w-[240px] truncate"
              >
                {projects.map((p) => (
                  <option key={p.id} value={p.id} className="bg-slate-900 text-slate-100">
                    📁 {p.name}
                  </option>
                ))}
              </select>
            </div>
          ) : !isAdminRole ? (
            <Link
              to="/projects"
              className="px-3 py-1.5 rounded-lg bg-blue-600 hover:bg-blue-500 text-white text-xs font-semibold flex items-center space-x-1 transition shadow"
            >
              <Plus className="w-3.5 h-3.5" />
              <span>{t('create_project', 'Create Project')}</span>
            </Link>

          ) : null}

          {/* AI Credits & Pricing Engine */}
          <CreditBalanceBadge />

          {/* Multilingual Selector */}
          <div className="flex items-center bg-slate-900 border border-slate-800 rounded-lg p-0.5 text-xs">
            <button
              onClick={() => setLanguage('en')}
              className={`px-2 py-1 rounded font-medium transition ${language === 'en' ? 'bg-blue-600 text-white shadow' : 'text-slate-400 hover:text-slate-200'}`}
              title="English"
            >
              EN
            </button>
            <button
              onClick={() => setLanguage('hi')}
              className={`px-2 py-1 rounded font-medium transition ${language === 'hi' ? 'bg-blue-600 text-white shadow' : 'text-slate-400 hover:text-slate-200'}`}
              title="हिन्दी (Hindi)"
            >
              हिं
            </button>
            <button
              onClick={() => setLanguage('gu')}
              className={`px-2 py-1 rounded font-medium transition ${language === 'gu' ? 'bg-blue-600 text-white shadow' : 'text-slate-400 hover:text-slate-200'}`}
              title="ગુજરાતી (Gujarati)"
            >
              ગુ
            </button>
          </div>

          {/* Notifications Bell */}
          <div className="relative">
            <button
              onClick={() => setNotificationsOpen(!notificationsOpen)}
              className="p-2 rounded-lg bg-slate-900 hover:bg-slate-800 border border-slate-800 text-slate-300 relative transition"
            >
              <Bell className="w-4 h-4" />
              {notifications.length > 0 && (
                <span className="absolute top-1 right-1 w-2 h-2 bg-blue-500 rounded-full"></span>
              )}
            </button>

            {notificationsOpen && (
              <div className="absolute right-0 mt-2 w-80 bg-slate-900 border border-slate-800 rounded-xl shadow-2xl p-4 z-50 animate-fadeIn">
                <div className="flex items-center justify-between pb-2 border-b border-slate-800 mb-3">
                  <h4 className="text-xs font-bold uppercase tracking-wider text-slate-300">Notifications</h4>
                  <span className="text-[10px] text-blue-400 bg-blue-500/10 px-2 py-0.5 rounded">Live</span>
                </div>
                <div className="space-y-2.5 max-h-60 overflow-y-auto">
                  {notifications.map((n) => (
                    <div key={n.id} className="text-xs p-2 rounded-lg bg-slate-800/60 border border-slate-700/50">
                      <p className="font-semibold text-slate-200">{n.title}</p>
                      <p className="text-slate-400 text-[11px] mt-0.5">{n.message}</p>
                    </div>
                  ))}
                  {notifications.length === 0 && (
                    <p className="text-xs text-slate-500 text-center py-4">No unread notifications</p>
                  )}
                </div>
              </div>
            )}
          </div>

          {/* User Profile Avatar & Trigger */}
          <div className="flex items-center space-x-2 pl-2 border-l border-slate-800">
            <button
              type="button"
              onClick={() => setIsProfileOpen(true)}
              className="flex items-center space-x-2 p-1 rounded-lg hover:bg-slate-800 transition text-left"
              title="Open User Profile"
            >
              <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-blue-600 to-emerald-500 border border-blue-400/40 flex items-center justify-center font-bold text-xs text-white shadow-md">
                {user?.full_name ? user.full_name.charAt(0).toUpperCase() : 'U'}
              </div>
              <div className="hidden md:block">
                <p className="text-xs font-semibold text-slate-200 leading-tight">{user?.full_name || 'Enterprise User'}</p>
                <div className="flex items-center space-x-1">
                  <p className={`text-[10px] font-mono font-bold ${roleDef.color.text}`}>{role}</p>
                  {isEvaluationMode && (
                    <span className="text-[9px] text-amber-400 font-bold">(EVAL)</span>
                  )}
                </div>
              </div>
            </button>

            {/* Direct Sign Out Button */}
            <button
              onClick={handleLogout}
              title="Sign Out"
              className="p-1.5 rounded-lg text-slate-400 hover:text-rose-400 hover:bg-slate-800 transition ml-1"
            >
              <LogOut className="w-4 h-4" />
            </button>
          </div>
        </div>
      </header>

      {/* USER PROFILE MODAL */}
      {isProfileOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm animate-fadeIn">
          <div className="bg-slate-900 border border-slate-700 rounded-2xl max-w-md w-full p-6 shadow-2xl relative">
            <button
              onClick={() => setIsProfileOpen(false)}
              className="absolute top-5 right-5 text-slate-400 hover:text-white p-1 rounded-lg bg-slate-800/60"
            >
              <X className="w-5 h-5" />
            </button>

            <div className="text-center mb-6">
              <div className="w-16 h-16 rounded-2xl bg-gradient-to-tr from-blue-600 via-indigo-500 to-emerald-400 mx-auto flex items-center justify-center text-white text-2xl font-black shadow-xl shadow-blue-500/30 mb-3">
                {user?.full_name ? user.full_name.charAt(0).toUpperCase() : 'U'}
              </div>
              <h3 className="text-lg font-bold text-white">{user?.full_name || 'Enterprise User'}</h3>
              <div className="mt-1 flex items-center justify-center gap-1.5">
                <span className={`px-3 py-0.5 rounded-full text-[11px] font-bold border ${roleDef.color.bg} ${roleDef.color.text} ${roleDef.color.border}`}>
                  ROLE: {role}
                </span>
                {isEvaluationMode && (
                  <span className="px-2 py-0.5 rounded-full text-[10px] font-extrabold bg-amber-500/20 text-amber-300 border border-amber-500/40">
                    EVALUATION MODE
                  </span>
                )}
              </div>
            </div>

            <div className="space-y-3 bg-slate-950/60 p-4 rounded-xl border border-slate-800 text-xs mb-6">
              <div className="flex items-center justify-between">
                <span className="text-slate-400 flex items-center">
                  <Mail className="w-3.5 h-3.5 mr-1.5 text-blue-400" /> Email
                </span>
                <span className="font-semibold text-slate-200">{user?.email || 'user@enterprise.com'}</span>
              </div>

              <div className="flex items-center justify-between">
                <span className="text-slate-400 flex items-center">
                  <Building2 className="w-3.5 h-3.5 mr-1.5 text-emerald-400" /> Organization
                </span>
                <span className="font-semibold text-slate-200">Acme Global Retail & Logistics</span>
              </div>

              <div className="flex items-center justify-between">
                <span className="text-slate-400 flex items-center">
                  <Shield className="w-3.5 h-3.5 mr-1.5 text-purple-400" /> Actual Database Role
                </span>
                <span className="font-mono font-bold text-rose-400">{actualRole}</span>
              </div>

              <div className="flex items-center justify-between">
                <span className="text-slate-400 flex items-center">
                  <Key className="w-3.5 h-3.5 mr-1.5 text-amber-400" /> Evaluation State
                </span>
                <span className={`font-semibold ${isEvaluationMode ? 'text-amber-400' : 'text-emerald-400'}`}>
                  {isEvaluationMode ? `Active Preview (${role})` : 'Standard Real Mode'}
                </span>
              </div>
            </div>

            <div className="flex items-center space-x-3">
              <button
                type="button"
                onClick={() => setIsProfileOpen(false)}
                className="flex-1 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 font-semibold text-xs transition"
              >
                Close
              </button>
              <button
                type="button"
                onClick={handleLogout}
                className="flex-1 py-2.5 rounded-xl bg-rose-600 hover:bg-rose-500 text-white font-bold text-xs transition shadow-lg flex items-center justify-center space-x-1.5"
              >
                <LogOut className="w-4 h-4" />
                <span>Sign Out</span>
              </button>
            </div>
          </div>
        </div>
      )}

      {/* BODY CONTENT: DYNAMIC SIDEBAR + MAIN */}
      <div className="flex-1 flex overflow-hidden">
        {/* TRANSFORMATION & ROLE DYNAMIC SIDEBAR */}
        <aside
          className={`${
            isSidebarOpen ? 'w-64' : 'w-0 -translate-x-full md:w-16 md:translate-x-0'
          } border-r border-slate-800/80 bg-slate-950/80 backdrop-blur-md flex flex-col justify-between transition-all duration-300 overflow-y-auto shrink-0 z-30`}
        >
          <div className="p-3 space-y-4">
            {/* Active Role Header / Badge in Sidebar */}
            {isSidebarOpen && (
              <div className={`p-2.5 rounded-xl border ${roleDef.color.bg} ${roleDef.color.border}`}>
                <div className="flex items-center justify-between text-[11px] font-bold mb-0.5">
                  <span className={`uppercase tracking-wider ${roleDef.color.text}`}>
                    {roleDef.displayName} View
                  </span>
                  {isEvaluationMode && (
                    <span className="px-1.5 py-0.2 rounded bg-amber-500/20 text-amber-300 text-[9px] font-mono font-bold">
                      EVAL
                    </span>
                  )}
                  {isReadOnly && (
                    <span className="px-1.5 py-0.2 rounded bg-slate-700 text-slate-300 text-[9px] font-bold">
                      READ ONLY
                    </span>
                  )}
                </div>
                <p className="text-[10px] text-slate-300 font-medium leading-tight">
                  {roleDef.description}
                </p>
              </div>
            )}

            {/* Active Project Card (for non-admin evaluation roles) */}
            {!isAdminRole && isSidebarOpen && activeProject && (
              <div className="p-2.5 rounded-xl bg-slate-900/70 border border-slate-800">
                <div className="flex items-center justify-between text-[10px] text-blue-400 font-semibold mb-0.5">
                  <span>PROJECT</span>
                  <span className="px-1.5 py-0.2 rounded bg-emerald-500/20 text-emerald-300 text-[9px]">
                    {activeProject.status}
                  </span>
                </div>
                <h4 className="text-xs font-bold text-slate-100 truncate">{activeProject.name}</h4>
              </div>
            )}

            {/* 1. ADMIN SIDEBAR (Section 5) */}
            {isAdminRole ? (
              <div className="space-y-3">
                {isSidebarOpen && (
                  <div className="px-3 pb-1 border-b border-slate-800/80 flex items-center justify-between">
                    <span className="text-[11px] font-extrabold uppercase tracking-wider text-rose-400 flex items-center space-x-1.5">
                      <ShieldCheck className="w-3.5 h-3.5" />
                      <span>ADMIN PLATFORM</span>
                    </span>
                    <span className="text-[9px] font-bold px-1.5 py-0.5 rounded bg-rose-500/20 text-rose-300 border border-rose-500/30">
                      CONTROL
                    </span>
                  </div>
                )}

                <nav className="space-y-0.5 font-sans">
                  {adminItems.map((item) => {
                    const currentTab = new URLSearchParams(location.search).get('tab') || 'dashboard';
                    const itemTab = item.route.includes('tab=') ? item.route.split('tab=')[1] : '';
                    const isTabActive = location.pathname.startsWith('/admin') && (itemTab ? currentTab === itemTab : currentTab === 'dashboard');
                    const Icon = item.icon;

                    return (
                      <div key={item.id} className="space-y-0.5">
                        <Link
                          to={item.route}
                          className={`flex items-center px-3 py-1.5 rounded-lg text-xs font-semibold transition-all group ${
                            isTabActive
                              ? 'bg-rose-600/90 text-white shadow-md shadow-rose-600/20'
                              : 'text-slate-400 hover:text-slate-100 hover:bg-slate-900'
                          }`}
                        >
                          <Icon className={`w-4 h-4 shrink-0 ${isTabActive ? 'text-white' : 'text-slate-400 group-hover:text-rose-400'}`} />
                          {isSidebarOpen && (
                            <div className="ml-3 flex items-center justify-between flex-1 truncate">
                              <span className="truncate">{t(item.id, item.label)}</span>
                              {isTabActive && (
                                <span className="w-1.5 h-1.5 rounded-full bg-white animate-pulse"></span>
                              )}
                            </div>
                          )}
                        </Link>

                        {/* Subitems */}
                        {item.subItems && isSidebarOpen && (
                          <div className="ml-7 pl-2 border-l border-slate-800 space-y-1 py-1">
                            {item.subItems.map((sub) => {
                              const isSubActive = location.pathname.startsWith('/admin') && currentTab === sub.tab;
                              return (
                                <Link
                                  key={sub.label}
                                  to={sub.route}
                                  className={`block px-2 py-1 rounded text-[11px] font-medium transition ${
                                    isSubActive ? 'text-rose-300 font-bold bg-rose-500/10' : 'text-slate-500 hover:text-slate-300'
                                  }`}
                                >
                                  └── {t(sub.label, sub.label)}
                                </Link>
                              );
                            })}
                          </div>
                        )}
                      </div>
                    );
                  })}
                </nav>
              </div>
            ) : (
              /* 2. ROLE-SPECIFIC DYNAMIC SIDEBAR */
              <div className="space-y-3">
                {/* Main Navigation Items (Dashboard, Projects) */}
                {mainItems.length > 0 && (
                  <nav className="space-y-0.5">
                    {mainItems.map((item) => {
                      const isActive = isItemActive(item.route);
                      const Icon = item.icon;

                      return (
                        <Link
                          key={item.id}
                          to={item.route}
                          className={`flex items-center px-3 py-1.5 rounded-lg text-xs font-semibold transition-all group ${
                            isActive
                              ? 'bg-blue-600 text-white shadow-md shadow-blue-600/30'
                              : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900'
                          }`}
                        >
                          <Icon className={`w-4 h-4 shrink-0 ${isActive ? 'text-white' : 'text-slate-400 group-hover:text-blue-400'}`} />
                          {isSidebarOpen && <span className="ml-3 truncate">{t(item.id, item.label)}</span>}
                        </Link>
                      );
                    })}
                  </nav>
                )}

                {/* Transformation Pipeline Modules (Step 01 - 13) */}
                {transformationItems.length > 0 && (
                  <div>
                    {isSidebarOpen && (
                      <p className="text-[10px] font-bold uppercase tracking-wider text-slate-500 px-3 mb-1.5">
                        {t('transformation_workflow', 'Transformation Workflow')}
                      </p>
                    )}
                    <nav className="space-y-0.5">
                      {transformationItems.map((item) => {
                        const isActive = isItemActive(item.route);
                        const Icon = item.icon;

                        return (
                          <Link
                            key={item.id}
                            to={item.route}
                            className={`flex items-center px-3 py-1.5 rounded-lg text-xs font-medium transition-all group ${
                              isActive
                                ? 'bg-blue-600 text-white shadow-md shadow-blue-600/30'
                                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900'
                            }`}
                          >
                            <Icon className={`w-4 h-4 shrink-0 ${isActive ? 'text-white' : 'text-slate-400 group-hover:text-blue-400'}`} />
                            {isSidebarOpen && (
                              <div className="ml-3 flex items-center justify-between flex-1 truncate">
                                <span className="truncate">{t(item.id, item.label)}</span>
                                {item.step && (
                                  <span
                                    className={`text-[10px] px-1.5 py-0.2 rounded font-mono ${
                                      isActive ? 'bg-blue-500 text-white' : 'bg-slate-800 text-slate-400'
                                    }`}
                                  >
                                    {item.step}
                                  </span>
                                )}
                              </div>
                            )}
                          </Link>
                        );
                      })}
                    </nav>
                  </div>
                )}

                {/* Collaboration & Governance Modules */}
                {collaborationItems.length > 0 && (
                  <div>
                    {isSidebarOpen && (
                      <p className="text-[10px] font-bold uppercase tracking-wider text-slate-500 px-3 mb-1.5">
                        {t('governance', 'Governance & Logs')}
                      </p>
                    )}
                    <nav className="space-y-0.5">
                      {collaborationItems.map((item) => {
                        const isActive = isItemActive(item.route);
                        const Icon = item.icon;

                        return (
                          <Link
                            key={item.id}
                            to={item.route}
                            className={`flex items-center px-3 py-1.5 rounded-lg text-xs font-medium transition-all group ${
                              isActive
                                ? 'bg-indigo-600 text-white shadow-md'
                                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900'
                            }`}
                          >
                            <Icon className={`w-4 h-4 shrink-0 ${isActive ? 'text-white' : 'text-slate-400 group-hover:text-indigo-400'}`} />
                            {isSidebarOpen && <span className="ml-3 truncate">{t(item.id, item.label)}</span>}
                          </Link>
                        );
                      })}
                    </nav>
                  </div>
                )}

              </div>
            )}
          </div>

          {/* Sidebar Footer */}
          {isSidebarOpen && (
            <div className="p-3 border-t border-slate-800/80 bg-slate-950/60 space-y-2">
              {isEvaluationMode ? (
                <button
                  type="button"
                  onClick={handleExitEvaluation}
                  className="w-full py-2 px-3 rounded-lg bg-amber-600/20 hover:bg-amber-600/30 text-amber-300 border border-amber-500/30 text-xs font-bold flex items-center justify-center space-x-1.5 transition"
                >
                  <RefreshCw className="w-3.5 h-3.5" />
                  <span>Exit Evaluation</span>
                </button>
              ) : !isAdminRole && hasPermission('blueprint.view') ? (
                <Link
                  to={`/projects/${activeProjectId}/blueprint`}
                  className="w-full py-2 px-3 rounded-lg bg-gradient-to-r from-blue-600 to-emerald-500 hover:from-blue-500 hover:to-emerald-400 text-white text-xs font-bold flex items-center justify-center space-x-1.5 shadow-lg transition"
                >
                  <FileCheck className="w-4 h-4" />
                  <span>{t('blueprint')}</span>
                </Link>
              ) : null}
            </div>
          )}
        </aside>

        {/* MAIN OUTLET CONTAINER */}
        <main className="flex-1 overflow-y-auto bg-slate-950 p-4 md:p-8">
          <Outlet />
        </main>
      </div>
    </div>
  );
};
