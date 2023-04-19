import React, { Component, ReactNode } from "react";
import { Message } from "semantic-ui-react";

interface IErrorCatcherState {
  hasError: boolean;
}
interface IErrorCatcherProps {
  message: string;
  children: ReactNode;
}

export const useAsyncError = () => {
  const [_, setError] = React.useState();
  return React.useCallback(
    (e: Error) => {
      setError(() => {
        throw e;
      });
    },
    [setError]
  );
};

export class ErrorCatcher extends Component<IErrorCatcherProps, IErrorCatcherState>{
  state: IErrorCatcherState = {
    hasError: false,
  };

  static getDerivedStateFromError(error: Error) {
    return { hasError: true };
  }

  componentDidCatch(error: Error, errorInfo) {
    // You can also log the error to an error reporting service
    console.log(error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return <Message negative>{this.props.message}</Message>;
    }
    return this.props.children;
  }
}
