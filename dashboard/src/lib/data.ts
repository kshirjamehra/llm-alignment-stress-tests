import React from 'react';
import fs from 'fs';
import path from 'path';

export interface TestCase {
    test_id: string;
    category: string;
    prompt: string;
    passed: boolean;
    actual_answer: string;
    expected_answer: string;
}

export async function getDataset(): Promise<{ results: TestCase[], [key: string]: any } | null> {
    try {
        const filePath = path.join(process.cwd(), '../reports/latest_evaluation_run.json');
        const fileContents = fs.readFileSync(filePath, 'utf8');
        return JSON.parse(fileContents);
    } catch (e) {
        console.error("Failed to load dataset", e);
        return null;
    }
}
