import { FormEvent, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Login.scss";

export const Login = () => {
  const [error, setError] = useState<string>("");
  const passwordRef = useRef<HTMLInputElement>(null);
  const navigate = useNavigate();
  const url = sessionStorage.getItem("loginURL");
  console.log("mi url:", url);

  const handleLogin = (event: FormEvent) => {
    event.preventDefault();
    if (passwordRef?.current?.value !== "SelfIA2024") {
      setError("Wrong password");
      return;
    }
    localStorage.setItem("selfia-token", "Wwg4hmHvRtKqvisHbvQX");

    if (url) {
      navigate(url);
    }
  };
  return (
    <>
      <div className="login">
        <form className="login__form" onSubmit={handleLogin}>
          <label className="login__label" htmlFor="password">
            Password
            <input
              className="login__input"
              id="password"
              type="password"
              ref={passwordRef}
              placeholder="Enter Password"
              required
            />
            {error && <span className="login__error">{error}</span>}
          </label>

          <button className="login__button" type="submit">
            Login
          </button>
        </form>
      </div>
    </>
  );
};
