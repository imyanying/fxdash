# FX Dashboard - Streamlit Cloud Deployment

## 🚀 Quick Deploy to Streamlit Cloud

### Prerequisites
- GitHub account
- Streamlit Cloud account (free at https://share.streamlit.io/)

### Deployment Steps

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Setup for Streamlit Cloud deployment"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to https://share.streamlit.io/
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Set main file path: `app.py`
   - Click "Deploy"

### App Structure
```
fxdash-1/
├── app.py              # Main entry point (home page)
├── pages/
│   ├── page1.py        # Visual charts
│   └── page2.py        # Performance analysis
├── fetchdata.py        # Data fetching module
├── plot.py            # Plotting utilities
├── requirements.txt    # Dependencies
└── .streamlit/
    └── config.toml    # App configuration
```

### Features
- **Home Page**: Navigation hub with app overview
- **Visual Charts**: Interactive currency trend analysis
- **Performance Analysis**: YTD, 1M, 3M, 6M, 12M performance metrics

### Data Source
- Yahoo Finance API for real-time FX data
- Supports major global currencies vs USD

### Navigation
- Use the sidebar to navigate between pages
- Or use the navigation buttons on the home page
