import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import WalletCard from './components/WalletCard';
import TransactionForm from './components/TransactionForm';
import TransactionPool from './components/TransactionPool';
import BlockchainViewer from './components/BlockchainViewer';
import { useBlockchain } from './hooks/useBlockchain';
import { useWallet } from './hooks/useWallet';
import { fetchTransactionPool, mineBlock } from './api/client';

function App() {
  const { chain, reload: reloadBlockchain } = useBlockchain();
  const { wallet, transact, reload: reloadWallet } = useWallet();
  const [transactions, setTransactions] = useState([]);

  const loadPool = async () => {
    try {
      const data = await fetchTransactionPool();
      setTransactions(data);
    } catch (err) {
      console.error('Failed to load transaction pool', err);
    }
  };

  useEffect(() => {
    loadPool();
  }, []);

  const handleTransact = async ({ recipient, amount }) => {
    try {
      await transact(recipient, amount);
      await loadPool();
    } catch (err) {
      alert(`Transaction failed: ${err.message}`);
    }
  };

  const handleMine = async () => {
    try {
      await mineBlock();
      await reloadBlockchain();
      await reloadWallet();
      await loadPool();
    } catch (err) {
      alert(`Mining failed: ${err.message}`);
    }
  };

  return (
    <div className="app-container">
      <Navbar />
      <main className="content">
        <WalletCard address={wallet.address} balance={wallet.balance} />
        <TransactionForm onSubmit={handleTransact} />
        <TransactionPool transactions={transactions} onMine={handleMine} />
        <BlockchainViewer chain={chain} />
      </main>
    </div>
  );
}

export default App;
