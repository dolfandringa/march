import React, { createContext, useState, ReactNode } from "react";
import { IEmail } from "../components/email";

interface IResultContext {
  emails: IEmail[];
  setEmails: (emails: IEmail[]) => void;
}

export const ResultsContext = createContext<IResultContext | null>(null);

export const ResultsProvider = (props: { children?: ReactNode }) => {
  const [emails, setEmails] = useState<IEmail[]>([]);

  return (
    <ResultsContext.Provider value={{ emails, setEmails }}>
      {props.children}
    </ResultsContext.Provider>
  );
};
