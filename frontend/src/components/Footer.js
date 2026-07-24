import React from 'react';

function Footer() {
    return (
        <footer className="footer">
            {/* Wave Effect - Footer Ke Andar Top */}
            <div className="footer-wave-top">
                <div className="wave-top"></div>
            </div>
            
            <div className="footer-content">
                <div className="footer-links">
                    <a href="#home">Home</a>
                    <a href="#about">About</a>
                    <a href="#services">Services</a>
                    <a href="#contact">Contact</a>
                    <a href="#">Privacy</a>
                    <a href="#">Terms</a>
                </div>
                <div className="footer-social">
                    <i className="fab fa-twitter"></i>
                    <i className="fab fa-github"></i>
                    <i className="fab fa-linkedin"></i>
                    <i className="fab fa-instagram"></i>
                </div>
                <div className="footer-copy">
                    &copy; 2026 ExamGPT — built with <i className="fas fa-heart"></i> for students.
                </div>
            </div>
        </footer>
    );
}

export default Footer;