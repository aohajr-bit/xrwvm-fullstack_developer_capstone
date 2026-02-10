const express = require('express');
const mongoose = require('mongoose');
const fs = require('fs');
const cors = require('cors');

const app = express();
const port = 3030;

app.use(cors());
app.use(require('body-parser').urlencoded({ extended: false }));

// ✅ If your JSON files are inside a "data" folder, change these paths to:
// "data/reviews.json" and "data/dealerships.json"
const reviews_data = JSON.parse(fs.readFileSync("reviews.json", "utf8"));
const dealerships_data = JSON.parse(fs.readFileSync("dealerships.json", "utf8"));

mongoose.connect("mongodb://mongo_db:27017/", { dbName: "dealershipsDB" });

const Reviews = require("./review");
const Dealerships = require("./dealership");

// ✅ Seed the database (don’t use res here — this is not inside a route)
try {
  Reviews.deleteMany({}).then(() => {
    Reviews.insertMany(reviews_data["reviews"]);
  });

  Dealerships.deleteMany({}).then(() => {
    Dealerships.insertMany(dealerships_data["dealerships"]);
  });
} catch (error) {
  console.log("DB seed error:", error);
}

// Home route
app.get("/", async (req, res) => {
  res.send("Welcome to the Mongoose API");
});

// Fetch all reviews
app.get("/fetchReviews", async (req, res) => {
  try {
    const documents = await Reviews.find();
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: "Error fetching documents" });
  }
});

// Fetch reviews for a particular dealer
app.get("/fetchReviews/dealer/:id", async (req, res) => {
  try {
    const documents = await Reviews.find({ dealership: req.params.id });
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: "Error fetching documents" });
  }
});

// ✅ Fetch all dealerships
app.get("/fetchDealers", async (req, res) => {
  try {
    const documents = await Dealerships.find();
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: "Error fetching documents" });
  }
});

// ✅ Fetch dealerships by state
app.get("/fetchDealers/:state", async (req, res) => {
  try {
    const stateParam = req.params.state;
    const documents = await Dealerships.find({ state: stateParam });
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: "Error fetching documents" });
  }
});

// ✅ Fetch dealer by id
app.get("/fetchDealer/:id", async (req, res) => {
  try {
    const dealerId = parseInt(req.params.id);
    const documents = await Dealerships.find({ id: dealerId });
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: "Error fetching documents" });
  }
});

// Insert review
app.post("/insert_review", express.raw({ type: "*/*" }), async (req, res) => {
  data = JSON.parse(req.body);

  const documents = await Reviews.find().sort({ id: -1 });
  let new_id = documents[0]["id"] + 1;

  const review = new Reviews({
    id: new_id,
    name: data["name"],
    dealership: data["dealership"],
    review: data["review"],
    purchase: data["purchase"],
    purchase_date: data["purchase_date"],
    car_make: data["car_make"],
    car_model: data["car_model"],
    car_year: data["car_year"],
  });

  try {
    const savedReview = await review.save();
    res.json(savedReview);
  } catch (error) {
    console.log(error);
    res.status(500).json({ error: "Error inserting review" });
  }
});

// Start server
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
