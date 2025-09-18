# EcoTI Dashboard - Renault Sustentabilidade Digital

**ALWAYS follow these instructions first and fallback to additional search and context gathering only if the information here is incomplete or found to be in error.**

## Working Effectively

### Bootstrap and Build Steps
- **CRITICAL**: There is NO build process - this is a simple Python Flask application that runs directly.
- Install Python dependencies: `pip install -r requirements.txt` 
- **NEVER CANCEL**: Dependency installation typically takes 10-15 seconds. Set timeout to 60+ seconds.
- Application startup time: ~0.16 seconds (very fast)

### Running the Applications

#### Flask Web Application (Recommended)
```bash
# Start the Flask server
python3 app_renault_mvp.py

# Application runs on: http://localhost:5000
# API endpoint: http://localhost:5000/api/metrics
```
- **NEVER CANCEL**: Application starts in under 1 second. Set timeout to 30+ seconds to be safe.
- The Flask app includes embedded HTML template and serves the dashboard directly.
- API returns real-time calculated sustainability metrics in JSON format.

#### Static HTML Version (Alternative)
```bash
# Serve static files using Python's built-in server
python3 -m http.server 8080 --bind localhost

# Access at: http://localhost:8080/index.html
```
- **NEVER CANCEL**: Static server starts instantly. Set timeout to 30+ seconds.
- This version uses separate HTML (`index.html`), CSS (`style.css`), and JavaScript (`app.js`) files.
- No backend API - uses simulated data in JavaScript.

### Testing and Validation

#### Functional Testing Commands
```bash
# Test API endpoint (Flask version)
curl -s http://localhost:5000/api/metrics | python3 -m json.tool

# Test dashboard availability
curl -s -I http://localhost:5000/

# Test static files (Static version)
curl -s -I http://localhost:8080/index.html
curl -s -I http://localhost:8080/style.css
curl -s -I http://localhost:8080/app.js
```

#### **VALIDATION SCENARIOS - MANDATORY TESTING**
After making any changes, **ALWAYS** run through these complete user scenarios:

##### Flask Application Validation
1. **Start Flask app**: `python3 app_renault_mvp.py` (starts in ~0.16s)
2. **Test API endpoint**: `curl -s http://localhost:5000/api/metrics` - should return JSON with metrics
3. **Verify dashboard loads**: Access `http://localhost:5000` - should show Renault-branded dashboard
4. **Test real-time updates**: API should return different values when called multiple times
5. **Stop cleanly**: `Ctrl+C` or `kill` process

##### Static HTML Validation  
1. **Start static server**: `python3 -m http.server 8080 --bind localhost`
2. **Test HTML file**: `curl -s http://localhost:8080/index.html` - should return full HTML
3. **Test CSS file**: `curl -s http://localhost:8080/style.css` - should return stylesheet
4. **Test JS file**: `curl -s http://localhost:8080/app.js` - should return JavaScript
5. **Verify content**: HTML should contain "EcoTI Dashboard" and "Renault" branding

### No Build System Required
- **DO NOT try to build the code** - it runs directly with Python
- **DO NOT look for build tools** like npm, webpack, or make - they don't exist
- **DO NOT add build processes** unless specifically requested

### No Tests Currently Available
- **NO unit tests exist** - the project currently has no test infrastructure
- **NO CI/CD pipeline** - no GitHub Actions or automation exists
- **Manual validation is the only testing method** - use the scenarios above
- If asked to add tests, suggest using Python's built-in `unittest` module

## Project Structure and Key Files

### Repository Root
```
eco-dashboard-renault/
├── app_renault_mvp.py          # Main Flask application (PRIMARY)
├── index.html                  # Static dashboard interface
├── style.css                   # Dashboard styling and Renault branding
├── app.js                      # Client-side JavaScript logic
├── requirements.txt            # Python dependencies (only flask==2.3.3)
├── script_1.py                 # Development/generation script
├── script_2.py                 # Development/generation script  
├── chart_script.py             # Chart generation utilities
├── eco-ti-dashboard.zip/       # Archive of alternative version
└── .github/                    # GitHub configuration
    └── copilot-instructions.md # This file
```

### Primary Application Files
- **`app_renault_mvp.py`** - Main Flask server with embedded HTML template
- **`index.html`** - Standalone HTML dashboard (alternative to Flask)
- **`style.css`** - Complete styling system with Renault brand colors (#FFCB00)
- **`app.js`** - Frontend JavaScript for charts and interactivity

### Key Architecture Points
- **Flask Backend**: Calculates real sustainability metrics for Renault infrastructure
- **Simulated Data**: Models 5,376 workstations, 90 HP servers, 10 VxRail systems
- **Metrics Calculated**: Energy consumption (kWh), CO2 emissions (kg/year), cost savings (R$/year), tree equivalents
- **Brand Integration**: Uses official Renault yellow (#FFCB00) and design patterns

## Common Tasks and Patterns

### Working with Sustainability Calculations
The core business logic is in the `RenaultInfrastructure` class:
```python
# Key calculation methods:
infra.calcular_consumo_atual()      # Current energy consumption
infra.calcular_emissoes_anuais()    # Annual CO2 emissions  
infra.calcular_economia_potencial() # Potential cost savings
infra.calcular_arvores_equivalentes() # Tree planting equivalent
```

### API Integration Points
- **GET `/api/metrics`** - Returns current sustainability metrics
- Response format:
```json
{
  "consumo_atual": 874.0,
  "emissoes_co2": 625514.808, 
  "economia_potencial": 352800.0,
  "arvores_equivalentes": 28432
}
```

### Frontend Interaction Patterns
- **Real-time updates**: Metrics refresh every 10 seconds via JavaScript
- **Chart.js integration**: For data visualization components
- **Responsive design**: Mobile-friendly layout with CSS Grid
- **Tab navigation**: Dashboard, Monitoring, Analytics, Settings sections

## Environment Details

### Python Environment
- **Version**: Python 3.12.3 (confirmed working)
- **Required packages**: Only Flask 2.3.3
- **Virtual environment**: Not required but recommended for development
- **Installation location**: `/usr/bin/python3`

### Port Configuration
- **Flask application**: Port 5000 (http://localhost:5000)
- **Static server**: Port 8080 (http://localhost:8080) - or any available port
- **No conflicting services** expected on these ports

### File Permissions and Access
- All files have standard read/write permissions
- No special system privileges required
- Can run in standard user environment

## Debugging and Troubleshooting

### Common Issues and Solutions

#### "Port already in use" Error
```bash
# Kill existing Flask processes
pkill -f app_renault_mvp
pkill -f python3

# For static server port conflicts
pkill -f "http.server"

# Alternative: Use different ports
# Flask: Change port in app_renault_mvp.py: app.run(port=5001)
# Static: python3 -m http.server 8081 --bind localhost
```

#### Flask Debug Mode
- Debug mode is enabled by default (`debug=True`)
- Auto-reloads on file changes
- Detailed error messages in browser
- Debugger PIN displayed in console

#### Static File Issues
- Ensure you're in the correct directory when running `python3 -m http.server`
- Check file paths are relative to repository root
- CSS/JS files must be in same directory as HTML

## Development Workflow Recommendations

### Making Changes
1. **Always test both versions** (Flask and static) after changes
2. **Run validation scenarios** after every modification
3. **Check browser console** for JavaScript errors when testing
4. **Verify API responses** with curl before testing in browser

### Code Style and Standards  
- **No formal linting** configured - but maintain consistent Python style
- **Portuguese language** used in UI and comments (maintain this)
- **Renault branding** must be preserved in all UI changes
- **No automated formatting** - manual code review only

This dashboard represents Renault's commitment to digital sustainability and IT infrastructure optimization. Always consider the business context when making changes.