"""
FX Data Fetching Module

This module provides functionality to fetch foreign exchange data for various currencies
against USD using Yahoo Finance API.
"""

import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
from typing import Dict, Optional, Union


# Currency pairs mapping
currency_pairs = {
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


def fetch_data(currencies: Dict[str, str], 
               start_date: Union[str, datetime], 
               end_date: Union[str, datetime]) -> pd.DataFrame:
    """
    Fetch FX data for multiple currencies against USD.
    
    Args:
        currencies: Dictionary mapping currency codes to country names
        start_date: Start date for data fetching (string or datetime)
        end_date: End date for data fetching (string or datetime)
    
    Returns:
        pandas.DataFrame: DataFrame with currency data, indexed by date
    """
    df = pd.DataFrame()
    
    for cur, country in currencies.items():
        try:
            data = yf.download(f'USD{cur}=X', start=start_date, end=end_date)
            if not data.empty and 'Close' in data.columns:
                data = data[['Close']]
                data.columns = [country]
                if df.empty:
                    df = data
                else:
                    df = df.join(data)
        except Exception as e:
            print(f"Error fetching data for {cur} ({country}): {str(e)}")
    
    return df


def get_currency_pairs() -> Dict[str, str]:
    """
    Get the default currency pairs mapping.
    
    Returns:
        Dict[str, str]: Dictionary mapping currency codes to country names
    """
    return currency_pairs.copy()


def fetch_default_currencies(start_date: Union[str, datetime], 
                           end_date: Union[str, datetime]) -> pd.DataFrame:
    """
    Fetch FX data for all default currency pairs.
    
    Args:
        start_date: Start date for data fetching (string or datetime)
        end_date: End date for data fetching (string or datetime)
    
    Returns:
        pandas.DataFrame: DataFrame with currency data for all default currencies
    """
    return fetch_data(currency_pairs, start_date, end_date)


# Example usage and testing
if __name__ == "__main__":
    # Example: Fetch data for the last 30 days
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    print("Fetching FX data for the last 30 days...")
    data = fetch_default_currencies(start_date, end_date)
    
    if not data.empty:
        print(f"Successfully fetched data for {len(data.columns)} currencies")
        print(f"Data shape: {data.shape}")
        print("\nFirst few rows:")
        print(data.head())
    else:
        print("No data was fetched.")

