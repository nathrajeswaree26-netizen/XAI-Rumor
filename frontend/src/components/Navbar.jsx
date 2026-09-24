import { Link } from "react-router-dom";

function Navbar() {
  return (
    <nav className="navbar">
      <div className="nav-container">

        <Link to="/" className="logo">
          Rumor<span>Detect</span>
        </Link>

        <div className="nav-links">
          <Link to="/">Home</Link>
          <Link to="/predict">Predict</Link>
          <Link to="/history">History</Link>
        </div>

      </div>
    </nav>
  );
}

export default Navbar;