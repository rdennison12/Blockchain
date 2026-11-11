import React from 'react';

export default function TransactionPool({ transactions = [], onMine }) {
  return (
    <section className="transaction-pool">
      <h2>Transaction Pool</h2>
      <button onClick={onMine}>Mine Pending Transactions</button>
      <ul>
        {transactions.map((tx, idx) => (
          <li key={tx.id || idx}>
            Tx ID: {tx.id} - Inputs: {JSON.stringify(tx.input)}
          </li>
        ))}
      </ul>
    </section>
  );
}
