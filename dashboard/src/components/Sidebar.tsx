"use client";

import { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
    LayoutDashboard,
    BrainCircuit,
    Ghost,
    Scale,
    Menu,
    ChevronLeft
} from "lucide-react";

const NAV_ITEMS = [
    { name: "Overview", path: "/", icon: LayoutDashboard },
    { name: "Reasoning", path: "/reasoning", icon: BrainCircuit },
    { name: "Hallucinations", path: "/hallucinations", icon: Ghost },
    { name: "Bias", path: "/bias", icon: Scale },
];

export default function Sidebar() {
    const [isCollapsed, setIsCollapsed] = useState(false);
    const pathname = usePathname();

    return (
        <aside
            className={`relative flex flex-col glass-panel m-4 transition-all duration-300 z-50 ${isCollapsed ? "w-20" : "w-64"}`}
        >
            <div className="p-4 flex items-center justify-between border-b border-pink-200/50">
                {!isCollapsed && (
                    <div className="font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-pink-500 to-rose-400">
                        STRESS<span className="text-slate-800">Op</span>
                    </div>
                )}
                <button
                    onClick={() => setIsCollapsed(!isCollapsed)}
                    className="p-1.5 rounded-lg hover:bg-pink-100/50 text-slate-500 transition-colors mx-auto"
                >
                    {isCollapsed ? <Menu size={20} /> : <ChevronLeft size={20} />}
                </button>
            </div>

            <nav className="flex-1 p-3 space-y-2 overflow-y-auto">
                {NAV_ITEMS.map((item) => {
                    const Icon = item.icon;
                    const isActive = pathname === item.path;

                    return (
                        <Link
                            key={item.path}
                            href={item.path}
                            className={`flex items-center gap-3 px-3 py-2.5 rounded-lg transition-all ${isActive
                                    ? "bg-pink-500/10 text-pink-600 font-semibold border border-pink-200"
                                    : "text-slate-600 hover:bg-white/40 hover:text-slate-900"
                                }`}
                        >
                            <Icon size={20} className={isActive ? "text-pink-500" : ""} />
                            {!isCollapsed && <span>{item.name}</span>}
                        </Link>
                    );
                })}
            </nav>

            <div className="p-4 border-t border-pink-200/50">
                <div className={`flex items-center gap-3 ${isCollapsed ? 'justify-center' : ''}`}>
                    <div className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse shadow-[0_0_8px_rgba(52,211,153,0.8)]" />
                    {!isCollapsed && <span className="text-xs font-mono text-slate-500">SYSTEM ONLINE</span>}
                </div>
            </div>
        </aside>
    );
}
