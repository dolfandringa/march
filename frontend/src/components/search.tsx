import React, { useContext, useEffect, useState } from "react";
import { Input, Icon } from "semantic-ui-react";
import { ResultsContext } from "../contexts/results-context";
import { GmailService } from "../services/gmail-service";
import { AuthContext } from "../contexts/auth-context";
import { PermissionDeniedError } from "../exceptions";
import { useAsyncError } from "./error-catcher";

const SearchBar = () => {
  const [query, setQuery] = useState("");
  const [busy, setBusy] = useState(false);
  const throwAsyncError = useAsyncError();
  const ctx = useContext(ResultsContext);
  if (!ctx) {
    throw new Error("Not a valid context given yet.");
  }
  const { emails, setEmails } = ctx;
  const { user, token, fb, logout } = useContext(AuthContext);
  if (!logout) {
    throw new Error("AuthContext not initialized");
  }
  const handleChange = (event: React.FormEvent<HTMLInputElement>) => {
    setQuery(event.currentTarget.value);
  };
  const startSearch = async () => {
    setBusy(true);
    console.log("Starting search");
    if (!user || !user.email || !token || !fb) {
      logout();
      throw new PermissionDeniedError("User is not logged in.");
    }
    const backend_url = await fb.getConfigVariable("backend_url");
    try {
      const res = await GmailService.search(
        backend_url,
        query,
        user.email,
        token
      );
    } catch(error) {
      throwAsyncError(error);
    }
    setEmails(res);
    setBusy(false);
  };

  useEffect(() => {
    console.log("useEffect emails", emails);
  }, [emails]);

  const handleKeyDown = (event: React.KeyboardEvent<HTMLInputElement>) => {
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
