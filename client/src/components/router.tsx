import { FunctionComponent } from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Home from "./pages/home/home";
import Visualisation from "./pages/visualisation/visualisation";
import FileUpload from "./pages/fileUpload/fileUpload";
import Questionnaire from "./pages/questionnaires/userLevelQuestionnaires";

const RouterComponent: FunctionComponent = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/visualisation" element={<Visualisation />} />
        <Route path="/fileUpload" element={<FileUpload />} />
        <Route path="/questionnaires" element={<Questionnaire />} />
      </Routes>
    </Router>
  );
};

export default RouterComponent;
