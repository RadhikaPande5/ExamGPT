import React from 'react';

function Contact() {
    return (
        <section id="contact" className="contact-section">
            <div className="contact-flex">
                <div className="contact-info">
                    <h3><i className="fas fa-paper-plane" style={{ color: '#6c5ce7' }}></i> Share Your Feedback</h3>
                    <p>We'd love to hear your thoughts! Share your feedback with us.</p>
                </div>
                <div className="contact-form">
                    <form onSubmit={(e) => { e.preventDefault(); alert('📬 Feedback sent! (demo)'); }}>
                        <input type="text" placeholder="Your name" required />
                        <input type="email" placeholder="Email address" required />
                        <textarea placeholder="Share your feedback..."></textarea>
                        <button type="submit"><i className="fas fa-paper-plane"></i> Send Feedback</button>
                    </form>
                </div>
            </div>
        </section>
    );
}

export default Contact;