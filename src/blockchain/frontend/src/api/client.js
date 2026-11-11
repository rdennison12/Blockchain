const API_BASE = '/api';

export async function fetchBlockchain() {
  const res = await fetch(`${API_BASE}/blockchain`);
  if (!res.ok) throw new Error('Failed to fetch blockchain');
  return res.json();
}

export async function fetchWalletInfo() {
  const res = await fetch(`${API_BASE}/wallet/info`);
  if (!res.ok) throw new Error('Failed to fetch wallet info');
  return res.json();
}

export async function sendTransaction(recipient, amount) {
  const res = await fetch(`${API_BASE}/wallet/transact`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ recipient, amount })
  });
  if (!res.ok) throw new Error('Transaction failed');
  return res.json();
}

export async function fetchTransactionPool() {
  const res = await fetch(`${API_BASE}/transactions/pool`);
  if (!res.ok) throw new Error('Failed to fetch transaction pool');
  return res.json();
}

export async function mineBlock() {
  const res = await fetch(`${API_BASE}/blockchain/mine`, {
    method: 'POST'
  });
  if (!res.ok) throw new Error('Mining block failed');
  return res.json();
}
