import React, { useState, useRef } from 'react';
import { Upload, FileText, Loader2, CheckCircle, AlertCircle, ArrowLeft } from 'lucide-react';
import { documentService } from '../services/api';

const DocumentUpload = () => {
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState(null);
    const [error, setError] = useState(null);
    const [isDragging, setIsDragging] = useState(false);
    const fileInputRef = useRef(null);

    const handleFile = async (file) => {
        if (!file) return;

        // Validate file type
        const ext = file.name.split('.').pop().toLowerCase();
        if (!['txt', 'pdf'].includes(ext)) {
            setError('Please upload a .txt or .pdf file.');
            return;
        }

        // Validate file size (5MB limit)
        if (file.size > 5 * 1024 * 1024) {
            setError('File size must be less than 5MB.');
            return;
        }

        setLoading(true);
        setError(null);
        try {
            const data = await documentService.analyze(file);
            setResult(data);
        } catch (err) {
            console.error(err);
            setError('Error analyzing document. Please make sure the backend is running.');
        }
        setLoading(false);
    };

    const handleDrop = (e) => {
        e.preventDefault();
        setIsDragging(false);
        const file = e.dataTransfer.files[0];
        handleFile(file);
    };

    const handleDragOver = (e) => {
        e.preventDefault();
        setIsDragging(true);
    };

    const handleDragLeave = () => {
        setIsDragging(false);
    };

    return (
        <div className="max-w-xl mx-auto">
            <div className="mb-6 text-center md:text-left">
                <h2 className="section-title">Document Explainer</h2>
                <p className="text-gray-500 text-sm mt-1">
                    Upload a government document and get a simplified explanation.
                </p>
            </div>

            <div className="glass-card p-6 md:p-8">
                {!result ? (
                    <div>
                        {/* Drop Zone */}
                        <div
                            onDrop={handleDrop}
                            onDragOver={handleDragOver}
                            onDragLeave={handleDragLeave}
                            onClick={() => !loading && fileInputRef.current?.click()}
                            className={`border-2 border-dashed rounded-2xl p-10 flex flex-col items-center justify-center transition-all cursor-pointer ${isDragging
                                    ? 'border-primary-500 bg-primary-50 scale-[1.02]'
                                    : 'border-gray-300 hover:border-primary-400 hover:bg-gray-50'
                                }`}
                        >
                            <input
                                ref={fileInputRef}
                                type="file"
                                accept=".txt,.pdf"
                                className="hidden"
                                onChange={(e) => handleFile(e.target.files[0])}
                            />

                            <div className={`p-4 rounded-full mb-4 transition-colors ${isDragging ? 'bg-primary-100' : 'bg-primary-50'
                                }`}>
                                {loading ? (
                                    <Loader2 className="w-8 h-8 text-primary-600 animate-spin" />
                                ) : (
                                    <Upload className="w-8 h-8 text-primary-600" />
                                )}
                            </div>

                            <p className="text-gray-700 font-medium">
                                {loading ? 'Analyzing document...' : 'Click or drag document to simplify'}
                            </p>
                            <p className="text-gray-400 text-sm mt-1">
                                Supports PDF and Text files (Max 5MB)
                            </p>
                        </div>

                        {error && (
                            <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-xl text-red-700 text-sm flex items-center gap-2">
                                <AlertCircle className="w-4 h-4 flex-shrink-0" />
                                {error}
                            </div>
                        )}
                    </div>
                ) : (
                    <div className="space-y-5 animate-fade-in">
                        {/* Success Header */}
                        <div className="flex items-center gap-2 text-accent-600">
                            <CheckCircle className="w-5 h-5" />
                            <span className="font-semibold">Analysis Complete</span>
                            <span className="ml-auto text-xs text-gray-400 flex items-center gap-1">
                                <FileText className="w-3 h-3" /> {result.filename}
                            </span>
                        </div>

                        {/* Simplified Version */}
                        <div className="p-4 bg-gray-50 rounded-xl border border-gray-200">
                            <h4 className="text-sm font-bold text-gray-500 uppercase mb-2">Simplified Explanation</h4>
                            <p className="text-gray-800 leading-relaxed text-sm whitespace-pre-wrap">
                                {result.simplification}
                            </p>
                        </div>

                        {/* Next Steps */}
                        {result.next_steps && (
                            <div className="p-4 bg-accent-50 rounded-xl border border-accent-100">
                                <h4 className="text-sm font-bold text-accent-700 uppercase mb-2">Next Steps</h4>
                                <p className="text-gray-800 text-sm leading-relaxed whitespace-pre-wrap">
                                    {result.next_steps}
                                </p>
                            </div>
                        )}

                        {/* Original Summary */}
                        <div className="p-4 bg-primary-50 rounded-xl border border-primary-100">
                            <h4 className="text-sm font-bold text-primary-700 uppercase mb-2">Original Extract</h4>
                            <p className="text-primary-900/80 text-sm italic leading-relaxed">
                                "{result.summary}"
                            </p>
                        </div>

                        <button
                            onClick={() => { setResult(null); setError(null); }}
                            className="w-full py-3 flex items-center justify-center gap-2 text-primary-600 font-semibold hover:bg-primary-50 rounded-xl transition-colors"
                        >
                            <ArrowLeft className="w-4 h-4" /> Upload Another
                        </button>
                    </div>
                )}
            </div>
        </div>
    );
};

export default DocumentUpload;
