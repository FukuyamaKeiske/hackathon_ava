import Image from "next/image";

export default function Home() {
  return (
      <div
          className="bg-[url('/img/bg.png')] flex justify-center items-center min-h-screen">
          <div
              className="w-[90vw] h-[90vh] bg-[#d9d9d9]/0 rounded-[30px] border-4 border-[#83f8a0] flex justify-start items-center flex-col gap-10 p-10">
              <div className="flex justify-start items-start flex-row w-[100%]">
                  <div className="relative">
                      <img className=" " src="/img/button-circle.png"/>
                      <img className="absolute top-[50%] left-[50%] translate-x-[-50%] translate-y-[-50%]"
                           src="/img/union.png"/>
                  </div>
                  <div className="relative self-end ml-auto">
                      <img className=" " src="/img/button-circle.png"/>
                      <img className="absolute h-[58px] w-[49px] top-[50%] left-[50%] translate-x-[-50%] translate-y-[-50%]"
                           src="/img/user.png"/>
                  </div>
              </div>

              <div className="flex justify-center items-end flex-col w-[100%]">
                  <div
                      className="w-[1500px] h-[229.37px] bg-[#cffef6]/10 rounded-[30px] border-4 border-[#83f8a0]"></div>
              </div>

              <div className="flex justify-center items-start flex-col w-[100%]">
                  <div
                      className="w-[1503px] h-[228.55px] bg-[#e0f0f9]/10 rounded-[30px] border-4 border-[#eaa1fc]"></div>
              </div>

              <div className="relative flex justify-start items-start flex-row w-[100%] mt-auto">
                  <div
                      className="w-[95%] h-[76px] bg-[#d9d9d9]/10 rounded-[90px] shadow border-4 border-[#83f8a0]"></div>
                  <img className="absolute translate-y-4 translate-x-7"
                       src="/img/attach_file.png"/>
                  <div className="relative self-end ml-auto">
                      <img className="h-[76px] w-[76px]" src="/img/button-circle.png"/>
                      <img className="absolute top-[50%] left-[50%] translate-x-[-50%] translate-y-[-50%]"
                           src="/img/lupa.png"/>
                  </div>
              </div>
          </div>

      </div>
  );
}
