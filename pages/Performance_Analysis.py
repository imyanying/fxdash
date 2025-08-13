# -*- coding: utf-8 -*-
"""
📊 Performance Analysis
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import fetchdata

def calculate_currency_performance(fx_data):
    """
    Calculate YTD, 1M, 3M, 6M, 12M percentage changes for each currency.
    Note: Data shows USD/local currency, so we use 1/data to get local/USD.
    
    Args:
        fx_data: DataFrame with FX data (dates as index, currencies as columns)
    
    Returns:
        DataFrame with percentage changes for each time period
    """
    if fx_data.empty:
        return pd.DataFrame()
    
    # Convert USD/local to local/USD by taking reciprocal
    local_vs_usd = 1 / fx_data
    
    # Get the latest date and calculate reference dates
    latest_date = local_vs_usd.index.max()
    
    # Calculate reference dates for different periods
    periods = {
        'YTD': datetime(latest_date.year, 1, 1),
        '1M': latest_date - timedelta(days=30),
        '3M': latest_date - timedelta(days=90),
        '6M': latest_date - timedelta(days=180),
        '12M': latest_date - timedelta(days=365)
    }
    
    # Initialize results DataFrame
    results = []
    
    for currency in local_vs_usd.columns:
        currency_data = local_vs_usd[currency].dropna()
        if len(currency_data) == 0:
            continue
            
        latest_value = currency_data.iloc[-1]
        currency_changes = {'Currency': currency}
        
        for period_name, ref_date in periods.items():
            # Find the closest available date to the reference date
            available_dates = currency_data.index[currency_data.index >= ref_date]
            
            if len(available_dates) > 0:
                # Get the first available date after the reference date
                start_date = available_dates[0]
                start_value = currency_data.loc[start_date]
                
                # Calculate percentage change
                pct_change = ((latest_value - start_value) / start_value) * 100
                currency_changes[period_name] = round(pct_change, 2)
            else:
                currency_changes[period_name] = None
        
        results.append(currency_changes)
    
    return pd.DataFrame(results)

def main():
    st.set_page_config(
        page_title="Currency Performance Analysis",
        page_icon="📊",
        layout="wide"
    )
    
    st.title("📊 Currency Performance Analysis")
    st.markdown("---")
    
    # Sidebar for date selection
    st.sidebar.header("📅 Data Range Selection")
    
    # Default date range (last 365 days to ensure we have enough data for 12M)
    default_end = datetime.now()
    default_start = default_end - timedelta(days=365)
    
    # Date inputs
    start_date = st.sidebar.date_input(
        "Start Date",
        value=default_start.date(),
        max_value=datetime.now().date()
    )
    
    end_date = st.sidebar.date_input(
        "End Date",
        value=default_end.date(),
        max_value=datetime.now().date()
    )

    # Convert to datetime for fetchdata
    start_datetime = datetime.combine(start_date, datetime.min.time())
    end_datetime = datetime.combine(end_date, datetime.min.time())

    # Validation
    if start_date >= end_date:
        st.error("Start date must be before end date!")
        return
    
    # Fetch data button
    if st.sidebar.button("Fetch Performance Data", type="primary"):
        with st.spinner("Fetching currency data for performance analysis..."):
            try:
                # Fetch data using fetchdata module
                fx_data = fetchdata.fetch_default_currencies(start_datetime, end_datetime)
                
                if not fx_data.empty:
                    st.success(f"✅ Successfully fetched data from Yahoo Finance")
                    
                    # Store data in session state
                    st.session_state.fx_data = fx_data
                    st.session_state.start_date = start_datetime
                    st.session_state.end_date = end_datetime
                    
                else:
                    st.warning("⚠️ No data available for the selected date range")
                    
            except Exception as e:
                st.error(f"❌ Error fetching data: {str(e)}")
    
    # Display performance analysis if data is available
    if 'fx_data' in st.session_state and not st.session_state.fx_data.empty:
        fx_data = st.session_state.fx_data
        start_dt = st.session_state.start_date
        end_dt = st.session_state.end_date
        
        # Calculate performance metrics
        st.subheader("📈 Currency Performance vs USD")
        
       
        performance_df = calculate_currency_performance(fx_data)
        
        if not performance_df.empty:
            # Display performance table
            st.write("**Percentage Change (Local Currency vs USD)**")
            
            # Style the DataFrame for better display
            styled_df = performance_df.style.format({
                'YTD': '{:.2f}%',
                '1M': '{:.2f}%', 
                '3M': '{:.2f}%',
                '6M': '{:.2f}%',
                '12M': '{:.2f}%'
            }).background_gradient(cmap='PiYG', subset=['YTD', '1M', '3M', '6M', '12M'])
            
            st.dataframe(styled_df, use_container_width=True, height=450)
            
            # Add detailed legend
            st.caption("""
            **Time Periods:** 
            - **YTD**: Year-to-Date (from January 1st of current year)
            - **1M**: 1 Month (last 30 days)
            - **3M**: 3 Months (last 90 days) 
            - **6M**: 6 Months (last 180 days)
            - **12M**: 12 Months (last 365 days)
            
            **Color Coding:**
            - 🟢 **Green**: Local currency appreciation against USD
            - 🔴 **Red**: Local currency depreciation against USD
            """)
            
            
            
            # Show best and worst performers
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("🏆 Best Performers (12M)")
                best_12m = performance_df.nlargest(3, '12M')[['Currency', '12M']]
                st.dataframe(best_12m, use_container_width=True)
            
            with col2:
                st.subheader("📉 Worst Performers (12M)")
                worst_12m = performance_df.nsmallest(3, '12M')[['Currency', '12M']]
                st.dataframe(worst_12m, use_container_width=True)
        
        # Add download option
        if not performance_df.empty:
            st.markdown("---")
            st.subheader("💾 Download Options")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Download performance data
                performance_csv = performance_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download Performance Data (CSV)",
                    data=performance_csv,
                    file_name=f"currency_performance_{start_dt.strftime('%Y%m%d')}_{end_dt.strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
            
            with col2:
                # Download raw FX data
                raw_csv = fx_data.to_csv(index=True).encode('utf-8')
                st.download_button(
                    label="📥 Download Raw FX Data (CSV)",
                    data=raw_csv,
                    file_name=f"raw_fx_data_{start_dt.strftime('%Y%m%d')}_{end_dt.strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
    
    else:
        # Initial state - show instructions
        st.info("Use the sidebar to select a date range and click 'Fetch Performance Data' to get started!")
        
        
        
        # Add note about data requirements
        st.markdown("---")
        st.subheader("📋 Data Requirements")
        st.write("""
        **For accurate performance analysis:**
        - Select a date range of at least 365 days to get 12M performance
        - Longer date ranges provide more comprehensive analysis
        - Data is fetched from Yahoo Finance (USD vs local currency pairs)
        """)

if __name__ == "__main__":
    main()
