import React, { useState, useRef } from 'react';
import { Mic, Square, Loader2 } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const VoiceInput = ({ onTranscriptionReceived }) => {
    const [isRecording, setIsRecording] = useState(false);
    const [isProcessing, setIsProcessing] = useState(false);
    const mediaRecorderRef = useRef(null);
    const audioChunksRef = useRef([]);

    const startRecording = async () => {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaRecorderRef.current = new MediaRecorder(stream);
            audioChunksRef.current = [];

            mediaRecorderRef.current.ondataavailable = (event) => {
                audioChunksRef.current.push(event.data);
            };

            mediaRecorderRef.current.onstop = async () => {
                const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' });
                setIsProcessing(true);
                try {
                    await onTranscriptionReceived(audioBlob);
                } catch (err) {
                    console.error('Voice processing error:', err);
                }
                setIsProcessing(false);
                // Stop all tracks
                stream.getTracks().forEach(track => track.stop());
            };

            mediaRecorderRef.current.start();
            setIsRecording(true);
        } catch (err) {
            console.error('Error accessing microphone:', err);
            alert('Please allow microphone access to use voice features.');
        }
    };

    const stopRecording = () => {
        if (mediaRecorderRef.current && isRecording) {
            mediaRecorderRef.current.stop();
            setIsRecording(false);
        }
    };

    return (
        <div className="flex flex-col items-center justify-center p-4">
            {/* Mic Button */}
            <div className="relative">
                <AnimatePresence>
                    {isRecording && (
                        <motion.div
                            initial={{ scale: 0.8, opacity: 0 }}
                            animate={{
                                scale: [1, 1.5, 1],
                                opacity: [0, 0.4, 0]
                            }}
                            exit={{ opacity: 0 }}
                            transition={{
                                duration: 1.5,
                                repeat: Infinity,
                                ease: "easeInOut"
                            }}
                            className="absolute inset-0 w-20 h-20 rounded-full bg-red-400/40 -z-10"
                        />
                    )}
                </AnimatePresence>

                <motion.button
                    onClick={isRecording ? stopRecording : startRecording}
                    disabled={isProcessing}
                    animate={isRecording ? { scale: [1, 1.05, 1] } : { scale: 1 }}
                    transition={isRecording ? { duration: 1, repeat: Infinity } : {}}
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    className={`relative w-20 h-20 rounded-full flex items-center justify-center shadow-lg transition-all duration-300 ${isProcessing
                        ? 'bg-gray-400 cursor-not-allowed'
                        : isRecording
                            ? 'bg-red-500 shadow-red-500/30'
                            : 'bg-primary-600 shadow-primary-500/30'
                        }`}
                >
                    {isProcessing ? (
                        <Loader2 className="w-10 h-10 text-white animate-spin" />
                    ) : isRecording ? (
                        <Square className="w-8 h-8 text-white" />
                    ) : (
                        <Mic className="w-10 h-10 text-white" />
                    )}
                </motion.button>
            </div>

            {/* Status Text */}
            <p className="mt-4 text-sm font-medium text-gray-500">
                {isRecording
                    ? "Listening... Tap to stop"
                    : isProcessing
                        ? "Processing voice..."
                        : "Tap the mic to speak"
                }
            </p>

            {/* Voice Wave Animation */}
            <AnimatePresence>
                {isRecording && (
                    <motion.div
                        initial={{ opacity: 0, y: 5 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: 5 }}
                        className="flex items-center gap-1 mt-3 h-5"
                    >
                        {[0.2, 0.4, 0.6, 0.4, 0.2].map((height, i) => (
                            <motion.span
                                key={i}
                                className="w-1 bg-red-400 rounded-full"
                                animate={{
                                    height: ["40%", "100%", "40%"],
                                }}
                                transition={{
                                    duration: 0.5,
                                    repeat: Infinity,
                                    delay: i * 0.1,
                                    ease: "easeInOut"
                                }}
                            />
                        ))}
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
};

export default VoiceInput;
