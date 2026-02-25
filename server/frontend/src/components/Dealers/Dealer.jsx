import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";

const Dealers = () => {
  const [dealers, setDealers] = useState([]);
  const [filteredDealers, setFilteredDealers] = useState([]);
  const [states, setStates] = useState(["All"]);
  const [selectedState, setSelectedState] = useState("All");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const normalizeDealers = (data) => {
    if (Array.isArray(data)) return data;
    if (data && Array.isArray(data.dealers)) return data.dealers;
    throw new Error("Unexpected dealers response shape");
  };

  useEffect(() => {
    const fetchDealers = async () => {
      try {
        setLoading(true);
        setError("");

        const response = await fetch("/djangoapp/get_dealers", {
          method: "GET",
          credentials: "include",
        });

        if (!response.ok) {
          throw new Error(`Failed to fetch dealers (${response.status})`);
        }

        const data = await response.json();
        const dealerList = normalizeDealers(data);

        setDealers(dealerList);
        setFilteredDealers(dealerList);

        const uniqueStates = [
          "All",
          ...Array.from(new Set(dealerList.map((d) => d.state).filter(Boolean))).sort(),
        ];
        setStates(uniqueStates);
      } catch (err) {
        console.error("Error fetching dealers:", err);
        setError(err.message || "Unable to load dealers.");
        setDealers([]);
        setFilteredDealers([]);
      } finally {
        setLoading(false);
      }
    };

    fetchDealers();
  }, []);

  const handleStateChange = (e) => {
    const state = e.target.value;
    setSelectedState(state);

    if (state === "All") {
      setFilteredDealers(dealers);
    } else {
      setFilteredDealers(dealers.filter((dealer) => dealer.state === state));
    }
  };

  return (
    <div className="container mt-4">
      <h2>Dealerships</h2>

      <div className="mb-3" style={{ maxWidth: "300px" }}>
        <label className="form-label">Filter by State</label>
        <select
          className="form-select"
          value={selectedState}
          onChange={handleStateChange}
        >
          {states.map((state) => (
            <option key={state} value={state}>
              {state}
            </option>
          ))}
        </select>
      </div>

      {loading && <p>Loading dealers...</p>}
      {error && <div className="alert alert-danger">{error}</div>}

      {!loading && !error && (
        <>
          {filteredDealers.length > 0 ? (
            <div className="row">
              {filteredDealers.map((dealer) => {
                if (dealer.id === undefined || dealer.id === null) {
                  throw new Error("Dealer is missing required 'id' field");
                }

                return (
                  <div className="col-md-6 col-lg-4 mb-4" key={dealer.id}>
                    <div className="card h-100 shadow-sm">
                      <div className="card-body">
                        <h5 className="card-title">
                          {dealer.full_name || dealer.name || "Dealer"}
                        </h5>

                        <p className="card-text mb-1">
                          <strong>City:</strong> {dealer.city || "N/A"}
                        </p>
                        <p className="card-text mb-1">
                          <strong>State:</strong> {dealer.state || "N/A"}
                        </p>
                        <p className="card-text mb-2">
                          <strong>Address:</strong> {dealer.address || "N/A"}
                        </p>

                        <div className="d-flex gap-2 flex-wrap">
                          <Link
                            className="btn btn-primary btn-sm"
                            to={`/postreview/${dealer.id}`}
                          >
                            Add Review
                          </Link>
                        </div>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          ) : (
            <p>No dealers found.</p>
          )}
        </>
      )}
    </div>
  );
};

export default Dealers;