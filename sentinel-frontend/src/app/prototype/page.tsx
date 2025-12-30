"use client";

import React from 'react';
import Link from 'next/link';
import Image from 'next/image';
import { ArrowLeft, Zap, BarChart3, Shield, Database, Layout, Sparkles } from 'lucide-react';

export default function PrototypePage() {
    return (
        <div className="min-h-screen bg-[#0a0a0a] text-white font-sans selection:bg-cyan-500/30">
            {/* Navigation */}
            <nav className="border-b border-white/5 bg-black/50 backdrop-blur-xl sticky top-0 z-50">
                <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
                    <div className="flex items-center gap-4">
                        <Link href="/" className="hover:text-cyan-400 transition-colors flex items-center gap-2 text-sm font-medium">
                            <ArrowLeft size={16} /> Back to Dashboard
                        </Link>
                        <div className="h-4 w-[1px] bg-white/10" />
                        <span className="text-white/40 text-sm font-mono tracking-tighter uppercase italic">SENTINEL v2.0 Prototype</span>
                    </div>
                    <div className="flex items-center gap-2">
                        <div className="h-2 w-2 rounded-full bg-cyan-500 animate-pulse" />
                        <span className="text-[10px] font-bold text-cyan-500 uppercase tracking-widest">Visionary Mode Active</span>
                    </div>
                </div>
            </nav>

            {/* Hero Section */}
            <section className="relative pt-20 pb-32 px-6 overflow-hidden">
                <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[1000px] h-[600px] bg-cyan-500/10 blur-[120px] rounded-full -z-10" />

                <div className="max-w-5xl mx-auto text-center">
                    <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-cyan-500/10 border border-cyan-500/20 text-cyan-400 text-xs font-bold uppercase tracking-wider mb-8">
                        <Sparkles size={14} /> Future Roadmap
                    </div>
                    <h1 className="text-6xl md:text-8xl font-bold tracking-tight mb-6 bg-gradient-to-b from-white to-white/40 bg-clip-text text-transparent">
                        Surveillance <br /> Redefined
                    </h1>
                    <p className="text-xl text-white/50 max-w-2xl mx-auto mb-12 leading-relaxed">
                        Welcome to the future of capital market compliance. SENTINEL v2.0 transitions from a core utility to an
                        <span className="text-white font-medium"> enterprise-grade intelligence platform</span>.
                    </p>
                </div>

                {/* Feature 1: Hero Dashboard */}
                <div className="max-w-6xl mx-auto mt-12 group cursor-zoom-in">
                    <div className="relative rounded-2xl overflow-hidden border border-white/10 bg-white/5 shadow-2xl transition-all duration-700 group-hover:border-cyan-500/30 group-hover:scale-[1.01]">
                        <img
                            src="/images/v2_hero.png"
                            alt="v2.0 Dashboard Hero"
                            className="w-full h-auto object-cover opacity-90 group-hover:opacity-100 transition-opacity"
                        />
                        <div className="absolute inset-0 bg-gradient-to-t from-black to-transparent opacity-40" />
                        <div className="absolute bottom-8 left-8 right-8">
                            <div className="flex flex-col md:flex-row md:items-end justify-between gap-6">
                                <div>
                                    <h3 className="text-2xl font-bold mb-2">Next-Gen Interface</h3>
                                    <p className="text-white/60 text-sm max-w-md">Glassmorphism design language with dynamic 3D visualizations and real-time risk pulse monitors.</p>
                                </div>
                                <div className="flex gap-4">
                                    <div className="px-4 py-2 rounded-lg bg-black/60 backdrop-blur-md border border-white/10 text-xs font-mono uppercase tracking-widest text-white/40">
                                        High-Fidelity Preview
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            {/* Split Features */}
            <section className="py-24 px-6 border-t border-white/5 bg-[#080808]">
                <div className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-12">

                    {/* Advanced Analytics */}
                    <div className="space-y-8">
                        <div className="space-y-4">
                            <div className="h-12 w-12 rounded-xl bg-violet-500/10 border border-violet-500/20 flex items-center justify-center text-violet-400">
                                <BarChart3 size={24} />
                            </div>
                            <h2 className="text-3xl font-bold italic tracking-tight">Quant-Grade <br /> Analytics Dashboard</h2>
                            <p className="text-white/50 leading-relaxed">
                                Melihat pola yang tidak terlihat. v2.0 memperkenalkan visualisasi jaringan (network graphs)
                                dan heatmap anomali pasar untuk deteksi insider trading yang lebih presisi.
                            </p>
                            <ul className="space-y-3 pt-4">
                                {['Temporal Anomaly Heatmaps', 'Entity Connectivity Graphs', 'Regulatory Radar Charts'].map((item) => (
                                    <li key={item} className="flex items-center gap-3 text-sm text-white/70">
                                        <div className="h-1 w-1 rounded-full bg-violet-400" /> {item}
                                    </li>
                                ))}
                            </ul>
                        </div>

                        <div className="relative rounded-xl overflow-hidden border border-white/10 bg-white/5 shadow-xl transition-all hover:border-violet-500/30">
                            <img
                                src="/images/v2_analytics.png"
                                alt="Advanced Analytics View"
                                className="w-full h-auto h-full object-cover"
                            />
                        </div>
                    </div>

                    {/* Batch Analysis */}
                    <div className="space-y-8">
                        <div className="space-y-4">
                            <div className="h-12 w-12 rounded-xl bg-cyan-500/10 border border-cyan-500/20 flex items-center justify-center text-cyan-400">
                                <Database size={24} />
                            </div>
                            <h2 className="text-3xl font-bold italic tracking-tight">Massive Batch <br /> Processing Engine</h2>
                            <p className="text-white/50 leading-relaxed">
                                Dari analisa per-transaksi menuju pemrosesan ribuan data sekaligus. v2.0 dioptimasi untuk
                                menangani feed transaksi harian bursa dengan integrasi DVC & MLflow.
                            </p>
                            <ul className="space-y-3 pt-4">
                                {['1,000+ Transactions/Sec', 'Auto-Flagging Logic', 'MLOps Performance Tracking'].map((item) => (
                                    <li key={item} className="flex items-center gap-3 text-sm text-white/70">
                                        <div className="h-1 w-1 rounded-full bg-cyan-400" /> {item}
                                    </li>
                                ))}
                            </ul>
                        </div>

                        <div className="relative rounded-xl overflow-hidden border border-white/10 bg-white/5 shadow-xl transition-all hover:border-cyan-500/30">
                            <img
                                src="/images/v1_preview.png"
                                alt="Batch Preview"
                                className="w-full h-auto opacity-80"
                            />
                            <div className="absolute inset-0 flex items-center justify-center">
                                <div className="px-6 py-3 rounded-full bg-black/80 backdrop-blur-xl border border-white/10 text-sm font-bold tracking-widest uppercase">
                                    V1 Foundation Status: Active
                                </div>
                            </div>
                        </div>
                    </div>

                </div>
            </section>

            {/* NEW: Interactive Audit Simulation */}
            <section className="py-24 px-6 border-t border-white/5">
                <div className="max-w-5xl mx-auto space-y-16">
                    <div className="text-center space-y-4">
                        <h2 className="text-4xl font-bold tracking-tight italic uppercase">Live "Agentic" Audit Flow</h2>
                        <p className="text-white/40 max-w-xl mx-auto">Lihat bagaimana AI memproses transaksi mencurigakan secara otomatis (Simulasi v2.0).</p>
                    </div>

                    <div className="rounded-2xl border border-white/10 bg-[#0c0c0c] overflow-hidden shadow-2xl transition-transform hover:scale-[1.01] duration-500">
                        {/* Terminal Header */}
                        <div className="px-4 py-3 bg-white/5 border-b border-white/5 flex items-center justify-between">
                            <div className="flex gap-1.5">
                                <div className="h-2.5 w-2.5 rounded-full bg-red-500/50" />
                                <div className="h-2.5 w-2.5 rounded-full bg-amber-500/50" />
                                <div className="h-2.5 w-2.5 rounded-full bg-green-500/50" />
                            </div>
                            <div className="text-[10px] font-mono text-white/20 uppercase tracking-widest">Sentinel.sh — Agent Instance #0442</div>
                        </div>

                        {/* Terminal Content */}
                        <div className="p-8 font-mono text-sm space-y-4 overflow-x-auto text-left">
                            <div className="flex gap-4">
                                <span className="text-cyan-500 font-bold">→</span>
                                <span className="text-white/40">Injesting real-time feed from IDX API...</span>
                            </div>
                            <div className="flex gap-4">
                                <span className="text-cyan-500 font-bold">→</span>
                                <span className="text-white/80">Anomaly Detected: <span className="text-red-400 font-bold">STOCK_XYZ</span> (Vol spike 4.5x std_dev)</span>
                            </div>
                            <div className="flex gap-4 pl-8 border-l border-white/10">
                                <span className="text-white/40 italic">Searching regulatory database (RAG)...</span>
                            </div>
                            <div className="flex gap-4 pl-8 border-l border-white/10">
                                <span className="text-white/40 font-bold">Found Reference:</span> <span className="text-cyan-400 underline underline-offset-4 decoration-cyan-400/30 font-bold">POJK 31/04/2015 Artikel 2</span>
                            </div>
                            <div className="flex gap-4 pt-4">
                                <span className="text-cyan-500 font-bold">→</span>
                                <span className="text-amber-400 font-bold tracking-tighter uppercase text-xs">[AI Reasoning Insight]</span>
                            </div>
                            <div className="mt-2 p-6 bg-white/[0.02] rounded-lg border border-white/5 italic text-white/50 text-xs leading-relaxed max-w-2xl">
                                "Transaksi ini menunjukkan pola 'front-running' yang berkorelasi dengan berita RUPS internal pukul 14:00 WIB.
                                Sesuai POJK 31, akun ini harus masuk ke daftar pantau investigasi level 1."
                            </div>
                            <div className="flex gap-4 pt-6">
                                <div className="h-2 w-2 rounded-full bg-green-400 animate-ping mt-1" />
                                <span className="text-green-400 font-bold">Action Taken: Alert generated and assigned to Investigator Herald.</span>
                            </div>
                        </div>
                    </div>
                </div>
            </section>
            <section className="py-24 px-6 border-t border-white/5 relative overflow-hidden">
                <div className="absolute top-1/2 left-0 -translate-y-1/2 w-96 h-96 bg-cyan-500/5 blur-[100px] rounded-full -z-10" />

                <div className="max-w-4xl mx-auto text-center space-y-12">
                    <div className="space-y-4">
                        <h2 className="text-4xl font-bold tracking-tighter italic uppercase">Powered by Modern Atoms</h2>
                        <p className="text-white/40">Menyatukan design dan code dalam satu ekosistem yang kohesif.</p>
                    </div>

                    <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
                        {[
                            { name: 'Builder.io', role: 'Visual CMS', icon: Sparkles },
                            { name: 'Next.js 14', role: 'Core Engine', icon: Layout },
                            { name: 'LangChain', role: 'AI Orchestration', icon: Zap },
                            { name: 'ChromaDB', role: 'Vector Search', icon: Shield },
                        ].map((tech) => (
                            <div key={tech.name} className="p-6 rounded-2xl bg-white/5 border border-white/10 flex flex-col items-center gap-4 group transition-all hover:bg-white/10">
                                <div className="h-10 w-10 text-white/20 transition-colors group-hover:text-cyan-400">
                                    <tech.icon size={40} />
                                </div>
                                <div>
                                    <h4 className="font-bold text-sm tracking-widest uppercase">{tech.name}</h4>
                                    <p className="text-[10px] text-white/30 uppercase mt-1">{tech.role}</p>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </section>

            {/* Footer CTA */}
            <footer className="py-20 px-6 border-t border-white/5 text-center">
                <div className="max-w-2xl mx-auto space-y-8">
                    <h2 className="text-3xl font-medium tracking-tight">Siap Membangun Masa Depan?</h2>
                    <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
                        <Link href="/" className="px-8 py-4 rounded-full bg-white text-black font-bold text-sm hover:bg-cyan-400 transition-colors">
                            Back to v1.0 Live
                        </Link>
                        <a href="https://github.com/loxleyftsck/Sentinel-project" className="px-8 py-4 rounded-full bg-white/5 border border-white/10 font-bold text-sm hover:bg-white/10 transition-colors">
                            Contribute on GitHub
                        </a>
                    </div>
                    <p className="text-xs text-white/20 pt-12">
                        © 2025 SENTINEL AI Compliance Research. All rights reserved. <br />
                        Developed by Herald Michain Samuel Theo Ginting
                    </p>
                </div>
            </footer>
        </div>
    );
}
