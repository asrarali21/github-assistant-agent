import { cn } from "@/lib/utils";
import { Bot, User } from "lucide-react";
import { motion } from "framer-motion";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

interface ChatMessageProps {
    role: "user" | "assistant";
    content: string;
}

export function ChatMessage({ role, content }: ChatMessageProps) {
    const isUser = role === "user";

    return (
        <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
            className={cn(
                "flex w-full gap-4 p-4 md:p-6 rounded-xl",
                isUser
                    ? "bg-primary/10 border border-primary/20"
                    : "bg-white/5 backdrop-blur-sm border border-white/10"
            )}
        >
            <div className={cn(
                "flex size-8 shrink-0 select-none items-center justify-center rounded-lg shadow-sm",
                isUser ? "bg-primary text-primary-foreground" : "bg-black/40 border border-white/10 text-white"
            )}>
                {isUser ? (
                    <User className="size-4" />
                ) : (
                    <Bot className="size-4" />
                )}
            </div>
            <div className="flex-1 space-y-2 overflow-hidden">
                <div className="prose prose-invert max-w-none leading-7 text-white/90 prose-p:leading-7 prose-pre:bg-black/50 prose-pre:border prose-pre:border-white/10 prose-code:text-primary prose-code:bg-primary/10 prose-code:px-1 prose-code:rounded">
                    <ReactMarkdown
                        remarkPlugins={[remarkGfm]}
                        components={{
                            a: ({ node, ...props }) => (
                                <a {...props} target="_blank" rel="noopener noreferrer" className="text-primary underline underline-offset-4 hover:text-primary/80" />
                            ),
                        }}
                    >
                        {content}
                    </ReactMarkdown>
                </div>
            </div>
        </motion.div>
    );
}
