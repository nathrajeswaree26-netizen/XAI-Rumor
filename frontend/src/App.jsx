import { BrowserRouter, Routes, Route } from "react-router-dom";

import Navbar from "./components/Navbar";
import Home from "./pages/Home";
import Predict from "./pages/Predict";
import History from "./pages/History";

import "./App.css";

function App() {
  return (
    <BrowserRouter>
      <Navbar />

      <main>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/predict" element={<Predict />} />
          <Route path="/history" element={<History />} />
        </Routes>
      </main>
    </BrowserRouter>
  );
}

export default App;