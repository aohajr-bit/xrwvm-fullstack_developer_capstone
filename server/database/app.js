/*jshint esversion: 8 */
const express = require('express');
const mongoose = require('mongoose');
const fs = require('fs');
const cors = require('cors');

const app = express();
const port = 3030;

app.use(cors());

// Parse JSON + form bodies
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Load seed data (files must exist in server/database/)
const reviews_data = JSON.parse(fs.readFileSync('reviews.json', 'utf8'));
const dealerships_data = JSON.parse(fs.readFileSync('dealerships.json', 'utf8'));

// Connect to Mongo
mongoose.connect('mongodb://localhost:27017/', { dbName: 'dealershipsDB' });

const Reviews = require('./review');
const Dealerships = require('./dealership');

// Seed DB (best-effort)
(async () => {
  try {
    await Reviews.deleteMany({});
    await Reviews.insertMany(reviews_data.reviews || []);

    await Dealerships.deleteMany({});
    await Dealerships.insertMany(dealerships_data.dealerships || []);

    console.log('Seeded MongoDB: reviews + dealerships');
  } catch (err) {
    console.log('Seeding error:', err);
  }
})();

// Home
app.get('/', async (req, res) => {
  res.send('Welcome to the Mongoose API');
});

// Fetch all reviews
app.get('/fetchReviews', async (req, res) => {
  try {
    const documents = await Reviews.find();
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

// Fetch reviews by dealer
app.get('/fetchReviews/dealer/:id', async (req, res) => {
  try {
    const documents = await Reviews.find({ dealership: req.params.id });
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

// Fetch all dealerships
app.get('/fetchDealers', async (req, res) => {
  try {
    const documents = await Dealerships.find();
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

// Fetch dealers by state
app.get('/fetchDealers/:state', async (req, res) => {
  try {
    const state = (req.params.state || '').toUpperCase();
    let documents;

    if (state === 'ALL') {
      documents = await Dealerships.find();
    } else {
      documents = await Dealerships.find({ state: state });
    }

    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

// Fetch dealer by id
app.get('/fetchDealer/:id', async (req, res) => {
  try {
    const dealerId = parseInt(req.params.id, 10);
    const document = await Dealerships.findOne({ id: dealerId });
    res.json(document || {});
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

// Insert review (NOW WORKS with Django JSON posts)
app.post('/insert_review', async (req, res) => {
  try {
    const data = req.body || {};

    const latest = await Reviews.find().sort({ id: -1 }).limit(1);
    let new_id;

    if (latest && latest.length > 0 && latest[0].id != null) {
      new_id = latest[0].id + 1;
    } else {
      new_id = 1;
    }

    const review = new Reviews({
      id: new_id,
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
    res.json(savedReview);
  } catch (error) {
    console.log('Insert review error:', error);
    res.status(500).json({ error: 'Error inserting review' });
  }
});

// Start server
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
