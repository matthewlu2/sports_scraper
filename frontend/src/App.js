import { useState , useEffect} from "react";
import FileUploader from "./components/FileUploader";
import { DataGrid } from '@mui/x-data-grid';
import Paper from '@mui/material/Paper';
import refresh from './components/arrows-rotate-solid-full.svg'
import './App.css';

function App() {
  const [data, setData] = useState([]);
  const [error, setError] = useState(null);
  const [spinning, setSpinning] = useState(false);

  const [tab1, setTab1] = useState(true);
  const [tab2, setTab2] = useState(false);

  const [uploadedData, setUploadedData] = useState([]);
  const [uploadStatus, setUploadStatus] = useState("idle");

  const columns = [
    { field: 'name', headerClassName: 'super-app-theme--header', headerName: 'Name', flex: 1, width: 150 },
    { field: 'stat', headerClassName: 'super-app-theme--header', headerName: 'Stat', flex: 1, width: 150 },
    { field: 'projectedValue', headerClassName: 'super-app-theme--header', headerName: 'Projected Value', flex: 1, width: 150 },
    { field: 'type', headerClassName: 'super-app-theme--header', headerName: 'Type', flex: 1, width: 150 },
    { field: 'allowedOptions', headerClassName: 'super-app-theme--header', headerName: 'Allowed Options', flex: 1, width: 300 },
  ];

  const paginationModel = {page: 0, pageSize: 50};

  const fetchData = () => {
    setSpinning(true);
    setError(null);

    fetch("/scrape_betr")
      .then(res => res.json())
      .then(json => {
        const results = Array.isArray(json) ? json : json.data;
        setData(results ?? []);
      })
      .catch(err => setError(err.message))
      .finally(() => setSpinning(false));
  };

  useEffect(() => {
    fetchData();
  }, []);


  return (
    <div className="app">
      <div className="header">
        <button className={tab1 ? "tab active" : "tab"} onClick={() => {setTab1(true); setTab2(false);}}>Scraped Stats</button>
        <button className={tab2 ? "tab active" : "tab"} onClick={() => {setTab1(false); setTab2(true);}}>Upload File</button>
      </div>

      <div className="content">
        {tab1 && 
          <div>
            {error && <p>Error: {error}</p>}
            {data.length > 0 && (
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
                  sx={{ 
                    border: 0,
                    // color: 'white',
                    // bgcolor: '#1E1E1E',
                    // '& .super-app-theme--header': {
                    //   backgroundColor: '#1E1E1E',
                    // },    
                    // '& .MuiButtonBase-root': {
                    //   color: 'white',
                    // },     
                  }}
                />
                <img src = {refresh} onClick={fetchData} className={`refresh ${spinning ? "spin" : ""}`} alt="refresh"/>
              </Paper>
            )}
          </div>
        }
        {tab2 && 
          <FileUploader 
            data={uploadedData} 
            setData={setUploadedData} 
            status={uploadStatus} 
            setStatus={setUploadStatus}
          />
        }
      </div>
    </div>
  );
}

export default App;
