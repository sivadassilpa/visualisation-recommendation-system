import { FunctionComponent } from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Home from "./pages/home/home";
import Visualisation from "./pages/visualisation/visualisation";

const RouterComponent: FunctionComponent = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route
          path="/visualisation"
          element={<Visualisation></Visualisation>}
        />
      </Routes>
    </Router>
  );
};

export default RouterComponent;
