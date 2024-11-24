export async function addBusiness(userId, name, sphere, size, type, specialization) {
    const response = await fetch('http://localhost:8000/add_business', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ user_id: userId, name, sphere, size, type, specialization }),
    });
  
    if (!response.ok) {
      throw new Error('Ошибка добавления бизнеса');
    }
  
    return response.json();
  }
  
  export async function getUserBusinesses(userId) {
    const response = await fetch(`http://localhost:8000/user_businesses/${userId}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });
  
    if (!response.ok) {
      throw new Error('Ошибка получения бизнеса');
    }
  
    return response.json();
  }
  