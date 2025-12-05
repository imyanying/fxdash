# FX Rate Dashboard

This is a Streamlit-based dashboard for visualizing foreign exchange rates against USD for various Asian-Pacific currencies.

Link to the Streamlit application:

https://fxdash-ceyutaspltwxjeauad5hvo.streamlit.app/

## Introduction

I built this dashboard to make it easier to compare currency movements in a simpler, more visual way. I'm not an FX trader, I don't need to track real-time fluctuations. Instead, I'm more interested in observing how currencies respond to global and domestic economic news or political events, as well as their longer-term trends. I focus on APAC major economies at work, so the sample currencies I used are from this region. As there are so many currencies involved, putting everything on one chart would get messy, so I use subplots to make it easier to read. This also makes it easier for me to analyze individual currencies while comparing their movements with other APAC peers.

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

