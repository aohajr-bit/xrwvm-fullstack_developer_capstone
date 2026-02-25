import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";

const PostReview = () => {
  const { id } = useParams();
  const navigate = useNavigate();

  const [cars, setCars] = useState([]);
  const [form, setForm] = useState({
    review: "",
    purchase: false,
    purchase_date: "",
    car: "",
  });

  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");
  const [successMsg, setSuccessMsg] = useState("");

  useEffect(() => {
    if (!id) {
      setError("Missing dealer id in route.");
      return;
    }

    const fetchCars = async () => {
      try {
        const response = await fetch("/djangoapp/get_cars", {
          method: "GET",
          credentials: "include",
        });

        if (!response.ok) {
          throw new Error(`Failed to fetch cars (${response.status})`);
        }

        const data = await response.json();

        if (!Array.isArray(data)) {
          throw new Error("Unexpected cars response shape");
        }

        setCars(data);
      } catch (err) {
        console.error("Error fetching cars:", err);
        setError(err.message || "Unable to load cars.");
      }
    };

    fetchCars();
  }, [id]);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;

    setForm((prev) => ({
      ...prev,
      [name]: type === "checkbox" ? checked : value,
    }));
  };

  const submitReview = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    setError("");
    setSuccessMsg("");

    try {
      const userName = localStorage.getItem("userName");
      const fullName = localStorage.getItem("fullName");
      const reviewerName = fullName || userName;

      if (!reviewerName) {
        throw new Error("Missing logged-in user name. Please log in again.");
      }

      const payload = {
        dealer_id: parseInt(id, 10),
        name: reviewerName,
        review: form.review,
        purchase: Boolean(form.purchase),
        purchase_date: form.purchase ? form.purchase_date : "",
        car: form.purchase ? form.car : "",
      };

      const response = await fetch("/djangoapp/add_review", {
        method: "POST",
        credentials: "include",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      const data = await response.json();

      if (!response.ok || data.status !== 200) {
        throw new Error(data.message || `Review submission failed (${response.status})`);
      }

      setSuccessMsg("Review submitted successfully!");
      setTimeout(() => {
        navigate("/dealers");
      }, 1000);
    } catch (err) {
      console.error("Submit review error:", err);
      setError(err.message || "An error occurred while submitting review.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="container mt-4">
      <h2>Post Review</h2>
      <p className="text-muted">Dealer ID: {id}</p>

      <form onSubmit={submitReview} style={{ maxWidth: "700px" }}>
        <div className="mb-3">
          <label className="form-label">Review</label>
          <textarea
            className="form-control"
            rows="4"
            name="review"
            value={form.review}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-check mb-3">
          <input
            className="form-check-input"
            type="checkbox"
            id="purchase"
            name="purchase"
            checked={form.purchase}
            onChange={handleChange}
          />
          <label className="form-check-label" htmlFor="purchase">
            I purchased this car
          </label>
        </div>

        {form.purchase && (
          <div className="row">
            <div className="col-md-6 mb-3">
              <label className="form-label">Purchase Date</label>
              <input
                className="form-control"
                type="date"
                name="purchase_date"
                value={form.purchase_date}
                onChange={handleChange}
                required
              />
            </div>

            <div className="col-md-6 mb-3">
              <label className="form-label">Car Make / Model</label>
              <select
                className="form-select"
                name="car"
                value={form.car}
                onChange={handleChange}
                required
              >
                <option value="">Select Car</option>
                {cars.map((c) => (
                  <option
                    key={c.id}
                    value={`${c.make} ${c.model} ${c.year}`}
                  >
                    {c.make} - {c.model} ({c.year})
                  </option>
                ))}
              </select>
            </div>
          </div>
        )}

        {error && <div className="alert alert-danger py-2">{error}</div>}
        {successMsg && <div className="alert alert-success py-2">{successMsg}</div>}

        <button type="submit" className="btn btn-primary" disabled={submitting}>
          {submitting ? "Submitting..." : "Submit Review"}
        </button>
      </form>
    </div>
  );
};

export default PostReview;