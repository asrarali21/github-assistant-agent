import { motion } from "framer-motion";

export function Background() {
    return (
        <div className="fixed inset-0 -z-10 h-full w-full overflow-hidden bg-background">
            {/* Deep space gradient base */}
            <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-slate-900 via-[#09090b] to-[#09090b]" />

            {/* Animated blobs/nebula effects */}
            <motion.div
                animate={{
                    scale: [1, 1.2, 1],
                    opacity: [0.3, 0.5, 0.3],
                    rotate: [0, 90, 0],
                }}
                transition={{
                    duration: 20,
                    repeat: Infinity,
                    ease: "easeInOut",
                }}
                className="absolute -top-[20%] -left-[10%] h-[500px] w-[500px] rounded-full bg-purple-900/30 blur-[100px]"
            />

            <motion.div
                animate={{
                    scale: [1, 1.1, 1],
                    opacity: [0.2, 0.4, 0.2],
                    x: [0, 100, 0],
                }}
                transition={{
                    duration: 25,
                    repeat: Infinity,
                    ease: "easeInOut",
                }}
                className="absolute top-[20%] right-[10%] h-[400px] w-[400px] rounded-full bg-blue-900/20 blur-[120px]"
            />

            <motion.div
                animate={{
                    scale: [1, 1.3, 1],
                    opacity: [0.2, 0.5, 0.2],
                }}
                transition={{
                    duration: 18,
                    repeat: Infinity,
                    ease: "easeInOut",
                }}
                className="absolute bottom-[10%] left-[20%] h-[600px] w-[600px] rounded-full bg-indigo-900/20 blur-[100px]"
            />

            {/* Grid overlay for tech feel */}
            <div className="absolute inset-0 bg-[url('/grid.svg')] bg-center [mask-image:linear-gradient(180deg,white,rgba(255,255,255,0))]" />
        </div>
    );
}
