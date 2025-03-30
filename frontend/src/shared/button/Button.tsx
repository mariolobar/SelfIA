import React, { ReactNode } from "react";
import "./Button.scss";

interface ButtonProps {
  onClick?: () => void;
  type?: "button" | "submit" | "reset";
  className?: string;
  children: ReactNode;
  disabled?: boolean;
}

const Button: React.FC<ButtonProps> = ({
  onClick,
  className = "",
  type = "button",
  children,
  disabled = false,
}) => {
  return (
    <button
      type={type}
      onClick={onClick}
      className={`button ${className} ${disabled ? "button--disabled" : ""}`}
      disabled={disabled}
    >
      {children}
    </button>
  );
};

export default Button;
