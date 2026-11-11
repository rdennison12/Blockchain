import React from 'react';

export default function WalletCard({ address = '', balance = 0 }) {
  return (
    <section className="wallet-card">
      <h2>Wallet Info</h2>
      <p><strong>Address:</strong> {address || 'Loading...'}</p>
      <p><strong>Balance:</strong> {balance}</p>
    </section>
  );
}
