// This page need to be moved to backend

const countryList = require("country-list");
export interface IQuestion {
  title: string;
  question: string;
  options: string[];
}
const countryOptions = countryList.getNames();

export const dataLevelQuestions: IQuestion[] = [
  {
    title: "objective",
    question: "What is your primary objective with this data?",
    options: [
      "Understanding general trends (Exploratory Data Analysis)",
      "Comparing different groups or categories (Comparison)",
      "Tracking changes over time (Trend Analysis)",
      "Identifying the distribution of data (Distribution Analysis)",
      "I’m not sure/Other",
      "I prefer not to answer",
    ],
  },
  // Below option is currently ignored
  // {
  //   title: "dataType",
  //   question: "What kind of information are you working with?",
  //   options: [
  //     "Numbers (like counts or amounts)",
  //     "Categories (like types of things)",
  //     "Dates and times",
  //     "Words or sentences",
  //   ],
  // },
  {
    title: "patternsinterest",
    question: "Are you looking to identify patterns or trends in the data?",
    options: ["Yes", "No", "I'm not sure", "I prefer not to answer"],
  },
  {
    title: "groupcomparison",
    question:
      "Are you interested in comparing different groups within the dataset?",
    options: ["Yes", "No", "I'm not sure", "I prefer not to answer"],
  },
  {
    title: "colorpreferences",
    question:
      "Do you have any preferences for colour schemes or aesthetics in your visualizations??",
    options: [
      "Yes *then give a list to choose from",
      "No",
      "I prefer not to answer",
    ], // to be handled
  },
  {
    title: "usecase",
    question: "How do you want to use your visualizations??",
    options: [
      "Just to look at",
      "To interact with and explore",
      "I prefer not to answer",
    ],
  },
];
export const userLevelQuestions: IQuestion[] = [
  {
    title: "familiarity",
    question:
      "How familiar are you with data visualization terms like ‘bar chart’, ‘line graph’, etc.??",
    options: [
      "I prefer not to answer",
      "Very familiar",
      "Somewhat familiar",
      "Not familiar at all",
      "I know some terms but not others.",
    ],
  },
  {
    title: "profession",
    question: "What is your profession?",
    options: [
      "I prefer not to answer",
      "Data Analyst",
      "Research Assistant",
      "Scientist",
      "Data Scientist",
      "Business Analyst",
      "Software Engineer",
      "Data Engineer",
      "Statistician",
      "Financial Analyst",
      "Marketing Analyst",
      "Product Manager",
      "Operations Manager",
      "Consultant",
      "Academic Researcher",
      "Healthcare Analyst",
      "Sales Analyst",
      "Economist",
      "Sociologist",
      "Engineer (General)",
      "Project Manager",
      "Policy Analyst",
      "Educator/Teacher",
      "Student",
      "IT Specialist",
      "Others",
    ],
  },
  {
    title: "interests",
    question:
      "What specific domains or areas are you most interested in analyzing?",
    options: [
      "I prefer not to answer",
      "Finance",
      "Healthcare",
      "Marketing",
      "Sales",
      "Education",
      "Research",
      "Others",
    ],
  },
  {
    title: "country",
    question: "Which is your location?",
    options: ["I prefer not to answer", ...countryOptions], // first option should 'I prefer not to say
  },
];
