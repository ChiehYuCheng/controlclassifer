import streamlit as st
import subprocess
import os
import sys

def main():
    st.title('Export Control Classification Tool')
    user_input = st.text_input("Enter text for classification:")
    
    if st.button('Classify'):
        if user_input:

            process = subprocess.Popen([sys.executable, os.path.join(os.path.dirname(__file__), '..', '1_model', 'predict.py'), f'"{user_input}"'],
                                       stdout=subprocess.PIPE, 
                                       stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()

            if process.returncode == 0:
                result_line = stdout.decode().strip().split('\n')[-1]
                st.write(result_line)
            else:
                st.write("Error in prediction:")
                st.write(stderr.decode())
        else:
            st.write("Please enter some text to classify.")

if __name__ == '__main__':
    main()
