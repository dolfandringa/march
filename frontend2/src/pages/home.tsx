import React, { useContext } from "react";
import { Segment, Grid, Header } from "semantic-ui-react";
import SearchBar from "../components/search";
import { ResultsProvider } from "../contexts/results-context";
import { AuthProvider } from "../contexts/auth-context";
import { EmailList } from "../components/email-list";

function Home() {
  return (
    <Grid>
      <Grid.Column>
        <Segment raised>
          <Header as="h1">Mail</Header>
          <AuthProvider>
            <ResultsProvider>
              <SearchBar />
              <EmailList />
            </ResultsProvider>
          </AuthProvider>
        </Segment>
      </Grid.Column>
    </Grid>
  );
}

export default Home;
