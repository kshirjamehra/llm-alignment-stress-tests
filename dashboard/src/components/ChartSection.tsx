"use client";

import React, { useMemo } from 'react';
import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer, Tooltip } from 'recharts';

interface ChartSectionProps {
    data: { category?: string; passed?: boolean }[];
}

export default function ChartSection({ data }: ChartSectionProps) {
    // Aggregate performance by category for the radar chart
    const aggregatedData = useMemo(() => {
        if (!data || data.length === 0) return [];

        const stats: Record<string, { total: number, passed: number }> = {};

        data.forEach(test => {
            const cat = test.category || 'Unknown';
            if (!stats[cat]) {
                stats[cat] = { total: 0, passed: 0 };
            }
            stats[cat].total += 1;
            if (test.passed) {
                stats[cat].passed += 1;
            }
        });

        return Object.entries(stats).map(([category, counts]) => ({
            subject: category,
            score: counts.total > 0 ? Math.round((counts.passed / counts.total) * 100) : 0,
            fullMark: 100,
        }));
    }, [data]);

    return (
        <div className="glass-panel p-6 mb-8 relative overflow-hidden">
            {/* Decorative gradient orb for glassmorphism effect */}
            <div className="absolute -top-24 -right-24 w-64 h-64 bg-pink-400/20 rounded-full blur-3xl pointer-events-none" />

            <div className="flex justify-between items-center mb-6">
                <div>
                    <h3 className="text-xl font-bold text-slate-800">Vulnerability Radar</h3>
                    <p className="text-sm text-slate-500 mt-1">LLM performance distributed across logical alignment axes.</p>
                </div>
            </div>

            <div className="h-[400px] w-full relative z-10">
                {aggregatedData.length > 0 ? (
                    <ResponsiveContainer width="100%" height="100%">
                        <RadarChart cx="50%" cy="50%" outerRadius="70%" data={aggregatedData}>
                            <PolarGrid stroke="#fbcfe8" />
                            <PolarAngleAxis dataKey="subject" tick={{ fill: '#64748b', fontSize: 12, fontWeight: 600 }} />
                            <PolarRadiusAxis angle={30} domain={[0, 100]} tick={{ fill: '#94a3b8' }} />
                            <Radar
                                name="Pass Rate (%)"
                                dataKey="score"
                                stroke="#ec4899"
                                strokeWidth={3}
                                fill="#f472b6"
                                fillOpacity={0.4}
                                activeDot={{ r: 6, fill: '#db2777', stroke: '#fff', strokeWidth: 2 }}
                            />
                            <Tooltip
                                contentStyle={{
                                    backgroundColor: 'rgba(255, 255, 255, 0.9)',
                                    borderColor: '#fbcfe8',
                                    borderRadius: '12px',
                                    boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
                                    color: '#334155'
                                }}
                                itemStyle={{ color: '#db2777', fontWeight: 'bold' }}
                            />
                        </RadarChart>
                    </ResponsiveContainer>
                ) : (
                    <div className="flex items-center justify-center h-full">
                        <span className="text-slate-400 font-medium">Insufficient data for radar visualization.</span>
                    </div>
                )}
            </div>
        </div>
    );
}
