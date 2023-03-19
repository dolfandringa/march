import React, { useEffect, useCallback, useState } from "react";
import { Button, Segment, Grid, Header } from "semantic-ui-react";
import SearchBar from "../components/search";
import { ResultsContext } from "../components/results-context";
import { login, logout, onAuthStateChange } from "../services/firebase-service";

function Home() {
  const [emails, setEmails] = useState([]);
  const [user, setUser] = useState();
  const [token, setToken] = useState("");

  const onLogin = (auth) => {
    const { user, token } = auth;
    console.log("onLogin. user:", user, "token:", token);
    setUser(user);
    setToken(token);
  };

  const doLogin = async () => {
    await login(onLogin);
  };

  useEffect(() => {
    const unsubscribe = onAuthStateChange(setUser);
    return () => {
      unsubscribe();
    };
  }, []);

  return (
    <Grid>
      <Grid.Column>
        <Segment raised>
          <Header as="h1">Mail</Header>
          {user ? (
            <ResultsContext.Provider value={{ emails, setEmails }}>
              <SearchBar user={user} token={token} />
              <Button onClick={logout}>logout</Button>
            </ResultsContext.Provider>
          ) : (
            <h1>
              Please <Button onClick={doLogin}>login</Button>
            </h1>
          )}
        </Segment>
      </Grid.Column>
    </Grid>
  );
}

export default Home;
