import React, { useState } from 'react';
import { eligibilityService } from '../services/api';
import { CheckCircle2, AlertCircle, Loader2, ArrowLeft, MapPin, User, Wallet, Tag } from 'lucide-react';

const EligibilityForm = () => {
    const [formData, setFormData] = useState({
        age: '',
        income: '',
        category: 'General',
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
            const response = await eligibilityService.checkEligibility({
                age: parseInt(formData.age),
                income: parseFloat(formData.income),
                category: formData.category,
                location: formData.location
            });
            setResults(response);
        } catch (err) {
            console.error(err);
            setError('Failed to check eligibility. Please make sure the backend is running.');
        }
        setLoading(false);
    };

    const handleChange = (field, value) => {
        setFormData(prev => ({ ...prev, [field]: value }));
    };

    return (
        <div className="max-w-xl mx-auto">
            <div className="mb-6 text-center md:text-left">
                <h2 className="section-title">Eligibility Checker</h2>
                <p className="text-gray-500 text-sm mt-1">
                    Enter your details to find schemes you qualify for.
                </p>
            </div>

            <div className="glass-card p-6 md:p-8">
                {!results ? (
                    <form onSubmit={handleSubmit} className="space-y-5">
                        <div>
                            <label className="label-text flex items-center gap-1.5">
                                <User className="w-4 h-4 text-gray-400" /> Age
                            </label>
                            <input
                                type="number"
                                required
                                min="1"
                                max="120"
                                className="input-field"
                                placeholder="Enter your age"
                                value={formData.age}
                                onChange={(e) => handleChange('age', e.target.value)}
                            />
                        </div>

                        <div>
                            <label className="label-text flex items-center gap-1.5">
                                <Wallet className="w-4 h-4 text-gray-400" /> Annual Family Income (₹)
                            </label>
                            <input
                                type="number"
                                required
                                min="0"
                                className="input-field"
                                placeholder="e.g. 250000"
                                value={formData.income}
                                onChange={(e) => handleChange('income', e.target.value)}
                            />
                        </div>

                        <div>
                            <label className="label-text flex items-center gap-1.5">
                                <Tag className="w-4 h-4 text-gray-400" /> Category
                            </label>
                            <select
                                className="input-field"
                                value={formData.category}
                                onChange={(e) => handleChange('category', e.target.value)}
                            >
                                <option value="General">General</option>
                                <option value="SC">Scheduled Caste (SC)</option>
                                <option value="ST">Scheduled Tribe (ST)</option>
                                <option value="OBC">Other Backward Class (OBC)</option>
                            </select>
                        </div>

                        <div>
                            <label className="label-text flex items-center gap-1.5">
                                <MapPin className="w-4 h-4 text-gray-400" /> Location (State/City)
                            </label>
                            <input
                                type="text"
                                required
                                className="input-field"
                                placeholder="e.g. Maharashtra"
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
                                    Checking...
                                </>
                            ) : (
                                'Check My Eligibility'
                            )}
                        </button>
                    </form>
                ) : (
                    <div className="space-y-5 animate-fade-in">
                        {/* AI Explanation */}
                        <div className="p-4 bg-primary-50 rounded-xl border border-primary-100">
                            <h4 className="text-sm font-bold text-primary-700 uppercase mb-2">AI Analysis</h4>
                            <p className="text-gray-800 text-sm leading-relaxed whitespace-pre-wrap">
                                {results.ai_explanation}
                            </p>
                        </div>

                        {/* Eligible Schemes */}
                        <h3 className="text-lg font-semibold text-gray-700">
                            {results.total_found > 0
                                ? `${results.total_found} Scheme${results.total_found > 1 ? 's' : ''} Found`
                                : 'No Matching Schemes'}
                        </h3>

                        {results.eligible_schemes && results.eligible_schemes.length > 0 ? (
                            <div className="space-y-3">
                                {results.eligible_schemes.map((scheme, i) => (
                                    <div key={i} className="p-4 bg-accent-50 border border-accent-200 rounded-xl">
                                        <div className="flex items-center gap-2 mb-2">
                                            <CheckCircle2 className="w-5 h-5 text-accent-600 flex-shrink-0" />
                                            <span className="font-semibold text-gray-800">{scheme.name}</span>
                                            <span className="ml-auto text-xs px-2 py-0.5 bg-accent-100 text-accent-700 rounded-full">
                                                {scheme.category}
                                            </span>
                                        </div>
                                        <p className="text-sm text-gray-600 mb-2">{scheme.benefits}</p>
                                        <div className="text-xs text-gray-500 space-y-1">
                                            <p><strong>Documents:</strong> {scheme.documents_required}</p>
                                            <p><strong>How to apply:</strong> {scheme.application_process}</p>
                                            {scheme.contact_info && (
                                                <p><strong>Contact:</strong> {scheme.contact_info}</p>
                                            )}
                                        </div>
                                    </div>
                                ))}
                            </div>
                        ) : (
                            <div className="p-4 bg-yellow-50 border border-yellow-200 rounded-xl flex items-start gap-3">
                                <AlertCircle className="w-5 h-5 text-yellow-600 flex-shrink-0 mt-0.5" />
                                <p className="text-gray-700 text-sm">
                                    No schemes matched your current criteria. Try adjusting your income, age, or category.
                                </p>
                            </div>
                        )}

                        <button
                            onClick={() => { setResults(null); setError(null); }}
                            className="w-full py-3 flex items-center justify-center gap-2 text-primary-600 font-semibold hover:bg-primary-50 rounded-xl transition-colors"
                        >
                            <ArrowLeft className="w-4 h-4" /> Check Again
                        </button>
                    </div>
                )}
            </div>
        </div>
    );
};

export default EligibilityForm;
