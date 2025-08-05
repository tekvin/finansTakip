import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './Login.css'; // Aynı CSS dosyasını kullanıyoruz

const Register = () => {
  const [form, setForm] = useState({
    username: '',
    email: '',
    password: '',
  });

  const [message, setMessage] = useState('');
  const navigate = useNavigate();

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post('http://127.0.0.1:8000/register', form, {
        headers: {
          'Content-Type': 'application/json',
        },
      });
      setMessage('✅ Kayıt başarılı!');
      setTimeout(() => navigate('/login'), 1500); // Başarılıysa login sayfasına yönlendir
    } catch (error) {
      console.error(error);
      setMessage('❌ Kayıt başarısız: ' + (error.response?.data?.detail || 'Sunucu hatası'));
    }
  };

  return (
    <>
      <div className="login-title">Kayıt Ol</div>
      <div className="login-container">
        <form onSubmit={handleSubmit} className="login-form">
          <div className="input-group">
            <div className="icon-wrapper">
              <i className="fas fa-user"></i>
            </div>
            <input
              type="text"
              name="username"
              placeholder="Kullanıcı Adı"
              value={form.username}
              onChange={handleChange}
              className="login-input"
              required
            />
          </div>

          <div className="input-group">
            <div className="icon-wrapper">
              <i className="fas fa-envelope"></i>
            </div>
            <input
              type="email"
              name="email"
              placeholder="E-posta"
              value={form.email}
              onChange={handleChange}
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
              name="password"
              placeholder="Şifre"
              value={form.password}
              onChange={handleChange}
              className="login-input"
              required
            />
          </div>

          <button type="submit" className="login-button">Kayıt Ol</button>
        </form>

        {message && <p style={{ marginTop: '16px', color: '#9ba8ab' }}>{message}</p>}

        <p>
          Zaten hesabınız var mı?{' '}
          <button onClick={() => navigate('/login')} className="register-button">
            Giriş Yap
          </button>
        </p>
      </div>
    </>
  );
};

export default Register;
