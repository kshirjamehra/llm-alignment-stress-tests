import FailureLog from '@/components/FailureLog';
import { getDataset, TestCase } from '@/lib/data';

export default async function HallucinationPage() {
    const report = await getDataset();
    const dataset: TestCase[] = report?.results || [];

    // Filter for hallucination-related categories
    const data = dataset.filter(t =>
        t.category.toLowerCase().includes('hallucination') ||
        t.category.toLowerCase().includes('fabrication') ||
        t.category.toLowerCase().includes('factuality')
    );
    const failures = data.filter(t => !t.passed);

    return (
        <div className="animate-in fade-in duration-700">
            <header className="mb-8">
                <h1 className="text-3xl font-extrabold text-slate-800 tracking-tight">
                    Hallucination Tracker
                </h1>
                <p className="text-slate-500 mt-1 text-sm">Monitor model fabrication and source deterioration.</p>
            </header>

            <FailureLog failures={failures} title="Fabrication Incident Log" />
        </div>
    );
}
