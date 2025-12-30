"use client";

import { motion } from "framer-motion";
import { LucideIcon } from "lucide-react";

interface FeatureCardProps {
    icon: LucideIcon;
    title: string;
    description: string;
    gradient: string;
    delay?: number;
}

export function FeatureCard({ icon: Icon, title, description, gradient, delay = 0 }: FeatureCardProps) {
    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay }}
            whileHover={{ scale: 1.02, y: -5 }}
            className="group relative overflow-hidden rounded-2xl border border-white/10 bg-white/5 p-6 backdrop-blur-xl transition-all duration-300 hover:border-primary/50 hover:shadow-[0_0_30px_rgba(168,85,247,0.15)]"
        >
            {/* Gradient glow on hover */}
            <div className={`absolute inset-0 opacity-0 transition-opacity duration-500 group-hover:opacity-100 ${gradient} blur-3xl`} />

            {/* Content */}
            <div className="relative z-10">
                <div className={`mb-4 inline-flex rounded-xl p-3 ${gradient} bg-opacity-20`}>
                    <Icon className="size-6 text-white" />
                </div>
                <h3 className="mb-2 text-lg font-semibold text-white">{title}</h3>
                <p className="text-sm leading-relaxed text-white/60">{description}</p>
            </div>

            {/* Border gradient effect */}
            <div className="absolute inset-0 rounded-2xl bg-gradient-to-br from-primary/20 via-transparent to-transparent opacity-0 transition-opacity duration-300 group-hover:opacity-100" />
        </motion.div>
    );
}
