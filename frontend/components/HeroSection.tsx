"use client";

import { motion } from "framer-motion";
import { Github, Sparkles } from "lucide-react";

export function HeroSection() {
    return (
        <div className="flex flex-col items-center justify-center space-y-6 text-center">
            {/* Animated Logo */}
            <motion.div
                initial={{ scale: 0.5, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                transition={{ duration: 0.6, type: "spring", stiffness: 200 }}
                className="relative"
            >
                {/* Glow ring */}
                <motion.div
                    animate={{
                        scale: [1, 1.2, 1],
                        opacity: [0.5, 0.8, 0.5],
                    }}
                    transition={{
                        duration: 3,
                        repeat: Infinity,
                        ease: "easeInOut",
                    }}
                    className="absolute inset-0 rounded-full bg-primary/30 blur-xl"
                />

                {/* Icon container */}
                <div className="relative rounded-2xl bg-gradient-to-br from-primary/20 to-purple-900/20 p-5 backdrop-blur-sm ring-1 ring-white/20">
                    <Github className="size-12 text-primary" />
                </div>

                {/* Sparkle accent */}
                <motion.div
                    animate={{ rotate: 360 }}
                    transition={{ duration: 8, repeat: Infinity, ease: "linear" }}
                    className="absolute -right-2 -top-2"
                >
                    <Sparkles className="size-5 text-yellow-400" />
                </motion.div>
            </motion.div>

            {/* Title with gradient */}
            <motion.div
                initial={{ y: 20, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ delay: 0.2, duration: 0.5 }}
                className="space-y-3"
            >
                <h1 className="bg-gradient-to-r from-white via-purple-200 to-primary bg-clip-text text-4xl font-bold tracking-tight text-transparent sm:text-5xl">
                    GitHub Assistant
                </h1>
                <p className="text-lg text-white/60">
                    AI-powered insights for any GitHub repository
                </p>
            </motion.div>

            {/* Powered by badge */}
            {/* <motion.div
                initial={{ y: 20, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ delay: 0.4, duration: 0.5 }}
                className="flex items-center gap-2 rounded-full border border-white/10 bg-white/5 px-4 py-2 text-xs text-white/50 backdrop-blur-sm"
            >
                <span className="size-2 animate-pulse rounded-full bg-green-500" />
                Powered by Gemini AI + LangChain
            </motion.div> */}
        </div>
    );
}
