import { createContext, ReactNode, useContext, useState } from "react";

import { Step } from "../model/enum/step.enum";
import { Filter } from "../model/enum/filter.enum";

interface AppContextType {
  step: Step;
  setStep: React.Dispatch<React.SetStateAction<Step>>;
  filter: Filter | null;
  setFilter: React.Dispatch<React.SetStateAction<Filter | null>>;
  selfie: string | null;
  setSelfie: React.Dispatch<React.SetStateAction<string | null>>;
  selfieAI: string | null;
  setSelfieAI: React.Dispatch<React.SetStateAction<string | null>>;
  mergedSelfieAI: string | null;
  setMergedSelfieAI: React.Dispatch<React.SetStateAction<string | null>>;
  sessionId: string | null;
  setSessionId: React.Dispatch<React.SetStateAction<string | null>>;
  loading: boolean;
  setLoading: React.Dispatch<React.SetStateAction<boolean>>;
}

export const AppContext = createContext<AppContextType>({
  step: Step.home,
  setStep: () => {},
  filter: null,
  setFilter: () => {},
  selfie: null,
  setSelfie: () => {},
  selfieAI: null,
  setSelfieAI: () => {},
  mergedSelfieAI: null,
  setMergedSelfieAI: () => {},
  sessionId: null,
  setSessionId: () => {},
  loading: false,
  setLoading: () => {},
});

interface AppContextProps {
  children: ReactNode;
}

export const AppContextProvider: React.FC<AppContextProps> = ({ children }) => {
  const [step, setStep] = useState<Step>(Step.home);
  const [filter, setFilter] = useState<Filter | null>(null);
  const [selfie, setSelfie] = useState<string | null>(null);
  const [selfieAI, setSelfieAI] = useState<string | null>(null);
  const [mergedSelfieAI, setMergedSelfieAI] = useState<string | null>(null);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);

  return (
    <AppContext.Provider
      value={{
        step,
        setStep,
        filter,
        setFilter,
        selfie,
        setSelfie,
        selfieAI,
        setSelfieAI,
        mergedSelfieAI,
        setMergedSelfieAI,
        sessionId,
        setSessionId,
        loading,
        setLoading,
      }}
    >
      {children}
    </AppContext.Provider>
  );
};

export const useAppContext = () => {
  const context = useContext(AppContext);
  return context;
};
