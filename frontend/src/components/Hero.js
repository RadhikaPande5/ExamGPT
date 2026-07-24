import React from 'react';

function Hero() {
    return (
        <section className="hero" id="home">
            {/* Background Particles */}
            <div className="particle"></div>
            <div className="particle"></div>
            <div className="particle"></div>
            
            <div className="hero-content">
                <div className="badge">
                    <i className="fas fa-sparkles"></i> AI-Powered Learning
                </div>
                <h1>
                    <i className="fas fa-robot"></i> <span className="highlight">ExamGPT</span><br />
                    Ace your exams with AI
                </h1>
                <p className="subtitle">
                    Upload your notes, ask anything, and get instant, intelligent answers.
                    Powered by advanced RAG and Gemini — your personal exam assistant.
                </p>
                <a 
                    href="http://localhost:8501"
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="btn-primary" 
                    style={{ 
                        padding: '0.8rem 2.8rem', 
                        fontSize: '1.1rem',
                        textDecoration: 'none',
                        display: 'inline-block'
                    }}
                >
                    <i className="fas fa-rocket"></i> Get started
                </a>
            </div>
            
            <div className="hero-illustration">
                <div className="image-container">
                    <i className="fas fa-brain floating-icons"></i>
                    <i className="fas fa-microchip floating-icons"></i>
                    <i className="fas fa-cloud floating-icons"></i>
                    <i className="fas fa-database floating-icons"></i>
                    <i className="fas fa-graduation-cap main-icon"></i>
                    <div className="tech-stack">
                        <span>🤖 AI</span>
                        <span>⚡ RAG</span>
                        <span>🧠 Gemini</span>
                        <span>📊 ML</span>
                    </div>
                </div>
            </div>
        </section>
    );
}

export default Hero;