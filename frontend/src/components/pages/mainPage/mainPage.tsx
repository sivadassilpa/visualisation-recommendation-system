import { Grid } from "@mui/material";
import { FunctionComponent, useState } from "react";
import FileUpload from "../fileUpload/fileUpload";
import Visualisation from "../visualisation/visualisation";

const MainPage: FunctionComponent = () => {
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
