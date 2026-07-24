import React from 'react';

function Contact() {
    return (
        <section id="contact" className="contact-section">
            <div className="contact-flex">
                <div className="contact-info">
                    <h3><i className="fas fa-paper-plane" style={{ color: '#6c5ce7' }}></i> Contact Us</h3>
                    <p>Have a question or need help? Reach out — we'd love to hear from you.</p>
                    <div className="contact-item"><i className="fas fa-envelope"></i> support@examgpt.ai</div>
                    <div className="contact-item"><i className="fas fa-phone-alt"></i> +1 (555) 123-4567</div>
                    <div className="contact-item"><i className="fas fa-map-marker-alt"></i> 123 AI Avenue, San Francisco</div>
                    <div style={{ marginTop: '1rem', display: 'flex', gap: '1.2rem', fontSize: '1.5rem', color: '#6c5ce7' }}>
                        <i className="fab fa-twitter"></i>
                        <i className="fab fa-linkedin"></i>
                        <i className="fab fa-github"></i>
                        <i className="fab fa-youtube"></i>
                    </div>
                </div>
                <div className="contact-form">
                    <form onSubmit={(e) => { e.preventDefault(); alert('📬 Message sent! (demo)'); }}>
                        <input type="text" placeholder="Your name" required />
                        <input type="email" placeholder="Email address" required />
                        <textarea placeholder="How can we help?"></textarea>
                        <button type="submit"><i className="fas fa-paper-plane"></i> Send message</button>
                    </form>
                </div>
            </div>
        </section>
    );
}

export default Contact;