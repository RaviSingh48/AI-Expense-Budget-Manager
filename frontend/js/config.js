const isLocal = typeof window !== 'undefined' && (
  window.location.hostname === 'localhost' ||
  window.location.hostname === '127.0.0.1' ||
  window.location.hostname === '0.0.0.0'
);

export const CONFIG = {
  API_BASE_URL: isLocal 
    ? 'http://127.0.0.1:8000/api/v1' 
    : 'https://ai-budget-expense-advisor-4.onrender.com/api/v1',
  DEFAULT_PAGE_SIZE: 20,
  CATEGORIES: [
    'Food', 'Shopping', 'Transport', 'Medical',
    'Entertainment', 'Bills', 'Education', 'Travel', 'Others'
  ],
  PAYMENT_METHODS: ['Cash', 'Credit Card', 'Debit Card', 'UPI', 'Bank Transfer']
};
