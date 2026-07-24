import React from 'react';

const services = [
    { 
        icon: 'fa-cloud-upload-alt', 
        title: 'Upload & Parse', 
        desc: 'Upload PDFs, docs, or images. Our parser extracts clean text for instant indexing.', 
        action: 'Try now',
        link: 'http://localhost:8501'
    },
    { 
        icon: 'fa-robot', 
        title: 'RAG + Gemini', 
        desc: 'State‑of‑the‑art retrieval with Gemini for accurate, human‑like answers.', 
        action: 'Explore',
        link: 'http://localhost:8501'
    },
    { 
        icon: 'fa-comment-dots', 
        title: 'Smart Chat', 
        desc: 'Ask anything about your materials. Get detailed explanations, summaries, and more.', 
        action: 'Chat now',
        link: 'http://localhost:8501'
    },
    { 
        icon: 'fa-chart-line', 
        title: 'Performance Insights', 
        desc: 'Track your progress, identify weak topics, and get personalized recommendations.', 
        action: 'Learn more',
        link: 'http://localhost:8501'
    }
];

function Services() {
    return (
        <section id="services" className="services-section">
            <h2 className="section-title"><i className="fas fa-cogs"></i> Our Services</h2>
            <div className="services-grid">
                {services.map((service, index) => (
                    <div className="service-card" key={index}>
                        <i className={`fas ${service.icon}`}></i>
                        <h3>{service.title}</h3>
                        <p>{service.desc}</p>
                        <a 
                            href={service.link}
                            target="_blank" 
                            rel="noopener noreferrer"
                            className="service-btn"
                            style={{ 
                                textDecoration: 'none', 
                                display: 'inline-block',
                                color: 'white'
                            }}
                        >
                            {service.action} 
                            <i className="fas fa-external-link-alt" style={{ marginLeft: '5px', fontSize: '0.8rem' }}></i>
                        </a>
                    </div>
                ))}
            </div>
        </section>
    );
}

export default Services;