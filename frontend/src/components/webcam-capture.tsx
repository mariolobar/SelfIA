import { ReactNode, useCallback, useRef } from "react";
import Webcam from "react-webcam";

import { useAppContext } from "../core/context/AppContext";
import Button from "../shared/button/Button";

interface WebcamCaptureProps {
  children: ReactNode;
}

export const WebcamCapture: React.FC<WebcamCaptureProps> = ({ children }) => {
  const {
    selfie,
    setSelfie,
    setSessionId,
    setSelfieAI,
    mergedSelfieAI,
    setMergedSelfieAI,
    loading,
  } = useAppContext();
  const webcamRef = useRef<Webcam>(null);

  const videoConstraints = {
    width: { min: 680 },
    height: { min: 680 },
    aspectRatio: 1,
  };

  const capture = useCallback(() => {
    if (webcamRef.current === null) return;
    const imageSrc = webcamRef.current.getScreenshot({
      width: 1024,
      height: 1024,
    });
    setSelfie(imageSrc);
  }, [webcamRef, setSelfie]);

  const resetSelfie = () => {
    setSelfie(null);
    setSessionId(null);
    setSelfieAI(null);
    setMergedSelfieAI(null);
  };

  return (
    <>
      {!selfie && (
        <>
          <div className="w-full aspect-square">
            <Webcam
              screenshotFormat="image/png"
              audio={false}
              ref={webcamRef}
              videoConstraints={videoConstraints}
            />
          </div>
          <Button onClick={capture}>Take selfie</Button>
        </>
      )}
      {selfie && (
        <>
          <div className="w-full aspect-square relative overflow-hidden">
            {children}
          </div>
          {!loading && mergedSelfieAI && (
            <Button onClick={resetSelfie}>Take new selfie</Button>
          )}
          {loading && (
            <Button
              className="animate-pulse pointer-events-none"
              onClick={resetSelfie}
            >
              analyzing...
            </Button>
          )}
        </>
      )}
    </>
  );
};

export default WebcamCapture;
