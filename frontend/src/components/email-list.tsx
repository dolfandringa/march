import React, { FormEvent, useContext, useState } from "react";
import { ResultsContext } from "../contexts/results-context";
import { Email } from "./email";
import { Table, Form, CheckboxProps } from "semantic-ui-react";

export const EmailList = () => {
  const ctx = useContext(ResultsContext);
  const [selected, setSelected] = useState<string[]>([]);
  if (!ctx) {
    throw new Error("ResultsContext is not set");
  }
  const { emails } = ctx;

  const selectEmail = (
    event: FormEvent<HTMLInputElement>,
    data: CheckboxProps
  ) => {
    const msgid = data.name ?? "";
    if (data.checked) {
      setSelected([...selected, msgid]);
      return;
    }
    const newSelected = [...selected];
    const idx = newSelected.indexOf(msgid);
    if (idx >= 0) {
      newSelected.splice(idx, 1);
      setSelected(newSelected);
    }
  };

  const renderedEmails = emails.map((email) => {
    return (
      <Email
        key={`${email["X-GM-MSGID"]}`}
        selectEmail={selectEmail}
        email={email}
      />
    );
  });
  return (
    <>
      <h1>Woopwoop</h1>
      <Form>
        <Table basic="very">
          <Table.Body>{renderedEmails}</Table.Body>
        </Table>
      </Form>
    </>
  );
};
