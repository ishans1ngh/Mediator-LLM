const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(cors());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// Routes
app.get('/api', (req, res) => {
  res.json({ message: 'Mediator LLM API Server' });
});

// Clinical trial routes
app.get('/api/trials', (req, res) => {
  res.json({
    trials: [
      {
        id: 1,
        name: 'Alzheimer\'s Study',
        description: 'Investigating new treatments for early-stage Alzheimer\'s disease',
        status: 'Active',
        phase: 'Phase 2',
        enrollment: '45/100'
      },
      {
        id: 2,
        name: 'Parkinson\'s Research',
        description: 'Testing neuroprotective agents for Parkinson\'s disease',
        status: 'Recruiting',
        phase: 'Phase 3',
        enrollment: '78/150'
      }
    ]
  });
});

// Patient routes
app.post('/api/patients', (req, res) => {
  const patientData = req.body;
  res.json({
    message: 'Patient created successfully',
    patient: { ...patientData, id: Date.now() }
  });
});

// Start server
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
