import { BrowserRouter, Routes, Route } from "react-router-dom";
import DashboardPage from "./pages/DashboardPage";
import DevicePage from "./pages/DevicePage";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<DashboardPage />} />
        <Route path="/device/:id" element={<DevicePage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
