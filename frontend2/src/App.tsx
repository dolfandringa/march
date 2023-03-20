import * as React from "react";
export interface InterfaceAppProps {
  testMessage: string;
}
export interface AppState {}
export class App extends React.Component<InterfaceAppProps, AppState> {
  render() {
    return (
      <>
        <div>Testing...{this.props.testMessage}</div>
      </>
    );
  }
}
