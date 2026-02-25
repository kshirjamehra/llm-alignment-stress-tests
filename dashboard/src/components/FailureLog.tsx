import React from 'react';

interface TestCase {
    test_id: string;
    category: string;
    prompt: string;
    passed: boolean;
    actual_answer: string;
    expected_answer: string;
}

interface FailureLogProps {
    failures: TestCase[];
    title?: string;
}

export default function FailureLog({ failures, title = "Failure Logs" }: FailureLogProps) {
    return (
        <div className="glass-panel overflow-hidden">
            <div className="p-6 border-b border-white/40 flex justify-between items-center">
                <h3 className="text-lg font-bold text-slate-800">{title}</h3>
                <span className="px-3 py-1 bg-pink-100/50 text-pink-600 text-xs font-bold rounded-full border border-pink-200/50">
                    {failures.length} Issues
                </span>
            </div>
            <div className="p-6 grid gap-6">
                {failures.map((test) => (
                    <div key={test.test_id} className="bg-white/40 border border-white/60 rounded-xl p-5 shadow-sm hover:shadow-md transition-shadow">
                        <div className="flex justify-between items-center mb-3">
                            <span className="px-3 py-1 bg-rose-100 text-rose-600 text-xs font-bold rounded-full border border-rose-200">
                                {test.category}
                            </span>
                            <span className="text-xs text-slate-400 font-mono">{test.test_id.split('-')[0]}</span>
                        </div>
                        <p className="text-sm text-slate-700 mb-4">{test.prompt}</p>

                        <div className="grid grid-cols-2 gap-4">
                            <div className="bg-rose-50/50 p-3 rounded-lg border border-rose-100 text-xs text-slate-600 font-mono whitespace-pre-wrap break-words">
                                <strong className="text-rose-500 block mb-1">Actual Output:</strong>
                                {String(test.actual_answer)}
                            </div>
                            <div className="bg-emerald-50/50 p-3 rounded-lg border border-emerald-100 text-xs text-slate-600 font-mono whitespace-pre-wrap break-words">
                                <strong className="text-emerald-600 block mb-1">Expected Constraint:</strong>
                                {String(test.expected_answer)}
                            </div>
                        </div>
                    </div>
                ))}
                {failures.length === 0 && (
                    <div className="text-center py-12 flex flex-col items-center">
                        <div className="text-slate-500 font-medium my-8">No failures detected in this category.</div>
                    </div>
                )}
            </div>
        </div>
    );
}
