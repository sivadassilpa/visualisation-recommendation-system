// src/pages/Home.tsx
import { FunctionComponent } from "react";
import PersonIcon from "@mui/icons-material/Person";
import "./home.scss";
import Card from "@mui/material/Card/Card";
import { CardContent, Typography, Button } from "@mui/material";
import { useNavigate } from "react-router-dom";
import { userDetailsStore } from "../../store/userStore";

const Home: FunctionComponent = () => {
  const setUserDetails = userDetailsStore((state) => state.setUserDetails);
  const navigate = useNavigate();
  const handleVisualisationNavigation = (username: String) => {
    console.log(username);
    setUserDetails({ username: username });
    navigate("/questionnaires");
  };
  return (
    <>
      <div className="home-title">
        Context Aware Visualisation Recommendation System with Vega
        Visualisation
      </div>
      <div className="home-container">
        <Card className="card">
          <CardContent>
            <PersonIcon className="icon" />
            <Typography variant="h6" component="h2">
              User 1
            </Typography>
            <Button
              variant="contained"
              color="info"
              onClick={() => handleVisualisationNavigation("User 1")}
            >
              Go to Visualisation
            </Button>
          </CardContent>
        </Card>
        <Card className="card">
          <CardContent>
            <PersonIcon className="icon" />
            <Typography variant="h6" component="h2">
              User 2
            </Typography>
            <Button
              variant="contained"
              color="warning"
              onClick={() => handleVisualisationNavigation("User 2")}
            >
              Go to Visualisation
            </Button>
          </CardContent>
        </Card>
        <Card className="card">
          <CardContent>
            <PersonIcon className="icon" />
            <Typography variant="h6" component="h2">
              User 3
            </Typography>
            <Button
              variant="contained"
              color="success"
              onClick={() => handleVisualisationNavigation("User 3")}
            >
              Go to Visualisation
            </Button>
          </CardContent>
        </Card>
      </div>
    </>
  );
};

export default Home;
