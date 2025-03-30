import { BrowserRouter, Route, Routes } from "react-router-dom";

import { Login } from "./public/Login";
import { PrivateGuard } from "./guard/PrivateGuard";
import App from "./App";

export const AppRouter = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route element={<PrivateGuard />}>
          <Route path="/" element={<App />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
};
