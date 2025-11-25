import streamlit as st
import requests
import os

# Configuration
API_URL = "http://localhost:8000"

st.set_page_config(page_title="Autonomous QA Agent", layout="wide")

st.title("🤖 Autonomous QA Agent")
st.markdown("Generate Test Cases and Selenium Scripts from Documentation and HTML.")

# Sidebar for API Key
with st.sidebar:
    st.header("Configuration")
    api_key = st.text_input("OpenAI API Key", type="password")
    if api_key:
        os.environ["OPENAI_API_KEY"] = api_key
        # Note: In a real production app, we'd pass this to the backend securely.
        # For this demo running locally, setting it here might not affect the separate backend process 
        # unless we pass it in the request or run them in the same env.
        # To make it work easily, we will assume the user runs the backend with the key set, 
        # OR we can pass it in headers (requires backend update).
        # For now, let's instruct the user to set it in the terminal or .env.
        st.info("Ensure the backend is running with this API Key available.")

# Tabs
tab1, tab2, tab3 = st.tabs(["📂 Knowledge Base", "📝 Test Case Agent", "💻 Script Agent"])

# Tab 1: Knowledge Base
with tab1:
    st.header("Build Knowledge Base")
    uploaded_files = st.file_uploader("Upload Support Documents (MD, TXT, JSON)", accept_multiple_files=True)
    
    if st.button("Build Knowledge Base"):
        if uploaded_files:
            files = [("files", (file.name, file.getvalue(), file.type)) for file in uploaded_files]
            with st.spinner("Parsing documents and building vector store..."):
                try:
                    response = requests.post(f"{API_URL}/upload", files=files)
                    if response.status_code == 200:
                        st.success(response.json()["message"])
                    else:
                        st.error(f"Error: {response.text}")
                except Exception as e:
                    st.error(f"Connection Error: {e}")
        else:
            st.warning("Please upload at least one document.")

    st.subheader("Target HTML")
    html_file = st.file_uploader("Upload checkout.html", type=["html"])
    html_content = ""
    if html_file:
        html_content = html_file.getvalue().decode("utf-8")
        st.code(html_content[:500] + "...", language="html")
        # Store HTML in session state for other tabs
        st.session_state["html_content"] = html_content

# Tab 2: Test Case Agent
with tab2:
    st.header("Generate Test Cases")
    query = st.text_area("Enter your request (e.g., 'Generate positive and negative test cases for discount code')")
    
    if st.button("Generate Test Cases"):
        if query:
            with st.spinner("Analyzing Knowledge Base..."):
                try:
                    response = requests.post(f"{API_URL}/generate-test-cases", json={"query": query})
                    if response.status_code == 200:
                        test_cases = response.json()["test_cases"]
                        st.session_state["generated_test_cases"] = test_cases
                        st.markdown(test_cases)
                    else:
                        st.error(f"Error: {response.text}")
                except Exception as e:
                    st.error(f"Connection Error: {e}")
        else:
            st.warning("Please enter a query.")

# Tab 3: Script Agent
with tab3:
    st.header("Generate Selenium Script")
    
    if "generated_test_cases" in st.session_state:
        st.markdown("### Generated Test Cases Context")
        st.text_area("Reference Test Cases", st.session_state["generated_test_cases"], height=150, disabled=True)
        
        selected_test_case = st.text_area("Copy & Paste the specific Test Case you want to automate here:", height=100)
        
        if st.button("Generate Script"):
            if selected_test_case and "html_content" in st.session_state:
                with st.spinner("Generating Selenium Script..."):
                    try:
                        payload = {
                            "test_case": selected_test_case,
                            "html_content": st.session_state["html_content"]
                        }
                        response = requests.post(f"{API_URL}/generate-script", json=payload)
                        if response.status_code == 200:
                            script = response.json()["script"]
                            st.code(script, language="python")
                        else:
                            st.error(f"Error: {response.text}")
                    except Exception as e:
                        st.error(f"Connection Error: {e}")
            else:
                st.warning("Please provide a test case and ensure HTML is uploaded in Tab 1.")
    else:
        st.info("Please generate test cases in Tab 2 first.")
