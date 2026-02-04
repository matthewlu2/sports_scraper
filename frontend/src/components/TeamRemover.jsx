import { useState } from "react";
import "./TeamRemover.css";
import axios from "axios";

const NBA_TEAMS = [
  "ATL", "BOS", "BKN", "CHA", "CHI", "CLE", "DAL", "DEN",
  "DET", "GSW", "HOU", "IND", "LAC", "LAL", "MEM", "MIA",
  "MIL", "MIN", "NOP", "NYK", "OKC", "ORL", "PHI", "PHX",
  "POR", "SAC", "SAS", "TOR", "UTA", "WAS"
];

const TeamRemover = ({setData}) => {
  const [removedTeams, setRemovedTeams] = useState(new Set());
  const [showOverlay, setShowOverlay] = useState(false);

  function toggleTeam(team) {
    setRemovedTeams(prev => {
      const next = new Set(prev);
      next.has(team) ? next.delete(team) : next.add(team);
      return next;
    });
  }

  async function updateTeam() {
    setShowOverlay(false);
    try {
        await axios.post("/remove_teams", { removed_teams: Array.from(removedTeams) });
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
        className="remove-teams-btn"
        onClick={() => setShowOverlay(true)}
      >
        Remove Teams ({removedTeams.size})
      </button>

      {showOverlay && (
        <div className="overlay">
          <div className="modal">
            <h2>Remove Teams</h2>

            <div className="team-grid">
              {NBA_TEAMS.map(team => (
                <label key={team} className="team-item">
                  <input
                    type="checkbox"
                    checked={removedTeams.has(team)}
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

export default TeamRemover;
