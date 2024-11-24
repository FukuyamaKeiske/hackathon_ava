import Image from "next/image";

export default function Home() {
  return (
      <div
          className="bg-[url('/img/bg.png')] flex justify-center items-center min-h-screen">
          <div
              className="w-[90vw] h-[90vh] bg-[#d9d9d9]/0 rounded-[30px] border-4 border-[#83f8a0] flex justify-center items-center flex-col gap-10">
              <div
                  className="w-[984px] h-[461px] bg-[#d9d9d9]/10 rounded-[90px] backdrop-blur-[50px] flex justify-start items-center flex-col gap-10">
                  <div className="w-[560px] h-[86px] text-[#eaa1fc] text-[80px] font-bold font-['Angst']">регистрация
                  </div>

                  <div
                      className="w-[810px] h-[73px] bg-[#d9d9d9]/10 rounded-[30px] border-4 border-[#83f8a0] backdrop-blur-[50px]"></div>
                  <div
                      className="w-[810px] h-[73px] bg-[#d9d9d9]/10 rounded-[30px] border-4 border-[#83f8a0] backdrop-blur-[50px]"></div>
                  <div
                      className="w-[810px] h-[73px] bg-[#d9d9d9]/10 rounded-[30px] border-4 border-[#83f8a0] backdrop-blur-[50px]"></div>
              </div>

              <div
                  className="w-[869px] h-[129px] bg-[#d9d9d9]/10 rounded-[30px] backdrop-blur-[50px] flex justify-center items-center flex-col mt-10">
                  <div
                      className="w-[579px] h-14 text-[#eaa1fc] text-[65px] font-bold font-['Angst'] flex justify-center items-center flex-col">далее
                  </div>
              </div>

          </div>

      </div>
  );
}
