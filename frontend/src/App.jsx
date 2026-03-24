import { useEffect, useState } from "react";

const API_BASE_URL = "http://localhost:8080/api/alerts";

function formatTimestamp(timestamp) {
  if (!timestamp) {
    return "No alerts yet";
  }

  return new Date(timestamp).toLocaleString();
}

function App() {
  const [alerts, setAlerts] = useState([]);
  const [systemArmed, setSystemArmed] = useState(true);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let mounted = true;

    async function fetchAlerts() {
      try {
        // Polling is enough for a showcase and simpler than wiring WebSockets on day one.
        const response = await fetch(API_BASE_URL);
        const data = await response.json();

        if (mounted) {
          setAlerts(data);
          setLoading(false);
        }
      } catch (error) {
        if (mounted) {
          setLoading(false);
        }
      }
    }

    fetchAlerts();
    const intervalId = setInterval(fetchAlerts, 3000);

    return () => {
      mounted = false;
      clearInterval(intervalId);
    };
  }, []);

  async function clearAlerts() {
    await fetch(API_BASE_URL, { method: "DELETE" });
    setAlerts([]);
  }

  // The UI treats the newest alert as the active incident.
  const latestAlert = alerts[0] ?? null;
  const intruderDetected = Boolean(latestAlert) && systemArmed;

  return (
    <div className={intruderDetected ? "app alert-state" : "app"}>
      <div className="background-grid" />
      <header className="hero">
        <div>
          <p className="eyebrow">Tech Sutra Showcase</p>
          <h1>Smart Intruder Alert System</h1>
          <p className="subtitle">
            AI-assisted surveillance dashboard for live unauthorized access
            detection.
          </p>
        </div>

        <div className="hero-actions">
          <button
            className={systemArmed ? "arm-button armed" : "arm-button"}
            onClick={() => setSystemArmed((value) => !value)}
          >
            {systemArmed ? "System Armed" : "System Disarmed"}
          </button>
          <button className="secondary-button" onClick={clearAlerts}>
            Clear Alerts
          </button>
        </div>
      </header>

      <main className="dashboard">
        <section className="status-card">
          <span className="status-dot" />
          <div>
            <h2>{intruderDetected ? "Intruder Detected" : "System Secure"}</h2>
            <p>
              {intruderDetected
                ? "Unknown face captured and reported to control center."
                : "No active intrusions in the current monitoring window."}
            </p>
          </div>
        </section>

        <section className="metrics-grid">
          <article className="metric-card">
            <p>Total Alerts</p>
            <strong>{alerts.length}</strong>
          </article>
          <article className="metric-card">
            <p>Camera ID</p>
            <strong>{latestAlert?.cameraId ?? "CAM-01"}</strong>
          </article>
          <article className="metric-card">
            <p>Last Incident</p>
            <strong>{formatTimestamp(latestAlert?.timestamp)}</strong>
          </article>
        </section>

        <section className="content-grid">
          <article className="panel spotlight-panel">
            <div className="panel-header">
              <h3>Latest Snapshot</h3>
              <span>{latestAlert?.severity ?? "NORMAL"}</span>
            </div>

            {latestAlert ? (
              <>
                <img
                  className="intruder-image"
                  src={`data:image/jpeg;base64,${latestAlert.imageBase64}`}
                  alt="Intruder snapshot"
                />
                <div className="snapshot-meta">
                  <p>{latestAlert.message}</p>
                  <p>{formatTimestamp(latestAlert.timestamp)}</p>
                </div>
              </>
            ) : (
              <div className="empty-state">
                {loading ? "Loading alerts..." : "Waiting for first incident..."}
              </div>
            )}
          </article>

          <article className="panel">
            <div className="panel-header">
              <h3>Alert Timeline</h3>
              <span>{alerts.length} event(s)</span>
            </div>

            <div className="alert-list">
              {alerts.length === 0 ? (
                <div className="empty-state">No alerts recorded yet.</div>
              ) : (
                alerts.map((alert) => (
                  <div className="alert-item" key={alert.id}>
                    <div>
                      <strong>Alert #{alert.id}</strong>
                      <p>{alert.message}</p>
                    </div>
                    <span>{formatTimestamp(alert.timestamp)}</span>
                  </div>
                ))
              )}
            </div>
          </article>
        </section>
      </main>
    </div>
  );
}

export default App;
