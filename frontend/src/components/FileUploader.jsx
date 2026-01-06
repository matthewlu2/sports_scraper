import axios from "axios";
import { DataGrid } from '@mui/x-data-grid';
import Paper from '@mui/material/Paper';
import './FileUploader.css';
import upload from './arrow-up-from-bracket-solid-full.svg';
import refresh from './arrows-rotate-solid-full.svg'
import { useState } from "react";


const FileUploader = ({data, setData, status, setStatus}) => {
  const columns = [
    { field: 'name', headerName: 'Name', flex: 1, width: 150 },
    { field: 'stat', headerName: 'Stat', flex: 1, width: 150 },
    { field: 'projectedValue', headerName: 'Projected Value', flex: 1, width: 150 },
    { field: 'playerMean', headerName: 'Player Mean', flex: 1, width: 150 },
    { field: 'percentageOver', headerName: 'Percentage Over', flex: 1, width: 150 },
    { field: 'percentageUnder', headerName: 'Percentage Under', flex: 1, width: 150 },
    { field: 'percentOverThreshold', headerName: 'Percent Over Threshold', flex: 1, width: 150 },
    { field: 'type', headerName: 'Type', flex: 1, width: 150 },
    { field: 'allowedOptions', headerName: 'Allowed Options', flex: 1, width: 300 },
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
          <img src = {refresh} onClick={fetchData} className={`refresh ${spinning ? "spin" : ""}`} alt="refresh"/>
        </Paper>
      )}
    </div>
  )
};

export default FileUploader;
