# FX Rate Dashboard

This is a Streamlit-based dashboard for visualizing foreign exchange rates against USD for various Asian-Pacific currencies.

Link to the Dashboard:

https://fxdash-ceyutaspltwxjeauad5hvo.streamlit.app/

## Introduction

I built this dashboard to make it easier to compare currency movements in a simpler, more visual way. I'm interested in observing how currencies respond to global and domestic economic news or political events, as well as their longer-term trends. I focus on APAC major economies at work, so the sample currencies I used are from this region. As there are so many currencies involved, putting everything on one chart would get messy, so I use subplots to make it easier to read. This also makes it easier for me to analyze individual currencies while comparing their movements with other APAC peers.

## Pages
**Home Page**
<img width="1656" height="908" alt="image" src="https://github.com/user-attachments/assets/d4230ad2-f9f7-46fd-ae4d-4473095871f2" />
**Line Charts**
<img width="1912" height="909" alt="image" src="https://github.com/user-attachments/assets/b73a715f-6f56-40fd-bb06-ad9e0f84093f" />
**Performance Comparison**
<img width="1909" height="911" alt="image" src="https://github.com/user-attachments/assets/0351f72f-b335-49d4-abba-0728f4909f8e" />


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

