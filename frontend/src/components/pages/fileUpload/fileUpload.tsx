import { FunctionComponent, useEffect, useRef, useState } from "react";
import "./fileUpload.scss";
import {
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
import CloudUploadIcon from "@mui/icons-material/CloudUpload";
import * as XLSX from "xlsx"; // Import xlsx library
import DataContextQuestionaire from "../questionnaires/dataContextQuestionaire";

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
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [selectedColumns, setSelectedColumns] = useState<string[]>([]);
  const [columnNames, setColumnNames] = useState<string[]>([]);
  const [errorMessage, setErrorMessage] = useState<string>("");
  const fileInputRef = useRef<HTMLInputElement>(null);
  const allColumnsSelected =
    columnNames.length > 0 && selectedColumns.length === columnNames.length;
  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
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
    if (fileInputRef.current) {
      fileInputRef.current.click();
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

  const handleSelectAllClick = () => {
    if (allColumnsSelected) {
      setSelectedColumns([]);
    } else {
      setSelectedColumns(columnNames);
    }
  };

  useEffect(() => {
    handleSelectAllClick();
  }, [columnNames]);

  return (
    <Grid container className="file-upload-main-container">
      <Grid item xs={12} style={{ height: "5vh" }}>
        <h1>File Upload</h1>
      </Grid>
      <Grid
        item
        xs={12}
        className="file-upload-container"
        style={{ height: "20vh" }}
      >
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
                  sx={{
                    ".MuiSelect-select": {
                      paddingTop: "8px",
                      paddingBottom: "8px",
                      minHeight: "auto",
                      fontSize: "12px", // Adjust the font size as needed
                    },
                  }}
                  labelId="demo-multiple-checkbox-label"
                  id="demo-multiple-checkbox"
                  multiple
                  value={selectedColumns}
                  onChange={handleColumnChange}
                  input={<OutlinedInput label="Tag" />}
                  renderValue={(selected) => selected.join(", ")}
                  MenuProps={MenuProps}
                >
                  <MenuItem>
                    <Checkbox
                      checked={allColumnsSelected}
                      indeterminate={
                        selectedColumns.length > 0 &&
                        selectedColumns.length < columnNames.length
                      }
                      onChange={handleSelectAllClick}
                    />
                    <ListItemText primary="Select All" />
                  </MenuItem>
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
        </Grid>
      </Grid>
      {selectedFile && (
        <Grid
          item
          xs={12}
          className="questionaire-container"
          style={{ height: "50vh" }}
        >
          <h3>Questionaire</h3>
          <h5>
            The Questionnaire helps understand the purpose of data
            visualization. Participation is optional.
          </h5>
          <DataContextQuestionaire
            selectedFile={selectedFile}
            selectedColumns={selectedColumns}
          ></DataContextQuestionaire>
        </Grid>
      )}
    </Grid>
  );
};

export default FileUpload;
