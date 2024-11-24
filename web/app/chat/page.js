'use client'
import { useState } from 'react';
import { getUserBusinesses } from '../services/businessService';

export default function Home() {
  const [showNav, setShowNav] = useState(false);
  const [value, setValue] = useState("");
  const [usermessage, setUsermessage] = useState("");
  const [bot, setBot] = useState("");
  const [businesses, setBusinesses] = useState([]);

  const handleFetchBusinesses = async (userId) => {
    try {
      const result = await getUserBusinesses(userId);
      setBusinesses(result.businesses);
    } catch (error) {
      console.error('Ошибка:', error.message);
    }
  };

  const handleSendMessage = () => {
    setUsermessage(value);
    setValue("");
    setBot("Ваше сообщение отправлено.");
  };

  return (
    <div className="bg-[url('/img/bg.png')] flex justify-center items-center min-h-screen">
      <div className="w-[90vw] h-[90vh] bg-[#d9d9d9]/0 rounded-[30px] border-4 border-[#83f8a0] flex justify-start items-center flex-col gap-10 p-10">
        <div onClick={() => setShowNav(!showNav)} className="flex justify-start items-start flex-row w-[100%]">
          <div className="relative">
            <img className=" " src="/img/button-circle.png"/>
            <img className="absolute top-[50%] left-[50%] translate-x-[-50%] translate-y-[-50%]" src="/img/union.png"/>
          </div>
          <a href="/biznes" className="relative self-end ml-auto">
            <img className=" " src="/img/button-circle.png"/>
            <img className="absolute h-[58px] w-[49px] top-[50%] left-[50%] translate-x-[-50%] translate-y-[-50%]" src="/img/user.png"/>
          </a>
        </div>

        <div className="flex justify-center items-end flex-col w-[100%]">
          <div className="text-white font-bold text-xl p-3 bg-[#cffef6]/10 rounded-[30px] border-4 border-[#83f8a0]">{usermessage}</div>
        </div>

        <div className="flex justify-center items-start flex-col w-[100%]">
          <div className="bg-[#e0f0f9]/10 rounded-[30px] border-4 border-[#eaa1fc] p-3">
            <pre className="text-white font-bold text-l font-[Angst]">{bot}</pre>
          </div>
        </div>

        <div className="fixed w-[85%] top-[85%] flex justify-start items-start flex-row mt-auto">
          <input value={value} onChange={(v) => setValue(v.target.value)} className="text-white pl-20 w-[95%] h-[76px] bg-[#d9d9d9]/10 rounded-[90px] shadow border-4 border-[#83f8a0]"></input>
          <img className="absolute translate-y-4 translate-x-7" src="/img/attach_file.png"/>
          <div className="relative self-end ml-auto" onClick={handleSendMessage}>
            <img className="h-[76px] w-[76px]" src="/img/button-circle.png"/>
            <img className="absolute top-[50%] left-[50%] translate-x-[-50%] translate-y-[-50%]" src="/img/lupa.png"/>
          </div>
        </div>
      </div>

      <div style={{backdropFilter: "blur(20px)"}} className={"absolute w-full h-screen backdrop-blur-lg flex justify-end items-center flex-col " + (showNav ? "block" : "hidden")}>
        <div className="w-[837px] h-[639px] p-10 bg-[#d9d9d9]/10 border-4 border-[#eaa1fc] backdrop-blur-lg mb-20 flex justify-start items-center flex-col gap-5">
          <div onClick={() => setShowNav(!showNav)} className="text-xl text-white border-[#F8E984] border-4 p-3 rounded-full">Закрыть</div>
          <div className="w-[791px] h-[73px] bg-[#d9d9d9]/10 rounded-[30px] border-4 border-[#83f8a0] backdrop-blur-[50px]"></div>
          <div className="w-[791px] h-[73px] bg-[#d9d9d9]/10 rounded-[30px] border-4 border-[#83f8a0] backdrop-blur-[50px]"></div>
          <div className="w-[791px] h-[73px] bg-[#d9d9d9]/10 rounded-[30px] border-4 border-[#F8E984] backdrop-blur-[50px] flex justify-center items-center flex-col">
            <img className="" src="/img/Icon.png"/>
          </div>
        </div>
      </div>
    </div>
  );
}
