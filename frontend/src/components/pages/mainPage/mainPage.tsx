import { Grid } from "@mui/material";
import { FunctionComponent, useEffect, useState } from "react";
import FileUpload from "../fileUpload/fileUpload";
import Visualisation from "../visualisation/visualisation";
import { userDetailsStore } from "../../store/userStore";

const MainPage: FunctionComponent = () => {
  const setUserDetails = userDetailsStore((state) => state.setUserDetails);
  const userDetails = userDetailsStore((state) => state.userDetails);
  useEffect(() => {
    if (userDetails == null)
      //default user is user2
      setUserDetails({
        username: "User2",
        password: "User2@123",
        userId: 2,
      });
  }, [setUserDetails, userDetails]);
  const [showVisualisation, setShowVisualisation] = useState(false);
  const [vegaObject, setVegaObject] = useState<any[]>([]);
  return (
    <Grid container>
      <Grid item xs={4}>
        <FileUpload
          setShowVisualisation={setShowVisualisation}
          setVegaObject={setVegaObject}
        />
      </Grid>
      <Grid item xs={8}>
        {showVisualisation && (
          <Visualisation vegaObject={vegaObject}></Visualisation>
        )}
      </Grid>
    </Grid>
  );
};

export default MainPage;
