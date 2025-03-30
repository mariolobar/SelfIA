import { createRoot } from "react-dom/client";
import { AppContextProvider } from "./core/context/AppContext.tsx";
import { AppRouter } from "./AppRouter.tsx";
import "./index.scss";

createRoot(document.getElementById("root")!).render(
  <AppContextProvider>
    <AppRouter />
  </AppContextProvider>
);
