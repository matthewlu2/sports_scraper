import axios from "axios";
import { DataGrid } from '@mui/x-data-grid';
import Paper from '@mui/material/Paper';
import './FileUploader.css';
import upload from './arrow-up-from-bracket-solid-full.svg';
import refresh from './arrows-rotate-solid-full.svg'
import { useState } from "react";
import TeamUnderRemover from "./TeamUnderRemover";
import SecondaryUpload from "./SecondaryUpload";
import TeamRemover from "./TeamRemover";


const FileUploader = ({data, setData, status, setStatus}) => {
  const columns = [
    { field: 'name', headerName: 'Name', flex: 1, width: 150 },
    { field: 'team', headerName: 'Team', flex: 1, width: 50 },
    { field: 'stat', headerName: 'Stat', flex: 1, width: 150 },
    { field: 'projectedValue', headerName: 'Line', flex: 1, width: 150 },
    { field: 'playerMean', headerName: 'Proj', flex: 1, width: 150 },
    { field: 'percentageOver', headerName: '% Over', flex: 1, width: 150 },
    { field: 'percentageUnder', headerName: '% Under', flex: 1, width: 150 },
    { field: 'percentOverThreshold', headerName: '% > Threshold', flex: 1, width: 150 },
    { field: 'odds', headerName: 'Fair Value', flex: 1, width: 150 },
    { field: 'type', headerName: 'Type', flex: 1, width: 150 },
    { field: 'option', headerName: 'Option', flex: 1, width: 300 },
  ];

  const paginationModel = {page: 0, pageSize: 50};

  const [spinning, setSpinning] = useState(false);


  async function handleFileChange(e) {
    const selectedFile = e.target.files[0];
    if (!selectedFile) return;
    setStatus("uploading");
    const formData = new FormData();
    formData.append("file", selectedFile); 
    try {
        await axios.post("/upload", formData, {
            headers: { "Content-Type": "multipart/form-data" },
        });
        fetchData();
        setStatus("success");
    } catch (error) {
        console.error(error);
        setStatus("error");
    }
  }

  const fetchData = () => {
    setSpinning(true);

    fetch("/get_calculations")
      .then(res => res.json())
      .then(json => {
        const results = Array.isArray(json) ? json : json.data;
        setData(results ?? []);
      })
      .catch(err => console.error(err.message))
      .finally(() => setSpinning(false));
  };

  return (
    <div className="file-container">
      {data.length === 0 && 
        <div className="file-upload">
          <input id="fileInput" type="file" className='upload' onChange={handleFileChange}/>
          <img src={upload} alt="Upload Icon" className='upload-icon'/>
          <label htmlFor="fileInput" className='file-label'>Choose File</label>
        </div>
      }
      {status === "uploading" && <p className="uploading-message">Uploading file...</p>}
      {status === "error" && <p className="error-message">Upload failed. Please try again.</p>}
      {status === "success" && data.length > 0 && (
        <Paper sx={{ 
                    height: "95vh", 
                    width: '100%',
                    }}>
          <DataGrid
            rows={data}
            columns={columns}
            initialState={{ pagination: { paginationModel } }}
            pageSizeOptions={[50, 100]}
            disableRowSelectionOnClick
            sx={{ border: 0 }}
          />
          <div className="bottom-left">
            <img src = {refresh} onClick={fetchData} className={`refresh_upload ${spinning ? "spin" : ""}`} alt="refresh"/>
            <TeamUnderRemover setData={setData} />
            <SecondaryUpload setData={setData} />
            <TeamRemover setData={setData} />
          </div>
        </Paper>
      )}
    </div>
  )
};

export default FileUploader;
