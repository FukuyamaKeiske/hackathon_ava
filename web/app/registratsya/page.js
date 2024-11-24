'use client'
import { useState } from 'react';
import { registerUser } from '../services/authService';

export default function Home() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');

  const handleRegister = async () => {
    try {
      const result = await registerUser(email, password);
      setMessage('Регистрация успешна: ' + result.user_id);
    } catch (error) {
      setMessage('Ошибка: ' + error.message);
    }
  };

  return (
    <div className="bg-[url('/img/bg.png')] flex justify-center items-center min-h-screen">
      <div className="w-[90vw] h-[90vh] bg-[#d9d9d9]/0 rounded-[30px] border-4 border-[#83f8a0] flex justify-center items-center flex-col gap-10">
        <div className="w-[984px] h-72 bg-[#d9d9d9]/10 rounded-[90px] backdrop-blur-[50px] flex justify-start items-center flex-col">
          <div className="w-[566px] h-28 text-[#84f8a1] text-[80px] font-bold font-['Angst']">Регистрация</div>
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="text-white w-[810px] h-[73px] bg-[#d9d9d9]/10 rounded-[30px] border-4 border-[#83f8a0] backdrop-blur-[50px]"
          />
          <input
            type="password"
            placeholder="Пароль"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="text-white w-[810px] h-[73px] bg-[#d9d9d9]/10 rounded-[30px] border-4 border-[#83f8a0] backdrop-blur-[50px]"
          />
        </div>
        <div onClick={handleRegister} className="w-[869px] h-[129px] bg-[#d9d9d9]/10 rounded-[30px] backdrop-blur-[50px] flex justify-center items-center flex-col mt-[250px] cursor-pointer">
          <div className="w-[579px] h-14 text-[#eaa1fc] text-[65px] font-bold font-['Angst'] flex justify-center items-center flex-col">Зарегистрироваться</div>
        </div>
        {message && <div className="text-white">{message}</div>}
      </div>
    </div>
  );
}
