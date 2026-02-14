import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Mic, Shield, BookOpen, Briefcase, ArrowRight, Heart } from 'lucide-react';
import { motion } from 'framer-motion';
import { useTranslation } from 'react-i18next';
import PersonaSelector from '../components/PersonaSelector';
import LanguageSwitcher from '../components/LanguageSwitcher';

const Home = () => {
    const navigate = useNavigate();
    const { t } = useTranslation();

    const features = [
        { icon: Mic, title: t('home.features.assistant.title'), desc: t('home.features.assistant.description'), color: "primary" },
        { icon: Shield, title: t('home.features.eligibility.title'), desc: t('home.features.eligibility.description'), color: "accent" },
        { icon: BookOpen, title: t('home.features.documents.title'), desc: t('home.features.documents.description'), color: "primary" },
        { icon: Briefcase, title: t('home.features.skills.title'), desc: t('home.features.skills.description'), color: "accent" },
    ];

    const containerVariants = {
        hidden: { opacity: 0 },
        visible: {
            opacity: 1,
            transition: {
                staggerChildren: 0.1
            }
        }
    };

    const itemVariants = {
        hidden: { opacity: 0, y: 20 },
        visible: {
            opacity: 1,
            y: 0,
            transition: { duration: 0.6, ease: "easeOut" }
        }
    };

    return (
        <div className="min-h-screen bg-white">
            {/* Navigation */}
            <nav className="sticky top-0 z-50 bg-white/80 backdrop-blur-md border-b border-gray-100">
                <div className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
                    <div className="flex items-center gap-2">
                        <div className="w-9 h-9 bg-gradient-to-br from-primary-500 to-accent-500 rounded-xl flex items-center justify-center shadow-lg shadow-primary-500/20">
                            <span className="text-white font-extrabold text-sm">J</span>
                        </div>
                        <h1 className="text-xl font-extrabold gradient-text">JanAccess AI</h1>
                    </div>
                    <div className="flex items-center gap-4">
                        <LanguageSwitcher />
                        <button
                            onClick={() => navigate('/dashboard')}
                            className="btn-primary text-sm px-5 py-2.5"
                        >
                            Open Dashboard
                        </button>
                    </div>
                </div>
            </nav>

            {/* Hero Section */}
            <section className="relative py-20 md:py-32 overflow-hidden">
                {/* Background decorations */}
                <div className="absolute top-0 right-0 w-96 h-96 bg-primary-100/40 rounded-full blur-3xl -z-10"></div>
                <div className="absolute bottom-0 left-0 w-72 h-72 bg-accent-100/40 rounded-full blur-3xl -z-10"></div>

                <div className="max-w-6xl mx-auto px-6 text-center">
                    <motion.div
                        initial={{ opacity: 0, scale: 0.9 }}
                        animate={{ opacity: 1, scale: 1 }}
                        transition={{ duration: 0.5 }}
                    >
                        <span className="inline-block px-5 py-2 mb-6 text-sm font-bold tracking-widest text-primary-600 uppercase bg-primary-50 rounded-full border border-primary-100">
                            {t('home.tagline')}
                        </span>
                    </motion.div>

                    <motion.h1
                        initial={{ opacity: 0, y: 30 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.6, delay: 0.2 }}
                        className="text-4xl sm:text-5xl md:text-7xl font-extrabold text-gray-900 mb-8 leading-tight"
                    >
                        {t('home.title')} <br />
                        <span className="gradient-text">
                            {t('home.subtitle')}
                        </span>
                    </motion.h1>

                    <motion.p
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.6, delay: 0.4 }}
                        className="max-w-2xl mx-auto text-lg md:text-xl text-gray-500 mb-10 leading-relaxed"
                    >
                        {t('home.description')}
                    </motion.p>

                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.6, delay: 0.6 }}
                        className="flex flex-col sm:flex-row gap-4 justify-center"
                    >
                        <button
                            onClick={() => navigate('/dashboard')}
                            className="btn-primary text-lg px-10 py-5 flex items-center justify-center gap-2 group"
                        >
                            {t('home.getStarted')}
                            <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
                        </button>
                        <a
                            href="#features"
                            className="btn-outline text-lg px-10 py-5"
                        >
                            {t('home.learnMore')}
                        </a>
                    </motion.div>
                </div>
            </section>

            {/* Stats */}
            <section className="py-12 bg-gray-50 border-y border-gray-100">
                <motion.div
                    variants={containerVariants}
                    initial="hidden"
                    whileInView="visible"
                    viewport={{ once: true }}
                    className="max-w-6xl mx-auto px-6 grid grid-cols-2 md:grid-cols-4 gap-8 text-center"
                >
                    {[
                        { value: "30+", label: t('home.stats.schemes') },
                        { value: "5", label: t('home.stats.features') },
                        { value: "100%", label: t('home.stats.free') },
                        { value: "24/7", label: t('home.stats.access') },
                    ].map((stat, i) => (
                        <motion.div key={i} variants={itemVariants}>
                            <p className="text-3xl md:text-4xl font-extrabold gradient-text">{stat.value}</p>
                            <p className="text-sm text-gray-500 mt-1 font-medium">{stat.label}</p>
                        </motion.div>
                    ))}
                </motion.div>
            </section>

            {/* Persona Selection */}
            <PersonaSelector />

            {/* Features */}
            <section id="features" className="py-24 bg-white">
                <div className="max-w-6xl mx-auto px-6">
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        viewport={{ once: true }}
                        transition={{ duration: 0.6 }}
                        className="text-center mb-16"
                    >
                        <h2 className="text-3xl md:text-4xl font-extrabold text-gray-900 mb-4">
                            Everything You Need, <span className="gradient-text">Simplified</span>
                        </h2>
                        <p className="text-gray-500 max-w-xl mx-auto">
                            Built for accessibility. Works with voice, text, or both.
                        </p>
                    </motion.div>

                    <motion.div
                        variants={containerVariants}
                        initial="hidden"
                        whileInView="visible"
                        viewport={{ once: true }}
                        className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8"
                    >
                        {features.map((feature, i) => (
                            <motion.div
                                key={i}
                                variants={itemVariants}
                                whileHover={{ y: -10, shadow: "0 20px 25px -5px rgb(0 0 0 / 0.1)" }}
                                className="group flex flex-col items-center text-center p-8 rounded-3xl bg-gray-50 border border-gray-100 hover:border-primary-200 hover:bg-white transition-all duration-300 cursor-pointer"
                            >
                                <div className={`p-4 rounded-2xl shadow-sm mb-6 ${feature.color === 'primary'
                                    ? 'bg-primary-50 group-hover:bg-primary-100'
                                    : 'bg-accent-50 group-hover:bg-accent-100'
                                    } transition-colors`}>
                                    <feature.icon className={`w-8 h-8 ${feature.color === 'primary' ? 'text-primary-600' : 'text-accent-600'
                                        }`} />
                                </div>
                                <h3 className="text-xl font-bold text-gray-900 mb-3">{feature.title}</h3>
                                <p className="text-gray-500 text-sm leading-relaxed">{feature.desc}</p>
                            </motion.div>
                        ))}
                    </motion.div>
                </div>
            </section>

            {/* CTA Section */}
            <section className="py-20 bg-gradient-to-br from-primary-600 to-primary-800">
                <div className="max-w-4xl mx-auto px-6 text-center">
                    <h2 className="text-3xl md:text-4xl font-extrabold text-white mb-6">
                        Ready to Get Started?
                    </h2>
                    <p className="text-primary-100 text-lg mb-8 max-w-xl mx-auto">
                        No login required. Just speak or type your question.
                    </p>
                    <button
                        onClick={() => navigate('/dashboard')}
                        className="px-10 py-5 bg-white text-primary-600 rounded-2xl font-bold text-lg shadow-2xl hover:bg-gray-50 transition-all hover:-translate-y-1 active:scale-[0.98]"
                    >
                        Start Using JanAccess AI
                    </button>
                </div>
            </section>

            {/* Footer */}
            <footer className="py-12 bg-gray-900 text-center">
                <div className="max-w-6xl mx-auto px-6">
                    <div className="flex items-center justify-center gap-2 mb-4">
                        <div className="w-8 h-8 bg-gradient-to-br from-primary-500 to-accent-500 rounded-lg flex items-center justify-center">
                            <span className="text-white font-bold text-xs">J</span>
                        </div>
                        <span className="text-white font-bold text-lg">JanAccess AI</span>
                    </div>
                    <p className="text-gray-400 text-sm flex items-center justify-center gap-1">
                        Built with <Heart className="w-4 h-4 text-red-400 fill-red-400" /> for communities
                    </p>
                    <p className="text-gray-500 text-xs mt-2">{t('home.footer.copyright')}</p>
                </div>
            </footer>
        </div>
    );
};

export default Home;
