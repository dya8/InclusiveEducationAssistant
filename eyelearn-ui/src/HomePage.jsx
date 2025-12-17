import { useNavigate } from "react-router-dom";
import "./HomePage.css";

export default function HomePage() {
  const navigate = useNavigate();

  return (
    <div className="home-container">
      <div className="header">
        <h2>EyeLearn</h2>
      </div>

      <div className="main-layout">
        <div className="left-panel">
          <div className="profile-box"></div>
        </div>

        <div className="content-area">
          <div className="top-buttons">
            <div className="btn" onClick={() => navigate("/notes")}>
              Notes
            </div>
            <div className="btn" onClick={() => navigate("/coding")}>
              Coding
            </div>
            <div className="btn" onClick={() => navigate("/ppt")}>
              PPT
            </div>
            <div className="btn" onClick={() => navigate("/ask-teacher")}>
              Ask Teacher
            </div>
          </div>

          <div className="display-area">
            <div className="scroll-bar"></div>
          </div>
        </div>
      </div>
    </div>
  );
}
