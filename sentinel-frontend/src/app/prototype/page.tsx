"use client";

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import Image from 'next/image';
import { ArrowLeft, Zap, BarChart3, Shield, Database, Layout, Sparkles, AlertTriangle, RefreshCcw, Activity } from 'lucide-react';

export default function PrototypePage() {
    const [status, setStatus] = useState<'idle' | 'scanning' | 'alert' | 'crash' | 'recovering'>('idle');
    const [progress, setProgress] = useState(0);
    const [priceData, setPriceData] = useState<{ x: number, y: number, anomalous?: boolean }[]>([]);
    const [orderBook, setOrderBook] = useState<{ price: number, size: number, type: 'buy' | 'sell' }[]>([]);

    // Order Book Generator
    useEffect(() => {
        const generateOrders = () => {
            const base = 150.42;
            const orders: { price: number, size: number, type: 'buy' | 'sell' }[] = [];
            for (let i = 0; i < 12; i++) {
                orders.push({ price: base + (i + 1) * 0.05, size: Math.floor(Math.random() * 5000), type: 'sell' });
                orders.push({ price: base - (i + 1) * 0.05, size: Math.floor(Math.random() * 5000), type: 'buy' });
            }
            return orders;
        };
        setOrderBook(generateOrders());

        const interval = setInterval(() => {
            setOrderBook(prev => prev.map(o => ({
                ...o,
                size: Math.max(10, o.size + (Math.random() - 0.5) * 500)
            })));
        }, 500);
        return () => clearInterval(interval);
    }, []);

    // Chart Data Generator
    useEffect(() => {
        const initialData = Array.from({ length: 40 }, (_, i) => ({
            x: i * 20,
            y: 150 + Math.sin(i / 5) * 40 + Math.random() * 20,
            anomalous: false
        }));
        setPriceData(initialData);

        const interval = setInterval(() => {
            setPriceData(prev => {
                const last = prev[prev.length - 1];
                const nextY = status === 'alert'
                    ? last.y + (Math.random() - 0.2) * 50 // Sharp spike
                    : last.y + (Math.random() - 0.5) * 10;

                const newData = [...prev.slice(1), {
                    x: last.x + 20,
                    y: Math.max(50, Math.min(250, nextY)),
                    anomalous: status === 'alert' && Math.random() > 0.7
                }];
                return newData;
            });
        }, 800);
        return () => clearInterval(interval);
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
                            <div className="h-full bg-red-500 animate-loading" />
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
                        <div key={i} className={`p-6 rounded-2xl border transition-all duration-300 hover:scale-[1.05] flex flex-col items-center justify-center gap-2 group ${status === 'alert' && i === 1 ? 'border-red-500 bg-red-500/5 animate-pulse-red' : 'border-white/5 bg-white/2'
                            }`}>
                            <stat.icon size={20} className="text-white/20 group-hover:text-white transition-colors" />
                            <span className="text-[10px] text-white/40 uppercase font-mono">{stat.label}</span>
                            <span className={`text-2xl font-black font-mono transition-all ${status === 'alert' && i === 1 ? 'text-red-500 animate-bounce' : 'text-white'
                                }`}>{stat.value}</span>
                        </div>
                    ))}
                </div>
            </section>

            {/* Bloomberg-Grade Terminal Section */}
            <section className="py-12 px-6 bg-[#050505] border-y border-white/5">
                <div className="max-w-7xl mx-auto space-y-8">
                    {/* Global Market Summary */}
                    <div className="grid grid-cols-2 md:grid-cols-5 gap-4 border-b border-white/5 pb-8">
                        {[
                            { l: 'IHSG', v: '7,234.20', c: '+0.12%', s: 'emerald' },
                            { l: 'USD/IDR', v: '15,440', c: '-0.05%', s: 'red' },
                            { l: 'BTC/USD', v: '98,240', c: '+4.55%', s: 'emerald' },
                            { l: 'COMPX', v: 'Lv. 92', c: 'STABLE', s: 'cyan' },
                            { l: 'NET_VALUE', v: '$42.2B', c: 'AUDITED', s: 'violet' }
                        ].map((m, i) => (
                            <div key={i} className="space-y-1">
                                <div className="text-[10px] text-white/20 font-mono uppercase tracking-widest">{m.l}</div>
                                <div className="flex items-center gap-2">
                                    <span className="text-sm font-black italic">{m.v}</span>
                                    <span className={`text-[9px] font-bold text-${m.s}-500/80`}>{m.c}</span>
                                </div>
                            </div>
                        ))}
                    </div>

                    <div className="flex items-center justify-between">
                        <div className="space-y-1">
                            <h2 className="text-2xl font-black italic tracking-tighter uppercase text-white flex items-center gap-2">
                                <Layout className="text-cyan-400" /> Market Terminal Pro
                            </h2>
                            <p className="text-[10px] text-white/30 font-mono uppercase tracking-[0.2em]">High-Frequency Monitoring Node #8821</p>
                        </div>
                        <div className="flex items-center gap-4 text-[10px] font-mono">
                            <div className="flex items-center gap-2 px-3 py-1 bg-white/5 border border-white/10 rounded-full">
                                <span className={`w-1.5 h-1.5 rounded-full ${status === 'alert' ? 'bg-red-500' : 'bg-emerald-500'} animate-pulse`} />
                                <span className={status === 'alert' ? 'text-red-500' : 'text-emerald-500'}>FEED: {status === 'alert' ? 'VOLATILE' : 'STABLE'}</span>
                            </div>
                            <div className="text-white/40">UTC: {new Date().toISOString().split('T')[1].split('.')[0]}</div>
                        </div>
                    </div>

                    <div className="grid grid-cols-1 lg:grid-cols-4 gap-4 h-[500px]">
                        {/* Order Book Sidepanel */}
                        <div className="bg-black border border-white/10 rounded-xl p-4 flex flex-col gap-4 overflow-hidden relative">
                            <div className="absolute inset-0 bg-linear-to-b from-cyan-500/5 to-transparent pointer-events-none" />
                            <div className="flex justify-between items-center border-b border-white/5 pb-2 relative z-10">
                                <span className="text-[10px] font-bold uppercase text-white/40">Order Book</span>
                                <span className="text-[10px] font-mono text-cyan-400">DEPTH: {Math.floor(progress + 200)}MB</span>
                            </div>
                            <div className="flex-1 space-y-1 font-mono text-[9px] relative z-10">
                                {/* Sells */}
                                {orderBook.filter(o => o.type === 'sell').reverse().map((o, i) => (
                                    <div key={`sell-${i}`} className="flex justify-between items-center group cursor-crosshair relative">
                                        <span className="text-red-500/80">{o.price.toFixed(2)}</span>
                                        <span className="text-white/40 font-mono">{Math.floor(o.size).toLocaleString()}</span>
                                        <div className="absolute right-0 h-full bg-red-500/5 transition-all group-hover:bg-red-500/20" style={{ width: `${(o.size / 5000) * 100}%` }} />
                                    </div>
                                ))}
                                <div className="py-2 border-y border-white/10 text-center bg-white/2 my-2">
                                    <span className={`text-xl font-black italic transition-colors ${status === 'alert' ? 'text-red-500' : 'text-white'} animate-pulse`}>
                                        {status === 'alert' ? '148.12' : '150.42'}
                                    </span>
                                </div>
                                {/* Buys */}
                                {orderBook.filter(o => o.type === 'buy').map((o, i) => (
                                    <div key={`buy-${i}`} className="flex justify-between items-center group cursor-crosshair relative">
                                        <span className="text-emerald-500/80">{o.price.toFixed(2)}</span>
                                        <span className="text-white/40 font-mono">{Math.floor(o.size).toLocaleString()}</span>
                                        <div className="absolute right-0 h-full bg-emerald-500/5 transition-all group-hover:bg-emerald-500/20" style={{ width: `${(o.size / 5000) * 100}%` }} />
                                    </div>
                                ))}
                            </div>
                        </div>

                        {/* Main SVG Price Chart */}
                        <div className="lg:col-span-3 bg-black border border-white/10 rounded-xl relative overflow-hidden group">
                            <div className="absolute top-4 left-6 z-10 space-y-1">
                                <div className="flex items-center gap-2">
                                    <span className="text-xl font-black italic tracking-tighter text-white">GOTO.JK</span>
                                    <span className={`text-xs font-bold ${status === 'alert' ? 'text-red-500' : 'text-emerald-500'}`}>
                                        {status === 'alert' ? '-12.42%' : '+4.22%'}
                                    </span>
                                </div>
                                <div className="text-[10px] text-white/40 font-mono uppercase tracking-widest">VOL: 1.2B | HIGH: 152.00 | LOW: 148.50</div>
                            </div>

                            <div className="absolute inset-0 flex items-center justify-center p-8">
                                <svg width="100%" height="100%" viewBox="0 0 1000 300" className="overflow-visible">
                                    {/* Grid Lines */}
                                    {Array.from({ length: 15 }).map((_, i) => (
                                        <line key={`v-${i}`} x1={i * (1000 / 14)} y1="0" x2={i * (1000 / 14)} y2="300" stroke="rgba(255,255,255,0.02)" strokeWidth="1" />
                                    ))}
                                    {Array.from({ length: 6 }).map((_, i) => (
                                        <line key={`h-${i}`} x1="0" y1={i * 60} x2="1000" y2={i * 60} stroke="rgba(255,255,255,0.02)" strokeWidth="1" />
                                    ))}

                                    {/* Price Path with Glow */}
                                    <path
                                        d={`M ${priceData.map((d, i) => `${i * (1000 / 39)},${d.y}`).join(' L ')}`}
                                        fill="none"
                                        stroke={status === 'alert' ? '#ef4444' : '#22d3ee'}
                                        strokeWidth="2"
                                        className="transition-all duration-500"
                                        style={{ filter: 'drop-shadow(0 0 8px currentColor)' }}
                                    />

                                    {/* Anomaly Indicators */}
                                    {priceData.map((d, i) => d.anomalous && (
                                        <g key={i} className="animate-in zoom-in duration-300">
                                            <circle cx={i * (1000 / 39)} cy={d.y} r="8" fill="rgba(239, 68, 68, 0.2)" className="animate-pulse" />
                                            <circle cx={i * (1000 / 39)} cy={d.y} r="4" fill="#ef4444" />
                                            <line x1={i * (1000 / 39)} y1={d.y} x2={i * (1000 / 39)} y2="0" stroke="#ef4444" strokeWidth="1" strokeDasharray="4 4" opacity="0.5" />
                                            <text x={i * (1000 / 39)} y="15" fontSize="10" fill="#ef4444" className="font-mono font-bold" textAnchor="middle">ANOMALY DETECTED</text>
                                        </g>
                                    ))}
                                </svg>
                            </div>

                            {/* Ticker Tape Overlay */}
                            <div className="absolute bottom-0 inset-x-0 h-10 bg-black/80 border-t border-white/5 backdrop-blur-md flex items-center overflow-hidden">
                                <div className="flex gap-12 animate-ticker px-6 items-center">
                                    {[
                                        'IDX:BBCA +0.5%', 'IDX:TLKM -1.2%', 'IDX:BMRI +2.1%', 'IDX:ASII -0.8%',
                                        'SENTINEL: SCANNED 4402 TRANSACTIONS IN 0.2s', 'RISK: LOW', 'IDX:GOTO +4.2%',
                                        'IDX:BBCA +0.5%', 'IDX:TLKM -1.2%', 'IDX:BMRI +2.1%', 'IDX:ASII -0.8%',
                                        'SENTINEL: SCANNED 4402 TRANSACTIONS IN 0.2s', 'RISK: LOW', 'IDX:GOTO +4.2%'
                                    ].map((txt, i) => (
                                        <span key={i} className="text-[9px] font-mono text-white/60 flex items-center gap-2 whitespace-nowrap">
                                            <div className={`w-1 h-1 rounded-full ${txt.includes('+') ? 'bg-emerald-500' : 'bg-red-500'}`} />
                                            {txt}
                                        </span>
                                    ))}
                                </div>
                            </div>
                        </div>
                    </div>
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
                                                    className={`h-full bg-cyan-500 transition-all duration-1000 ${status === 'scanning' ? 'animate-progress-infinite' : ''}`}
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
        </div>
    );
}
