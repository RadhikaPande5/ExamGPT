import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Hero from './components/Hero';
import About from './components/About';
import Services from './components/Services';
import Contact from './components/Contact';
import Footer from './components/Footer';
import Login from './components/Login';
import './styles/App.css';

function App() {
    return (
        <Router>
            <div className="app">
                <Navbar />
                <Routes>
                    {/* Home Page - Sab sections yahan */}
                    <Route path="/" element={
                        <>
                            <Hero />
                            <About />
                            <Services />
                            <Contact />
                            <Footer />
                        </>
                    } />
                    {/* Login Page - Alag se */}
                    <Route path="/login" element={<Login />} />
                </Routes>
            </div>
        </Router>
    );
}

export default App;