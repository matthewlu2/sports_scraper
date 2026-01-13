import axios from "axios";
import upload from './arrow-up-from-bracket-solid-full.svg';
import './SecondaryUpload.css';


const SecondaryUpload = ({ setData }) => {
  async function handleFileChange(e) {
    const selectedFile = e.target.files[0];
    if (!selectedFile) return;

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      await axios.post("/upload_secondary", formData);
      fetchData();
    } catch (error) {
      console.error(error);
    }
  }

  const fetchData = () => {
    fetch("/get_calculations")
      .then(res => res.json())
      .then(json => {
        const results = Array.isArray(json) ? json : json.data;
        setData(results ?? []);
      })
      .catch(err => console.error(err.message));
  };

  return (
    <div className="secondary-container">
      <input
        id="secondaryInput"
        type="file"
        onChange={handleFileChange}
      />

      <label htmlFor="secondaryInput" className="secondary-label">
        <img src={upload} alt="Upload" className="secondary-icon" />
        <span>Upload Secondary</span>
      </label>
    </div>
  );
};

export default SecondaryUpload;
