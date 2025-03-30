import { useEffect, useState } from "react";
import mergeImages from "merge-images";
import { useAppContext } from "../core/context/AppContext";
import { base64ToFile } from "../utils/base64ToFile";
import LoadingFilter from "./loading-filter";
import frameImage from "../assets/images/selfia_marca-agua-01.png";

export const Selfie = () => {
  const {
    filter,
    selfie,
    sessionId,
    setSessionId,
    selfieAI,
    setSelfieAI,
    mergedSelfieAI,
    setMergedSelfieAI,
    loading,
    setLoading,
  } = useAppContext();
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!selfie) {
      return;
    }
    setLoading(true);

    const fetchData = async () => {
      try {
        const response = await fetch("/api/af_upload_img", {
          method: "POST",
          headers: {
            "x-functions-key":
              "gfzcUXdkYoVI7RmpJjlPX0aXIQMWzPYloKYrEIeXskO5AzFu4dzctQ==",
          },
          body: JSON.stringify({
            upload_file: selfie,
          }),
        });
        if (!response.ok) {
          throw new Error("Network response error");
        }
        const result = await response.json();
        setSessionId(result.session_id);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Unknown error");
      }
    };
    fetchData();
  }, [selfie, setLoading, setSessionId]);

  useEffect(() => {
    if (!sessionId || !filter) {
      return;
    }
    setLoading(true);

    const fetchData = async () => {
      try {
        const response = await fetch("/api/af_process_files", {
          method: "POST",
          headers: {
            "x-functions-key":
              "gfzcUXdkYoVI7RmpJjlPX0aXIQMWzPYloKYrEIeXskO5AzFu4dzctQ==",
          },
          body: JSON.stringify({
            session_id: sessionId,
            stored_img: `${sessionId}.png`,
            filters: [filter],
          }),
        });
        if (!response.ok) {
          throw new Error("Network response error");
        }

        const fetchData = async () => {
          try {
            const response = await fetch("/api/af_return_img", {
              method: "POST",
              headers: {
                "x-functions-key":
                  "gfzcUXdkYoVI7RmpJjlPX0aXIQMWzPYloKYrEIeXskO5AzFu4dzctQ==",
              },
              body: JSON.stringify({
                image_id: `${sessionId}/${sessionId}_${filter}.png`,
              }),
            });
            if (!response.ok) {
              throw new Error("Network response error");
            }
            const result = await response.json();
            setSelfieAI(base64ToFile(result.base64_img));
          } catch (err) {
            setError(err instanceof Error ? err.message : "Unknown error");
          }
        };
        fetchData();
      } catch (err) {
        setError(err instanceof Error ? err.message : "Unknown error");
      }
    };
    fetchData();
  }, [filter, sessionId, setSelfieAI, setLoading]);

  useEffect(() => {
    if (!selfieAI) {
      return;
    }
    mergeImages([selfieAI, frameImage]).then((b64) => setMergedSelfieAI(b64));

    setLoading(false);
  }, [selfieAI, setLoading, setMergedSelfieAI]);

  return (
    <>
      {error && (
        <p className="text-error text-center bg-red-100 px-4 py-2 mb-6 rounded">
          Error: {error}
        </p>
      )}
      {loading && selfie && !mergedSelfieAI && (
        <>
          <LoadingFilter />
          <img className="selfie-loader__img" src={selfie} />
        </>
      )}
      {mergedSelfieAI && <img src={mergedSelfieAI} />}
    </>
  );
};

export default Selfie;
