import React from 'react';

function Services() {
    return (
        <section id="services" className="services-section">
            <h2 className="section-title"><i className="fas fa-cogs"></i> Our Services</h2>
            <div className="services-grid">
                <div className="service-card">
                    <i className="fas fa-cloud-upload-alt"></i>
                    <h3>Upload & Parse</h3>
                    <p>Upload PDFs, docs, or images. Our parser extracts clean text for instant indexing.</p>
                </div>
                <div className="service-card">
                    <i className="fas fa-robot"></i>
                    <h3>RAG + Gemini</h3>
                    <p>State‑of‑the‑art retrieval with Gemini for accurate, human‑like answers.</p>
                </div>
                <div className="service-card">
                    <i className="fas fa-comment-dots"></i>
                    <h3>Smart Chat</h3>
                    <p>Ask anything about your materials. Get detailed explanations, summaries, and more.</p>
                </div>
                <div className="service-card">
                    <i className="fas fa-chart-line"></i>
                    <h3>Performance Insights</h3>
                    <p>Track your progress, identify weak topics, and get personalized recommendations.</p>
                </div>
            </div>

            {/* Try ExamGPT Button */}
            <div style={{ textAlign: 'center', marginTop: '3rem' }}>
                <a 
                    href="https://examgpt.streamlit.app/"
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="btn-primary"
                    style={{ 
                        padding: '1rem 3rem', 
                        fontSize: '1.2rem',
                        textDecoration: 'none',
                        display: 'inline-block',
                        borderRadius: '50px',
                        fontWeight: '700'
                    }}
                >
                    🚀 Try ExamGPT Now
                </a>
            </div>
        </section>
    );
}

export default Services;