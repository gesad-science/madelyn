// import { redirect } from 'next/navigation';
// import { getSeeion } from '@/auth-lib';
import InputBox from "@/components/InputBox";


export default function Home() {
  return (
    <main className="">
      <section className='bg-grey-1 py-20 dark:bg-dark lg:py-[120px]'>
      <div className="container mx-auto ">
        <div className="-mx-4 flex flex-wrap">
          <div className="w-full px-4">
            <div className="relative mx-auto max-w-[525px] overflow-hidden rounded-lg bg-white px-10 py-16 text-center dark:bg-dark-2 sm:px-12 md:px-[60px]">
              <div className="mb-10 text-center md:mb-16 text-2xl text-gray-950">
                <h1> Login </h1>
              </div>
              <form>
                <InputBox type="email" name="email" placeholder="Email" />
                <InputBox
                  type="password"
                  name="password"
                  placeholder="Password"
                />
                <div className="mb-10">
                  <input
                    type="submit"
                    value="Sign In"
                    className="w-full  bg-blue-950 cursor-pointer rounded-md border border-primary bg-primary px-5 py-3 text-base font-medium text-white transition hover:bg-opacity-90"
                  />
                </div>
              </form>
              <p className="text-base text-gray-950">
                <a
                  href="/#"
                  className="text-primary hover:underline"
                >
                  Sign Up
                </a>
              </p>
            </div>
          </div>
        </div>
      </div>
      </section>
    </main>
  );
};
