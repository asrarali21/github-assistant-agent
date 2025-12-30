"use client";

import { useState, useRef, useEffect } from "react";
import axios from "axios";
import { ChatInput } from "./ChatInput";
import { ChatMessage } from "./ChatMessage";
import { motion, AnimatePresence } from "framer-motion";
import { Github, ArrowDown } from "lucide-react";
import { Background } from "./Background";
import { HeroSection } from "./HeroSection";
import { FeaturesGrid } from "./FeaturesGrid";
import { QuickStartExamples } from "./QuickStartExamples";
import { TechStackBadges } from "./TechStackBadges";

interface Message {
    role: "user" | "assistant";
    content: string;
}

export function ChatInterface() {
    const [messages, setMessages] = useState<Message[]>([]);
    const [isLoading, setIsLoading] = useState(false);
    const [inputValue, setInputValue] = useState("");
    const messagesEndRef = useRef<HTMLDivElement>(null);
    const chatInputRef = useRef<{ focus: () => void }>(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSend = async (input: string) => {
        // Add user message immediately
        const userMessage: Message = { role: "user", content: input };
        setMessages((prev) => [...prev, userMessage]);
        setIsLoading(true);

        try {
            // Use environment variable for API URL, fallback to localhost for development
            const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
            const response = await axios.post(`${apiUrl}/chat`, {
                query: input,
            });

            const content = response.data.response || response.data.message || JSON.stringify(response.data);

            const assistantMessage: Message = {
                role: "assistant",
                content: content,
            };
            setMessages((prev) => [...prev, assistantMessage]);
        } catch (error) {
            console.error("Failed to send message:", error);
            const errorMessage: Message = {
                role: "assistant",
                content: "Sorry, I encountered an error while processing your request. Please make sure the backend server is running on port 8000.",
            };
            setMessages((prev) => [...prev, errorMessage]);
        } finally {
            setIsLoading(false);
        }
    };

    const handleExampleClick = (example: string) => {
        handleSend(example);
    };

    return (
        <div className="relative flex flex-col h-screen text-foreground overflow-hidden">
            <Background />

            {/* Header */}
            <header className="sticky top-0 z-10 flex items-center justify-between border-b border-white/10 bg-background/50 px-4 md:px-6 py-3 backdrop-blur-xl">
                <div className="flex items-center gap-3">
                    <div className="flex size-9 items-center justify-center rounded-xl bg-gradient-to-br from-primary/30 to-purple-900/30 text-primary shadow-[0_0_20px_rgba(168,85,247,0.3)] ring-1 ring-white/10">
                        <Github className="size-5" />
                    </div>
                    <div>
                        <h1 className="text-base font-semibold tracking-tight text-white">GitHub Assistant</h1>
                        <p className="text-[10px] text-white/40">AI-Powered Repository Insights</p>
                    </div>
                </div>

                {messages.length > 0 && (
                    <motion.button
                        initial={{ opacity: 0, scale: 0.8 }}
                        animate={{ opacity: 1, scale: 1 }}
                        onClick={() => setMessages([])}
                        className="rounded-lg border border-white/10 bg-white/5 px-3 py-1.5 text-xs text-white/60 transition-all hover:border-primary/50 hover:text-white"
                    >
                        New Chat
                    </motion.button>
                )}
            </header>

            {/* Messages Area */}
            <div className="flex-1 overflow-y-auto scroll-smooth">
                {messages.length === 0 ? (
                    /* Welcome Screen */
                    <div className="flex min-h-full flex-col items-center justify-start gap-8 px-4 py-8 md:py-12">
                        <HeroSection />
                        <FeaturesGrid />
                        <QuickStartExamples onExampleClick={handleExampleClick} />
                        <TechStackBadges />

                        {/* Scroll indicator */}
                        <motion.div
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1, y: [0, 5, 0] }}
                            transition={{ delay: 1.5, duration: 1.5, repeat: Infinity }}
                            className="flex flex-col items-center gap-1 text-white/20"
                        >
                            <span className="text-xs">Start chatting below</span>
                            <ArrowDown className="size-4" />
                        </motion.div>
                    </div>
                ) : (
                    /* Chat Messages */
                    <div className="p-4 md:p-6">
                        <div className="mx-auto max-w-3xl space-y-6">
                            <AnimatePresence initial={false}>
                                {messages.map((msg, index) => (
                                    <ChatMessage
                                        key={index}
                                        role={msg.role}
                                        content={msg.content}
                                    />
                                ))}
                            </AnimatePresence>

                            {isLoading && (
                                <motion.div
                                    initial={{ opacity: 0, y: 10 }}
                                    animate={{ opacity: 1, y: 0 }}
                                    className="flex w-full gap-4 p-4 md:p-6 bg-white/5 backdrop-blur-sm rounded-xl border border-white/10"
                                >
                                    <div className="flex size-8 shrink-0 items-center justify-center rounded-lg border border-white/10 bg-gradient-to-br from-primary/20 to-purple-900/20 shadow">
                                        <Github className="size-4 animate-pulse text-primary" />
                                    </div>
                                    <div className="flex items-center gap-2">
                                        <span className="text-sm text-white/50">Analyzing repository</span>
                                        <div className="flex items-center gap-1">
                                            <span className="size-1.5 rounded-full bg-primary animate-bounce [animation-delay:-0.3s]"></span>
                                            <span className="size-1.5 rounded-full bg-primary animate-bounce [animation-delay:-0.15s]"></span>
                                            <span className="size-1.5 rounded-full bg-primary animate-bounce"></span>
                                        </div>
                                    </div>
                                </motion.div>
                            )}
                            <div ref={messagesEndRef} />
                        </div>
                    </div>
                )}
            </div>

            {/* Input Area */}
            <div className="border-t border-white/5 bg-background/30 p-4 backdrop-blur-xl">
                <div className="mx-auto max-w-3xl">
                    <ChatInput onSend={handleSend} disabled={isLoading} />
                    <p className="mt-2 text-center text-[10px] text-white/30">
                        Press Enter to send • Shift+Enter for new line
                    </p>
                </div>
            </div>
        </div>
    );
}
