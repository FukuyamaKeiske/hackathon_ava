export async function registerUser(email, password) {
    const response = await fetch('http://localhost:8000/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, password }),
    });
  
    if (!response.ok) {
      throw new Error('Ошибка регистрации');
    }
  
    return response.json();
  }
  
  export async function authenticateUser(email, password) {
    const response = await fetch('http://localhost:8000/authenticate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, password }),
    });
  
    if (!response.ok) {
      throw new Error('Ошибка аутентификации');
    }
  
    return response.json();
  }
  