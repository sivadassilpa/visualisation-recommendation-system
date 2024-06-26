import { Fragment, FunctionComponent, useEffect, useState } from "react";
import VegaChart from "../vega/vega";
import { userDetailsStore } from "../../store/userStore";
import { useLocation } from "react-router-dom";
import { Grid } from "@mui/material";

const Visualisation: FunctionComponent = () => {
  const userDetails = userDetailsStore((state) => state.userDetails);
  const [vegaObject, setVegaObject] = useState([]);
  const location = useLocation();

  useEffect(() => {
    if (userDetails?.username && location.state.vegaspec) {
      setVegaObject(location.state.vegaspec);
    }
  }, [userDetails, location.state.vegaspec, location.state]);

  return (
    <div>
      <div className="home-title">Visualization Page for {"username"}</div>
      <Grid style={{ width: "100%" }} container>
        {vegaObject &&
          vegaObject.map((object: any, index) => (
            <Grid key={index} item xs={6} style={{ textAlign: "center" }}>
              {object.title.includes("Pie Chart:") && (
                <div>
                  <h5>{object.title}</h5>
                </div>
              )}
              <VegaChart spec={object} />
              <div style={{ height: "50px" }}></div>
            </Grid>
          ))}
      </Grid>
    </div>
  );
};

export default Visualisation;
