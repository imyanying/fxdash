import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Set the start and end date
start_date = '2024-01-01'
end_date = '2024-12-17'

# Country-currency pairs
countries_currency = {'IDR':'Indonesia','MYR':'Malaysia','SGD':'Singapore','VND':'Vietnam',
                      'THB':'Thailand','PHP':'Philippines','KRW':'South Korea','JPY':'Japan',
                      'CNY':'China','INR':'India','AUD':'Australia','NZD':'New Zealand',
}
# Get the FX data from Yahoo Finance
def get_fx(cur):
    data = yf.download(f'USD{cur}=X', start=start_date, end=end_date)
    return data

df = pd.DataFrame()
for cur,country in countries_currency.items():
    data = get_fx(cur)
    data = data[['Adj Close']]
    data.columns = [country]
    if df.empty:
        df = data
    else:
        df = df.join(data)

# Use plotly to plot the data
fig = make_subplots(rows=3, cols=4, subplot_titles=list(countries_currency.values()))
for i,country in enumerate(countries_currency.values()):
    fig.add_trace(go.Scatter(x=df.index, y=df[country], mode='lines', name=country), row=(i//4)+1, col=(i%4)+1)
    fig.update_xaxes(tickangle=40)
fig.update_layout(height=800, width=1100, title_text="Currency to USD ({} to {})".format(start_date,end_date))

# Save the plot as an HTML file
fig.write_html("currency_to_usd.html")