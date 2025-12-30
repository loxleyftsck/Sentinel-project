"use client";

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import Image from 'next/image';
import { ArrowLeft, Zap, BarChart3, Shield, Database, Layout, Sparkles, AlertTriangle, RefreshCcw, Activity } from 'lucide-react';

export default function PrototypePage() {
    const [status, setStatus] = useState<'idle' | 'scanning' | 'alert' | 'crash' | 'recovering'>('idle');
    const [progress, setProgress] = useState(0);

    // Simulation logic
    useEffect(() => {
        let interval: NodeJS.Timeout;
        if (status === 'scanning') {
            interval = setInterval(() => {
                setProgress(prev => {
                    if (prev >= 100) {
                        setStatus('alert');
                        return 100;
                    }
                    return prev + 2;
                });
            }, 50);
        } else if (status === 'crash') {
            interval = setTimeout(() => {
                setStatus('recovering');
                setTimeout(() => setStatus('idle'), 2000);
            }, 3000);
        }
        return () => {
            if (interval) clearInterval(interval as any);
        };
    }, [status]);

    const triggerCrash = () => {
        setStatus('scanning');
        setProgress(0);
        setTimeout(() => {
            // Force crash after scanning
        }, 3000);
    };

    return (
        <div className={`min-h-screen transition-colors duration-700 font-sans selection:bg-cyan-500/30 ${status === 'crash' ? 'bg-red-950/20 grayscale' : 'bg-[#0a0a0a]'
            } text-white`}>

            {/* Crash Overlay */}
            {status === 'crash' && (
                <div className="fixed inset-0 z-100 flex flex-col items-center justify-center bg-red-900/40 backdrop-blur-md animate-pulse">
                    <div className="p-12 rounded-3xl bg-black border-2 border-red-500 shadow-[0_0_50px_rgba(239,68,68,0.5)] text-center space-y-6">
                        <AlertTriangle size={80} className="text-red-500 mx-auto animate-bounce" />
                        <h2 className="text-4xl font-black font-mono tracking-tighter uppercase italic">Kernel Panic</h2>
                        <p className="text-red-400 font-mono text-sm">CRITICAL_BUFFER_OVERFLOW: Transaction Feed #0xFA21</p>
                        <div className="h-1 w-full bg-red-900 overflow-hidden rounded-full">
                            <div className="h-full bg-red-500 animate-[loading_1s_infinite]" />
                        </div>
                        <p className="text-white/20 text-[10px] animate-pulse">Autorecovery active... Stand by</p>
                    </div>
                </div>
            )}

            {/* Navigation */}
            <nav className="border-b border-white/5 bg-black/50 backdrop-blur-xl sticky top-0 z-50">
                <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
                    <div className="flex items-center gap-4">
                        <Link href="/" className="hover:text-cyan-400 transition-colors flex items-center gap-2 text-sm font-medium">
                            <ArrowLeft size={16} /> Back
                        </Link>
                        <div className="h-4 w-px bg-white/10" />
                        <span className="text-white/40 text-sm font-mono tracking-tighter uppercase italic">SENTINEL v2.0</span>
                    </div>
                    <div className="flex items-center gap-6">
                        <div className="flex items-center gap-2">
                            <div className={`h-2 w-2 rounded-full animate-pulse ${status === 'alert' ? 'bg-red-500' : 'bg-cyan-500'}`} />
                            <span className="text-[10px] font-bold text-white uppercase tracking-widest">{status === 'idle' ? 'System Stable' : status}</span>
                        </div>
                        <button
                            onClick={() => setStatus('crash')}
                            className="bg-red-500/10 hover:bg-red-500/20 text-red-400 text-[10px] px-3 py-1 rounded-full border border-red-500/20 transition-all uppercase font-bold"
                        >
                            Stress Test
                        </button>
                    </div>
                </div>
            </nav>

            {/* Content Header */}
            <section className="relative pt-20 pb-32 px-6 overflow-hidden">
                <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[1000px] h-[600px] bg-cyan-500/10 blur-[120px] rounded-full -z-10" />

                <div className="max-w-5xl mx-auto text-center space-y-6">
                    <div className="relative inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-white/5 border border-white/10 text-white/50 text-xs font-bold uppercase tracking-wider overflow-hidden group">
                        <div className="absolute inset-0 bg-linear-to-r from-cyan-500/0 via-cyan-500/20 to-cyan-500/0 -translate-x-full group-hover:translate-x-full transition-transform duration-1000" />
                        <Sparkles size={14} className="text-cyan-400" /> Dynamic Visualization v2.0
                    </div>
                    <h1 className="text-6xl md:text-8xl font-black tracking-tighter italic uppercase text-white transition-all delay-75 duration-700">
                        Visual <span className="text-cyan-400 drop-shadow-[0_0_15px_rgba(34,211,238,0.4)]">Intelligence</span>
                    </h1>
                </div>

                {/* Dashboard Matrix Interaction */}
                <div className="max-w-6xl mx-auto mt-16 grid grid-cols-1 md:grid-cols-4 gap-4">
                    {[
                        { label: 'Latency', value: '1.2ms', color: 'cyan', icon: Zap },
                        { label: 'Complexity', value: 'Lv. 92', color: 'violet', icon: Shield },
                        { label: 'RAG Nodes', value: '1,442', color: 'emerald', icon: Database },
                        { label: 'Success', value: '99.9%', color: 'blue', icon: Activity },
                    ].map((stat, i) => (
                        <div key={i} className={`p-6 rounded-2xl border transition-all duration-300 hover:scale-[1.05] flex flex-col items-center justify-center gap-2 group ${status === 'alert' && i === 1 ? 'border-red-500 bg-red-500/5 pulse' : 'border-white/5 bg-white/2'
                            }`}>
                            <stat.icon size={20} className="text-white/20 group-hover:text-white transition-colors" />
                            <span className="text-[10px] text-white/40 uppercase font-mono">{stat.label}</span>
                            <span className={`text-2xl font-black font-mono transition-all ${status === 'alert' && i === 1 ? 'text-red-500 animate-bounce' : 'text-white'
                                }`}>{stat.value}</span>
                        </div>
                    ))}
                </div>
            </section>

            {/* Interactive Simulation Console */}
            <section className="py-24 px-6 border-t border-white/5 bg-black/40">
                <div className="max-w-5xl mx-auto">
                    <div className="grid grid-cols-1 lg:grid-cols-3 gap-12">
                        <div className="lg:col-span-2 space-y-8">
                            <div className="flex items-center justify-between mb-4">
                                <h3 className="text-xl font-bold uppercase tracking-widest italic flex items-center gap-3">
                                    <Activity className="text-cyan-400" /> Advanced Simulation Room
                                </h3>
                                {status === 'idle' && (
                                    <button
                                        onClick={() => setStatus('scanning')}
                                        className="px-6 py-2 rounded-lg bg-cyan-500 text-black font-black text-xs uppercase hover:bg-cyan-400 transition-all shadow-[0_0_20px_rgba(34,211,238,0.3)]"
                                    >
                                        Start Scan
                                    </button>
                                )}
                            </div>

                            <div className="rounded-2xl border border-white/10 bg-[#0c0c0c] overflow-hidden shadow-2xl transition-all duration-700">
                                <div className="px-4 py-3 bg-white/5 border-b border-white/5 flex items-center justify-between">
                                    <div className="flex gap-1.5">
                                        <div className="h-2 w-12 bg-white/20 rounded-full" />
                                    </div>
                                    <div className="text-[10px] font-mono text-white/20 uppercase tracking-widest animate-pulse">
                                        {status === 'scanning' ? 'Scanning Feed...' : 'Monitoring...'}
                                    </div>
                                </div>

                                <div className="p-8 font-mono text-[13px] space-y-4 min-h-[300px] overflow-hidden text-left">
                                    {status === 'idle' && (
                                        <div className="text-white/20 text-center py-20 italic">Press "Start Scan" to trigger AI reasoning simulation...</div>
                                    )}
                                    {status !== 'idle' && (
                                        <div className="space-y-4 animate-in fade-in slide-in-from-bottom-4 duration-500">
                                            <div className="flex gap-4"><span className="text-cyan-500">→</span> Analyzing transaction pool #220...</div>
                                            {(progress > 20 || status === 'alert') && <div className="flex gap-4"><span className="text-cyan-500">→</span> High volume detected in <span className="text-cyan-400">GOTO.JK</span></div>}
                                            {(progress > 50 || status === 'alert') && <div className="flex gap-4"><span className="text-cyan-500">→</span> Cross-referencing news sentiment (IDX-News)</div>}
                                            {(progress > 80 || status === 'alert') && <div className="flex gap-4"><span className="text-cyan-500">→</span> RAG Retrieval: <span className="text-violet-400 italic">POJK 31 Security Laws...</span></div>}
                                            {status === 'alert' && (
                                                <div className="mt-8 p-6 bg-red-500/10 border border-red-500/30 rounded-xl space-y-4 animate-in zoom-in duration-300">
                                                    <div className="flex items-center gap-3 text-red-500 font-black uppercase text-xs">
                                                        <AlertTriangle size={18} /> High Risk indicator detected
                                                    </div>
                                                    <p className="text-white/60 italic text-xs leading-relaxed">
                                                        "Potensi Insider Trading terdeteksi. Akun X melakukan akumulasi 2 jam sebelum pengumuman merger.
                                                        Probabilitas korelasi: 94.2%. Segera kirim notifikasi ke tim audit."
                                                    </p>
                                                    <button
                                                        onClick={() => setStatus('crash')}
                                                        className="w-full py-2 bg-red-500 text-white font-black text-[10px] uppercase rounded hover:bg-red-400 transition-colors"
                                                    >
                                                        Confirm & Lock Account
                                                    </button>
                                                </div>
                                            )}
                                        </div>
                                    )}
                                </div>
                            </div>
                        </div>

                        <div className="space-y-6">
                            <div className="p-8 rounded-2xl bg-white/5 border border-white/10 space-y-6">
                                <h4 className="text-sm font-black uppercase tracking-widest text-white/40">Visual Parameters</h4>
                                <div className="space-y-6">
                                    {[
                                        { l: 'Heat Intensity', v: '92%' },
                                        { l: 'Network Flux', v: '44ms' },
                                        { l: 'Reasoning Depth', v: '9.4' }
                                    ].map((p, i) => (
                                        <div key={i} className="space-y-2 group">
                                            <div className="flex justify-between text-[10px] font-mono uppercase">
                                                <span>{p.l}</span>
                                                <span className="text-cyan-400">{p.v}</span>
                                            </div>
                                            <div className="h-1 w-full bg-white/10 rounded-full overflow-hidden">
                                                <div
                                                    className={`h-full bg-cyan-500 transition-all duration-1000 ${status === 'scanning' ? 'animate-[progress_2s_infinite]' : ''}`}
                                                    style={{ width: status === 'alert' ? '100%' : '60%' }}
                                                />
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </div>

                            <div className="p-6 rounded-2xl bg-cyan-500/5 border border-cyan-500/20 text-center space-y-4">
                                <RefreshCcw className={`mx-auto text-cyan-400 ${status === 'scanning' ? 'animate-spin' : ''}`} />
                                <p className="text-[10px] text-white/60 uppercase font-bold tracking-tighter">Real-time Stream active</p>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            {/* Footer with Reset */}
            <footer className="py-20 px-6 border-t border-white/5 text-center">
                <div className="max-w-xl mx-auto space-y-8">
                    <p className="text-xs text-white/20 uppercase tracking-widest italic">Experience the resilience of SENTINEL AI</p>
                    <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
                        <Link href="/" className="px-10 py-4 rounded-xl bg-white text-black font-black text-xs uppercase hover:bg-cyan-400 transition-all">
                            Exit Simulation
                        </Link>
                        {status !== 'idle' && (
                            <button
                                onClick={() => { setStatus('idle'); setProgress(0); }}
                                className="px-10 py-4 rounded-xl bg-white/5 border border-white/10 font-black text-xs uppercase text-white hover:bg-white/10 transition-all"
                            >
                                Reset Terminal
                            </button>
                        )}
                    </div>
                </div>
            </footer>

            <style jsx global>{`
                @keyframes loading {
                    0% { transform: translateX(-100%); }
                    100% { transform: translateX(100%); }
                }
                @keyframes progress {
                    0% { width: 0%; }
                    50% { width: 100%; }
                    100% { width: 0%; }
                }
                .pulse {
                    animation: pulse-red 2s infinite;
                }
                @keyframes pulse-red {
                    0% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.4); }
                    70% { box-shadow: 0 0 0 15px rgba(239, 68, 68, 0); }
                    100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }
                }
            `}</style>
        </div>
    );
}
