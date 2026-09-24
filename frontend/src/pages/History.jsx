import { useEffect, useState } from "react";
import axios from "axios";
import API_URL from "../config/api";

function History() {

  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const loadHistory = async () => {

    try {

      console.log(
        "Loading history from:",
        API_URL
      );

      const response =
        await axios.get(API_URL);

      console.log(
        "History response:",
        response.data
      );

      setHistory(response.data);

    } catch (err) {

      console.error(
        "History error:",
        err
      );

      if (err.response) {

        setError(
          `Backend error: ${err.response.status}`
        );

      } else {

        setError(
          "Cannot connect to backend. Make sure Spring Boot is running."
        );
      }

    } finally {

      setLoading(false);
    }
  };

  useEffect(() => {
    loadHistory();
  }, []);

  return (

    <div className="page-container">

      {/* HEADER */}

      <div className="page-header">

        <div className="badge">
          DATABASE
        </div>

        <h1>
          Prediction History
        </h1>

        <p>
          View all predictions stored
          in the database.
        </p>

      </div>


      {/* LOADING */}

      {loading && (

        <div className="center-message">
          Loading prediction history...
        </div>

      )}


      {/* ERROR */}

      {error && (

        <div className="error-box">
          {error}
        </div>

      )}


      {/* EMPTY */}

      {!loading &&
        !error &&
        history.length === 0 && (

          <div className="empty-history">

            <div className="empty-icon">
              📭
            </div>

            <h2>
              No Predictions Yet
            </h2>

            <p>
              Your prediction history will
              appear here after you analyze
              some text.
            </p>

          </div>

        )}


      {/* TABLE */}

      {!loading &&
        !error &&
        history.length > 0 && (

          <div className="history-table-wrapper">

            <table className="history-table">

              <thead>

                <tr>

                  <th>
                    ID
                  </th>

                  <th>
                    Text
                  </th>

                  <th>
                    Result
                  </th>

                  <th>
                    Confidence
                  </th>

                  <th>
                    Date
                  </th>

                </tr>

              </thead>


              <tbody>

                {history.map((item) => (

                  <tr key={item.id}>

                    <td>
                      #{item.id}
                    </td>

                    <td className="history-text">
                      {item.text}
                    </td>

                    <td>

                      <span className="result-badge">
                        {item.result}
                      </span>

                    </td>

                    <td>
                      {
                        (
                          Number(
                            item.confidence || 0
                          ) * 100
                        ).toFixed(2)
                      }%
                    </td>

                    <td>
                      {item.createdAt
                        ? new Date(
                            item.createdAt
                          ).toLocaleString()
                        : "-"}
                    </td>

                  </tr>

                ))}

              </tbody>

            </table>

          </div>

        )}

    </div>
  );
}

export default History;