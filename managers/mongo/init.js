// init.js
// This script runs automatically when MongoDB container starts
// if placed in /docker-entrypoint-initdb.d/

// Switch to test database
db = db.getSiblingDB('test');

// Create an index for better query performance
db.users.createIndex({ region: 1 });

// Generate random data
function generateRandomData(count) {
    const regions = ['EU', 'US', 'ASIA'];
    const cities = ['Paris', 'New York', 'Tokyo', 'London', 'Beijing', 'Sydney'];
    const batch = [];
    
    for(let i = 0; i < count; i++) {
        batch.push({
            _id: i,
            userId: `USER_${i}`,
            age: Math.floor(Math.random() * 80) + 18,
            score: Math.floor(Math.random() * 100000),
            region: regions[i % regions.length],
            city: cities[Math.floor(Math.random() * cities.length)],
            isActive: Math.random() > 0.5,
            lastLogin: new Date(Date.now() - Math.floor(Math.random() * 90 * 24 * 60 * 60 * 1000)), // Random date within last 90 days
            tags: Array.from({length: Math.floor(Math.random() * 5) + 1}, 
                  () => ['premium', 'basic', 'trial', 'vip', 'new'][Math.floor(Math.random() * 5)])
        });

        // Insert in batches of 1000 for better performance
        if (batch.length === 1000) {
            db.users.insertMany(batch);
            batch.length = 0;
        }
    }

    // Insert remaining documents
    if (batch.length > 0) {
        db.users.insertMany(batch);
    }
}

// Generate 10,000 documents
generateRandomData(10000);

// Print summary
print('Data generation completed');
print('Total documents:', db.users.countDocuments());
print('Sample document:', db.users.findOne());