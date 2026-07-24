import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';

function Navbar() {
    const [menuOpen, setMenuOpen] = useState(false);
    const navigate = useNavigate();

    // Smooth scroll to section
    const scrollToSection = (sectionId) => {
        const element = document.getElementById(sectionId);
        if (element) {
            element.scrollIntoView({ behavior: 'smooth' });
        }
    };

    // Go to home page
    const goHome = () => {
        navigate('/');
        setTimeout(() => {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }, 100);
    };

    return (
        <nav className="navbar">
            <div className="logo" onClick={goHome} style={{ cursor: 'pointer' }}>
                <i className="fas fa-graduation-cap"></i>
                <span>Exam</span><span className="gpt-text">GPT</span>
            </div>
            
            <div className="hamburger" onClick={() => setMenuOpen(!menuOpen)}>
                <i className="fas fa-bars"></i>
            </div>
            
            <div className={`nav-links ${menuOpen ? 'open' : ''}`}>
                <a href="#about" onClick={(e) => {
                    e.preventDefault();
                    scrollToSection('about');
                    setMenuOpen(false);
                }}>
                    About
                </a>
                
                <a href="#services" onClick={(e) => {
                    e.preventDefault();
                    scrollToSection('services');
                    setMenuOpen(false);
                }}>
                    Services
                </a>
                
                <a href="#contact" onClick={(e) => {
                    e.preventDefault();
                    scrollToSection('contact');
                    setMenuOpen(false);
                }}>
                    Contact
                </a>
                
                <div className="nav-actions">
                    <Link to="/login">
                        <button className="btn-outline"><i className="fas fa-sign-in-alt"></i> Login</button>
                    </Link>
                    
                    <Link to="/login?mode=register">
                        <button className="btn-primary"><i className="fas fa-user-plus"></i> Register</button>
                    </Link>
                    
                    <button className="theme-toggle" style={{ cursor: 'default' }}>
                        <i className="fas fa-moon"></i>
                    </button>
                </div>
            </div>
        </nav>
    );
}

export default Navbar;