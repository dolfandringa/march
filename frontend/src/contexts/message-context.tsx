import React, { createContext, ReactNode } from "react";
import { Message } from "semantic-ui-react";

enum MessageSeverity {
  Error,
  Warning,
  Message,
  Info,
}

interface UIMessage {
  message?: string;
  severity: MessageSeverity;
}
export const MessageContext = createContext<UIMessage>({
  severity: MessageSeverity.Info,
});

export const MessageProvider = (props: { children?: ReactNode }) => {
  return (
    <>
      <Message></Message>
      {props.children}
    </>
  );
};
