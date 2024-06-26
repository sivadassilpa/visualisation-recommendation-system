import React, { useState } from "react";
import {
  TextField,
  Button,
  Typography,
  Box,
  Select,
  MenuItem,
  Checkbox,
  FormControl,
  InputLabel,
  ListItemText,
} from "@mui/material";
import { SApiService } from "../../services/app.service";

const RuleForm: React.FC = () => {
  const [ruleName, setRuleName] = useState("");
  const [description, setDescription] = useState("");
  const [condition, setCondition] = useState<string | null>("");
  const [informationType, setInformationType] = useState<string[]>([]);
  const [action, setAction] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const actions = [
    "Line Chart",
    "Bar Chart",
    "Scatter Plot",
    "Stacked Bar Chart",
    "Pie Chart",
    "Clustered Bar Chart",
  ];

  const informationTypes = [
    "null",
    "numbers",
    "categories",
    "dates",
    "boolean",
    "unknown",
  ];
  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();

    try {
      const response = await SApiService.insertRule({
        ruleName,
        description,
        condition: condition || null, // Ensure condition is null if empty string
        informationType:
          informationType.length > 0
            ? informationType.indexOf("null") > -1
              ? null
              : informationType.join(" AND ")
            : null,
        action,
      });

      if (response && response.message) {
        setMessage(response.message);
        setError("");
      } else {
        setMessage("");
        setError("Failed to insert rule.");
      }
    } catch (error) {
      setMessage("");
      setError("Failed to insert rule.");
    }
  };

  return (
    <Box
      sx={{
        maxWidth: 600,
        margin: "auto",
        mt: 4,
        p: 3,
        border: "1px solid #ccc",
        borderRadius: 5,
      }}
    >
      <Typography variant="h4" gutterBottom>
        Insert Rule
      </Typography>
      {message && (
        <Typography variant="body1" sx={{ color: "green" }}>
          {message}
        </Typography>
      )}
      {error && (
        <Typography variant="body1" sx={{ color: "red" }}>
          {error}
        </Typography>
      )}
      <form onSubmit={handleSubmit}>
        <TextField
          label="Rule Name"
          variant="outlined"
          fullWidth
          margin="normal"
          value={ruleName}
          onChange={(e) => setRuleName(e.target.value)}
          required
        />
        <TextField
          label="Description"
          variant="outlined"
          fullWidth
          margin="normal"
          multiline
          rows={4}
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          required
        />
        <TextField
          label="Condition"
          variant="outlined"
          fullWidth
          margin="normal"
          multiline
          rows={4}
          value={condition || null}
          onChange={(e) => setCondition(e.target.value)}
        />
        <FormControl fullWidth margin="normal">
          <InputLabel id="information-type-label">Information Type</InputLabel>
          <Select
            labelId="information-type-label"
            multiple
            value={informationType}
            onChange={(e) => setInformationType(e.target.value as string[])}
            renderValue={(selected) => (selected as string[]).join(" AND ")}
          >
            {informationTypes.map((type) => (
              <MenuItem key={type} value={type}>
                <Checkbox checked={informationType.includes(type)} />
                <ListItemText primary={type} />
              </MenuItem>
            ))}
          </Select>
        </FormControl>
        <Select
          label="Action"
          variant="outlined"
          fullWidth
          value={action}
          onChange={(e) => setAction(e.target.value as string)}
          required
        >
          {actions.map((option) => (
            <MenuItem key={option} value={option}>
              {option}
            </MenuItem>
          ))}
        </Select>
        <Button
          type="submit"
          variant="contained"
          color="primary"
          sx={{ mt: 2 }}
        >
          Insert Rule
        </Button>
      </form>
    </Box>
  );
};

export default RuleForm;
