import { useState } from "react";

import { useAppContext } from "../core/context/AppContext";
import Button from "../shared/button/Button";
import "./selfie-form.scss";

export const SelfieForm = () => {
  const { mergedSelfieAI } = useAppContext();
  const [success, setSuccess] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [formData, setFormData] = useState({
    firstName: "",
    lastName: "",
    email: "",
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    if (!mergedSelfieAI) {
      return;
    }

    const fetchData = async () => {
      try {
        const response = await fetch(
          "https://prod-92.westeurope.logic.azure.com:443/workflows/8fb0eacadf50419da201162018700801/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=P6-Bft6wN8bJeM1YtogSDMjG4WfmxtBlmIV0vlFl-Rs",
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              firstName: formData.firstName,
              lastName: formData.lastName,
              email: formData.email,
              ImageBase64: mergedSelfieAI,
            }),
          }
        );

        if (!response.ok) {
          throw new Error("Network response error");
        }

        if (response.ok) {
          setSuccess(true);
          setTimeout(() => {
            setSuccess(false);
          }, 5000);
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : "Unknown error");
      }
    };

    fetchData();

    setSuccess(true);
    setTimeout(() => {
      setSuccess(false);
    }, 5000);

    setFormData({
      firstName: "",
      lastName: "",
      email: "",
    });
  };

  return (
    <section className="selfie-form__container">
      <form className="selfie-form" onSubmit={handleSubmit}>
        <label className="selfie-form__label">
          Name
          <input
            type="text"
            className="selfie-form__input"
            name="firstName"
            value={formData.firstName}
            onChange={handleChange}
            required
          />
        </label>
        <label className="selfie-form__label">
          Surname
          <input
            type="text"
            className="selfie-form__input"
            name="lastName"
            value={formData.lastName}
            onChange={handleChange}
            required
          />
        </label>
        <label className="selfie-form__label">
          Email
          <input
            type="email"
            className="selfie-form__input"
            name="email"
            value={formData.email}
            onChange={handleChange}
            required
          />
        </label>
        <label className="selfie-form__label text-sm flex items-start gap-2">
          <input
            type="checkbox"
            className="selfie-form__checkbox"
            name="acceptance"
            required
          />
          <p>
            I agree to the processing of the data provided, in order to receive
            a response to my request for information.
            <a
              className="text-secondary"
              href="https://www.bravent.net/politica-privacidad/"
              target="blank"
            >
              &nbsp;Check our privacy policy
            </a>
          </p>
        </label>

        <Button className="selfie-form__button" type="submit">
          Send
        </Button>
      </form>
      {error && (
        <p className="absolute left-1/2 -translate-x-1/2 w-fit text-error text-center bg-red-100 px-4 py-2 mt-6 mx-auto rounded">
          Error: {error}
        </p>
      )}
      {success && (
        <p className="absolute left-1/2 -translate-x-1/2 w-fit text-success text-center bg-green-100 px-4 py-2 mt-6 mx-auto rounded">
          selfie successfully sent
        </p>
      )}
    </section>
  );
};

export default SelfieForm;
