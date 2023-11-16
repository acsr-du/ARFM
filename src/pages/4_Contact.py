import streamlit as st


st.set_page_config(layout="wide", page_title="Contact", page_icon="📞")

# ------------------------custom-css---------------------
css_changes = """ 
        <style>
        #MainMenu, footer {visibility: hidden;}
        .modebar-group {visibility: hidden;}
        header {visibility: hidden;}
        </style>
        """
#Hide Streamlit pre-built items

contact_form = """

<form action="https://formsubmit.co/@gmail.com" method="POST">
     <input type="hidden" name="_captcha" value="false">
     <input type="text" name="name" placeholder="Your Name" required>  
     <input type="email" name="email" placeholder="Your Email" required>
     <textarea name="message" placeholder="Details of your problem"></textarea>
     <button type="submit">Send</button>
</form>

"""
st.markdown(css_changes, unsafe_allow_html=True)



#-------------------------Functions-----------------------

def local_css(file):
    with open(file) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

        
#-------------------------Content-------------------------

st.header(":mailbox: Get In Touch With Us!")
st.markdown(contact_form, unsafe_allow_html=True)

local_css("/var/LearnStreamlit/assets/style.css")