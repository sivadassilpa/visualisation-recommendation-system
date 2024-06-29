import { Dispatch, FunctionComponent, useState } from "react";
import "./questionnaires.scss";
import { dataLevelQuestions } from "../../utils/questions";
import { useNavigate } from "react-router-dom";
import {
  FormControl,
  Select,
  MenuItem,
  Button,
  Grid,
  Tooltip,
} from "@mui/material";
import _ from "lodash";
import { SApiService } from "../../services/app.service";
import { userDetailsStore } from "../../store/userStore";

export interface IDataContextComponentProps {
  selectedFile: File;
  selectedColumns: string[];
  setShowVisualisation?: Dispatch<React.SetStateAction<boolean>>;
  setVegaObject?: React.Dispatch<React.SetStateAction<any[]>>;
}

export interface IQuestionaireResponse {
  title: string;
  optionSelected: string;
}

const defaultDataContextAnswers: IQuestionaireResponse[] =
  dataLevelQuestions.map((question) => ({
    title: question.title,
    optionSelected: "I prefer not to answer", // Default option: "Not familiar at all"
  }));

const DataContextQuestionaire: FunctionComponent<IDataContextComponentProps> = (
  props
) => {
  const { selectedFile, selectedColumns, setShowVisualisation, setVegaObject } =
    props;
  const userDetails = userDetailsStore((state) => state.userDetails);
  const [answers, setAnswers] = useState<IQuestionaireResponse[]>(
    _.cloneDeep(defaultDataContextAnswers)
  );
  const setUserDetails = userDetailsStore((state) => state.setUserDetails);

  const handleOptionSelect = (index: number, option: string) => {
    const newAnswers = [...answers];
    newAnswers[index].optionSelected = option;
    setAnswers(newAnswers);
  };

  const handleSubmit = (isSkip: boolean) => {
    if (!selectedFile) {
      console.error("No file selected.");
      return;
    }

    if (isSkip) {
      setAnswers(_.cloneDeep(defaultDataContextAnswers));
    }
    if (userDetails?.userId) {
      const dataProfileList = isSkip ? defaultDataContextAnswers : answers;
      const dataProfileDict = _.reduce(
        dataProfileList,
        (result, item) => {
          result[item.title] = item.optionSelected;
          return result;
        },
        {} as { [key: string]: string }
      );

      const data = {
        userId: userDetails?.userId,
        dataProfile: dataProfileDict,
        selectedFile: selectedFile,
        selectedColumns: selectedColumns,
      };
      setVegaObject && setVegaObject([]);
      SApiService.uploadFile(data)
        .then((res) => {
          // navigate("/visualisation", { state: res });
          const currentUserDetails = userDetailsStore.getState().userDetails;
          if (currentUserDetails) {
            userDetailsStore.getState().setUserDetails({
              ...currentUserDetails,
              dataProfileId: res.dataProfileId,
            });
          }
          setVegaObject && setVegaObject(res.vegaspec);
          setShowVisualisation && setShowVisualisation(true);
        })
        .catch((err) => {
          console.log(err);
          setVegaObject && setVegaObject([]);
          setShowVisualisation && setShowVisualisation(false);
        });
    }

    // navigate("/fileUpload");
  };

  return (
    <>
      <Grid item xs={12} className="questionaire-container">
        <Tooltip
          title="The Questionnaire helps understand the purpose of data
            visualization. Participation is optional."
        >
          <h3 style={{ paddingBottom: "5px" }}>Questionaire</h3>
        </Tooltip>{" "}
        <Grid
          container
          columnSpacing={3}
          rowSpacing={1}
          className="questionnaire-container-data"
        >
          {answers.map((question, index) => (
            <Grid item xs={12} key={index}>
              <FormControl fullWidth>
                <h6>{dataLevelQuestions[index].question}</h6>
                <Select
                  key={index}
                  labelId={`question-label-${index}`}
                  value={question.optionSelected}
                  onChange={(event) =>
                    handleOptionSelect(index, event.target.value)
                  }
                  sx={{
                    ".MuiSelect-select": {
                      paddingTop: "8px",
                      paddingBottom: "8px",
                      minHeight: "auto",
                      fontSize: "12px", // Adjust the font size as needed
                    },
                  }}
                >
                  {dataLevelQuestions[index].options.map(
                    (option, optionIndex) => (
                      <MenuItem key={optionIndex} value={option}>
                        {option}
                      </MenuItem>
                    )
                  )}
                </Select>
              </FormControl>
            </Grid>
          ))}
        </Grid>
      </Grid>
      <Grid item xs={12} style={{ margin: "5px" }}>
        <Button
          style={{ float: "right", marginTop: "5px", fontSize: "8pt" }}
          variant="contained"
          onClick={() => {
            handleSubmit(true);
          }}
          disabled={!selectedFile}
        >
          Skip Questionnaire
        </Button>
        <Button
          style={{ float: "left", marginTop: "5px", fontSize: "8pt" }}
          variant="contained"
          onClick={() => {
            handleSubmit(false);
          }}
          disabled={
            _.isEqual(answers, defaultDataContextAnswers) || !selectedFile
          }
        >
          Generate Visualisation
        </Button>
      </Grid>
    </>
  );
};

export default DataContextQuestionaire;
