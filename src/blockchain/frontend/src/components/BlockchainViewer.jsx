import React from 'react';
import BlockCard from './BlockCard';

export default function BlockchainViewer({ chain = [] }) {
  return (
    <section className="blockchain-viewer">
      <h2>Blockchain Explorer</h2>
      <div className="chain-list">
        {chain.map((block, idx) => (
          <BlockCard key={block.hash || idx} block={block} />
        ))}
      </div>
    </section>
  );
}
