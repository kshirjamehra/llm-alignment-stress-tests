import fs from 'fs';
import path from 'path';
import Image from 'next/image';
import { Activity, Hash, AlertTriangle } from 'lucide-react';
import MetricCard from '@/components/MetricCard';
import ChartSection from '@/components/ChartSection';

interface TestCase {
  test_id: string;
  category: string;
  prompt: string;
  passed: boolean;
  actual_answer: string;
  expected_answer: string;
}

async function getDataset() {
  try {
    const filePath = path.join(process.cwd(), '../reports/latest_evaluation_run.json');
    const fileContents = fs.readFileSync(filePath, 'utf8');
    return JSON.parse(fileContents);
  } catch (e) {
    console.error("Failed to load dataset", e);
    return null;
  }
}

export default async function Home() {
  const report = await getDataset();
  const dataset = report?.results || [];

  return (
    <div className="animate-in fade-in duration-700">
      {/* Header */}
      <div className="relative w-full h-48 rounded-2xl overflow-hidden mb-8 shadow-[0_4px_20px_-4px_rgba(236,72,153,0.3)] border border-pink-100/50">
        <Image src="/hero-banner.png" alt="Hero Banner" fill className="object-cover" priority />
        <div className="absolute inset-0 bg-gradient-to-r from-pink-500/80 to-transparent flex flex-col justify-center p-8">
          <h1 className="text-4xl font-extrabold text-white tracking-tight drop-shadow-md">
            Overview Dashboard
          </h1>
          <p className="text-pink-50 mt-2 text-sm max-w-md font-medium drop-shadow">Real-time metrics from the latest LLM stress test injection.</p>
        </div>
      </div>

      {/* Hero Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <MetricCard
          title="Overall Pass Rate"
          value={report?.metadata?.overall_pass_rate ? `${report.metadata.overall_pass_rate}%` : "0%"}
          trend="Live"
          trendColor="text-emerald-500"
          icon={<Activity className="text-emerald-600 w-6 h-6" />}
          color="glass-panel"
        />
        <MetricCard
          title="Total Tokens Processed"
          value={(dataset.length * 142).toLocaleString()}
          trend="Estimated"
          trendColor="text-pink-500"
          icon={<Hash className="text-pink-600 w-6 h-6" />}
          color="glass-panel"
        />
        <MetricCard
          title="Critical Failure Count"
          value={dataset.filter((t: TestCase) => !t.passed).length}
          trend="Needs Review"
          trendColor="text-rose-500"
          icon={<AlertTriangle className="text-rose-600 w-6 h-6" />}
          color="glass-panel"
        />
      </div>

      {/* Charts Section */}
      <ChartSection data={dataset} />

      {/* Dataset Preview */}
      <div className="glass-panel overflow-hidden">
        <div className="p-6 border-b border-white/40">
          <h3 className="text-lg font-bold text-slate-800">Latest Edge Case Failures</h3>
        </div>
        <div className="p-6 grid gap-6 max-h-[600px] overflow-y-auto">
          {dataset.filter((test: TestCase) => !test.passed).slice(0, 5).map((test: TestCase) => (
            <div key={test.test_id} className="bg-white/40 border border-white/60 rounded-xl p-5 shadow-sm hover:shadow-md transition-shadow">
              <div className="flex justify-between items-center mb-3">
                <span className="px-3 py-1 bg-rose-100 text-rose-600 text-xs font-bold rounded-full border border-rose-200">
                  {test.category}
                </span>
                <span className="text-xs text-slate-400 font-mono">{test.test_id.split('-')[0]}</span>
              </div>
              <p className="text-sm text-slate-700 mb-4">{test.prompt}</p>

              <div className="grid grid-cols-2 gap-4">
                <div className="bg-rose-50/50 p-3 rounded-lg border border-rose-100 text-xs text-slate-600 font-mono">
                  <strong className="text-rose-500 block mb-1">Actual (Failed):</strong>
                  {String(test.actual_answer).substring(0, 100)}...
                </div>
                <div className="bg-emerald-50/50 p-3 rounded-lg border border-emerald-100 text-xs text-slate-600 font-mono">
                  <strong className="text-emerald-600 block mb-1">Expected Rule:</strong>
                  {String(test.expected_answer).substring(0, 100)}...
                </div>
              </div>
            </div>
          ))}
          {dataset.filter((test: TestCase) => !test.passed).length === 0 && (
            <div className="text-center py-12 flex flex-col items-center">
              <Image src="/empty-states/shape1.png" alt="All Clear" width={160} height={160} className="mb-4 drop-shadow-md hover:scale-105 transition-transform duration-500" />
              <div className="text-slate-500 font-medium">No critical failures detected in this reporting batch.</div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
