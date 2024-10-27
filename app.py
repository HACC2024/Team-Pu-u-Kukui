import streamlit as st
import leafmap.foliumap as leafmap
import pandas as pd
import matplotlib.pyplot as plt

def main():
    st.set_page_config(layout="wide")
    
    # Customize the sidebar
    markdown = """
    A Streamlit map template
    <https://github.com/opengeos/streamlit-map-template>
    """
    
    st.sidebar.title("About")
    st.sidebar.info(markdown)
    logo = "https://i.imgur.com/UbOXYAU.png"
    st.sidebar.image(logo)
    
    # Customize page title
    st.title("Hawaii Digital Equity Dashboard")
    
    st.markdown(
        """
        This multipage app template demonstrates various interactive web apps created using [streamlit](https://streamlit.io) and [leafmap](https://leafmap.org). It is an open-source project and you are very welcome to contribute to the [GitHub repository](https://github.com/opengeos/streamlit-map-template).
        """
    )
    
    st.header("Instructions")
    
    markdown = """
    1. For the [GitHub repository](https://github.com/opengeos/streamlit-map-template) or [use it as a template](https://github.com/opengeos/streamlit-map-template/generate) for your own project.
    2. Customize the sidebar by changing the sidebar text and logo in each Python files.
    3. Find your favorite emoji from https://emojipedia.org.
    4. Add a new app to the `pages/` directory with an emoji in the file name, e.g., `1_🚀_Chart.py`.
    
    """
    
    st.markdown(markdown)

    # Load data
    data_file = "data/BroadBandCover_by_City.csv"
    data = pd.read_csv(data_file)
    
    # Drop rows where coordinates couldn't be found
    data.dropna(subset=['Latitude', 'Longitude'], inplace=True)

    # Create Leafmap map
    coverage_map = leafmap.Map(center=[20.5, -157.5], zoom=7)  # Center on Hawaii

    # Prepare data for heatmap
    data['BroadbandCoverage'] = data['BroadbandCoverage'].str.replace('%', '').astype(float)
    
    # Add heatmap layer
    coverage_map.add_heatmap(data=data,
                  latitude="Latitude",
                  longitude="Longitude",
                  value="BroadbandCoverage",
                  name="Heat map",
                  radius=15)

    coverage_map.to_streamlit(height=500)

    providers_map = leafmap.Map(center=[20.5, -157.5], zoom=7)  # Center on Hawaii
    # Add heatmap layer
    providers_map.add_heatmap(data=data,
                  latitude="Latitude",
                  longitude="Longitude",
                  value="Providers",
                  name="Heat map",
                  radius=15)

    providers_map.to_streamlit(height=500)

if __name__ == "__main__":
    main()
