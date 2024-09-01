import { Grid, IconButton, Tooltip } from "@mui/material";
import FileCopyIcon from "@mui/icons-material/FileCopy";
import OpenInNewIcon from "@mui/icons-material/OpenInNew";
import DownloadIcon from "@mui/icons-material/Download";
import DescriptionIcon from "@mui/icons-material/Description";

const VegaEditorButton = ({ vegaSpec }: any) => {
  const openVegaEditor = () => {
    window.open("https://vega.github.io/editor/#/edited", "_blank");
  };
  const copyToClipboard = async () => {
    try {
      await navigator.clipboard.writeText(JSON.stringify(vegaSpec, null, 2));
      alert("Vega specification copied to clipboard!");
    } catch (err) {
      console.error("Failed to copy: ", err);
    }
  };
  const downloadVegaObject = () => {
    const filename = "vegaJSON" + Date.now();
    const jsonStr = JSON.stringify(vegaSpec, null, 2);
    const blob = new Blob([jsonStr], { type: "application/json" });
    const link = document.createElement("a");
    link.download = `${filename}.json`;
    link.href = URL.createObjectURL(blob);
    document.body.appendChild(link);
    link.click();
    link.remove();
  };

  return (
    <Grid container xs={6}>
      {/* <Grid item xs={3}>
        <IconButton aria-label="description">
          <Tooltip title="Description">
            <DescriptionIcon fontSize="small" color="success" />
          </Tooltip>
        </IconButton>
      </Grid> */}
      <Grid item xs={3} key="copy">
        <IconButton aria-label="copy" onClick={copyToClipboard}>
          <Tooltip title="Copy Vega Object">
            <FileCopyIcon fontSize="small" color="success" />
          </Tooltip>
        </IconButton>
      </Grid>
      <Grid item xs={3} key="new-tab">
        <IconButton aria-label="open in new tab" onClick={openVegaEditor}>
          <Tooltip title="Open Vega Editor">
            <OpenInNewIcon fontSize="small" color="success" />
          </Tooltip>
        </IconButton>
      </Grid>
      <Grid item xs={3} key="download">
        <IconButton aria-label="download">
          <Tooltip title="Download Vega Object" onClick={downloadVegaObject}>
            <DownloadIcon fontSize="small" color="success" />
          </Tooltip>
        </IconButton>
      </Grid>
    </Grid>
  );
};

export default VegaEditorButton;
