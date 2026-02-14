import React, { useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { PersonaContext } from '../App';

/* ─── Persona Card Data ───────────────────────────────────────── */
const PERSONA_CARDS = [
    { id: 'Farmer', emoji: '🌾', label: 'Farmer', desc: 'Agriculture, subsidies & market prices', gradient: 'from-green-500 to-emerald-600' },
    { id: 'Student', emoji: '🎓', label: 'Student', desc: 'Scholarships, courses & education loans', gradient: 'from-blue-500 to-cyan-600' },
    { id: 'Job Seeker', emoji: '💼', label: 'Job Seeker', desc: 'Govt jobs, resume help & placements', gradient: 'from-violet-500 to-purple-600' },
    { id: 'Small Business Owner', emoji: '🏪', label: 'Small Business', desc: 'MUDRA, MSME & startup schemes', gradient: 'from-amber-500 to-orange-600' },
    { id: 'Senior Citizen', emoji: '🧓', label: 'Senior Citizen', desc: 'Pensions, health cover & savings', gradient: 'from-rose-500 to-pink-600' },
    { id: 'Differently Abled', emoji: '♿', label: 'Differently Abled', desc: 'UDID, assistive devices & reservations', gradient: 'from-teal-500 to-cyan-600' },
];

const PersonaSelector = () => {
    const navigate = useNavigate();
    const { setPersona } = useContext(PersonaContext);

    const handleSelect = (personaId) => {
        setPersona(personaId);
        navigate('/dashboard');
    };

    const containerVariants = {
        hidden: { opacity: 0 },
        visible: {
            opacity: 1,
            transition: {
                staggerChildren: 0.08
            }
        }
    };

    const itemVariants = {
        hidden: { opacity: 0, scale: 0.9, y: 20 },
        visible: {
            opacity: 1,
            scale: 1,
            y: 0,
            transition: { duration: 0.4, ease: "easeOut" }
        }
    };

    return (
        <section className="py-20 bg-white" id="persona">
            <div className="max-w-6xl mx-auto px-6">
                {/* Heading */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true }}
                    transition={{ duration: 0.6 }}
                    className="text-center mb-12"
                >
                    <span className="inline-block px-4 py-1.5 mb-4 text-xs font-bold tracking-widest text-accent-600 uppercase bg-accent-50 rounded-full border border-accent-100">
                        Smart Persona Mode
                    </span>
                    <h2 className="text-3xl md:text-4xl font-extrabold text-gray-900 mb-3">
                        I am a <span className="gradient-text">…</span>
                    </h2>
                    <p className="text-gray-500 max-w-lg mx-auto">
                        Select your role for a personalised experience — tailored schemes, quick actions, and AI responses.
                    </p>
                </motion.div>

                {/* Cards Grid */}
                <motion.div
                    variants={containerVariants}
                    initial="hidden"
                    whileInView="visible"
                    viewport={{ once: true, margin: "-100px" }}
                    className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-4 md:gap-6"
                >
                    {PERSONA_CARDS.map((card) => (
                        <motion.button
                            key={card.id}
                            variants={itemVariants}
                            whileHover={{
                                scale: 1.05,
                                y: -5,
                                shadow: "0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1)"
                            }}
                            onClick={() => handleSelect(card.id)}
                            className="group flex flex-col items-center text-center p-6 rounded-2xl border border-gray-100 bg-gray-50 hover:bg-white hover:border-primary-200 transition-all duration-300 cursor-pointer shadow-sm"
                        >
                            {/* Emoji Badge */}
                            <div className={`w-14 h-14 rounded-2xl bg-gradient-to-br ${card.gradient} flex items-center justify-center text-2xl shadow-lg mb-4 group-hover:rotate-6 transition-transform duration-300`}>
                                {card.emoji}
                            </div>

                            <h3 className="text-sm font-bold text-gray-800 mb-1 leading-tight">{card.label}</h3>
                            <p className="text-[11px] text-gray-500 leading-snug">{card.desc}</p>
                        </motion.button>
                    ))}
                </motion.div>
            </div>
        </section>
    );
};

export default PersonaSelector;
