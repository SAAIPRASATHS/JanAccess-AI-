import React, { useState, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { LowBandwidthContext, PersonaContext } from '../App';
import ChatWindow from '../components/ChatWindow';
import VoiceInput from '../components/VoiceInput';
import EligibilityForm from '../components/EligibilityForm';
import DocumentUpload from '../components/DocumentUpload';
import SkillJobForm from '../components/SkillJobForm';
import { assistantService } from '../services/api';
import {
    MessageSquare, LayoutGrid, FileText, Briefcase, Info,
    Menu, X, Zap, ArrowLeft, User
} from 'lucide-react';

/* ─── Persona Quick Actions ... same as before ─── */
const PERSONA_QUICK_ACTIONS = {
    Farmer: [
        { label: '🌾 Crop Subsidy', query: 'What crop subsidies are available for farmers?' },
        { label: '📊 Mandi Prices', query: 'Show me the latest mandi prices for crops.' },
        { label: '🌧️ Crop Insurance', query: 'How do I apply for crop insurance?' },
        { label: '💰 PM-KISAN', query: 'Tell me about PM-KISAN income support scheme.' },
    ],
    Student: [
        { label: '🎓 Scholarships', query: 'What scholarships are available for students?' },
        { label: '📚 Skill Courses', query: 'Show me free government skill courses.' },
        { label: '🏦 Education Loans', query: 'How to apply for an education loan?' },
        { label: '📝 Exam Guidance', query: 'Guide me on government competitive exams.' },
    ],
    'Job Seeker': [
        { label: '🏛️ Govt Jobs', query: 'What government jobs are open right now?' },
        { label: '📄 Resume Help', query: 'Help me build a strong resume.' },
        { label: '🛠️ Skill Training', query: 'What free skill training programs are available?' },
        { label: '💼 Placement', query: 'How to register on employment exchanges?' },
    ],
    'Small Business Owner': [
        { label: '🏦 MUDRA Loan', query: 'How to apply for a MUDRA loan?' },
        { label: '📋 MSME Register', query: 'How do I register my business as MSME?' },
        { label: '💡 Startup India', query: 'Tell me about Startup India benefits.' },
        { label: '📱 Digital Payments', query: 'How to adopt digital payments for my shop?' },
    ],
    'Senior Citizen': [
        { label: '🏥 Health Cover', query: 'What health insurance is available for senior citizens?' },
        { label: '💰 Pension Schemes', query: 'Tell me about pension schemes for seniors.' },
        { label: '🏦 Savings Schemes', query: 'What savings schemes are best for senior citizens?' },
        { label: '📞 Elder Helpline', query: 'What helplines are available for senior citizens?' },
    ],
    'Differently Abled': [
        { label: '🆔 UDID Card', query: 'How do I apply for a UDID disability card?' },
        { label: '💰 Disability Pension', query: 'What disability pension schemes are available?' },
        { label: '🦽 Assistive Devices', query: 'How to get free assistive devices from the government?' },
        { label: '💼 Job Reservation', query: 'What job reservations exist for differently abled persons?' },
    ],
};

const DEFAULT_QUICK_ACTIONS = [
    'How to apply for PMAY?',
    'Scholarships for SC students',
    'Free health insurance schemes',
    'Skill training programs near me',
];

const Dashboard = () => {
    const navigate = useNavigate();
    const { isLowBandwidth, toggleLowBandwidth } = useContext(LowBandwidthContext);
    const { persona, setPersona } = useContext(PersonaContext);
    const [activeTab, setActiveTab] = useState('chat');
    const [messages, setMessages] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

    const handleSendMessage = async (text) => {
        setMessages(prev => [...prev, { role: 'user', text }]);
        setIsLoading(true);
        try {
            const response = await assistantService.chat(text, isLowBandwidth, persona);
            setMessages(prev => [...prev, {
                role: 'assistant',
                text: response.text_response,
                audioUrl: isLowBandwidth ? null : response.audio_url,
                schemes: response.schemes || []
            }]);
        } catch (err) {
            console.error(err);
            setMessages(prev => [...prev, {
                role: 'assistant',
                text: "I'm having trouble connecting to the JanAccess server. This usually happens if the backend is not running or if there's a local network blocked. Please ensure the terminal running 'uvicorn' is active on port 8000."
            }]);
        }
        setIsLoading(false);
    };

    const handleVoiceInput = async (audioBlob) => {
        setMessages(prev => [...prev, { role: 'user', text: '🎤 Voice message...' }]);
        setIsLoading(true);
        try {
            const response = await assistantService.voiceChat(audioBlob, persona);
            setMessages(prev => {
                const updated = [...prev];
                const lastUserIdx = updated.map(m => m.role).lastIndexOf('user');
                if (lastUserIdx >= 0 && response.transcribed_text) {
                    updated[lastUserIdx].text = `🎤 "${response.transcribed_text}"`;
                }
                return [...updated, {
                    role: 'assistant',
                    text: response.text_response,
                    audioUrl: response.audio_url
                }];
            });
        } catch (err) {
            console.error(err);
            setMessages(prev => [...prev, {
                role: 'assistant',
                text: "I couldn't process the audio. Please try again or type your question."
            }]);
        }
        setIsLoading(false);
    };

    const quickActions = persona && PERSONA_QUICK_ACTIONS[persona]
        ? PERSONA_QUICK_ACTIONS[persona]
        : null;

    const tabs = [
        { id: 'chat', name: 'AI Assistant', icon: MessageSquare },
        { id: 'eligibility', name: 'Eligibility', icon: LayoutGrid },
        { id: 'documents', name: 'Document Help', icon: FileText },
        { id: 'skills', name: 'Skills & Jobs', icon: Briefcase },
        { id: 'about', name: 'About', icon: Info },
    ];

    const containerVariants = {
        hidden: { opacity: 0 },
        visible: {
            opacity: 1,
            transition: { staggerChildren: 0.1 }
        }
    };

    const itemVariants = {
        hidden: { opacity: 0, x: -20 },
        visible: { opacity: 1, x: 0 },
    };

    return (
        <div className="min-h-screen bg-gray-50 flex flex-col md:flex-row">

            {/* Sidebar — Desktop */}
            <aside className="hidden md:flex w-64 bg-white border-r border-gray-200 flex-col flex-shrink-0">
                <div className="p-6 flex-1">
                    {/* Logo */}
                    <div className="flex items-center gap-2 mb-8">
                        <button onClick={() => navigate('/')} className="flex items-center gap-2 group">
                            <motion.div
                                whileHover={{ rotate: 10 }}
                                className="w-9 h-9 bg-gradient-to-br from-primary-500 to-accent-500 rounded-xl flex items-center justify-center shadow-lg shadow-primary-500/20"
                            >
                                <span className="text-white font-extrabold text-sm">J</span>
                            </motion.div>
                            <h1 className="text-xl font-extrabold gradient-text">JanAccess AI</h1>
                        </button>
                    </div>

                    {/* Persona Badge */}
                    <AnimatePresence mode="wait">
                        {persona && (
                            <motion.div
                                initial={{ opacity: 0, x: -20 }}
                                animate={{ opacity: 1, x: 0 }}
                                exit={{ opacity: 0, x: -20 }}
                                className="mb-6 p-3 rounded-xl bg-gradient-to-r from-primary-50 to-accent-50 border border-primary-100"
                            >
                                <div className="flex items-center justify-between">
                                    <div className="flex items-center gap-2">
                                        <User className="w-4 h-4 text-primary-600" />
                                        <span className="text-xs font-bold text-primary-700 uppercase tracking-wider">{persona}</span>
                                    </div>
                                    <button
                                        onClick={() => { setPersona(null); navigate('/'); }}
                                        className="text-[10px] font-semibold text-primary-500 hover:text-primary-700 transition-colors"
                                    >
                                        Change
                                    </button>
                                </div>
                            </motion.div>
                        )}
                    </AnimatePresence>

                    {/* Nav tabs */}
                    <nav className="space-y-1">
                        {tabs.map(tab => (
                            <button
                                key={tab.id}
                                onClick={() => setActiveTab(tab.id)}
                                className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all text-sm ${activeTab === tab.id
                                    ? 'bg-primary-50 text-primary-600 font-semibold shadow-sm'
                                    : 'text-gray-500 hover:bg-gray-50 hover:text-gray-700'
                                    }`}
                            >
                                <tab.icon className="w-5 h-5" />
                                {tab.name}
                            </button>
                        ))}
                    </nav>
                </div>

                {/* Low Bandwidth Toggle */}
                <div className="p-6 border-t border-gray-100">
                    <motion.button
                        whileHover={{ scale: 1.02 }}
                        whileTap={{ scale: 0.98 }}
                        onClick={toggleLowBandwidth}
                        className={`w-full p-4 rounded-2xl border transition-all text-left ${isLowBandwidth
                            ? 'bg-accent-50 border-accent-200'
                            : 'bg-gray-50 border-gray-100 hover:border-gray-200'
                            }`}
                    >
                        <div className="flex items-center gap-2 mb-1">
                            <Zap className={`w-4 h-4 ${isLowBandwidth ? 'text-accent-600' : 'text-gray-400'}`} />
                            <span className={`text-xs font-bold uppercase tracking-wider ${isLowBandwidth ? 'text-accent-700' : 'text-gray-500'
                                }`}>
                                Low Bandwidth
                            </span>
                        </div>
                        <p className="text-[10px] text-gray-500">
                            {isLowBandwidth ? 'Text-only mode' : 'Enable for slow networks'}
                        </p>
                    </motion.button>

                    <button
                        onClick={() => navigate('/')}
                        className="w-full mt-3 flex items-center gap-2 px-4 py-2 text-sm text-gray-400 hover:text-gray-600 transition-colors"
                    >
                        <ArrowLeft className="w-4 h-4" /> Back to Home
                    </button>
                </div>
            </aside>

            {/* Mobile Header ... same as before ─── */}
            <header className="md:hidden bg-white border-b border-gray-200 p-4 flex items-center justify-between sticky top-0 z-50">
                <div className="flex items-center gap-2">
                    <div className="w-8 h-8 bg-gradient-to-br from-primary-500 to-accent-500 rounded-lg flex items-center justify-center">
                        <span className="text-white font-bold text-xs">J</span>
                    </div>
                    <h1 className="text-lg font-extrabold gradient-text">JanAccess AI</h1>
                </div>
                <div className="flex items-center gap-2">
                    <button onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}>
                        {isMobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
                    </button>
                </div>
            </header>

            {/* Mobile Nav Dropdown */}
            <AnimatePresence>
                {isMobileMenuOpen && (
                    <motion.div
                        initial={{ opacity: 0, height: 0 }}
                        animate={{ opacity: 1, height: 'auto' }}
                        exit={{ opacity: 0, height: 0 }}
                        className="md:hidden bg-white border-b border-gray-200 px-4 py-2 space-y-1 absolute w-full z-40 shadow-lg top-[64px] overflow-hidden"
                    >
                        {tabs.map(tab => (
                            <button
                                key={tab.id}
                                onClick={() => { setActiveTab(tab.id); setIsMobileMenuOpen(false); }}
                                className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm ${activeTab === tab.id
                                    ? 'bg-primary-50 text-primary-600 font-semibold'
                                    : 'text-gray-500'
                                    }`}
                            >
                                <tab.icon className="w-5 h-5" />
                                {tab.name}
                            </button>
                        ))}
                    </motion.div>
                )}
            </AnimatePresence>

            {/* Main Content */}
            <main className="flex-1 flex flex-col h-[calc(100vh-64px)] md:h-screen overflow-hidden">
                <div className="flex-1 overflow-y-auto p-4 md:p-8 scrollbar-hide">
                    <AnimatePresence mode="wait">
                        {activeTab === 'chat' && (
                            <motion.div
                                key="chat"
                                initial={{ opacity: 0, y: 10 }}
                                animate={{ opacity: 1, y: 0 }}
                                exit={{ opacity: 0, y: -10 }}
                                className="h-full flex flex-col"
                            >
                                <div className="mb-6 text-center md:text-left">
                                    <h2 className="section-title">AI Assistant</h2>
                                    <p className="text-gray-500 text-sm mt-1">
                                        {persona
                                            ? `Personalised for ${persona}`
                                            : 'Ask about schemes and services'}
                                    </p>
                                </div>
                                <div className="flex-1 grid grid-cols-1 lg:grid-cols-3 gap-6 overflow-hidden">
                                    <div className="lg:col-span-2 flex flex-col h-full overflow-hidden">
                                        <ChatWindow
                                            messages={messages}
                                            onSendMessage={handleSendMessage}
                                            isLoading={isLoading}
                                            isLowBandwidth={isLowBandwidth}
                                        />
                                    </div>
                                    {!isLowBandwidth && (
                                        <motion.div
                                            initial={{ opacity: 0, scale: 0.95 }}
                                            animate={{ opacity: 1, scale: 1 }}
                                            transition={{ delay: 0.2 }}
                                            className="lg:col-span-1 flex flex-col items-center justify-center glass-card p-8 h-fit"
                                        >
                                            <VoiceInput onTranscriptionReceived={handleVoiceInput} />
                                            <div className="mt-8 w-full">
                                                <h4 className="text-xs font-bold text-gray-400 uppercase tracking-widest mb-4">
                                                    {quickActions ? `Quick Actions` : 'Suggestions'}
                                                </h4>
                                                <motion.div
                                                    variants={containerVariants}
                                                    initial="hidden"
                                                    animate="visible"
                                                    className="space-y-2"
                                                >
                                                    {(quickActions || DEFAULT_QUICK_ACTIONS.map(q => ({ label: q, query: q }))).map((qa, i) => (
                                                        <motion.button
                                                            key={i}
                                                            variants={itemVariants}
                                                            disabled={isLoading}
                                                            whileHover={!isLoading ? { x: 5, backgroundColor: "rgba(var(--primary-rgb), 0.05)" } : {}}
                                                            onClick={() => handleSendMessage(qa.query || qa)}
                                                            className={`w-full text-left p-3 text-sm rounded-xl border border-gray-100 transition-all font-medium ${isLoading
                                                                ? 'opacity-50 cursor-not-allowed'
                                                                : 'hover:border-primary-200 text-gray-700'
                                                                }`}
                                                        >
                                                            {qa.label || qa}
                                                        </motion.button>
                                                    ))}
                                                </motion.div>
                                            </div>
                                        </motion.div>
                                    )}
                                </div>
                            </motion.div>
                        )}

                        {activeTab === 'eligibility' && (
                            <motion.div key="eligibility" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
                                <EligibilityForm />
                            </motion.div>
                        )}

                        {activeTab === 'documents' && (
                            <motion.div key="documents" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
                                <DocumentUpload />
                            </motion.div>
                        )}

                        {activeTab === 'skills' && (
                            <motion.div key="skills" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
                                <SkillJobForm />
                            </motion.div>
                        )}

                        {activeTab === 'about' && (
                            <motion.div
                                key="about"
                                initial={{ opacity: 0, scale: 0.95 }}
                                animate={{ opacity: 1, scale: 1 }}
                                exit={{ opacity: 0, scale: 0.95 }}
                                className="max-w-2xl mx-auto glass-card p-8"
                            >
                                <h2 className="section-title mb-4">About JanAccess AI</h2>
                                <p className="text-gray-600 mb-6 leading-relaxed">
                                    JanAccess AI is a voice-first platform tailored for underserved communities in India.
                                    Our mission is to bridge the digital divide by simplifying access to government services,
                                    schemes, and opportunities.
                                </p>
                                {/* ... rest of About content ... */}
                            </motion.div>
                        )}
                    </AnimatePresence>
                </div>
            </main>
        </div>
    );
};

export default Dashboard;
