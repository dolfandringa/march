import "semantic-ui-less/semantic.less";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/home";
import NavBar from "./components/navbar";
import About from "./pages/about";
import { Container } from "semantic-ui-react";

function App() {
  return (
    <Container>
      <Router>
        <NavBar />
        <Routes>
          <Route exact path="/" element={<Home />}></Route>
          <Route exact path="/about" element={<About />}></Route>
        </Routes>
      </Router>
    </Container>
  );
}

export default App;
