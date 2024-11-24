import Image from "next/image";

export default function Home() {
  return (
      <div
          className="bg-[url('/img/bg.png')] flex justify-center items-center min-h-screen">
          <div
              className="w-[90vw] h-[90vh] bg-[#d9d9d9]/0 rounded-[30px] border-4 border-[#83f8a0] flex justify-center items-center flex-col gap-10">
              <div
                  className="w-[984px] h-[339px] bg-[#d9d9d9]/10 rounded-[90px] backdrop-blur-[50px] flex justify-center items-center flex-col">
                  <img className="w-[282px] h-[172px] " src="/img/logo.png"/>
                  <div
                      className="w-[599px] h-[90px] mt-15 text-[#84f8a1] text-6xl font-bold font-['Angst']">приветствует
                      вас!
                  </div>
              </div>
              <div
                  className="w-[984px] h-[140px] bg-[#d9d9d9]/10 rounded-[90px] backdrop-blur-[50px] flex justify-center items-center flex-col">
                  <div className="w-[658px] text-[#84f8a1] text-[50px] font-bold font-['Angst'] text-center">для начала
                      работы
                      пройдите регистрацию
                  </div>
              </div>

              <div
                  className="w-[995px] h-28 bg-[#d9d9d9]/10 rounded-[30px] backdrop-blur-[50px] mt-[100px] flex justify-center items-center flex-col align-middle  ">
                  <div
                      className="w-[902px] h-[97px] text-[#eaa1fc] text-[80px] font-bold font-['Angst'] flex justify-center items-center flex-col">зарегистрироваться
                  </div>
              </div>
              <div
                  className="w-[995px] h-28 bg-[#d9d9d9]/10 rounded-[30px] backdrop-blur-[50px] flex justify-center items-center flex-col align-middle">
                  <div
                      className="w-[289px] h-[99px] text-[#eaa1fc] text-[80px] font-bold font-['Angst'] flex justify-center items-center flex-col">войти
                  </div>
              </div>
          </div>

          {/* INFO: ТУТ ТО ОКНО */}
          <div
              style={{backdropFilter: "blur(20px)"}}
              className="absolute w-full h-screen backdrop-blur-lg flex justify-end items-center flex-col hidden">
              <div
                  className="w-[837px] h-[639px] p-10 bg-[#d9d9d9]/10 border-4 border-[#eaa1fc] backdrop-blur-lg mb-20 flex justify-start items-center flex-col gap-5">
                  <div
                      className="w-[791px] h-[73px] bg-[#d9d9d9]/10 rounded-[30px] border-4 border-[#83f8a0] backdrop-blur-[50px]"></div>
                  <div
                      className="w-[791px] h-[73px] bg-[#d9d9d9]/10 rounded-[30px] border-4 border-[#F8E984] backdrop-blur-[50px] flex justify-center items-center flex-col">
                      <img className="" src="/img/Icon.png"/>
                  </div>
                  <div
                      className="w-[791px] h-[73px] bg-[#d9d9d9]/10 rounded-[30px] border-4 border-[#83f8a0] backdrop-blur-[50px]"></div>

              </div>
          </div>
      </div>
  );
}
