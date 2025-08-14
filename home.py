"""
Home Page: FX Dashboard Navigation
Simple navigation page to access different features of the FX dashboard.
"""

import streamlit as st

def main():
    st.set_page_config(
        page_title="FX Dashboard - Home",
        page_icon="🏠",
        layout="wide"
    )
    
    # Main title and description
    st.title("🏠 FX Dashboard")
    st.markdown("---")
    
    # Welcome message
    st.markdown("""
    ### Welcome to the FX Dashboard!
    
    This dashboard provides comprehensive foreign exchange analysis tools.
    Choose from the options below to explore different features.
    """)
    
    # Create two columns for navigation buttons
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📈 Visual Analysis")
        st.markdown("""
        **Interactive Line Charts**
        - View currency trends over time
        - Compare multiple currencies
        - Interactive date range selection
        """)
        
        # Navigation button to page1
        if st.button("Go to Visual Charts", type="primary", use_container_width=True):
            st.switch_page("pages/Visual_Charts.py")
    
    with col2:
        st.markdown("### 📊 Performance Analysis")
        st.markdown("""
        **Currency Performance Metrics**
        - YTD, 1M, 3M, 6M, 12M performance
        - Best and worst performers
        - Color-coded performance indicators
        """)
        
        # Navigation button to page2
        if st.button("Go to Performance View", type="primary", use_container_width=True):
            st.switch_page("pages/Performance_Analysis.py")
    
    # Additional information
    st.markdown("---")
    st.markdown("""
    ### 📋 About This Dashboard
    
    **Data Source:** Yahoo Finance  
    **Update Frequency:** Real-time data fetching  
    **Supported Currencies:** Major APAC currencies vs USD
   
    ---
    
    *Select an option above to get started with your FX analysis!*
    """)

if __name__ == "__main__":
    main()
