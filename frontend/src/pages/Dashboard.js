import React, { useEffect, useState } from 'react';
import axios from 'axios';

const Dashboard = () => {
  const [balance, setBalance] = useState(null);
  const [transactions, setTransactions] = useState([]);
  const token = localStorage.getItem('token');

  useEffect(() => {
    // Balance verisini çek
    axios.get('http://127.0.0.1:8000/balance', {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
    .then(res => {
      setBalance(res.data.balance);
    })
    .catch(err => {
      console.error('Balance error:', err);
    });

    // Transactions verisini çek
    axios.get('http://127.0.0.1:8000/transactions', {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
    .then(res => {
      setTransactions(res.data);
    })
    .catch(err => {
      console.error('Transactions error:', err);
    });
  }, [token]);

  return (
    <div style={{ padding: '30px', fontFamily: 'Poppins, sans-serif', color: '#273F4F' }}>
      <h1 style={{ marginBottom: '20px' }}>📊 Kullanıcı Paneli</h1>

      <div style={{ marginBottom: '30px', fontSize: '20px' }}>
        <strong>💰 Bakiye:</strong>{' '}
        {balance !== null ? `${balance} ₺` : 'Yükleniyor...'}
      </div>

      <div>
        <h3>📄 İşlem Geçmişi</h3>
        <ul style={{ listStyle: 'none', padding: 0 }}>
          {transactions.length > 0 ? (
            transactions.map((txn, index) => (
              <li key={index} style={{ marginBottom: '10px', background: '#f2f2f2', padding: '10px', borderRadius: '8px' }}>
                <strong>{txn.date}</strong><br />
                {txn.description} <br />
                <span style={{ color: txn.amount >= 0 ? 'green' : 'red' }}>
                  {txn.amount} ₺
                </span>
              </li>
            ))
          ) : (
            <p>İşlem bulunamadı veya yükleniyor...</p>
          )}
        </ul>
      </div>
    </div>
  );
};

export default Dashboard;
