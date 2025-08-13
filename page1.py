"""
Page 1: FX Data Dashboard
This page displays foreign exchange data with interactive date selection and visualization.
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plot
import fetchdata

def main():
    st.set_page_config(
        page_title="FX Data Dashboard",
        page_icon="📈",
        layout="wide"
    )
    
    st.title("📈 Foreign Exchange Data Dashboard")
    st.markdown("---")
    
    # Sidebar for date selection
    st.sidebar.header("📅 Date Range Selection")
    
    # Default date range (last 30 days)
    default_end = datetime.now()
    default_start = default_end - timedelta(days=30)
    
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
    if st.sidebar.button("Fetch FX Data", type="primary"):
        with st.spinner("Fetching FX data..."):
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
    
    # Display plot if data is available
    if 'fx_data' in st.session_state and not st.session_state.fx_data.empty:
        fx_data = st.session_state.fx_data
        start_dt = st.session_state.start_date
        end_dt = st.session_state.end_date
        
        # Create and display plot
        
        
        try:
            # Get currency mappings
            currencies = fetchdata.get_currency_pairs()
            
            # Create plot using plot module
            fig = plot.plot_fetchdata_output(
                fx_data,
                start_dt,
                end_dt,
                currencies
            )
            
            # Display the plot
            st.plotly_chart(fig, use_container_width=True)
            
        except Exception as e:
            st.error(f"❌ Error creating plot: {str(e)}")
    
    else:
        # Initial state - show instructions
        st.info("Use the sidebar to select a date range and click 'Fetch FX Data' to get started!")

    # Add a download button for the data if available
    if 'fx_data' in st.session_state and not st.session_state.fx_data.empty:
        csv = st.session_state.fx_data.to_csv(index=True).encode('utf-8')
        st.sidebar.download_button(
            label="Download FX Data as CSV",
            data=csv,
            file_name="fx_data.csv",
            mime="text/csv"
        )
        
if __name__ == "__main__":
    main()
