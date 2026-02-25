import FailureLog from '@/components/FailureLog';
import { getDataset, TestCase } from '@/lib/data';

export default async function ReasoningPage() {
    const report = await getDataset();
    const dataset: TestCase[] = report?.results || [];

    const reasoningCategories = [
        'Algorithmic Counting',
        'Negation & Constraint',
        'Timezone & Relativity',
        'Causal Chain Breakdown',
        'State-Tracking'
    ];

    // Exact or substring match to cover variations
    const data = dataset.filter(t =>
        reasoningCategories.some(c => t.category.includes(c))
    );
    const failures = data.filter(t => !t.passed);

    return (
        <div className="animate-in fade-in duration-700">
            <header className="mb-8">
                <h1 className="text-3xl font-extrabold text-slate-800 tracking-tight">
                    Reasoning Diagnostics
                </h1>
                <p className="text-slate-500 mt-1 text-sm">Deep dive into spatial, temporal, and logic chain failures.</p>
            </header>

            <FailureLog failures={failures} title="Reasoning Vulnerability Log" />
        </div>
    );
}
