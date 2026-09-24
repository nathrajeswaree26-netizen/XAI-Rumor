import { Link } from "react-router-dom";

function Home() {
  return (
    <div className="home-page">

      <section className="hero">

        <div className="hero-content">

          <div className="badge">
            AI-POWERED RUMOR DETECTION
          </div>

          <h1>
            Detect Rumors with
            <span> Artificial Intelligence</span>
          </h1>

          <p>
            Analyze online information and identify whether a piece of
            text contains potentially misleading or unverified information.
          </p>

          <div className="hero-buttons">
            <Link to="/predict" className="primary-button">
              Start Prediction
            </Link>

            <Link to="/history" className="secondary-button">
              View History
            </Link>
          </div>

        </div>

        <div className="hero-card">

          <div className="ai-circle">
            AI
          </div>

          <h3>Rumor Detection System</h3>

          <p>
            Machine learning based text classification
          </p>

          <div className="status">
            <span></span>
            System Connected
          </div>

        </div>

      </section>

      <section className="features">

        <div className="feature-card">
          <div className="feature-icon">🤖</div>
          <h3>AI Analysis</h3>
          <p>
            Analyze submitted text using a dedicated machine learning
            service.
          </p>
        </div>

        <div className="feature-card">
          <div className="feature-icon">⚡</div>
          <h3>Fast Prediction</h3>
          <p>
            Submit text and receive the classification result through
            the backend API.
          </p>
        </div>

        <div className="feature-card">
          <div className="feature-icon">📊</div>
          <h3>Prediction History</h3>
          <p>
            View previous predictions stored in the database.
          </p>
        </div>

      </section>

    </div>
  );
}

export default Home;