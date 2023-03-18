import React from "react";
import { Segment, Grid, Header } from "semantic-ui-react";

function Home() {
  return (
    <Grid>
      <Grid.Column>
        <Segment raised>
          <Header as="h1">Mail</Header>
        </Segment>
      </Grid.Column>
    </Grid>
  );
}

export default Home;
