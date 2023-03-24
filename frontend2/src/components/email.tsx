import React, { FormEvent } from "react";
import {
  Table,
  Form,
  Checkbox,
  Popup,
  Header,
  CheckboxProps,
} from "semantic-ui-react";

export interface IEmail {
  "X-GM-MSGID": string;
  To: string;
  From: string;
  Subject: string;
  Date: string;
  [k: string]: string;
}

const parseEmailAddr = (address: string) => {
  const re = /(.*)<(.*)>/;
  const match = address.match(re);
  if (!match) {
    return ["", address];
  }
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const [orig, name, email_addr] = match.map((s) => s.trim());
  return [name, email_addr];
};

export const Email = (props: {
  email: IEmail;
  selectEmail: (
    event: FormEvent<HTMLInputElement>,
    data: CheckboxProps
  ) => void;
}) => {
  const { email } = props;
  const [name, email_addr] = parseEmailAddr(email.From);
  const msgid = email["X-GM-MSGID"];
  return (
    <Table.Row>
      <Table.Cell collapsing>
        <Form.Field>
          <Checkbox name={msgid} onChange={props.selectEmail} />
        </Form.Field>
      </Table.Cell>
      <Table.Cell>
        <Popup content={email_addr} trigger={<Header sub>{name}</Header>} />
      </Table.Cell>
      <Table.Cell>{email.Subject}</Table.Cell>
      <Table.Cell collapsing>{email.Date}</Table.Cell>
    </Table.Row>
  );
};
