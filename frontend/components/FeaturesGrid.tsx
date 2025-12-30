"use client";

import { motion } from "framer-motion";
import { FeatureCard } from "./FeatureCard";
import {
    GitPullRequest,
    BarChart3,
    Users,
    GitCommit,
    Bug,
    Code2,
    Package,
    Telescope,
} from "lucide-react";

const features = [
    {
        icon: GitPullRequest,
        title: "PR Analytics",
        description: "Get accurate counts of open, closed, and merged pull requests with merge rates",
        gradient: "bg-gradient-to-br from-green-500/20 to-emerald-600/20",
    },
    {
        icon: BarChart3,
        title: "Repository Stats",
        description: "Stars, forks, watchers, open issues, and comprehensive repo metadata",
        gradient: "bg-gradient-to-br from-blue-500/20 to-cyan-600/20",
    },
    {
        icon: Users,
        title: "Top Contributors",
        description: "Discover the most active contributors with commit counts and percentages",
        gradient: "bg-gradient-to-br from-purple-500/20 to-violet-600/20",
    },
    {
        icon: GitCommit,
        title: "Commit History",
        description: "View recent commits with authors, messages, and timestamps",
        gradient: "bg-gradient-to-br from-orange-500/20 to-amber-600/20",
    },
    {
        icon: Bug,
        title: "Issue Tracking",
        description: "Open and closed issue counts with close rate analytics",
        gradient: "bg-gradient-to-br from-red-500/20 to-rose-600/20",
    },
    {
        icon: Code2,
        title: "Language Breakdown",
        description: "Visual breakdown of programming languages used in the repository",
        gradient: "bg-gradient-to-br from-pink-500/20 to-fuchsia-600/20",
    },
    {
        icon: Package,
        title: "Release Info",
        description: "Latest release details with version, date, and download counts",
        gradient: "bg-gradient-to-br from-teal-500/20 to-cyan-600/20",
    },
    {
        icon: Telescope,
        title: "Repo Overview",
        description: "Comprehensive summary combining all key metrics at a glance",
        gradient: "bg-gradient-to-br from-indigo-500/20 to-blue-600/20",
    },
];

export function FeaturesGrid() {
    return (
        <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.3, duration: 0.5 }}
            className="w-full max-w-5xl"
        >
            <motion.h2
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.25, duration: 0.4 }}
                className="mb-6 text-center text-sm font-semibold uppercase tracking-wider text-white/40"
            >
                What I can do for you
            </motion.h2>

            <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
                {features.map((feature, index) => (
                    <FeatureCard
                        key={feature.title}
                        icon={feature.icon}
                        title={feature.title}
                        description={feature.description}
                        gradient={feature.gradient}
                        delay={0.3 + index * 0.08}
                    />
                ))}
            </div>
        </motion.div>
    );
}
