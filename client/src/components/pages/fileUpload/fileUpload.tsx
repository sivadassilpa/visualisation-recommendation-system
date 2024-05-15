import { FunctionComponent, useRef, useState } from "react";
import "./fileUpload.scss";
import {
  Button,
  Checkbox,
  FormControl,
  Grid,
  IconButton,
  InputLabel,
  ListItemText,
  MenuItem,
  OutlinedInput,
  Select,
} from "@mui/material";
import PersonIcon from "@mui/icons-material/Person";
import CloudUploadIcon from "@mui/icons-material/CloudUpload";
import { userDetailsStore } from "../../store/userStore";
import * as XLSX from "xlsx"; // Import xlsx library
import { useNavigate } from "react-router-dom";

const ITEM_HEIGHT = 48;
const ITEM_PADDING_TOP = 8;
const MenuProps = {
  PaperProps: {
    style: {
      maxHeight: ITEM_HEIGHT * 4.5 + ITEM_PADDING_TOP,
      width: 250,
    },
  },
};

const FileUpload: FunctionComponent = () => {
  const userDetails = userDetailsStore((state) => state.userDetails);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [selectedColumns, setSelectedColumns] = useState<string[]>([]);
  const [columnNames, setColumnNames] = useState<string[]>([]);
  const [errorMessage, setErrorMessage] = useState<string>("");
  const fileInputRef = useRef<HTMLInputElement>(null);
  const navigate = useNavigate();
  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    console.log(file);
    if (file) {
      if (
        file.type === "text/csv" ||
        file.type === "application/vnd.ms-excel" ||
        file.type ===
          "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
      ) {
        setSelectedFile(file);
        setErrorMessage("");
        parseFile(file);
      } else {
        setSelectedFile(null);
        setErrorMessage("Only CSV or Excel files are allowed.");
      }
    }
  };

  const handleUploadButtonClick = () => {
    // Trigger the click event of the hidden file input
    if (fileInputRef.current) {
      fileInputRef.current.click();
    }
  };
  const handleSubmit = () => {
    if (selectedFile) {
      // Handle file upload here
      console.log("File uploaded:", selectedFile.name);
      navigate("/visualisation");
    } else {
      console.error("No file selected.");
    }
  };
  const parseFile = (file: File) => {
    const reader = new FileReader();
    reader.onload = (event) => {
      const data = event.target?.result as ArrayBuffer;
      const workbook = XLSX.read(data, { type: "array" });
      const firstSheetName = workbook.SheetNames[0];
      const worksheet = workbook.Sheets[firstSheetName];
      const sheetData: string[][] = XLSX.utils.sheet_to_json(worksheet, {
        header: 1,
      });
      if (sheetData.length > 0 && sheetData[0].length > 0) {
        setColumnNames(sheetData[0]);
      }
    };
    reader.readAsArrayBuffer(file);
  };
  const handleColumnChange = (event: any) => {
    setSelectedColumns(event.target.value as string[]);
  };

  return (
    <Grid container className="file-upload-main-container">
      {/* <Grid item container xs={12} className="header">
        <Grid item xs={6} className="username">
          <PersonIcon className="icon" />
          {userDetails?.username}
        </Grid>
        <Grid item xs={6} className="logout">
          Logout
        </Grid>
      </Grid> */}
      {/* <Grid item xs={12}>
        <hr />
      </Grid> */}
      <Grid item xs={12}>
        <h1>File Upload</h1>
      </Grid>
      <Grid item xs={12} className="file-upload-container">
        <Grid item xs={6} className="file-upload">
          <Grid item xs={12} className="file-upload-title">
            Please select a file
          </Grid>
          <Grid item xs={12}>
            <div>
              <input
                type="file"
                ref={fileInputRef}
                accept=".csv,.xls,.xlsx"
                onChange={handleFileChange}
                style={{ display: "none" }} // Hide the input element
              />
              <IconButton
                onClick={handleUploadButtonClick}
                className="icon-container"
              >
                <CloudUploadIcon className="icon" />
              </IconButton>
              {errorMessage && (
                <div style={{ color: "red", fontSize: "8pt" }}>
                  {errorMessage}
                </div>
              )}
            </div>
          </Grid>
          <Grid item xs={12} className="upload-hint">
            <div>Supported Formats : .csv, .xlsx, .xls</div>
          </Grid>
        </Grid>

        <Grid item xs={6} className="column-list">
          <Grid item xs={12} className="column-list-title">
            {selectedFile && <div>Selected file: {selectedFile.name}</div>}
          </Grid>
          <Grid item xs={12} className="column-list-selector">
            {selectedFile && (
              <FormControl sx={{ m: 1, width: 300 }}>
                <InputLabel id="demo-multiple-checkbox-label">Tag</InputLabel>
                <Select
                  labelId="demo-multiple-checkbox-label"
                  id="demo-multiple-checkbox"
                  multiple
                  value={selectedColumns}
                  onChange={handleColumnChange}
                  input={<OutlinedInput label="Tag" />}
                  renderValue={(selected) => selected.join(", ")}
                  MenuProps={MenuProps}
                >
                  {columnNames.map((columnName, index) => (
                    <MenuItem key={index} value={columnName}>
                      <Checkbox
                        checked={selectedColumns.indexOf(columnName) > -1}
                      />
                      <ListItemText primary={columnName} />
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            )}
          </Grid>
          <Grid item xs={12}>
            <Button
              variant="contained"
              className="upload-button"
              onClick={handleSubmit}
              disabled={!selectedFile}
            >
              Generate Visualisation
            </Button>
          </Grid>
        </Grid>
      </Grid>
    </Grid>
  );
};

export default FileUpload;
