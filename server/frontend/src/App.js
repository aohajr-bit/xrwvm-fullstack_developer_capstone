import LoginPanel from "./components/Login/Login";
import Dealers from "./components/Dealers/Dealers";
import PostReview from "./components/Dealers/PostReview";
import { Routes, Route, Navigate } from "react-router-dom";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/login" replace />} />
      <Route path="/login" element={<LoginPanel />} />
      <Route path="/dealers" element={<Dealers />} />
      <Route path="/postreview/:id" element={<PostReview />} />
    </Routes>
  );
}

export default App;