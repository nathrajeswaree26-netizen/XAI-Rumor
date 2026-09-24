
import { useState } from "react";
import axios from "axios";
import API_URL from "../config/api";

function Predict() {
  const [text, setText] = useState("");
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handlePredict = async () => {
    if (!text.trim()) {
      setError("Please enter some text first.");
      return;
    }

    setLoading(true);
    setError("");
    setPrediction(null);

    try {
      console.log("Sending request to:", API_URL);

      const response = await axios.post(API_URL, {
        text: text.trim(),
      });

      console.log("Backend response:", response.data);

      setPrediction(response.data);
    } catch (err) {
      console.error("Prediction error:", err);

      if (err.response) {
        setError(`Backend error: ${err.response.status}`);
      } else if (err.request) {
        setError(
          "Cannot connect to backend. Make sure Spring Boot is running on port 8081."
        );
      } else {
        setError("An unexpected error occurred.");
      }
    } finally {
      setLoading(false);
    }
  };

  const getResultClass = () => {
    if (!prediction?.result) {
      return "";
    }

    const result = prediction.result.toUpperCase();

    if (result === "RUMOR") {
      return "result-rumor";
    }

    if (
      result === "NON-RUMOR" ||
      result.includes("TRUE") ||
      result.includes("REAL")
    ) {
      return "result-real";
    }

    return "result-pending";
  };

  const confidence = Number(prediction?.confidence || 0) * 100;

  /*
   * Backend response example:
   *
   * {
   *   "id": 24,
   *   "text": "...",
   *   "result": "non-rumor",
   *   "confidence": 0.625,
   *   "limeExplanation": [
   *      {
   *        "word": "announced",
   *        "weight": -0.0877
   *      }
   *   ]
   * }
   */

  const limeExplanation = prediction?.limeExplanation || [];

  return (
    <div className="page-container">
      {/* PAGE HEADER */}

      <div className="page-header">
        <div className="badge">AI PREDICTION</div>

        <h1>Analyze a Statement</h1>

        <p>
          Enter a news statement, social media post, or claim to analyze it.
        </p>
      </div>

      {/* PREDICTION AREA */}

      <div className="prediction-layout">
        {/* INPUT CARD */}

        <div className="prediction-card">
          <label htmlFor="rumor-text">Enter Text</label>

          <textarea
            id="rumor-text"
            value={text}
            onChange={(event) => setText(event.target.value)}
            placeholder="Enter the statement you want to analyze..."
            rows="9"
          />

          <div className="character-count">
            {text.length} characters
          </div>

          <button
            className="predict-button"
            onClick={handlePredict}
            disabled={loading}
          >
            {loading ? "Analyzing..." : "Analyze Statement"}
          </button>

          {/* ERROR */}

          {error && <div className="error-box">{error}</div>}
        </div>

        {/* RESULT CARD */}

        <div className="result-card">
          <h2>Prediction Result</h2>

          {/* EMPTY RESULT */}

          {!prediction && !loading && (
            <div className="empty-result">
              <div className="empty-icon">🔍</div>

              <p>Your prediction result will appear here.</p>
            </div>
          )}

          {/* LOADING */}

          {loading && (
            <div className="loading-result">
              <div className="loader"></div>

              <p>Analyzing your text...</p>
            </div>
          )}

          {/* RESULT */}

          {prediction && !loading && (
            <div
              className={`prediction-result ${getResultClass()}`}
            >
              {/* CLASSIFICATION */}

              <div className="result-label">
                Classification
              </div>

              <div className="result-value">
                {prediction.result}
              </div>

              {/* CONFIDENCE */}

              <div className="confidence-section">
                <div className="confidence-header">
                  <span>Confidence</span>

                  <strong>
                    {confidence.toFixed(2)}%
                  </strong>
                </div>

                <div className="confidence-bar">
                  <div
                    className="confidence-fill"
                    style={{
                      width: `${Math.min(confidence, 100)}%`,
                    }}
                  ></div>
                </div>
              </div>

              {/* LIME EXPLAINABILITY */}

              <div className="lime-section">
                <div className="lime-header">
                  <div>
                    <h3>🧠 LIME Explainability</h3>

                    <p>
                      Words that influenced the prediction
                    </p>
                  </div>
                </div>

                {/* LIME RESULTS */}

                {limeExplanation.length > 0 ? (
                  <div className="lime-list">
                    {limeExplanation.map((item, index) => {
                      const weight = Number(item.weight || 0);

                      const positive = weight >= 0;

                      return (
                        <div
                          className={`lime-item ${
                            positive
                              ? "lime-positive"
                              : "lime-negative"
                          }`}
                          key={index}
                        >
                          <div className="lime-word">
                            {item.word}
                          </div>

                          <div className="lime-weight">
                            {positive ? "+" : ""}
                            {weight.toFixed(4)}
                          </div>
                        </div>
                      );
                    })}
                  </div>
                ) : (
                  <div className="lime-empty">
                    No LIME explanation is available for this
                    prediction.
                  </div>
                )}

                {/* LIME LEGEND */}

                {limeExplanation.length > 0 && (
                  <div className="lime-legend">
                    <div className="legend-positive">
                      <span className="legend-dot">●</span>
                      Positive influence
                    </div>

                    <div className="legend-negative">
                      <span className="legend-dot">●</span>
                      Negative influence
                    </div>
                  </div>
                )}
              </div>

              {/* PREDICTION ID */}

              {prediction.id && (
                <div className="prediction-id">
                  Prediction ID: #{prediction.id}
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default Predict;

