import { Button } from "@/components/ui/button";
import { SendHorizontal } from "lucide-react";
import { useState, useRef, useEffect } from "react";

interface ChatInputProps {
    onSend: (message: string) => void;
    disabled?: boolean;
}

export function ChatInput({ onSend, disabled }: ChatInputProps) {
    const [input, setInput] = useState("");
    const textareaRef = useRef<HTMLTextAreaElement>(null);

    const handleSend = () => {
        if (input.trim() && !disabled) {
            onSend(input);
            setInput("");
        }
    };

    const handleKeyDown = (e: React.KeyboardEvent) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    };

    // Auto-resize textarea
    useEffect(() => {
        if (textareaRef.current) {
            textareaRef.current.style.height = "inherit";
            textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`;
        }
    }, [input]);

    return (
        <div className="relative flex items-end gap-2 rounded-xl border border-white/10 bg-white/5 p-2 shadow-lg backdrop-blur-md focus-within:ring-1 focus-within:ring-primary/50 transition-all duration-200">
            <textarea
                ref={textareaRef}
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Ask anything..."
                className="min-h-[44px] w-full resize-none bg-transparent px-3 py-2.5 text-sm text-white outline-none placeholder:text-white/40 disabled:cursor-not-allowed disabled:opacity-50 max-h-32"
                disabled={disabled}
                rows={1}
            />
            <Button
                size="icon"
                onClick={handleSend}
                disabled={!input.trim() || disabled}
                className="shrink-0 rounded-lg bg-primary hover:bg-primary/90 text-white shadow-[0_0_10px_rgba(168,85,247,0.4)] transition-all hover:shadow-[0_0_15px_rgba(168,85,247,0.6)]"
            >
                <SendHorizontal className="size-4" />
                <span className="sr-only">Send</span>
            </Button>
        </div>
    );
}
