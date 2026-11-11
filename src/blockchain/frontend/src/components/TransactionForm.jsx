import React, { useState } from 'react';

export default function TransactionForm({ onSubmit }) {
  const [recipient, setRecipient] = useState('');
  const [amount, setAmount] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (onSubmit) {
      onSubmit({ recipient, amount: Number(amount) });
    }
  };

  return (
    <section className="transaction-form">
      <h2>Create Transaction</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Recipient Address: </label>
          <input
            type="text"
            value={recipient}
            onChange={(e) => setRecipient(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Amount: </label>
          <input
            type="number"
            value={amount}
            onChange={(e) => setAmount(e.target.value)}
            required
          />
        </div>
        <button type="submit">Send</button>
      </form>
    </section>
  );
}
