import React, { useState, useEffect } from "react";
import "./Dealers.css";
import "../assets/style.css";
import Header from "../Header/Header";
import review_icon from "../assets/reviewicon.png";

const Dealers = () => {
  const [dealersList, setDealersList] = useState([]);
  const [states, setStates] = useState([]);

  // ✅ Keep base URLs constant (don't mutate them)
  const dealer_url = "/djangoapp/get_dealers";
  const dealer_url_by_state_base = "/djangoapp/get_dealers/";

  const filterDealers = async (state) => {
    try {
      // ✅ Handle "All"
      const url =
        state === "All" ? dealer_url : `${dealer_url_by_state_base}${state}`;

      const res = await fetch(url, { method: "GET" });
      const retobj = await res.json();

      if (retobj.status === 200) {
        setDealersList(Array.from(retobj.dealers || []));
      } else {
        setDealersList([]);
      }
    } catch (e) {
      console.error("filterDealers error:", e);
      setDealersList([]);
    }
  };

  const get_dealers = async () => {
    try {
      const res = await fetch(dealer_url, { method: "GET" });
      const retobj = await res.json();

      if (retobj.status === 200) {
        const all_dealers = Array.from(retobj.dealers || []);

        const allStates = all_dealers
          .map((d) => d.state)
          .filter(Boolean);

        // ✅ include "All" option
        setStates(["All", ...Array.from(new Set(allStates)).sort()]);
        setDealersList(all_dealers);
      } else {
        setStates(["All"]);
        setDealersList([]);
      }
    } catch (e) {
      console.error("get_dealers error:", e);
      setStates(["All"]);
      setDealersList([]);
    }
  };

  useEffect(() => {
    get_dealers();
  }, []);

  const isLoggedIn =
    sessionStorage.getItem("username") != null ? true : false;

  return (
    <div>
      <Header />

      <table className="table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Dealer Name</th>
            <th>City</th>
            <th>Address</th>
            <th>Zip</th>
            <th>
              <select
                name="state"
                id="state"
                defaultValue=""
                onChange={(e) => filterDealers(e.target.value)}
              >
                <option value="" disabled hidden>
                  State
                </option>
                {states.map((state) => (
                  <option key={state} value={state}>
                    {state === "All" ? "All States" : state}
                  </option>
                ))}
              </select>
            </th>

            {isLoggedIn ? <th>Review Dealer</th> : null}
          </tr>
        </thead>

        <tbody>
          {dealersList.map((dealer) => (
            <tr key={dealer.id}>
              <td>{dealer["id"]}</td>

              {/* ✅ Keep this: it routes to the dealer reviews page */}
              <td>
                <a href={`/dealer/${dealer["id"]}`}>
                  {dealer["full_name"]}
                </a>
              </td>

              <td>{dealer["city"]}</td>
              <td>{dealer["address"]}</td>
              <td>{dealer["zip"]}</td>
              <td>{dealer["state"]}</td>

              {isLoggedIn ? (
                <td>
                  <a href={`/postreview/${dealer["id"]}`}>
                    <img
                      src={review_icon}
                      className="review_icon"
                      alt="Post Review"
                    />
                  </a>
                </td>
              ) : null}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Dealers;