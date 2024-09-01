import { FunctionComponent } from "react";
import VegaChart from "../vega/vega";
import { userDetailsStore } from "../../store/userStore";
import { Button, Grid } from "@mui/material";
import ThumbUpIcon from "@mui/icons-material/ThumbUp";
import ThumbDownIcon from "@mui/icons-material/ThumbDown";
import { SApiService } from "../../services/app.service";
import VegaEditorButton from "./vegaEditorButton";
const Visualisation: FunctionComponent<{ vegaObject?: any[] }> = (props) => {
  const { vegaObject } = props;
  const userDetails = userDetailsStore((state) => state.userDetails);
  const feedback = (userPreference: boolean, ruleId: number) => {
    if (userDetails?.userId && userDetails?.dataProfileId) {
      const data = {
        ruleId: ruleId,
        userProfileId: userDetails?.userId,
        dataProfileId: userDetails?.dataProfileId,
        preference: userPreference,
      };
      SApiService.insertFeedback(data)
        .then((res) => {
          console.log("Successfull", res);
        })
        .catch((err) => {
          console.log("Failed", err);
        });
    }
  };

  return (
    <div>
      <Grid
        item
        xs={12}
        style={{
          height: "5vh",
          textAlign: "center",
          fontSize: "18pt",
          fontWeight: "bold",
        }}
      >
        <span>Visualization Page for {userDetails?.username}</span>
      </Grid>
      <Grid
        style={{
          width: "100%",
          maxHeight: "90vh",
          overflowY: "auto",
          paddingRight: "10px",
          marginBottom: "10px",
        }}
        container
      >
        {vegaObject &&
          vegaObject.map((object: any, index) => {
            const vegaObject = object.vegaSpec;
            const ruleId = object.ruleId;
            const { title, ...vegaSpec } = vegaObject; // Destructure to remove title from object
            return (
              <Grid
                key={index}
                item
                xs={6}
                style={{
                  textAlign: "center",
                  border: "1px solid grey",
                  display: "flex",
                  flexDirection: "column",
                  justifyContent: "space-between",
                }}
              >
                <Grid
                  style={{
                    height: "70px",
                    width: "100%",
                    textAlign: "right",
                    padding: "20px 20px 0 0",
                  }}
                  container
                >
                  <Grid item xs={9}>
                    <div style={{ textAlign: "center", fontWeight: "bold" }}>
                      {title}
                    </div>
                  </Grid>
                  <Grid item xs={1.5}>
                    <Button
                      style={{ color: "#7bff73" }}
                      onClick={() => feedback(true, ruleId)}
                    >
                      <ThumbUpIcon />
                    </Button>
                  </Grid>
                  <Grid item xs={1.5}>
                    <Button
                      style={{ color: "#8a1b1b" }}
                      onClick={() => feedback(false, ruleId)}
                    >
                      <ThumbDownIcon />
                    </Button>
                  </Grid>
                </Grid>
                <Grid item style={{ flexGrow: 1 }}>
                  <VegaChart spec={vegaSpec} />
                </Grid>
                {userDetails?.useCase === "To interact with and explore" && (
                  <Grid item>
                    <VegaEditorButton vegaSpec={vegaSpec} />
                  </Grid>
                )}
              </Grid>
            );
          })}
      </Grid>
    </div>
  );
};

export default Visualisation;
