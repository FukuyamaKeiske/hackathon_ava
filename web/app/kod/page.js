import Image from "next/image";

export default function Home() {
  return (
      <div
          className="bg-[url('/img/bg.png')] flex justify-center items-center min-h-screen">
          <div
              className="w-[90vw] h-[90vh] bg-[#d9d9d9]/0 rounded-[30px] border-4 border-[#83f8a0] flex justify-center items-center flex-col gap-10">
              <div
                  className="w-[984px] h-72 bg-[#d9d9d9]/10 rounded-[90px] backdrop-blur-[50px] flex justify-start items-center flex-col">
                  <div className="w-[566px] h-28 text-[#84f8a1] text-[80px] font-bold font-['Angst']">введите код<br/>
                  </div>
                  <div className="w-[832px] h-[70px] text-[#84f8a1] text-[50px] font-bold font-['Angst']">отправленный
                      на вашу почту
                  </div>
                  <input
                      className="text-white w-[810px] h-[73px] bg-[#d9d9d9]/10 rounded-[30px] border-4 border-[#83f8a0] backdrop-blur-[50px]"></input>
              </div>
              <div
                  className="w-[869px] h-[129px] bg-[#d9d9d9]/10 rounded-[30px] backdrop-blur-[50px] flex justify-center items-center flex-col mt-[250px]">
                  <a href="/chat"
                      className="w-[579px] h-14 text-[#eaa1fc] text-[65px] font-bold font-['Angst'] flex justify-center items-center flex-col">далее
                  </a>
              </div>

          </div>

      </div>
  );
}
