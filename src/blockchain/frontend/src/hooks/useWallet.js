import { useState, useEffect } from 'react';
import { fetchWalletInfo, sendTransaction } from '../api/client';

export function useWallet() {
  const [wallet, setWallet] = useState({ address: '', balance: 0 });
  const [loading, setLoading] = useState(true);

  const loadWallet = async () => {
    try {
      const data = await fetchWalletInfo();
      setWallet(data);
    } catch (err) {
      console.error('Failed to load wallet', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadWallet();
  }, []);

  const transact = async (recipient, amount) => {
    await sendTransaction(recipient, amount);
    await loadWallet();
  };

  return { wallet, loading, transact, reload: loadWallet };
}
