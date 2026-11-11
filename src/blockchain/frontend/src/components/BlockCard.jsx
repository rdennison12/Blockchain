import React from 'react';

export default function BlockCard({ block }) {
  return (
    <div className="block-card">
      <h3>Block #{block?.index ?? '0'}</h3>
      <p><strong>Hash:</strong> {block?.hash}</p>
      <p><strong>Prev Hash:</strong> {block?.last_hash}</p>
      <p><strong>Timestamp:</strong> {block?.timestamp}</p>
      <p><strong>Difficulty:</strong> {block?.difficulty} | <strong>Nonce:</strong> {block?.nonce}</p>
    </div>
  );
}
