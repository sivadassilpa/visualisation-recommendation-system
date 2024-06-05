import { FunctionComponent, useEffect, useState } from "react";
import VegaChart from "../vega/vega";
import { userDetailsStore } from "../../store/userStore";
import { useLocation } from "react-router-dom";

const Visualisation: FunctionComponent = () => {
  const userDetails = userDetailsStore((state) => state.userDetails);
  const [vegaObject, setVegaObject] = useState();
  const location = useLocation();

  useEffect(() => {
    if (userDetails?.username && location.state.vegaspec) {
      setVegaObject(location.state.vegaspec);
    }
  }, [userDetails, location.state.vegaspec, location.state]);

  return (
    <div>
      <div className="home-title">Visualisation Page for {"username"}</div>
      {vegaObject && <VegaChart spec={vegaObject} />}
    </div>
  );
};

export default Visualisation;
