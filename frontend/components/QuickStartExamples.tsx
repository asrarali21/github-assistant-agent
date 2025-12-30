"use client";

import { motion } from "framer-motion";
import { ArrowRight } from "lucide-react";

interface QuickStartExamplesProps {
    onExampleClick: (example: string) => void;
}

const examples = [
    {
        text: "How many open PRs are in vercel/next.js?",
        category: "PR Stats",
    },
    {
        text: "Show me the stats for facebook/react",
        category: "Repository",
    },
    {
        text: "Who are the top contributors to kubernetes/kubernetes?",
        category: "Contributors",
    },
    {
        text: "What languages are used in microsoft/vscode?",
        category: "Languages",
    },
    {
        text: "What's the latest release of electron/electron?",
        category: "Releases",
    },
    {
        text: "Give me an overview of tensorflow/tensorflow",
        category: "Overview",
    },
];

export function QuickStartExamples({ onExampleClick }: QuickStartExamplesProps) {
    return (
        <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.6, duration: 0.5 }}
            className="w-full max-w-3xl space-y-4"
        >
            <p className="text-center text-sm font-medium text-white/40">Try these examples</p>

            <div className="grid gap-3 sm:grid-cols-2">
                {examples.map((example, index) => (
                    <motion.button
                        key={index}
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: 0.7 + index * 0.1, duration: 0.3 }}
                        whileHover={{ scale: 1.02, x: 5 }}
                        whileTap={{ scale: 0.98 }}
                        onClick={() => onExampleClick(example.text)}
                        className="group flex items-center gap-3 rounded-xl border border-white/10 bg-white/5 p-4 text-left backdrop-blur-sm transition-all hover:border-primary/50 hover:bg-white/10"
                    >
                        <div className="flex-1">
                            <span className="mb-1 block text-[10px] font-semibold uppercase tracking-wider text-primary">
                                {example.category}
                            </span>
                            <span className="text-sm text-white/80">{example.text}</span>
                        </div>
                        <ArrowRight className="size-4 text-white/30 transition-all group-hover:translate-x-1 group-hover:text-primary" />
                    </motion.button>
                ))}
            </div>
        </motion.div>
    );
}
