import React from "react";
import { Segment, Grid, Header } from "semantic-ui-react";
import SearchBar from "../components/search";
import { ResultsProvider } from "../contexts/results-context";
import { AuthProvider } from "../contexts/auth-context";
import { EmailList } from "../components/email-list";
import { ErrorCatcher } from "../components/error-catcher";

function Home() {
  return (
    <Grid>
      <Grid.Column>
        <Segment raised>
          <ErrorCatcher message="An error occured. Please notify the developers,">
            <Header as="h1">Mail</Header>
            <AuthProvider>
              <ResultsProvider>
                <SearchBar />
                <EmailList />
              </ResultsProvider>
            </AuthProvider>
          </ErrorCatcher>
        </Segment>
      </Grid.Column>
    </Grid>
  );
}

export default Home;
