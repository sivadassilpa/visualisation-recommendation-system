import { FunctionComponent, useState } from "react";
import "./questionnaires.scss";
import { userLevelQuestions } from "../../utils/questions";
import { useNavigate } from "react-router-dom";
import { FormControl, Select, MenuItem, Button } from "@mui/material";
import _ from "lodash";
import { SApiService } from "../../services/app.service";
import { userDetailsStore } from "../../store/userStore";

export interface IQuestionaireResponse {
  title: string;
  optionSelected: string;
}

const defaultUserLevelAnswers: IQuestionaireResponse[] = userLevelQuestions.map(
  (question) => ({
    title: question.title,
    optionSelected: "I prefer not to answer", // Default option: "Not familiar at all"
  })
);

const UserLevelQuestionnaires: FunctionComponent = () => {
  const userDetails = userDetailsStore((state) => state.userDetails);
  const [answers, setAnswers] = useState<IQuestionaireResponse[]>(
    _.cloneDeep(defaultUserLevelAnswers)
  );
  const navigate = useNavigate();
  const handleOptionSelect = (index: number, option: string) => {
    const newAnswers = [...answers];
    newAnswers[index].optionSelected = option;
    setAnswers(newAnswers);
  };

  const handleSubmit = (isSkip: boolean) => {
    if (isSkip) {
      setAnswers(_.cloneDeep(defaultUserLevelAnswers));
    } else if (!_.isEqual(answers, defaultUserLevelAnswers)) {
      if (userDetails?.userId) {
        const data = { userId: userDetails?.userId, userProfile: answers };
        SApiService.updateUserProfile(data);
      }
    }
    navigate("/main");
  };

  return (
    <div className="questionnaire">
      <h1>Questionnaire</h1>

      <div className="questionaire-container">
        {answers.map((question, index) => (
          <FormControl key={index} fullWidth>
            <h4>{userLevelQuestions[index].question}</h4>
            <Select
              labelId={`question-label-${index}`}
              value={question.optionSelected}
              onChange={(event) =>
                handleOptionSelect(index, event.target.value)
              }
            >
              {userLevelQuestions[index].options.map((option, optionIndex) => (
                <MenuItem key={optionIndex} value={option}>
                  {option}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        ))}

        <Button
          style={{ float: "right", marginTop: "20px" }}
          variant="contained"
          onClick={() => {
            handleSubmit(false);
          }}
        >
          Proceed
        </Button>
        <Button
          style={{ float: "left", marginTop: "20px" }}
          variant="contained"
          onClick={() => {
            handleSubmit(true);
          }}
        >
          Skip
        </Button>
      </div>
    </div>
  );
};

export default UserLevelQuestionnaires;
