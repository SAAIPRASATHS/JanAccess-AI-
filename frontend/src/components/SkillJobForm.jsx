import React, { useState } from 'react';
import { skillsService } from '../services/api';
import { Briefcase, GraduationCap, Loader2, MapPin, Sparkles, ArrowLeft, AlertCircle } from 'lucide-react';

const SkillJobForm = () => {
    const [formData, setFormData] = useState({
        education_level: '',
        interest: '',
        location: ''
    });
    const [results, setResults] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);
        try {
            const data = await skillsService.getRecommendations(formData);
            setResults(data);
        } catch (err) {
            console.error(err);
            setError('Failed to get recommendations. Please make sure the backend is running.');
        }
        setLoading(false);
    };

    const handleChange = (field, value) => {
        setFormData(prev => ({ ...prev, [field]: value }));
    };

    return (
        <div className="max-w-2xl mx-auto">
            <div className="mb-6 text-center md:text-left">
                <h2 className="section-title">Skills & Job Recommendations</h2>
                <p className="text-gray-500 text-sm mt-1">
                    Tell us about yourself and get personalized training and job suggestions.
                </p>
            </div>

            <div className="glass-card p-6 md:p-8">
                {!results ? (
                    <form onSubmit={handleSubmit} className="space-y-5">
                        <div>
                            <label className="label-text flex items-center gap-1.5">
                                <GraduationCap className="w-4 h-4 text-gray-400" /> Education Level
                            </label>
                            <select
                                required
                                className="input-field"
                                value={formData.education_level}
                                onChange={(e) => handleChange('education_level', e.target.value)}
                            >
                                <option value="">Select your education level</option>
                                <option value="Below 10th">Below 10th</option>
                                <option value="10th Pass">10th Pass</option>
                                <option value="12th Pass">12th Pass</option>
                                <option value="Diploma">Diploma/ITI</option>
                                <option value="Graduate">Graduate</option>
                                <option value="Post Graduate">Post Graduate</option>
                            </select>
                        </div>

                        <div>
                            <label className="label-text flex items-center gap-1.5">
                                <Sparkles className="w-4 h-4 text-gray-400" /> Interest / Skills
                            </label>
                            <input
                                type="text"
                                required
                                className="input-field"
                                placeholder="e.g. computers, cooking, tailoring, driving..."
                                value={formData.interest}
                                onChange={(e) => handleChange('interest', e.target.value)}
                            />
                        </div>

                        <div>
                            <label className="label-text flex items-center gap-1.5">
                                <MapPin className="w-4 h-4 text-gray-400" /> Location
                            </label>
                            <input
                                type="text"
                                required
                                className="input-field"
                                placeholder="e.g. Mumbai, Bihar, Tamil Nadu..."
                                value={formData.location}
                                onChange={(e) => handleChange('location', e.target.value)}
                            />
                        </div>

                        {error && (
                            <div className="p-3 bg-red-50 border border-red-200 rounded-xl text-red-700 text-sm flex items-center gap-2">
                                <AlertCircle className="w-4 h-4 flex-shrink-0" />
                                {error}
                            </div>
                        )}

                        <button
                            type="submit"
                            disabled={loading}
                            className="btn-primary w-full flex items-center justify-center gap-2"
                        >
                            {loading ? (
                                <>
                                    <Loader2 className="w-5 h-5 animate-spin" />
                                    Finding Opportunities...
                                </>
                            ) : (
                                <>
                                    <Sparkles className="w-5 h-5" />
                                    Get Recommendations
                                </>
                            )}
                        </button>
                    </form>
                ) : (
                    <div className="space-y-5 animate-fade-in">
                        {/* AI Summary */}
                        <div className="p-4 bg-primary-50 rounded-xl border border-primary-100">
                            <h4 className="text-sm font-bold text-primary-700 uppercase mb-2">AI Summary</h4>
                            <p className="text-gray-800 text-sm leading-relaxed">
                                {results.ai_summary}
                            </p>
                        </div>

                        {/* Recommendations */}
                        <h3 className="text-lg font-semibold text-gray-700">
                            {results.recommendations?.length || 0} Opportunities Found
                        </h3>

                        <div className="space-y-3">
                            {results.recommendations?.map((rec, i) => (
                                <div
                                    key={i}
                                    className={`p-4 rounded-xl border animate-slide-up ${rec.type === 'job'
                                            ? 'bg-blue-50 border-blue-200'
                                            : 'bg-accent-50 border-accent-200'
                                        }`}
                                    style={{ animationDelay: `${i * 0.1}s` }}
                                >
                                    <div className="flex items-start gap-3">
                                        <div className={`p-2 rounded-lg flex-shrink-0 ${rec.type === 'job'
                                                ? 'bg-blue-100'
                                                : 'bg-accent-100'
                                            }`}>
                                            {rec.type === 'job'
                                                ? <Briefcase className="w-5 h-5 text-blue-600" />
                                                : <GraduationCap className="w-5 h-5 text-accent-600" />
                                            }
                                        </div>
                                        <div className="flex-1 min-w-0">
                                            <div className="flex items-center gap-2 mb-1">
                                                <h4 className="font-semibold text-gray-800 text-sm">{rec.title}</h4>
                                                <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${rec.type === 'job'
                                                        ? 'bg-blue-100 text-blue-700'
                                                        : 'bg-accent-100 text-accent-700'
                                                    }`}>
                                                    {rec.type === 'job' ? 'Job' : 'Training'}
                                                </span>
                                            </div>
                                            <p className="text-sm text-gray-600 mb-1">{rec.description}</p>
                                            <div className="flex flex-wrap gap-3 text-xs text-gray-500">
                                                {rec.provider && (
                                                    <span className="flex items-center gap-1">
                                                        <GraduationCap className="w-3 h-3" /> {rec.provider}
                                                    </span>
                                                )}
                                                {rec.location && (
                                                    <span className="flex items-center gap-1">
                                                        <MapPin className="w-3 h-3" /> {rec.location}
                                                    </span>
                                                )}
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>

                        <button
                            onClick={() => { setResults(null); setError(null); }}
                            className="w-full py-3 flex items-center justify-center gap-2 text-primary-600 font-semibold hover:bg-primary-50 rounded-xl transition-colors"
                        >
                            <ArrowLeft className="w-4 h-4" /> Search Again
                        </button>
                    </div>
                )}
            </div>
        </div>
    );
};

export default SkillJobForm;
