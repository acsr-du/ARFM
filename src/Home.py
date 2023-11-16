# ---------------------imports-------------------
import streamlit as st
import pandas as pd
import time
import plotly.graph_objects as go
import pandas as pd
import os
from PIL import Image
from streamlit_extras.switch_page_button import switch_page
import psutil
# ---------------------custom modes-------------------------




st.set_page_config(layout="wide", page_title="Home", page_icon="🏠")

css_changes = """
        <style>
        MainMenu, footer {visibility: hidden;}

        ul {list-style: none; padding-right: 0;}

        .css-1oe5cao1{position:relative; right:40px}

        .modebar-group {visibility: hidden;}

        button[title="View fullscreen"] { display: none;}

        .list-container, .css-k7vsyb {padding: 20px 2px 2px 2px;}

        details[title="Click to view actions"] {display: none;}

        </style>
        """
#Hide Streamlit pre-built items
st.markdown(css_changes, unsafe_allow_html=True)



# --------------------------functions-----------------------


def disk_size():
    st.title("Disk Information")
    
    disk_usage = psutil.disk_usage("/")
    total_size = disk_usage.total
    free_space = disk_usage.free
    used_space = total_size - free_space
    
    st.write(f"Total Disk Size: {format_size(total_size)}")
    st.write(f"Used Space: {format_size(used_space)}")
    st.write(f"Free Space: {format_size(free_space)}")
    
    st.progress(used_space / total_size)

def format_size(size):
    # Convert bytes to human-readable format
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024


def copy_uploaded_files(files, destination_folder):
    for file in files:
        filename = file.name
        destination_path = os.path.join(destination_folder, filename)
        with open(destination_path, "wb") as f:
            f.write(file.getvalue())



def navigate_to_page(page_name):
    # Replace "unique_id" with a unique string to identify this anchor.
    st.markdown(f'<a id="{page_name}"></a>', unsafe_allow_html=True)

    # Create a link to the hidden anchor.
    st.markdown(f'[Click here to go to {page_name}](#{page_name})')




def plot_graph():
    df = pd.read_csv("/var/malwareDetectorV0.1/src/assets/data.csv")
    df.set_index('Family', inplace=True)
    # Plot the data as a line chart using st.line_chart
    chart = st.line_chart(df['Samples'])
    # Plot the data as a line chart using st.line_chart
    # st.write('Showing the relationship between Malware Families and Samples.')

def display_dataframe():
    # Display the DataFrame using st.dataframe
    df = pd.read_csv("/var/malwareDetectorV0.1/src/assets/data.csv")
    st.table(df)
    # st.write('Malware Samples Data')

def download_data():
    # Provide a link to download the DataFrame as a CSV file
    df = pd.read_csv("/var/malwareDetectorV0.1/src/assets/data.csv")
    csv = df.to_csv(index=False)
    st.download_button("Download CSV", data=csv, file_name='malware_data.csv', mime='text/csv')
    # st.write('Download the Malware Samples Data as CSV.')

def main():

    st.title("")
    # -------------------Porject-Banner--------------------
    image = Image.open('/var/malwareDetectorV0.1/src/images/b1.png')
    st.image(image) 
    st.divider()

    # --------------------sidebar---------------------------------------
    with st.sidebar:

        disk_size()

        st.divider()

        st.subheader(":1234: Version ***(Beta)***")
        st.code("0.1")
    #-------------------------upload-button------------------------------

    server_folder_path = "/var/malwareDetectorV0.1/src/uploaded"  # Replace with the desired folder path

    uploaded_files = st.file_uploader("Upload CSV File", type=["csv"])

    time.sleep(3)
    if uploaded_files:
        # Save the uploaded CSV file to the server folder
        os.makedirs(server_folder_path, exist_ok=True)
        copy_uploaded_files([uploaded_files], server_folder_path)
        # copy_uploaded_files([uploaded_files], "/var/malwareDetectorV0.1/src/analysis/preprocessing/csv")
        switch_page("config")


    st.divider()


    # ------------------------Contents-------------------------
        

        
    st.subheader(":clipboard: Tested Malware Data")

    tab1, tab2, tab3 = st.tabs(["Graph 📈", "Dataframe 📃", "Download ⬇️"])
    # Show content based on the selected tab
    with tab1:
        plot_graph()
    with tab2:
        display_dataframe()
    with tab3:
        download_data()

    





# ---------------------driver-----------------------
if __name__ == '__main__':
    main()


