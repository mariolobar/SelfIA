import { useAppContext } from "./core/context/AppContext";
import { FilterList } from "./components/filter-list";
import WebcamCapture from "./components/webcam-capture";

import Logo from "./assets/images/selfia-logo.svg";
import BraventLogo from "./assets/images/bravent-logo.svg";
import SelfieForm from "./components/selfie-form";
import Selfie from "./components/selfie";

function App() {
  const { filter } = useAppContext();

  return (
    <>
      <main className="flex flex-col items-center min-h-dvh">
        {!filter && (
          <section className="flex flex-col items-center my-auto">
            <img className="w-full max-w-64" src={Logo} />
            <div className="my-8">
              <FilterList />
            </div>
          </section>
        )}
        {filter && (
          <section className="w-full grid grid-cols-12 sm:gap-12 items-center my-auto p-6">
            <div className="col-span-12 xl:col-span-4 flex flex-col items-center p-4 sm:p-6">
              <img className="w-full max-w-64" src={Logo} />
              <FilterList />
            </div>
            <div className="col-span-12 xl:col-span-4 flex justify-center items-center p-4">
              <div className="flex flex-col justify-center items-center grow mt-16 gap-6">
                <WebcamCapture>
                  <Selfie />
                </WebcamCapture>
              </div>
            </div>
            <div className="col-span-12 xl:col-span-4 flex flex-col gap-6 p-4">
              <SelfieForm />
            </div>
          </section>
        )}
        <footer className="w-full bg-enriched-black">
          <img className="max-w-48 mx-auto py-4" src={BraventLogo} />
        </footer>
      </main>
    </>
  );
}

export default App;
