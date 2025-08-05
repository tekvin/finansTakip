import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './Login.css';

function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const formData = new URLSearchParams();
      formData.append('username', username);
      formData.append('password', password);

      const response = await axios.post('http://127.0.0.1:8000/login', formData, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      });

      console.log('Giriş başarılı:', response.data);
      localStorage.setItem('token', response.data.access_token);
      navigate('/dashboard');
    } catch (error) {
      console.error('Giriş başarısız:', error.response?.data || error.message);
      alert('Giriş başarısız. Lütfen bilgilerinizi kontrol edin.');
    }
  };

  return (
    <>
      <div className="login-title">Giriş Yap</div>
      <div className="login-container">
        <form onSubmit={handleSubmit} className="login-form">
          <div className="input-group">
            <div className="icon-wrapper">
              <i className="fas fa-user"></i>
            </div>
            <input
              type="text"
              placeholder="Kullanıcı Adı"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="login-input"
              required
            />
          </div>

          <div className="input-group">
            <div className="icon-wrapper">
              <i className="fas fa-lock"></i>
            </div>
            <input
              type="password"
              placeholder="Şifre"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="login-input"
              required
            />
          </div>

          <button type="submit" className="login-button">Giriş Yap</button>
        </form>

        <p style={{ marginTop: '20px' }}>
          Hesabınız yok mu?{' '}
          <button onClick={() => navigate('/register')} className="register-button">
            Kayıt Ol
          </button>
        </p>
      </div>
    </>
  );
}

export default Login;
