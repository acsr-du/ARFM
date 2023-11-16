import os
import time
import pandas as pd
import streamlit as st
import streamlit_toggle as tog
from streamlit_extras.switch_page_button import switch_page



st.set_page_config(layout="wide" , page_title="Analysis Settings", page_icon=":gear:")


css_changes = """ 
        <style>
        #MainMenu, footer {visibility: hidden;}

        strong{font-size: 17px}

        button[title="View fullscreen"] { display: none;}

        th[aria-colindex="2"] {length: 2000px}

        .css-1oe5cao {display: none;}

        #analyze-exe-s {padding-top: 39px}

        .css-1qg05tj {margin-bottom: 11px}

        div[data-testid="block-container"] {position: relative;padding-bottom: 10px;}

        # p {text-align: center;}


        </style>
        """
#Hide Streamlit pre-built items
st.markdown(css_changes, unsafe_allow_html=True)

loading_gif_html_css = """
<div style="display: flex; justify-content: center; align-items: center; height: 10vh;"><div class="lds-ellipsis"><div></div><div></div><div></div><div></div></div></div>

<style>
.lds-ellipsis {
  display: inline-block;
  position: relative;
  width: 80px;
  height: 80px;
}
.lds-ellipsis div {
  position: absolute;
  top: 33px;
  width: 13px;
  height: 13px;
  border-radius: 50%;
  background: #fcf;
  animation-timing-function: cubic-bezier(0, 1, 1, 0);
}
.lds-ellipsis div:nth-child(1) {
  left: 8px;
  animation: lds-ellipsis1 0.6s infinite;
}
.lds-ellipsis div:nth-child(2) {
  left: 8px;
  animation: lds-ellipsis2 0.6s infinite;
}
.lds-ellipsis div:nth-child(3) {
  left: 32px;
  animation: lds-ellipsis2 0.6s infinite;
}
.lds-ellipsis div:nth-child(4) {
  left: 56px;ML Settings
  animation: lds-ellipsis3 0.6s infinite;
}
@keyframes lds-ellipsis1 {
  0% {
    transform: scale(0);
  }
  100% {
    transform: scale(1);
  }
}
@keyframes lds-ellipsis3 {
  0% {
    transform: scale(1);
  }
  100% {
    transform: scale(0);
  }
}
@keyframes lds-ellipsis2 {
  0% {
    transform: translate(0, 0);
  }
  100% {
    transform: translate(24px, 0);
  }
}

</style>
"""

# Initialize the session state with the button's disabled state
if 'disabled' not in st.session_state:
        st.session_state.disabled = False



col1, col2 = st.columns([4,1.5])

with col1:

        # Your Streamlit app code here 
        st.subheader(":page_facing_up: Files Uploaded for Analysis")

        # Replace 'your_folder_path' with the path to the folder on your desktop
        folder_path = "/var/malwareDetectorV0.1/src/uploaded"

        if not os.path.exists(folder_path):
                st.error("Folder not found. Please provide a valid folder path.")

        files = []
        for filename in os.listdir(folder_path):
                files.append(filename)


        def get_formatted_size(size_in_bytes):
                if size_in_bytes >= 1e9:
                        return f"{size_in_bytes / 1e9:.1f} GB"
                elif size_in_bytes >= 1e6:
                        return f"{size_in_bytes / 1e6:.1f} MB"
                elif size_in_bytes >= 1e3:
                        return f"{size_in_bytes / 1e3:.1f} KB"
                else:
                        return f"{size_in_bytes} B"


        # Create a table to display file details
        file_data = []
        for idx, file in enumerate(files, 1):
                file_path = os.path.join(folder_path, file)
                file_size = os.path.getsize(file_path)
                formatted_size = get_formatted_size(file_size)
                file_data.append((idx, file, formatted_size))


        df = pd.DataFrame(file_data, columns=["Serial No.", "File Name", "Size"])

        st.dataframe(df, hide_index=True, column_config={"File Name": st.column_config.Column(width=550), "Size": st.column_config.Column(width=100)})

        

with col2:

        st.subheader(":wrench: Analyze CSV")

        folder_path = "/var/malwareDetectorV0.1/src/uploaded"
        is_empty = not os.listdir(folder_path)

        if is_empty:
                st.button('Start analysis', key='start_analysis', use_container_width=True, disabled=True)
                st.error("No files uploaded for analysis.\n Please upload files from dashboard first.")
        else:
        
                # Add the "Start Analysis" button
                if st.button('Start analysis', key='start_analysis', type="primary", use_container_width=True, disabled=st.session_state.disabled):

                        def postbtn(): 

                                # Set the button state to True when it's clicked
                                st.session_state.disabled = True
                                
                        postbtn()

                        st.experimental_rerun()  # Force the app to rerun to update the button's state
                
                if st.session_state.disabled:

                        st.markdown("""
                                        <style>
                                        div[data-testid="stVerticalBlock"] {pointer-events: none;}            
                                        </style>
                                        """, unsafe_allow_html=True)
                        # Check if the button is clicked and the disabled state is True

                        # Load GIF
                        st.markdown(loading_gif_html_css, unsafe_allow_html=True)

                        # Show Running text
                        processing_text = st.empty()
                        processing_text.markdown("<div style='text-align: center;'>Initializing...</div>", unsafe_allow_html=True)

                        # Simulate a 5-second processing delay
                        time.sleep(3)
                        
                #  <-----Result Generation----->
                        
                        processing_text.markdown("<div style='text-align: center;'>Suspicious application detection is going on using our trained detection model based on AI...</div>", unsafe_allow_html=True)
                        # process_behaviour()
                        time.sleep(6)
                        processing_text.markdown("<div style='text-align: center;'>Detection is complete threat labels are displayed!!!</div>", unsafe_allow_html=True)
                        time.sleep(4)

                        # Switch to the "results" page
                        switch_page("results")
