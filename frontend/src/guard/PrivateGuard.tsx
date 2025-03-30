import { Navigate, Outlet, useLocation } from "react-router-dom";

export const PrivateGuard = () => {
  const token = localStorage.getItem("selfia-token");
  const location = useLocation();
  const { pathname } = location;

  if (!token) {
    sessionStorage.setItem("loginURL", pathname);
  }

  return token ? <Outlet /> : <Navigate to="/login" replace />;
};
