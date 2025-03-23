# FX Rate Dashboard

A Streamlit-based dashboard for visualizing foreign exchange rates against USD for various Asian-Pacific currencies.

## Introduction

I built this dashboard to make it easier to compare currency movements in a simpler, more visual way. I'm not an FX trader, I don't need to track real-time fluctuations. Instead, I'm more interested in observing how currencies respond to global and domestic economic news or political events, as well as their longer-term trends. I focus on APAC major economies at work, so the sample currencies I used are from this region. As there are so many currencies involved, putting everything on one chart would get messy, so I use subplots to make it easier to read. This also makes it easier for me to analyze individual currencies while comparing their movements with other APAC peers.

## Usage

Use the sidebar controls to:
1. Select your desired date range
2. Choose which currencies to display
3. View the interactive charts and raw data

## Key Changes from Previous Version

1. **Interactive Interface**
   - Converted from static script to interactive Streamlit web app
   - Added sidebar controls for easy customization
   - Real-time data updates and visualization

2. **Enhanced Features**
   - Dynamic date range selection
   - Individual currency selection
   - Raw data table display
   - Responsive plot sizing
   - Better error handling and user feedback

3. **Improved Visualization**
   - Dynamic subplot layout based on selected currencies
   - Interactive Plotly charts with zoom and pan capabilities
   - Better spacing and layout optimization
   - Clearer axis labels and titles

## Features

- **Date Range Selection**: Choose any date range up to the current date
- **Currency Selection**: Select/deselect currencies to display
- **Interactive Charts**: 
  - Zoom in/out
  - Pan across time periods
  - Hover for detailed values
- **Raw Data Display**: View the underlying data in a table format
- **Responsive Design**: Adapts to different screen sizes





## Supported Currencies

- IDR (Indonesia)
- MYR (Malaysia)
- SGD (Singapore)
- VND (Vietnam)
- THB (Thailand)
- PHP (Philippines)
- KRW (South Korea)
- JPY (Japan)
- CNY (China)
- INR (India)
- AUD (Australia)
- NZD (New Zealand)

## Data Source

The FX rate data is fetched from Yahoo Finance using the `yfinance` package.
