const express = require('express');
const path = require('path');
const bodyParser = require('body-parser');
const ejs = require('ejs');
const fs = require('fs');
const axios = require('axios'); // Import axios library


const app = express();
const port = 3000;

// Middleware to parse JSON and URL-encoded bodies

app.use(bodyParser.json({ limit: '500mb' }));
app.use(bodyParser.urlencoded({ extended: true }));


// Middleware to serve static files from the 'public' directory
app.use(express.static(path.join(__dirname, 'public')));

// Set EJS as the view engine
app.set('view engine', 'ejs');

const desti = "Mylapore";
const coord = [[80.254, 12.99514], [80.25615, 12.99933], [80.25698, 13.00391], [80.25898, 13.00812], [80.25917, 13.01353], [80.26074, 13.0179], [80.26554, 13.01883], [80.27022, 13.02123], [80.27391, 13.02406], [80.27615, 13.02805], [80.27752, 13.03245], [80.27815, 13.03695], [80.275, 13.04071]]

const ins = [
  'Leave from Indira Nagar 22nd Cross Link Street',
  'Turn left onto Indira Nagar 3rd Main Road',
  'Turn right onto Indira Nagar 2nd Avenue',
  'Turn left onto Dr Muthulakshmi Road',
  'Keep right at Durgabai Deshmukh Road',
  'Turn sharp right onto Brodies Castle Road',
  'Turn left onto Dr D G S Dhinakaran Road',
  'Turn left onto Karneeswarar Koil Street',
  'Bear right at Karneeswarar Koil Street',
  'Turn left',
  'You have arrived. Your destination is on the left'
];
// Root Page
app.get('/', (req, res) => {
    // Read content from userDetails.txt
    fs.readFile('userDetails.txt', 'utf-8', (err, data) => {
      if (err) {
        console.error('Error reading userDetails.txt:', err);
        res.status(500).send('Error reading userDetails.txt');
      } else {
        // Check if userDetails.txt is empty
        if (data.trim() === '') {
          // If empty, redirect to the register page
          res.redirect('/register');
        } else {
          // If not empty, parse the data and render the home page
          const userDetails = JSON.parse(data);
          res.render('home', { userDetails });
        }
      }
    });
  });
  
// Home Page
app.get('/home', (req, res) => {
  // Check if user details are provided in the query parameters
  const { name, otp, pref_lan, isaudio, visionImpairment, hearingImpairment, mobilityPhysicalImpairment, breathingIssues, dyslexia } = req.query;

  // Convert string values "true" and "false" to actual boolean values
  const userDetails = {
    name,
    otp,
    pref_lan,
    isaudio: convertToBoolean(isaudio),
    visionImpairment: convertToBoolean(visionImpairment),
    hearingImpairment: convertToBoolean(hearingImpairment),
    mobilityPhysicalImpairment: convertToBoolean(mobilityPhysicalImpairment),
    breathingIssues: convertToBoolean(breathingIssues),
    dyslexia: convertToBoolean(dyslexia)
  };
  console.log(userDetails.pref_lan, req.query.pref_lan)
  console.log(req.query, userDetails);
  const userDetailsText = JSON.stringify(userDetails, null, 2);
  fs.writeFileSync('userDetails.txt', userDetailsText);

  res.render('home', { userDetails });
});
  
  // Function to convert "true" and "false" strings to boolean values
  function convertToBoolean(value) {
    return value === "true";
  }

  app.get('/map', (req, res) => {
    res.render('map', { coord });
});
app.get('/rate', (req, res) => {
  res.render('rate', { desti });
});

// Rate Page - POST (Handle form submission)
app.post('/rate', (req, res) => {
  // Handle form submission logic here
  const { safetyRating, wheelchairRating } = req.body;

  // Process the ratings as needed (store in a database, etc.)
  console.log('Received ratings:', { safetyRating, wheelchairRating });

  // Save destination info to rateInfo.txt
  const rateInfo = {
    desti,
    safetyRating,
    wheelchairRating
    // Add other rating fields as needed
  };

  const rateInfoText = JSON.stringify(rateInfo, null, 2);
  fs.writeFileSync('rateInfo.txt', rateInfoText);

  // Redirect to a thank you page or back to the home page
  res.redirect('/');
});
app.post('/submit-text', async (req, res) => {
  const textData = req.body.textInput;

  // Read userDetails.txt
  const userDetailsFilePath = path.join(__dirname, 'userDetails.txt');
  fs.readFile(userDetailsFilePath, 'utf8', async (err, data) => {
      if (err) {
          console.error('Error reading userDetails.txt:', err);
          return res.status(500).send('Error reading userDetails.txt');
      }

      try {
          // Parse contents of userDetails.txt into a JSON object
          const userDetails = JSON.parse(data);

          // Add inputText to userDetails
          userDetails.data = textData;

          // Convert userDetails back to JSON string
          const updatedUserDetails = JSON.stringify(userDetails);

          // Overwrite userDetails.txt with the updated JSON string
          fs.writeFileSync(userDetailsFilePath, updatedUserDetails);

          // Send a POST request to 192.168.82.1:8000 with userDetails data
          try {
            const response = await axios.post('http://192.168.82.1:8000/planroute', userDetails, {
                headers: {
                    'Content-Type': 'application/json',
                },
            });
        
            console.log('Text data added to userDetails.txt');
            res.redirect('/answer');
        } catch (postError) {
            console.error('Error sending POST request:', postError);
            //res.status(500).send('Error sending POST request');
            res.redirect('/answer');
        }
      } catch (parseError) {
          console.error('Error parsing JSON from userDetails.txt:', parseError);
          res.status(500).send('Error parsing JSON from userDetails.txt');
      }
  });
});
app.get('/answer', (req, res) => {

  res.render('answer', { coord, ins, desti });
});
// Registration Page
app.get('/register', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'register.html'));
});

// Handle registration form submission
app.post('/register', (req, res) => {
  // Extract form details from the request body
  const { name, otp, pref_lan, isaudio, visionImpairment, hearingImpairment, mobilityPhysicalImpairment, breathingIssues, dyslexia } = req.body;

  // Redirect to the home page with form details as query parameters
  const queryString = `name=${encodeURIComponent(name)}&otp=${encodeURIComponent(otp)}&pref_lan=${encodeURIComponent(pref_lan)}&isaudio=${isaudio}&visionImpairment=${visionImpairment}&hearingImpairment=${hearingImpairment}&mobilityPhysicalImpairment=${mobilityPhysicalImpairment}&breathingIssues=${breathingIssues}&dyslexia=${dyslexia}`;
  res.redirect(`/home?${queryString}`);
});

// Start the server
app.listen(port, () => {
  console.log(`Server is running at http://localhost:${port}`);
});