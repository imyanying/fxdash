"""
FX Data Visualization Module

This module provides functionality to create interactive plots for foreign exchange data
using Plotly. It supports multi-subplot layouts for visualizing multiple currencies.
Designed to work seamlessly with data from fetchdata.py module.
"""

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from typing import Dict, List, Optional, Union
from datetime import datetime


def create_fx_plot(df: pd.DataFrame, 
                   start_date: Union[str, datetime], 
                   end_date: Union[str, datetime], 
                   currencies: Dict[str, str],
                   max_cols: int = 4,
                   height_per_row: int = 300,
                   width: int = 1200) -> go.Figure:
    """
    Create a multi-subplot line chart for FX rates.
    
    Args:
        df: DataFrame containing FX data with dates as index and countries as columns
        start_date: Start date for the plot period
        end_date: End date for the plot period
        currencies: Dictionary mapping currency codes to country names
        max_cols: Maximum number of columns in the subplot grid (default: 4)
        height_per_row: Height in pixels per row (default: 300)
        width: Width of the plot in pixels (default: 1200)
    
    Returns:
        go.Figure: Plotly figure object with the FX rate plots
    
    Raises:
        ValueError: If DataFrame is empty or no valid currency data is found
    """
    if df.empty:
        raise ValueError("DataFrame is empty. No data to plot.")
    
    # Filter currencies that exist in the DataFrame
    available_currencies = {cur: country for cur, country in currencies.items() 
                          if country in df.columns}
    
    if not available_currencies:
        raise ValueError("No valid currency data found in the DataFrame.")
    
    n_currencies = len(available_currencies)
    n_cols = min(max_cols, n_currencies)
    n_rows = (n_currencies + n_cols - 1) // n_cols
    
    fig = make_subplots(
        rows=n_rows, 
        cols=n_cols,
        subplot_titles=list(available_currencies.values()),
        vertical_spacing=0.16,
        horizontal_spacing=0.1
    )
    
    for idx, (cur, country) in enumerate(available_currencies.items()):
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
    
    # Create a proper title with currency names
    currency_names = list(available_currencies.values())
    if len(currency_names) <= 3:
        title_currencies = ", ".join(currency_names)
    else:
        title_currencies = f"{len(currency_names)} currencies"
    
    fig.update_layout(
        height=max(800, height_per_row * n_rows),
        width=width,
        title_text=f"1 USD in Local Currency",
        title_x=0,
        title_font_size=20,
        showlegend=False
    )
    
    return fig


def get_available_currencies(df: pd.DataFrame, currencies: Dict[str, str]) -> Dict[str, str]:
    """
    Get currencies that are available in the DataFrame.
    
    Args:
        df: DataFrame containing FX data
        currencies: Dictionary mapping currency codes to country names
    
    Returns:
        Dict[str, str]: Dictionary of available currencies
    """
    return {cur: country for cur, country in currencies.items() 
            if country in df.columns}


def save_plot(fig: go.Figure, filename: str, format: str = 'html') -> None:
    """
    Save a plot to a file.
    
    Args:
        fig: Plotly figure object to save
        filename: Name of the file to save (without extension)
        format: Format to save in ('html', 'png', 'jpg', 'svg', 'pdf')
    """
    if format.lower() == 'html':
        fig.write_html(f"{filename}.html")
    else:
        fig.write_image(f"{filename}.{format}")


def plot_fetchdata_output(df: pd.DataFrame, 
                         start_date: Union[str, datetime],
                         end_date: Union[str, datetime],
                         currencies: Optional[Dict[str, str]] = None) -> go.Figure:
    """
    Convenience function to plot data directly from fetchdata.py output.
    
    Args:
        df: DataFrame from fetchdata.py (with dates as index, countries as columns)
        start_date: Start date for the plot period
        end_date: End date for the plot period
        currencies: Optional currency mapping. If None, will try to import from fetchdata
    
    Returns:
        go.Figure: Plotly figure object with the FX rate plots
    """
    if currencies is None:
        try:
            import fetchdata
            currencies = fetchdata.get_currency_pairs()
        except ImportError:
            # If fetchdata is not available, create a simple mapping from column names
            currencies = {col: col for col in df.columns}
    
    return create_fx_plot(df, start_date, end_date, currencies)


# Example usage and testing
if __name__ == "__main__":
    # Example: Use fetchdata.py to get real sample data
    from datetime import datetime, timedelta
    
    try:
        # Import fetchdata module
        import fetchdata
        
        # Get sample data for the last 30 days
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        
        print("Fetching sample FX data for the last 30 days...")
        sample_data = fetchdata.fetch_default_currencies(start_date, end_date)
        
        if not sample_data.empty:
            print(f"Successfully fetched data for {len(sample_data.columns)} currencies")
            print(f"Data shape: {sample_data.shape}")
            
            # Get currency mappings
            sample_currencies = fetchdata.get_currency_pairs()
            
            # Test the main plotting function
            fig = create_fx_plot(
                sample_data, 
                start_date, 
                end_date, 
                sample_currencies
            )
            
            print("Multi-currency plot created successfully!")
            print(f"Plot dimensions: {fig.layout.width} x {fig.layout.height}")
            
            # Show available currencies
            available = get_available_currencies(sample_data, sample_currencies)
            print(f"Available currencies: {list(available.values())}")
            
            # Test the convenience function
            convenience_fig = plot_fetchdata_output(
                sample_data,
                start_date,
                end_date
            )
            
            print("Convenience function test successful!")
            
        else:
            print("No data was fetched from fetchdata.py")
            
    except ImportError:
        print("fetchdata.py module not found. Skipping test.")
    except Exception as e:
        print(f"Error creating plots: {str(e)}")