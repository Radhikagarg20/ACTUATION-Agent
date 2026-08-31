import React, {
  useEffect,
  useState
} from "react";


const API =
  import.meta.env.VITE_API_URL ||
  "http://localhost:8000";


const demoIncident = {
  title: "Major water leakage near Block B",
  description:
    "A large water leak has been flowing onto the road since morning. The leakage appears to be getting worse and is creating a serious obstruction.",
  location: "Block B Campus Road"
};


function App() {

  const [
    incidents,
    setIncidents
  ] = useState([]);

  const [
    selected,
    setSelected
  ] = useState(null);

  const [
    form,
    setForm
  ] = useState(demoIncident);

  const [
    loading,
    setLoading
  ] = useState(false);

  const [
    agentStatus,
    setAgentStatus
  ] = useState(
    "AUTONOMOUS SYSTEM ONLINE"
  );


  async function loadIncidents() {

    try {

      const response =
        await fetch(
          `${API}/api/incidents`
        );

      const data =
        await response.json();

      setIncidents(
        data.incidents || []
      );

    } catch (error) {

      console.error(error);

    }

  }


  async function submitIncident(
    event
  ) {

    event.preventDefault();

    setLoading(true);

    setAgentStatus(
      "AGENT PROCESSING..."
    );

    try {

      const response =
        await fetch(
          `${API}/api/incidents/sync`,
          {
            method: "POST",

            headers: {
              "Content-Type":
                "application/json"
            },

            body: JSON.stringify(form)
          }
        );

      const data =
        await response.json();

      setSelected(data);

      await loadIncidents();

      setAgentStatus(
        "AUTONOMOUS RESPONSE COMPLETE"
      );

    } catch (error) {

      console.error(error);

      setAgentStatus(
        "CONNECTION ERROR"
      );

    } finally {

      setLoading(false);

    }

  }


  useEffect(() => {

    loadIncidents();

    const interval =
      setInterval(
        loadIncidents,
        3000
      );

    return () =>
      clearInterval(interval);

  }, []);


  async function openIncident(
    incident
  ) {

    try {

      const response =
        await fetch(
          `${API}/api/incidents/${incident.id}`
        );

      const data =
        await response.json();

      setSelected(data);

    } catch (error) {

      console.error(error);

    }

  }


  return (

    <div className="app">

      <header className="topbar">

        <div className="brand">

          <div className="brandMark">
            A
          </div>

          <div>

            <h1>ACTUATION</h1>

            <p>
              Autonomous Incident Operations
            </p>

          </div>

        </div>


        <div className="systemStatus">

          <span className="pulse"></span>

          {agentStatus}

        </div>

      </header>


      <main className="layout">


        <section className="mainPanel">


          <div className="hero">

            <div>

              <span className="eyebrow">
                AI OPERATIONS ENGINE
              </span>

              <h2>
                Problems shouldn't wait
                for people to solve them.
              </h2>

              <p>

                ACTUATION detects,
                analyzes, routes,
                monitors and verifies
                real-world incidents
                autonomously.

              </p>

            </div>


            <div className="heroOrb">

              <div className="orbCore">
                AI
              </div>

            </div>

          </div>


          <div className="stats">

            <Stat
              label="Active Incidents"
              value={incidents.length}
            />

            <Stat
              label="Autonomous Actions"
              value="24"
            />

            <Stat
              label="Resolution Confidence"
              value="87%"
            />

            <Stat
              label="System Status"
              value="LIVE"
            />

          </div>


          <section className="card">

            <div className="cardHeader">

              <div>

                <span className="eyebrow">
                  NEW INCIDENT
                </span>

                <h3>
                  Start autonomous response
                </h3>

              </div>

              <span className="liveBadge">
                LIVE
              </span>

            </div>


            <form
              onSubmit={submitIncident}
            >

              <label>
                Incident title

                <input
                  value={form.title}
                  onChange={(e) =>
                    setForm({
                      ...form,
                      title:
                        e.target.value
                    })
                  }
                />

              </label>


              <label>
                Location

                <input
                  value={form.location}
                  onChange={(e) =>
                    setForm({
                      ...form,
                      location:
                        e.target.value
                    })
                  }
                />

              </label>


              <label>
                Description

                <textarea
                  rows="5"
                  value={
                    form.description
                  }
                  onChange={(e) =>
                    setForm({
                      ...form,
                      description:
                        e.target.value
                    })
                  }
                />

              </label>


              <button
                disabled={loading}
                className="primaryButton"
              >

                {loading
                  ? "AGENT WORKING..."
                  : "ACTIVATE AUTONOMOUS RESPONSE →"}

              </button>

            </form>

          </section>


          <section className="card">

            <div className="cardHeader">

              <div>

                <span className="eyebrow">
                  OPERATIONS
                </span>

                <h3>
                  Incident stream
                </h3>

              </div>

            </div>


            <div className="incidentList">

              {incidents.length === 0 ? (

                <div className="empty">
                  No incidents yet.
                </div>

              ) : (

                incidents.map(
                  (incident) => (

                    <button
                      className="incidentRow"
                      key={incident.id}
                      onClick={() =>
                        openIncident(
                          incident
                        )
                      }
                    >

                      <div className="incidentIcon">
                        {incident.severity ===
                        "CRITICAL"
                          ? "!"
                          : "●"}
                      </div>


                      <div className="incidentInfo">

                        <strong>
                          {incident.title}
                        </strong>

                        <span>
                          {incident.location}
                        </span>

                      </div>


                      <div className="incidentMeta">

                        <span>
                          {incident.priority}
                        </span>

                        <small>
                          {incident.status}
                        </small>

                      </div>

                    </button>

                  )
                )

              )}

            </div>

          </section>

        </section>


        <aside className="sidePanel">


          {selected ? (

            <IncidentDetail
              incident={selected}
              api={API}
            />

          ) : (

            <div className="agentPanel">

              <span className="eyebrow">
                AGENT ACTIVITY
              </span>

              <h3>
                Autonomous engine
              </h3>

              <p>
                Submit an incident to watch
                ACTUATION reason and act.
              </p>


              <div className="flow">

                <FlowStep
                  active
                  title="Detect"
                  description="Understand incoming signal"
                />

                <FlowStep
                  title="Decide"
                  description="Classify and prioritize"
                />

                <FlowStep
                  title="Act"
                  description="Route and initiate response"
                />

                <FlowStep
                  title="Monitor"
                  description="Track operational state"
                />

                <FlowStep
                  title="Verify"
                  description="Confirm resolution"
                />

                <FlowStep
                  title="Resolve"
                  description="Close or escalate"
                />

              </div>

            </div>

          )}

        </aside>

      </main>

    </div>
  );
}


function Stat({
  label,
  value
}) {

  return (

    <div className="stat">

      <span>
        {label}
      </span>

      <strong>
        {value}
      </strong>

    </div>

  );

}


function FlowStep({
  title,
  description,
  active
}) {

  return (

    <div
      className={
        `flowStep ${
          active ? "active" : ""
        }`
      }
    >

      <div className="flowDot">
        {active ? "✓" : "○"}
      </div>

      <div>

        <strong>
          {title}
        </strong>

        <span>
          {description}
        </span>

      </div>

    </div>

  );

}


function IncidentDetail({
  incident,
  api
}) {

  const [
    events,
    setEvents
  ] = useState([]);


  useEffect(() => {

    async function load() {

      const response =
        await fetch(
          `${api}/api/incidents/${incident.id}/events`
        );

      const data =
        await response.json();

      setEvents(
        data.events || []
      );

    }

    load();

    const timer =
      setInterval(
        load,
        2000
      );

    return () =>
      clearInterval(timer);

  }, [
    incident.id,
    api
  ]);


  return (

    <div className="agentPanel">

      <span className="eyebrow">
        INCIDENT {incident.id}
      </span>

      <h3>
        {incident.title}
      </h3>


      <div className="statusLarge">

        <span>
          STATUS
        </span>

        <strong>
          {incident.status}
        </strong>

      </div>


      <div className="metrics">

        <Metric
          label="Severity"
          value={
            incident.severity
          }
        />

        <Metric
          label="Priority"
          value={
            incident.priority
          }
        />

        <Metric
          label="Confidence"
          value={
            `${Math.round(
              incident.confidence * 100
            )}%`
          }
        />

        <Metric
          label="Duplicates"
          value={
            incident.duplicate_count
          }
        />

      </div>


      <div className="routeBox">

        <span>
          RESPONSIBLE DEPARTMENT
        </span>

        <strong>
          {incident.department}
        </strong>

      </div>


      <div className="timeline">

        <div className="timelineTitle">
          AUTONOMOUS TIMELINE
        </div>


        {events.map(
          (event, index) => (

            <div
              className="timelineItem"
              key={index}
            >

              <div className="timelineDot">
                ✓
              </div>

              <div>

                <strong>
                  {event.type}
                </strong>

                <p>
                  {event.message}
                </p>

              </div>

            </div>

          )
        )}

      </div>


      <div className="plan">

        <div className="timelineTitle">
          ACTION PLAN
        </div>

        {(
          incident.action_plan ||
          []
        ).map(
          (step, index) => (

            <div
              className="planItem"
              key={index}
            >

              <span>
                {index + 1}
              </span>

              {step}

            </div>

          )
        )}

      </div>

    </div>

  );

}


function Metric({
  label,
  value
}) {

  return (

    <div className="metric">

      <span>
        {label}
      </span>

      <strong>
        {value}
      </strong>

    </div>

  );

}


export default App;