# Chart.js Loading Issue - Fix Instructions

## Problem
The dashboard charts are not displaying because Chart.js CDN is being blocked in the deployment environment.

## Root Cause
All external CDN requests (cdn.jsdelivr.net, unpkg.com, cdnjs.cloudflare.com) are being blocked by the network/environment, preventing Chart.js from loading.

Error in console:
```
ReferenceError: Chart is not defined
Failed to load resource: net::ERR_BLOCKED_BY_CLIENT
```

## Solution: Host Chart.js Locally

### Step 1: Download Chart.js
Download Chart.js 4.4.0 UMD version:
```bash
# Create vendor directory
mkdir -p static/js/vendor

# Download Chart.js (from a machine with internet access)
curl -o static/js/vendor/chart.umd.min.js \
  https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.umd.min.js

# Or download from:
# https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js
```

### Step 2: Update HTML Files
Update the script tag in both files:

**File: `templates/dashboard.html`**
```html
<!-- Change from: -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.umd.min.js"></script>

<!-- To: -->
<script src="{{ url_for('static', filename='js/vendor/chart.umd.min.js') }}"></script>
```

**File: `index.html`**
```html
<!-- Change from: -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.umd.min.js"></script>

<!-- To: -->
<script src="static/js/vendor/chart.umd.min.js"></script>
```

### Step 3: Verify
After making these changes:
1. Restart the Flask server
2. Refresh the browser (Ctrl+F5 to clear cache)
3. Check browser console - should see no "Chart is not defined" errors
4. The "Consumo Energético em Tempo Real" chart should display with data

## Alternative: Use npm
If you have Node.js installed:
```bash
npm install chart.js
cp node_modules/chart.js/dist/chart.umd.min.js static/js/vendor/
```

## Files to Update
- [ ] Download chart.umd.min.js to `static/js/vendor/`
- [ ] Update `templates/dashboard.html` script tag
- [ ] Update `index.html` script tag
- [ ] Add `static/js/vendor/` to git (ensure not in .gitignore)
- [ ] Test in browser

## Expected Result
Once fixed, you should see:
- Line chart showing energy consumption over time
- Doughnut chart showing consumption by sector  
- Prediction chart with forecasts
