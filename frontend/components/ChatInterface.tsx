import { useState, useRef, useEffect } from "react";
import axios from "axios";
import { ChatInput } from "./ChatInput";
import { ChatMessage } from "./ChatMessage";
import { motion, AnimatePresence } from "framer-motion";
import { Github } from "lucide-react";
import { Background } from "./Background";

interface Message {
    role: "user" | "assistant";
    content: string;
}

export function ChatInterface() {
    const [messages, setMessages] = useState<Message[]>([]);
    const [isLoading, setIsLoading] = useState(false);
    const messagesEndRef = useRef<HTMLDivElement>(null);

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
            // Call the backend
            const response = await axios.post("http://localhost:8000/chat", {
                query: input,
            });

            // Add assistant message
            // Assuming response.data.response is the format, based on typical patterns. 
            // The original code just logged response, so I'll assume response.data is the string or has a property.
            // I'll assume response.data is the object and it might have a 'response' or 'answer' field.
            // Let's try to be safe and dump the whole data if unsure, or just response.data if it's a string.
            // Looking at the original code: const response = await axios.post("http://localhost:8000/chat" , {query :input} )
            // It didn't use the response.

            // I will assume the backend returns { response: string } or just the string.
            // For now, I'll use a safe fallback.
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
                content: "Sorry, I encountered an error while processing your request.",
            };
            setMessages((prev) => [...prev, errorMessage]);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="relative flex flex-col h-screen text-foreground overflow-hidden">
            <Background />

            {/* Header */}
            <header className="sticky top-0 z-10 flex items-center gap-3 border-b border-white/10 bg-background/20 px-6 py-4 backdrop-blur-md">
                <div className="flex size-8 items-center justify-center rounded-lg bg-primary/20 text-primary shadow-[0_0_15px_rgba(168,85,247,0.5)]">
                    <Github className="size-5" />
                </div>
                <h1 className="text-lg font-semibold tracking-tight text-white">GitHub Agent</h1>
            </header>

            {/* Messages Area */}
            <div className="flex-1 overflow-y-auto p-4 md:p-6 scroll-smooth">
                <div className="mx-auto max-w-3xl space-y-6">
                    {messages.length === 0 ? (
                        <div className="flex h-full flex-col items-center justify-center space-y-4 py-20 text-center text-muted-foreground">
                            <motion.div
                                initial={{ scale: 0.8, opacity: 0 }}
                                animate={{ scale: 1, opacity: 1 }}
                                transition={{ duration: 0.5 }}
                                className="rounded-full bg-white/5 p-6 backdrop-blur-sm ring-1 ring-white/10"
                            >
                                <Github className="size-16 opacity-80 text-primary" />
                            </motion.div>
                            <motion.div
                                initial={{ y: 20, opacity: 0 }}
                                animate={{ y: 0, opacity: 1 }}
                                transition={{ delay: 0.2, duration: 0.5 }}
                                className="space-y-2"
                            >
                                <h2 className="text-3xl font-bold text-white tracking-tight">
                                    How can I help you today?
                                </h2>
                                <p className="text-lg text-white/60">Ask me anything about your repositories or code.</p>
                            </motion.div>
                        </div>
                    ) : (
                        <AnimatePresence initial={false}>
                            {messages.map((msg, index) => (
                                <ChatMessage
                                    key={index}
                                    role={msg.role}
                                    content={msg.content}
                                />
                            ))}
                        </AnimatePresence>
                    )}

                    {isLoading && (
                        <motion.div
                            initial={{ opacity: 0, y: 10 }}
                            animate={{ opacity: 1, y: 0 }}
                            className="flex w-full gap-4 p-4 md:p-6 bg-white/5 backdrop-blur-sm rounded-xl border border-white/10"
                        >
                            <div className="flex size-8 shrink-0 items-center justify-center rounded-md border border-white/10 bg-black/20 shadow">
                                <Github className="size-4 animate-pulse text-primary" />
                            </div>
                            <div className="flex items-center gap-1">
                                <span className="size-1.5 rounded-full bg-primary animate-bounce [animation-delay:-0.3s]"></span>
                                <span className="size-1.5 rounded-full bg-primary animate-bounce [animation-delay:-0.15s]"></span>
                                <span className="size-1.5 rounded-full bg-primary animate-bounce"></span>
                            </div>
                        </motion.div>
                    )}
                    <div ref={messagesEndRef} />
                </div>
            </div>

            {/* Input Area */}
            <div className="p-4 md:p-6">
                <div className="mx-auto max-w-3xl">
                    <ChatInput onSend={handleSend} disabled={isLoading} />
                    <p className="mt-2 text-center text-xs text-white/40">
                        AI can make mistakes. Please verify important information.
                    </p>
                </div>
            </div>
        </div>
    );
}
