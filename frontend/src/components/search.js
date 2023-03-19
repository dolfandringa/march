import React, { useContext, useState } from "react";
import { Input, Icon } from "semantic-ui-react";
import { ResultsContext } from "./results-context";
import { GmailService } from "../services/gmail-service";

const SearchBar = (props) => {
  const { user, token } = props;
  const [query, setQuery] = useState("");
  const [busy, setBusy] = useState(false);
  const { emails, setEmails } = useContext(ResultsContext);
  const handleChange = (event) => {
    console.log("Handling change", event);
    setQuery(event.target.value);
  };
  const startSearch = async () => {
    setBusy(true);
    console.log("Starting search");
    const res = await GmailService.search(query, user.email, token);
    setEmails(res);
    console.log("emails", emails);
    setBusy(false);
  };

  const handleKeyDown = (event) => {
    console.log(event);
    if (event.key === "Enter") {
      startSearch();
    }
  };
  return (
    <Input
      icon={<Icon name="search" circular link onClick={startSearch} />}
      placeholder="Search..."
      onKeyDown={handleKeyDown}
      fluid
      loading={busy}
      onChange={handleChange}
    />
  );
};

export default SearchBar;
