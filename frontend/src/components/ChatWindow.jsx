import React, { useState, useEffect, useRef } from 'react';
import { Send, User, Bot, Volume2, ExternalLink } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const API_BASE = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

const ChatWindow = ({ messages, onSendMessage, isLoading, isLowBandwidth }) => {
    const [input, setInput] = useState('');
    const scrollRef = useRef(null);

    useEffect(() => {
        if (scrollRef.current) {
            scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
        }
    }, [messages]);

    const handleSubmit = (e) => {
        e.preventDefault();
        if (input.trim() && !isLoading) {
            onSendMessage(input);
            setInput('');
        }
    };

    const playAudio = (url) => {
        if (url && !isLowBandwidth) {
            const fullUrl = `${API_BASE}${url}`;
            const audio = new Audio(fullUrl);
            audio.play().catch(e => console.error("Audio playback failed:", e));
        }
    };

    return (
        <div className="flex flex-col h-full glass-card overflow-hidden">
            {/* Messages Area */}
            <div
                ref={scrollRef}
                className="flex-1 overflow-y-auto p-4 space-y-4 scrollbar-hide"
            >
                <AnimatePresence initial={false}>
                    {messages.length === 0 && !isLoading && (
                        <motion.div
                            initial={{ opacity: 0, scale: 0.95 }}
                            animate={{ opacity: 1, scale: 1 }}
                            className="text-center mt-10"
                        >
                            <div className="w-16 h-16 bg-primary-50 rounded-full flex items-center justify-center mx-auto mb-4">
                                <Bot className="w-8 h-8 text-primary-500" />
                            </div>
                            <h3 className="text-lg font-semibold text-gray-700">Welcome to JanAccess AI</h3>
                            <p className="text-gray-500 text-sm mt-2 max-w-sm mx-auto">
                                Ask about government schemes, eligibility, scholarships, or any public service.
                            </p>
                        </motion.div>
                    )}

                    {messages.map((msg, idx) => (
                        <motion.div
                            key={idx}
                            initial={{ opacity: 0, y: 20, scale: 0.95 }}
                            animate={{ opacity: 1, y: 0, scale: 1 }}
                            transition={{ duration: 0.4, ease: "easeOut" }}
                            className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                        >
                            <div className={`flex max-w-[85%] items-start gap-2 ${msg.role === 'user' ? 'flex-row-reverse' : ''}`}>
                                <div className={`p-2 rounded-full flex-shrink-0 ${msg.role === 'user' ? 'bg-primary-100' : 'bg-accent-100'
                                    }`}>
                                    {msg.role === 'user'
                                        ? <User className="w-4 h-4 text-primary-600" />
                                        : <Bot className="w-4 h-4 text-accent-600" />
                                    }
                                </div>
                                <div className={`p-3.5 rounded-2xl ${msg.role === 'user'
                                    ? 'bg-primary-600 text-white rounded-tr-sm shadow-md'
                                    : 'bg-white border border-gray-200 text-gray-800 rounded-tl-sm shadow-sm'
                                    }`}>
                                    <p className="text-sm leading-relaxed whitespace-pre-wrap">{msg.text}</p>

                                    {msg.audioUrl && !isLowBandwidth && (
                                        <button
                                            onClick={() => playAudio(msg.audioUrl)}
                                            className="mt-2 flex items-center gap-1 text-xs font-semibold text-primary-400 hover:text-primary-300 transition-colors"
                                        >
                                            <Volume2 className="w-3.5 h-3.5" /> Listen
                                        </button>
                                    )}

                                    {msg.schemes && msg.schemes.length > 0 && (
                                        <div className="mt-3 flex flex-wrap gap-2">
                                            {msg.schemes.map((s, i) => (
                                                typeof s === 'object' && s.website ? (
                                                    <a
                                                        key={i}
                                                        href={s.website}
                                                        target="_blank"
                                                        rel="noopener noreferrer"
                                                        className="flex items-center gap-1.5 px-3 py-1.5 bg-primary-50 text-primary-700 rounded-full text-[11px] font-bold border border-primary-100 hover:bg-primary-100 hover:border-primary-200 transition-all shadow-sm hover:shadow group"
                                                    >
                                                        <ExternalLink className="w-3 h-3 group-hover:scale-110 transition-transform" />
                                                        {s.name}
                                                    </a>
                                                ) : (
                                                    <span
                                                        key={i}
                                                        className="inline-block px-2.5 py-1 bg-gray-50 text-gray-600 rounded-full text-[11px] font-semibold border border-gray-100"
                                                    >
                                                        {typeof s === 'object' ? s.name : s}
                                                    </span>
                                                )
                                            ))}
                                        </div>
                                    )}
                                </div>
                            </div>
                        </motion.div>
                    ))}

                    {isLoading && (
                        <motion.div
                            initial={{ opacity: 0, y: 10 }}
                            animate={{ opacity: 1, y: 0 }}
                            className="flex justify-start"
                        >
                            <div className="flex items-start gap-2">
                                <div className="p-2 rounded-full bg-accent-100 flex-shrink-0">
                                    <Bot className="w-4 h-4 text-accent-600" />
                                </div>
                                <div className="bg-white border border-gray-200 p-4 rounded-2xl rounded-tl-sm shadow-sm">
                                    <div className="flex gap-1.5">
                                        {[0, 1, 2].map(i => (
                                            <motion.div
                                                key={i}
                                                className="w-2 h-2 bg-primary-400 rounded-full"
                                                animate={{
                                                    scale: [1, 1.2, 1],
                                                    opacity: [0.5, 1, 0.5]
                                                }}
                                                transition={{
                                                    duration: 0.6,
                                                    repeat: Infinity,
                                                    delay: i * 0.2
                                                }}
                                            />
                                        ))}
                                    </div>
                                </div>
                            </div>
                        </motion.div>
                    )}
                </AnimatePresence>
            </div>

            {/* Input Area */}
            <form onSubmit={handleSubmit} className="p-4 border-t border-gray-100 bg-white/80 backdrop-blur-sm">
                <div className="relative">
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        placeholder="Type your question about schemes, services..."
                        className="input-field pr-12"
                    />
                    <button
                        type="submit"
                        disabled={!input.trim() || isLoading}
                        className="absolute right-2 top-1/2 -translate-y-1/2 p-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-30 disabled:hover:bg-primary-600 transition-colors"
                    >
                        <Send className="w-4 h-4" />
                    </button>
                </div>
            </form>
        </div>
    );
};

export default ChatWindow;
