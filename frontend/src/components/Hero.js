import React from 'react';

function Hero() {
    return (
        <section className="hero" id="home">
            <div className="hero-content">
                <div className="badge">
                    <i className="fas fa-sparkles"></i> AI-Powered Learning
                </div>
                <h1>
                    <span className="highlight">ExamGPT</span><br />
                    Ace your exams with AI
                </h1>
                <p className="subtitle">
                    Upload your notes, ask anything, and get instant, intelligent answers.
                    Powered by advanced RAG and Gemini — your personal exam assistant.
                </p>
                <a 
                    href="https://examgpt.streamlit.app/"
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
        </section>
    );
}

export default Hero;