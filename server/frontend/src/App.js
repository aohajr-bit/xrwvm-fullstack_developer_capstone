import LoginPanel from "./components/Login/Login";
import Dealers from "./components/Dealers/Dealers";
import Dealer from "./components/Dealers/Dealer";
import PostReview from "./components/Dealers/PostReview";
import { Routes, Route, Navigate } from "react-router-dom";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/login" replace />} />
      <Route path="/login" element={<LoginPanel />} />
      <Route path="/dealers" element={<Dealers />} />

      {/* ✅ ADD THIS */}
      <Route path="/dealer/:id" element={<Dealer />} />

      <Route path="/postreview/:id" element={<PostReview />} />
    </Routes>
  );
}

export default App;