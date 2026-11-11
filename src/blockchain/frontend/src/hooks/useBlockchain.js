import { useState, useEffect } from 'react';
import { fetchBlockchain } from '../api/client';

export function useBlockchain() {
  const [chain, setChain] = useState([]);
  const [loading, setLoading] = useState(true);

  const loadChain = async () => {
    try {
      const data = await fetchBlockchain();
      setChain(data);
    } catch (err) {
      console.error('Failed to load blockchain', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadChain();
  }, []);

  return { chain, loading, reload: loadChain };
}
