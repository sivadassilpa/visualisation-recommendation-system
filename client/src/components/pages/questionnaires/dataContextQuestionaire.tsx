import { FunctionComponent, useState } from "react";
import "./questionnaires.scss";
import { dataLevelQuestions } from "../../utils/questions";
import { useNavigate } from "react-router-dom";
import { FormControl, Select, MenuItem, Button, Grid } from "@mui/material";
import _ from "lodash";
import { SApiService } from "../../services/app.service";
import { userDetailsStore } from "../../store/userStore";
interface IDataContextComponentProps {
  selectedFile: File;
  selectedColumns: string[];
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
  const { selectedFile, selectedColumns } = props;
  const userDetails = userDetailsStore((state) => state.userDetails);
  const [answers, setAnswers] = useState<IQuestionaireResponse[]>(
    _.cloneDeep(defaultDataContextAnswers)
  );
  const navigate = useNavigate();
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
      console.log("skipping..."); // ignore and go to fileupload
    }
    console.log("after skip...");
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
      console.log(data);
      SApiService.uploadFile(data)
        .then((res) => {
          console.log(res);
          //navigate('/visualisation')
        })
        .catch((err) => {
          console.log(err);
        });
    }

    navigate("/fileUpload");
  };

  return (
    <Grid
      container
      columnSpacing={3}
      rowSpacing={1}
      className="questionnaire-container-data"
    >
      {answers.map((question, index) => (
        <Grid item xs={6} key={index}>
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
              {dataLevelQuestions[index].options.map((option, optionIndex) => (
                <MenuItem key={optionIndex} value={option}>
                  {option}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </Grid>
      ))}
      <Grid item xs={12}>
        <Button
          style={{ float: "right", marginTop: "20px" }}
          variant="contained"
          onClick={() => {
            handleSubmit(true);
          }}
          disabled={!selectedFile}
        >
          Skip Questionnaire
        </Button>
        <Button
          style={{ float: "left", marginTop: "20px" }}
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
    </Grid>
  );
};

export default DataContextQuestionaire;
