import { Routes, Route } from "react-router-dom";
import HomePage from "./HomePage.jsx";
import Notes from "./pages/Notes.jsx";
import Coding from "./pages/Coding.jsx";
import PPT from "./pages/PPT.jsx";
import AskTeacher from "./pages/AskTeacher.jsx";

function App() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/notes" element={<Notes />} />
      <Route path="/coding" element={<Coding />} />
      <Route path="/ppt" element={<PPT />} />
      <Route path="/ask-teacher" element={<AskTeacher />} />
    </Routes>
  );
}

export default App;
