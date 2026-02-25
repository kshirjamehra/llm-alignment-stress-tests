import React from 'react';

interface MetricCardProps {
    title: string;
    value: string | number;
    icon?: React.ReactNode;
    trend?: string;
    trendColor?: string;
    color?: string;
}

export default function MetricCard({ title, value, icon, trend, trendColor, color = 'bg-gray-800' }: MetricCardProps) {
    return (
        <div className={`${color} border border-gray-700/50 p-6 rounded-xl shadow-lg hover:shadow-cyan-500/10 transition-all duration-300 backdrop-blur-sm bg-opacity-80`}>
            <div className="flex justify-between items-start">
                <div>
                    <h3 className="text-slate-500 text-xs uppercase tracking-widest font-semibold mb-1">{title}</h3>
                    <div className="text-3xl font-bold text-slate-800 tracking-tight">{value}</div>
                </div>
                {icon && <div className="p-3 bg-white/40 rounded-lg border border-pink-100">{icon}</div>}
            </div>
            {trend && (
                <div className={`mt-4 text-xs font-medium flex items-center gap-1 ${trendColor || 'text-green-400'}`}>
                    {trend}
                </div>
            )}
        </div>
    );
}
