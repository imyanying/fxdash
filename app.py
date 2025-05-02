import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import time

# Set page config
st.set_page_config(
    page_title="FX Rate Dashboard",
    page_icon="📈",
    layout="wide"
)

# Define currency pairs with their full names
CURRENCY_PAIRS = {
    'IDR': 'Indonesia',
    'MYR': 'Malaysia',
    'SGD': 'Singapore',
    'VND': 'Vietnam',
    'THB': 'Thailand',
    'PHP': 'Philippines',
    'KRW': 'South Korea',
    'JPY': 'Japan',
    'CNY': 'China',
    'INR': 'India',
    'AUD': 'Australia',
    'NZD': 'New Zealand'
}

def get_fx_data(currencies, start_date, end_date):
    """Fetch FX data for multiple currencies against USD with rate limiting"""
    df = pd.DataFrame()
    
    with st.spinner('Fetching FX data...'):
        for idx, (cur, country) in enumerate(currencies.items()):
            try:
                # Add a delay between requests to avoid rate limiting
                if idx > 0:
                    time.sleep(2)  # Wait 2 seconds between requests
                
                data = yf.download(f'USD{cur}=X', start=start_date, end=end_date)
                if not data.empty and 'Close' in data.columns:
                    data = data[['Close']]
                    data.columns = [country]
                    if df.empty:
                        df = data
                    else:
                        df = df.join(data)
                else:
                    st.warning(f"No data available for {cur} ({country})")
            except Exception as e:
                if "Too Many Requests" in str(e):
                    st.warning(f"Rate limit reached. Waiting before retrying {cur} ({country})...")
                    time.sleep(5)  # Wait longer if we hit the rate limit
                    try:
                        data = yf.download(f'USD{cur}=X', start=start_date, end=end_date)
                        if not data.empty and 'Close' in data.columns:
                            data = data[['Close']]
                            data.columns = [country]
                            if df.empty:
                                df = data
                            else:
                                df = df.join(data)
                    except Exception as retry_error:
                        st.error(f"Failed to fetch data for {cur} ({country}) after retry: {str(retry_error)}")
                else:
                    st.error(f"Error fetching data for {cur} ({country}): {str(e)}")
    
    return df

def create_fx_plot(df, start_date, end_date, currencies):
    """Create a multi-subplot line chart for FX rates"""
    n_currencies = len(currencies)
    n_cols = min(4, n_currencies)
    n_rows = (n_currencies + n_cols - 1) // n_cols
    
    fig = make_subplots(
        rows=n_rows, 
        cols=n_cols,
        subplot_titles=list(currencies.values()),
        vertical_spacing=0.16,
        horizontal_spacing=0.1
    )
    
    for idx, (cur, country) in enumerate(currencies.items()):
        if country in df.columns:
            row = (idx // n_cols) + 1
            col = (idx % n_cols) + 1
            
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df[country],
                    mode='lines',
                    name=country,
                    showlegend=False
                ),
                row=row, col=col
            )
            
            fig.update_xaxes(
                tickangle=45,
                row=row, col=col,
                title_text="Date"
            )
            fig.update_yaxes(
                row=row, col=col,
                title_text=f"USD/{cur}"
            )
    
    fig.update_layout(
        height=max(800, 300 * n_rows),
        width=1200,
        title_text=f"Currency vs USD ({start_date} to {end_date})",
        title_x=0,
        title_font_size=20,
        showlegend=False
    )
    
    return fig

def main():
    st.title("📈 FX Rate Dashboard")
    
    
    # Sidebar controls
    st.sidebar.header("Settings")
    
    # Date range selection
    st.sidebar.subheader("Date Range")
    default_start = datetime.now() - timedelta(days=365)
    default_end = datetime.now()
    
    start_date = st.sidebar.date_input(
        "Start Date",
        value=default_start,
        max_value=default_end
    )
    
    end_date = st.sidebar.date_input(
        "End Date",
        value=default_end,
        max_value=default_end
    )
    
    # Currency selection
    st.sidebar.subheader("Select Currencies")
    selected_currencies = {}
    for cur, country in CURRENCY_PAIRS.items():
        if st.sidebar.checkbox(f"{cur} - {country}", value=True):
            selected_currencies[cur] = country
    
    if not selected_currencies:
        st.warning("Please select at least one currency")
        return
    
    # Get FX data
    df = get_fx_data(selected_currencies, start_date, end_date)
    
    if df.empty:
        st.error("No data available for the selected period and currencies")
        return
    
    # Display the plot
    fig = create_fx_plot(df, start_date, end_date, selected_currencies)
    st.plotly_chart(fig, use_container_width=True)
    
    # Display data table
    st.subheader("Raw Data")
    st.dataframe(df)

if __name__ == "__main__":
    main() 