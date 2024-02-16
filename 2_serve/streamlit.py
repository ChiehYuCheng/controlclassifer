import streamlit as st
import subprocess
import os
import sys

def model_prediction(user_input):
    process = subprocess.Popen([sys.executable, os.path.join(os.path.dirname(__file__), '..', '1_model', 'predict.py'), f'"{user_input}"'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode == 0:
        return stdout.decode().strip().split('\n')[-1]
    else:
        return "Error in prediction:", stderr.decode()

def landing_page():
    st.title('Choose your request type')
    st.session_state['choice'] = st.radio("Choose an option",
                      ('Request classification',
                       'Request export control status with classified item',
                       'Request export control status with unclassified item'), label_visibility='collapsed')
    if st.button('Next'):
        if st.session_state['choice'] == 'Request classification' or st.session_state['choice'] == 'Request export control status with unclassified item':
            st.session_state['page'] = model_page
            st.rerun()
        elif st.session_state['choice'] == 'Request export control status with classified item':
            st.session_state['page'] = control_page
            st.rerun()
            

def control_page():
    st.title('Is your item control?')
    st.session_state['control'] = st.radio("Choose an option", ('Yes', 'No'), label_visibility='collapsed')
    if st.button('Next'):
        st.session_state['page'] = country_page

def vitesco_page():
    st.title('Is your item manufactured by Vitesco?')
    st.session_state['vitesco'] = st.radio("Choose an option", ('Yes', 'No'), label_visibility='collapsed')
    if st.button('Next'):
        st.session_state['page'] = country_page

def model_page():
    st.title('Enter item description for classification')
    st.session_state['user_input'] = st.text_input("Enter text", label_visibility='collapsed')
    if st.button('Next'):
        if st.session_state['user_input']:
            st.write("Please wait...")
            st.session_state['prediction'] = float(model_prediction(st.session_state['user_input']))
            st.session_state['page'] = vitesco_page
            st.session_state['user_input'] = None
            st.rerun()
        else:
            st.write("Please enter some text to classify.")

def country_page():
    st.title('Is the item intended for export to one of the following countries?')
    st.write('Afghanistan, Belarus, Burma, Central African Republic, China, Cuba, Cyprus, Democratic Republic of the Congo, Eritrea, Haiti, Iran, Iraq, Lebanon, Liberia, Libya, North Korea, Russia, Somalia, South Sudan, Sudan, Syria, Venezuela, Yemen, Zimbabwe')
    st.session_state['country'] = st.radio("Choose an option", ('Yes', 'No'), label_visibility='collapsed')
    if st.button('Next'):
        if st.session_state['choice'] == 'Request export control status with classified item':
            if st.session_state['control'] == 'Yes' or st.session_state['country'] == 'Yes':
                # Annex 8
                st.markdown("Please [click here](https://docs.google.com/forms/d/e/1FAIpQLSeO9y_g_LV-KqlPXRuF0_Y4pAYxy4n4v8p45RNMToHyQT_ggQ/viewform) to proceed to the next step.")
        else:
            st.write("Your shipment is ready to go.")
        
        if st.session_state['vitesco'] == 'No' and st.session_state['prediction'] < 0.5 and st.session_state['country'] == 'No':
            # Annex 6
            st.markdown("Please [click here](https://docs.google.com/forms/d/e/1FAIpQLSdroe6sJXEt9d1rfDmb0mv3NlyU2vIIrHUCy2BQxJC1L35YQQ/viewform) to proceed to the next step.")
        elif st.session_state['vitesco'] == 'No' and st.session_state['prediction'] < 0.5 and st.session_state['country'] == 'Yes':
            # Annex 6 + 8
            st.markdown("Please [click here](https://docs.google.com/forms/d/e/1FAIpQLSfucMnZA9u7z9mHJjwpWcGb_HaBQ1dtlFNdRveaynzHcX0AFA/viewform) to proceed to the next step.")
        elif st.session_state['vitesco'] == 'No' and st.session_state['prediction'] >= 0.5 and st.session_state['country'] == 'No':
            # Annex 6 + 8
            st.markdown("Please [click here](https://docs.google.com/forms/d/e/1FAIpQLSfucMnZA9u7z9mHJjwpWcGb_HaBQ1dtlFNdRveaynzHcX0AFA/viewform) to proceed to the next step.")
        elif st.session_state['vitesco'] == 'No' and st.session_state['prediction'] >= 0.5 and st.session_state['country'] == 'Yes':
            # Annex 6 + 8
            st.markdown("Please [click here](https://docs.google.com/forms/d/e/1FAIpQLSfucMnZA9u7z9mHJjwpWcGb_HaBQ1dtlFNdRveaynzHcX0AFA/viewform) to proceed to the next step.")
        elif st.session_state['vitesco'] == 'Yes' and st.session_state['prediction'] < 0.5 and st.session_state['country'] == 'No':
            # Annex 7
            st.markdown("Please [click here](https://docs.google.com/forms/d/e/1FAIpQLSel5eP92d3OTvMKDBTh9bWL7Kg-jVs6DzkwsTcf-hRFM_uFNw/viewform) to proceed to the next step.")
        else:
            # Annex 7 + 8
            st.markdown("Please [click here](https://docs.google.com/forms/d/18_jvzJj9J37pM-fzUB5ZzlqKaOtlqFpKufytNSJ7W2A/prefill) to proceed to the next step.")
                                          
def main():
    if 'page' not in st.session_state:
        landing_page()
    else:
        st.session_state['page']()
        
if __name__ == '__main__':
    main()
