import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import Header from "../Header/Header";

const Dealer = () => {
  const { id } = useParams();

  const [dealer, setDealer] = useState(null);
  const [reviews, setReviews] = useState([]);
  const [error, setError] = useState("");

  const isLoggedIn = sessionStorage.getItem("username") != null;

  const normalizeReviews = (data) => {
    if (Array.isArray(data)) return data;
    if (data && Array.isArray(data.reviews)) return data.reviews;
    if (data && Array.isArray(data.results)) return data.results;
    if (data && Array.isArray(data.data)) return data.data;
    return [];
  };

  useEffect(() => {
    const load = async () => {
      try {
        setError("");

        // Dealer details
        const d = await fetch(`/djangoapp/get_dealer/${id}`, { method: "GET" });
        const dealerData = await d.json();
        setDealer(dealerData);

        // Reviews
        const r = await fetch(`/djangoapp/get_reviews/${id}`, { method: "GET" });
        const reviewsData = await r.json();
        setReviews(normalizeReviews(reviewsData));
      } catch (e) {
        console.error(e);
        setError("Unable to load dealer and reviews.");
      }
    };

    load();
  }, [id]);

  return (
    <div>
      <Header />
      <div className="container mt-4">
        {error ? <div className="alert alert-danger">{error}</div> : null}

        <h2>Dealer Details</h2>
        {dealer ? (
          <div style={{ marginBottom: "16px" }}>
            <div>
              <strong>{dealer.full_name || dealer.name || `Dealer ${id}`}</strong>
            </div>
            <div>{dealer.address || ""}</div>
            <div>
              {dealer.city || ""} {dealer.state || ""} {dealer.zip || ""}
            </div>

            {/* ✅ Requirement: PostReview link on Dealer page for logged-in users */}
            {isLoggedIn ? (
              <div style={{ marginTop: "12px" }}>
                <a className="btn btn-primary btn-sm" href={`/postreview/${id}`}>
                  Post Review
                </a>
              </div>
            ) : null}
          </div>
        ) : (
          <p>Loading dealer...</p>
        )}

        <h3>Reviews</h3>
        {reviews.length > 0 ? (
          <ul>
            {reviews.map((rev, idx) => (
              <li key={rev.id ?? idx} style={{ marginBottom: "12px" }}>
                <div>
                  <strong>{rev.name || "Anonymous User"}</strong>{" "}
                  {rev.sentiment ? `(${rev.sentiment})` : ""}
                </div>
                <div>{rev.review}</div>
                <div style={{ fontSize: "0.9em", opacity: 0.8 }}>
                  {rev.car_make && rev.car_model && rev.car_year
                    ? `${rev.car_make} ${rev.car_model} (${rev.car_year})`
                    : ""}
                  {rev.purchase_date ? ` • ${rev.purchase_date}` : ""}
                </div>
              </li>
            ))}
          </ul>
        ) : (
          <p>No reviews found.</p>
        )}
      </div>
    </div>
  );
};

export default Dealer;