"use client";

import Image from "next/image";
import Link from "next/link";
import { Shield, Sparkles, ArrowRight, BarChart3, Lock } from "lucide-react";

export default function Home() {
  return (
    <div className="flex min-h-screen flex-col bg-[#050505] text-white font-sans selection:bg-cyan-500/30">
      {/* Background Glow */}
      <div className="fixed top-0 left-1/2 -translate-x-1/2 w-full h-full max-w-6xl -z-10 bg-cyan-500/5 blur-[120px] rounded-full pointer-events-none" />

      <header className="px-8 py-6 flex items-center justify-between border-b border-white/5 backdrop-blur-md sticky top-0 z-50">
        <div className="flex items-center gap-2">
          <Shield className="text-cyan-400" size={24} />
          <span className="font-bold tracking-tighter text-xl uppercase italic">Sentinel</span>
        </div>
        <div className="flex items-center gap-4">
          <span className="text-[10px] font-mono text-white/40 uppercase tracking-widest border border-white/10 px-2 py-1 rounded">v1.0 Stable</span>
        </div>
      </header>

      <main className="flex-1 flex flex-col items-center justify-center px-6 py-20 text-center max-w-5xl mx-auto">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-cyan-500/10 border border-cyan-500/20 text-cyan-400 text-xs font-bold uppercase tracking-widest mb-8 animate-in fade-in slide-in-from-bottom-4 duration-1000">
          <Lock size={12} /> Secure Trading Intelligence
        </div>

        <h1 className="text-5xl md:text-7xl font-bold tracking-tight mb-8 bg-gradient-to-b from-white to-white/40 bg-clip-text text-transparent italic">
          Protecting The <br /> Future of IDX
        </h1>

        <p className="text-lg text-white/50 max-w-2xl mb-12 leading-relaxed">
          SENTINEL menggunakan RAG (Retrieval-Augmented Generation) berbasis
          POJK untuk mendeteksi indikasi insider trading secara real-time.
        </p>

        <div className="flex flex-col sm:flex-row gap-6">
          <Link href="/prototype" className="group relative px-8 py-4 rounded-xl bg-cyan-500 text-black font-bold flex items-center gap-2 hover:bg-cyan-400 transition-all hover:scale-105">
            <Sparkles size={18} />
            Run v2.0 Prototype
            <ArrowRight size={18} className="transition-transform group-hover:translate-x-1" />
          </Link>

          <a href="/docs/RESEARCH_REFERENCES.md" className="px-8 py-4 rounded-xl bg-white/5 border border-white/10 font-bold flex items-center gap-2 hover:bg-white/10 transition-colors">
            <BarChart3 size={18} />
            View Research
          </a>
        </div>

        {/* Preview Grid */}
        <div className="mt-24 grid grid-cols-1 md:grid-cols-3 gap-8 text-left w-full">
          {[
            { title: 'POJK Compliance', desc: 'Analisa otomatis berdasarkan regulasi OJK terbaru.', icon: Shield },
            { title: 'AI Reasoning', desc: 'Menggunakan Llama 3.1 untuk interpretasi narasi transaksi.', icon: Sparkles },
            { title: 'Quant Metrics', desc: 'Skoring resiko berdasarkan volume dan anomali harga.', icon: BarChart3 }
          ].map((item, i) => (
            <div key={i} className="p-8 rounded-2xl bg-white/[0.02] border border-white/5 hover:border-white/10 transition-colors">
              <item.icon className="text-cyan-400 mb-4" size={24} />
              <h3 className="font-bold text-lg mb-2">{item.title}</h3>
              <p className="text-sm text-white/40 leading-relaxed">{item.desc}</p>
            </div>
          ))}
        </div>
      </main>

      <footer className="py-12 border-t border-white/5 px-8 flex flex-col md:flex-row items-center justify-between gap-6">
        <p className="text-xs text-white/30 tracking-tight uppercase">
          © 2025 SENTINEL AI RESEARCH • SECURED DATA PIPELINE
        </p>
        <div className="flex gap-8">
          <a href="https://github.com/loxleyftsck" className="text-xs text-white/30 hover:text-white uppercase font-bold tracking-widest transition-colors">GitHub</a>
          <a href="#" className="text-xs text-white/30 hover:text-white uppercase font-bold tracking-widest transition-colors">Documentation</a>
        </div>
      </footer>
    </div>
  );
}
