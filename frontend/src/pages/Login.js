import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      // FastAPI, application/x-www-form-urlencoded formatında veri bekliyor
      const formData = new URLSearchParams();
      formData.append('username', username);
      formData.append('password', password);

      const response = await axios.post('http://127.0.0.1:8000/login', formData, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      });

      console.log('Giriş başarılı:', response.data);

      // Genellikle FastAPI JWT token döndürür
      localStorage.setItem('token', response.data.access_token);

      // Başarılı girişten sonra yönlendir
      navigate('/dashboard');

    } catch (error) {
      console.error('Giriş başarısız:', error.response?.data || error.message);
      alert('Giriş başarısız. Lütfen bilgilerinizi kontrol edin.');
    }
  };

  return (
    <div style={styles.container}>
      <h2>Giriş Yap</h2>
      <form onSubmit={handleSubmit} style={styles.form}>
        <input
          type="text"
          placeholder="Kullanıcı Adı"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          style={styles.input}
          required
        />
        <input
          type="password"
          placeholder="Şifre"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          style={styles.input}
          required
        />
        <button type="submit" style={styles.button}>Giriş Yap</button>
      </form>

      <p style={{ marginTop: '20px' }}>
        Hesabınız yok mu?{' '}
        <button onClick={() => navigate('/register')} style={styles.registerButton}>
          Kayıt Ol
        </button>
      </p>
    </div>
  );
}

const styles = {
  container: {
    marginTop: '100px',
    textAlign: 'center',
  },
  form: {
    display: 'inline-block',
    flexDirection: 'column',
  },
  input: {
    display: 'block',
    padding: '10px',
    width: '250px',
    margin: '10px auto',
    fontSize: '16px',
  },
  button: {
    padding: '10px 20px',
    fontSize: '16px',
    cursor: 'pointer',
  },
  registerButton: {
    padding: '5px 10px',
    fontSize: '14px',
    backgroundColor: '#eee',
    border: '1px solid #999',
    borderRadius: '4px',
    cursor: 'pointer',
  },
};

export default Login;
