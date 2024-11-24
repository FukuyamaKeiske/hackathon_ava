export async function processText(userId, text, businessId) {
    const response = await fetch('http://localhost:8000/process_text', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ user_id: userId, text, business_id: businessId }),
    });
  
    if (!response.ok) {
      throw new Error('Ошибка обработки текста');
    }
  
    return response.json();
  }
  