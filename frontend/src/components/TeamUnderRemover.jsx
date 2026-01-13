import { useState } from "react";
import "./TeamUnderRemover.css";
import axios from "axios";

const NBA_TEAMS = [
  "ATL", "BOS", "BKN", "CHA", "CHI", "CLE", "DAL", "DEN",
  "DET", "GSW", "HOU", "IND", "LAC", "LAL", "MEM", "MIA",
  "MIL", "MIN", "NOP", "NYK", "OKC", "ORL", "PHI", "PHX",
  "POR", "SAC", "SAS", "TOR", "UTA", "WAS"
];

const TeamUnderRemover = ({setData}) => {
  const [selectedTeams, setSelectedTeams] = useState(new Set());
  const [showOverlay, setShowOverlay] = useState(false);

  function toggleTeam(team) {
    setSelectedTeams(prev => {
      const next = new Set(prev);
      next.has(team) ? next.delete(team) : next.add(team);
      return next;
    });
  }

  async function updateTeam() {
    setShowOverlay(false);
    try {
        await axios.post("/update_teams", { selected_teams: Array.from(selectedTeams) });
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
      .catch(err => console.error(err.message))
  };

  return (
    <>
      <button
        className="select-teams-btn"
        onClick={() => setShowOverlay(true)}
      >
        Select Teams ({selectedTeams.size})
      </button>

      {showOverlay && (
        <div className="overlay">
          <div className="modal">
            <h2>Select Teams</h2>

            <div className="team-grid">
              {NBA_TEAMS.map(team => (
                <label key={team} className="team-item">
                  <input
                    type="checkbox"
                    checked={selectedTeams.has(team)}
                    onChange={() => toggleTeam(team)}
                  />
                  {team}
                </label>
              ))}
            </div>

            <div className="modal-actions">
              <button
                className="close-btn"
                onClick={() => updateTeam()}
              >
                Done
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default TeamUnderRemover;
