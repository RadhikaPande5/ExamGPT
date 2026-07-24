import React from 'react';

function About() {
    const features = [
        { 
            icon: 'fa-brain', 
            title: 'AI-Powered Learning', 
            desc: 'Advanced Gemini AI for accurate, human-like answers to your questions' 
        },
        { 
            icon: 'fa-vector-square', 
            title: 'Smart RAG System', 
            desc: 'Retrieval-Augmented Generation that finds the most relevant context' 
        },
        { 
            icon: 'fa-file-pdf', 
            title: 'Multi-Format Support', 
            desc: 'Upload PDFs, DOCX, TXT, and even images with OCR support' 
        },
        { 
            icon: 'fa-clock', 
            title: 'Real-Time Response', 
            desc: 'Get instant answers with zero waiting time for quick learning' 
        },
        { 
            icon: 'fa-shield-alt', 
            title: 'Secure & Private', 
            desc: 'Your data is encrypted and never shared with third parties' 
        },
        { 
            icon: 'fa-mobile-alt', 
            title: 'Access Anywhere', 
            desc: 'Study on any device - desktop, tablet, or mobile phone' 
        }
    ];

    return (
        <div id="about">
            <h2 className="section-title">
                <i className="fas fa-info-circle"></i> About ExamGPT
            </h2>
            
            <div className="about-grid">
                <div className="about-content">
                    <div className="about-text">
                        <p className="highlight-text">
                            <strong>ExamGPT</strong> is an AI-powered platform designed to help students 
                            prepare for exams with confidence. Upload your lecture notes, PDFs, or any 
                            study material — our system uses advanced Retrieval-Augmented Generation (RAG) 
                            combined with Google's Gemini to deliver precise, context-aware answers.
                        </p>
                        <p>
                            Whether you need a quick summary, a deep explanation, or practice questions,
                            ExamGPT adapts to your learning style. No more endless scrolling — just ask and learn.
                        </p>
                    </div>
                </div>
            </div>

            {/* Features - Horizontal Scroll */}
            <div className="features-section">
                <h3 className="features-title">
                    <i className="fas fa-star"></i> Why Choose ExamGPT?
                </h3>
                <div className="features-horizontal">
                    {features.map((feature, index) => (
                        <div className="feature-card" key={index}>
                            <div className="feature-icon">
                                <i className={`fas ${feature.icon}`}></i>
                            </div>
                            <h4>{feature.title}</h4>
                            <p>{feature.desc}</p>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}

export default About;