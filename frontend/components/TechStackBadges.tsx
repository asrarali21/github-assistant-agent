"use client";

import { motion } from "framer-motion";

const techStack = [
    { name: "Next.js", color: "from-gray-500 to-gray-700" },
    { name: "React", color: "from-cyan-500 to-blue-600" },
    { name: "Python", color: "from-yellow-500 to-blue-500" },
    { name: "LangChain", color: "from-green-500 to-emerald-600" },
    { name: "Gemini AI", color: "from-blue-500 to-purple-600" },
    { name: "FastAPI", color: "from-teal-500 to-green-600" },
];

export function TechStackBadges() {
    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 1.2, duration: 0.5 }}
            className="flex flex-wrap items-center justify-center gap-2"
        >
            <span className="text-xs text-white/30">Built with</span>
            {techStack.map((tech, index) => (
                <motion.span
                    key={tech.name}
                    initial={{ opacity: 0, scale: 0.8 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ delay: 1.3 + index * 0.08, duration: 0.3 }}
                    className={`rounded-full bg-gradient-to-r ${tech.color} px-3 py-1 text-[10px] font-medium text-white/90 shadow-sm`}
                >
                    {tech.name}
                </motion.span>
            ))}
        </motion.div>
    );
}
