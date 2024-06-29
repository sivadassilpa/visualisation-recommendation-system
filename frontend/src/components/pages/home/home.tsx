import { FunctionComponent } from "react";
import PersonIcon from "@mui/icons-material/Person";
import "./home.scss";
import Card from "@mui/material/Card/Card";
import { CardContent, Typography, Button } from "@mui/material";
import { useNavigate } from "react-router-dom";
import { userDetailsStore } from "../../store/userStore";
import { SApiService } from "../../services/app.service";

const Home: FunctionComponent = () => {
  const setUserDetails = userDetailsStore((state) => state.setUserDetails);
  const navigate = useNavigate();
  const handleVisualisationNavigation = (username: string) => {
    SApiService.login({ username: username, password: username + "@123" })
      .then((res) => {
        const userProfile = res.data.userProfile;
        setUserDetails({
          username: username,
          password: username + "@123",
          userId: res.data.userId,
        }); // donot store password
        if (!userProfile) {
          navigate("/questionnaires");
        } else {
          navigate("/main");
        }
      })
      .catch((err) => {
        console.log(err);
      });
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
              onClick={() => handleVisualisationNavigation("User1")}
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
              onClick={() => handleVisualisationNavigation("User2")}
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
              onClick={() => handleVisualisationNavigation("User3")}
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
