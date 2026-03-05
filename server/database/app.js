/*jshint esversion: 8 */
const express = require("express");
const mongoose = require("mongoose");
const fs = require("fs");
const cors = require("cors");

const app = express();
const port = process.env.PORT || 3030;

app.use(cors());

// Parse JSON + form bodies
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Connect to Mongo (K8s uses MONGODB_URI, local falls back)
const mongoUri = process.env.MONGODB_URI || "mongodb://localhost:27017/";
mongoose.connect(mongoUri, { dbName: "dealershipsDB" });

const Reviews = require("./review");
const Dealerships = require("./dealership");

// Load seed data (files must exist in server/database/)
function loadJsonFile(path) {
  try {
    return JSON.parse(fs.readFileSync(path, "utf8"));
  } catch (err) {
    console.log(`Seed file missing or invalid: ${path}`);
    return null;
  }
}

const reviewsData = loadJsonFile("reviews.json");
const dealershipsData = loadJsonFile("dealerships.json");

// Seed DB (best-effort)
(async () => {
  try {
    if (reviewsData && Array.isArray(reviewsData.reviews)) {
      await Reviews.deleteMany({});
      await Reviews.insertMany(reviewsData.reviews);
    }

    if (dealershipsData && Array.isArray(dealershipsData.dealerships)) {
      await Dealerships.deleteMany({});
      await Dealerships.insertMany(dealershipsData.dealerships);
    }

    console.log("Seeded MongoDB: reviews + dealerships");
  } catch (err) {
    console.log("Seeding error:", err);
  }
})();

// Home
app.get("/", async (req, res) => {
  res.send("Welcome to the Mongoose API");
});

// Fetch all reviews
app.get("/fetchReviews", async (req, res) => {
  try {
    const documents = await Reviews.find();
    return res.json({ reviews: documents });
  } catch (error) {
    return res.status(500).json({ error: "Error fetching documents" });
  }
});

// Fetch reviews by dealer
app.get("/fetchReviews/dealer/:id", async (req, res) => {
  try {
    const dealerId = parseInt(req.params.id, 10);
    const documents = await Reviews.find({ dealership: dealerId });
    return res.json({ reviews: documents });
  } catch (error) {
    return res.status(500).json({ error: "Error fetching documents" });
  }
});

// Fetch all dealerships
app.get("/fetchDealers", async (req, res) => {
  try {
    const documents = await Dealerships.find();
    return res.json({ dealerships: documents });
  } catch (error) {
    return res.status(500).json({ error: "Error fetching documents" });
  }
});

// Fetch dealers by state
app.get("/fetchDealers/:state", async (req, res) => {
  try {
    const state = String(req.params.state || "").toUpperCase();
    let documents;

    if (state === "ALL") {
      documents = await Dealerships.find();
    } else {
      documents = await Dealerships.find({ state: state });
    }

    return res.json({ dealerships: documents });
  } catch (error) {
    return res.status(500).json({ error: "Error fetching documents" });
  }
});

// Fetch dealer by id
app.get("/fetchDealer/:id", async (req, res) => {
  try {
    const dealerId = parseInt(req.params.id, 10);
    const document = await Dealerships.findOne({ id: dealerId });
    return res.json({ dealership: document || {} });
  } catch (error) {
    return res.status(500).json({ error: "Error fetching documents" });
  }
});

// Insert review (works with Django JSON posts)
app.post("/insert_review", async (req, res) => {
  try {
    const data = req.body || {};

    const latest = await Reviews.find().sort({ id: -1 }).limit(1);
    const newId =
      latest && latest.length > 0 && latest[0].id != null ? latest[0].id + 1 : 1;

    const review = new Reviews({
      id: newId,
      name: data.name,
      dealership: data.dealership,
      review: data.review,
      purchase: data.purchase,
      purchase_date: data.purchase_date,
      car_make: data.car_make,
      car_model: data.car_model,
      car_year: data.car_year,
      sentiment: data.sentiment,
    });

    const savedReview = await review.save();
    return res.json(savedReview);
  } catch (error) {
    console.log("Insert review error:", error);
    return res.status(500).json({ error: "Error inserting review" });
  }
});

// Start server
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
