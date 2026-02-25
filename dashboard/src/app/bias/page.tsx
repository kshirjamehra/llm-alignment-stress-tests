import FailureLog from '@/components/FailureLog';
import { getDataset, TestCase } from '@/lib/data';

export default async function BiasPage() {
    const report = await getDataset();
    const dataset: TestCase[] = report?.results || [];

    // Filter for bias and refusal-related categories
    const data = dataset.filter(t =>
        t.category.toLowerCase().includes('bias') ||
        t.category.toLowerCase().includes('refusal') ||
        t.category.toLowerCase().includes('safety')
    );
    const failures = data.filter(t => !t.passed);

    return (
        <div className="animate-in fade-in duration-700">
            <header className="mb-8">
                <h1 className="text-3xl font-extrabold text-slate-800 tracking-tight">
                    Bias & Refusal Metrics
                </h1>
                <p className="text-slate-500 mt-1 text-sm">Analyze over-cautious refusals and systemic bias injections.</p>
            </header>

            <FailureLog failures={failures} title="Refusal & Bias Detection Log" />
        </div>
    );
}
