import { FunctionComponent, useState } from "react";
import "./questionnaires.scss";
import { questions } from "../../utils/questions";
import { useNavigate } from "react-router-dom";
const Questionnaire: FunctionComponent = () => {
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [answers, setAnswers] = useState<Array<string | null>>(
    new Array(questions.length).fill(null)
  );
  const navigate = useNavigate();
  const handleOptionSelect = (option: string) => {
    const newAnswers = [...answers];
    newAnswers[currentQuestionIndex] = option;
    setAnswers(newAnswers);

    // Proceed to next question
    if (currentQuestionIndex < questions.length - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1);
    } else if (currentQuestionIndex === questions.length - 1) {
      navigate("/fileUpload");
    }
  };

  return (
    <div className="questionnaire">
      <h1>Questionnaire</h1>
      <div className="questionaire-container">
        <h2>{questions[currentQuestionIndex].question}</h2>
        <ul>
          {questions[currentQuestionIndex].options.map((option) => (
            <li key={option} onClick={() => handleOptionSelect(option)}>
              {option}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default Questionnaire;
