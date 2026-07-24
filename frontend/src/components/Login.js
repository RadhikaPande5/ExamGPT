import React, { useState, useEffect } from 'react';
import { useLocation, Link } from 'react-router-dom';

function Login() {
    const location = useLocation();
    
    // Check URL parameter for register mode
    const [isLogin, setIsLogin] = useState(true);
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');

    useEffect(() => {
        const params = new URLSearchParams(location.search);
        if (params.get('mode') === 'register') {
            setIsLogin(false);
        }
    }, [location]);

    const handleSubmit = (e) => {
        e.preventDefault();
        
        if (isLogin) {
            // LOGIN
            if (!email || !password) {
                alert('Please enter email and password');
                return;
            }
            alert('✅ Login successful! (Demo)');
            window.location.href = '/';
        } else {
            // REGISTER
            if (!name || !email || !password || !confirmPassword) {
                alert('Please fill all fields');
                return;
            }
            if (password !== confirmPassword) {
                alert('Passwords do not match!');
                return;
            }
            alert('✅ Registration successful! (Demo)');
            // Switch to login mode after registration
            setIsLogin(true);
        }
    };

    return (
        <div className="login-container">
            <div className="login-card">
                <div className="login-header">
                    <i className="fas fa-graduation-cap"></i>
                    <h2>{isLogin ? 'Welcome Back' : 'Create Account'}</h2>
                    <p>{isLogin ? 'Login to your ExamGPT account' : 'Start your learning journey'}</p>
                </div>

                <form onSubmit={handleSubmit} className="login-form">
                    {/* Register mode mein Name field */}
                    {!isLogin && (
                        <input 
                            type="text" 
                            placeholder="Full Name" 
                            value={name}
                            onChange={(e) => setName(e.target.value)}
                            required
                        />
                    )}
                    
                    <input 
                        type="email" 
                        placeholder="Email Address" 
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                    />
                    
                    <input 
                        type="password" 
                        placeholder="Password" 
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />
                    
                    {/* Register mode mein Confirm Password */}
                    {!isLogin && (
                        <input 
                            type="password" 
                            placeholder="Confirm Password" 
                            value={confirmPassword}
                            onChange={(e) => setConfirmPassword(e.target.value)}
                            required
                        />
                    )}
                    
                    {isLogin && (
                        <div className="login-options">
                            <label>
                                <input type="checkbox" /> Remember me
                            </label>
                            <a href="#">Forgot Password?</a>
                        </div>
                    )}

                    <button type="submit" className="login-btn">
                        {isLogin ? 'Login' : 'Register'}
                    </button>
                </form>

                <div className="login-footer">
                    <p>
                        {isLogin ? "Don't have an account?" : "Already have an account?"}
                        <span onClick={() => setIsLogin(!isLogin)}>
                            {isLogin ? ' Register' : ' Login'}
                        </span>
                    </p>
                </div>
            </div>
        </div>
    );
}

export default Login;