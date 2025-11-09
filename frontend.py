import streamlit as st
import requests
import json
 
url = "http://127.0.0.1:8000/v1/"
 
 
headers = {
  'Content-Type': 'application/json'
}

def fetch_stores_list(api_url):
    try:
        resp = requests.get(api_url, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            return data.get("stores", [])
        else:
            st.error(f"Failed to fetch stores list: {resp.status_code} {resp.text}")
            return []
    except Exception as e:
        st.error(f"Error fetching stores list: {e}")
        return []

stores_list = fetch_stores_list(url + "stores_list")

def fetch_store_reviews(api_url):
    pass

st.set_page_config(page_title="ChatBot", page_icon="https://cdn3.iconfinder.com/data/icons/artificial-intelligence-1-2-1/1024/Artificial_intelligence-10-1024.png", layout="wide")



# Inject CSS to reduce/remove Streamlit page padding so content spans fuller width
st.markdown("""
<style>
/* Remove default left/right padding from Streamlit's main block container */
.main .block-container, .block-container, [data-testid="stMain"] .block-container {
  padding-top: 0rem !important;
  padding-bottom: 0rem !important;
  max-width: 100% !important;
}
/* Reduce top padding if present */
.stAppViewContainer, [data-testid="stMain"] {
  padding-top: 0rem !important;
}
</style>
""", unsafe_allow_html=True)

# Inject robust JS to blur focused element and scroll to top on load/rerun
st.markdown("""
    <script>
    (function(){
        function topNow(){
            try{
                if(document.activeElement && typeof document.activeElement.blur === 'function'){
                    document.activeElement.blur();
                }
                window.scrollTo(0,0);
            }catch(e){/* ignore */}
        }
        // run a few times to handle Streamlit reruns/focus changes
        window.addEventListener('load', function(){ setTimeout(topNow, 50); });
        document.addEventListener('DOMContentLoaded', function(){ setTimeout(topNow, 50); });
        var runCount = 0;
        var interval = setInterval(function(){ topNow(); runCount++; if(runCount>20) clearInterval(interval); }, 200);
    })();
    </script>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; margin-bottom: 0.5rem;'>AI Store Manager</h1>", unsafe_allow_html=True)


tab_store_wise, tab_all = st.tabs(["Store Wise Analysis", "Complete Analysis"])

with tab_store_wise:
    # Three-column layout: left (60%), divider (thin), right (40%)
    col_left, col_div, col_right = st.columns([3, 0.08, 2])

    # vertical divider in the middle column
    with col_div:
        st.markdown(
            "<div style='border-left:1px solid #ddd; height:600px; margin-left:10px;'></div>",
            unsafe_allow_html=True,
        )

    with col_left:

        # Dropdown (selectbox) for choosing a store (shows human-friendly names)
        store_names = [s["name"] for s in stores_list]
        selected_name = st.selectbox("Choose a store", store_names)
        # find the selected store dict (fallback to first)
        selected_store = next((s for s in stores_list if s["name"] == selected_name), stores_list[0])
        st.write(f"Selected store: {selected_store['name']} (id: {selected_store['id']})")

        tab_sentiment, tab_media, tab_structured = st.tabs(["Sentiment", "Video & Image Scorecard", "Structured Data Analysis"])

        with tab_sentiment:
            st.header("Sentiment Analysis")
 # need to integrate the API and show the response
        with tab_media:
            st.header("Video & Image Analysis Scorecard")
 # need to integrate the API and show the response
  

        with tab_structured:
            st.header("Structured Data Analysis")
 # need to integrate the API and show the response


        st.markdown("---")
        st.subheader("Store Monitoring")

 # need to integrate the API and show the response

        st.write("Upload images or videos to generate a store monitoring alerts.")
        uploaded_files = st.file_uploader("Upload images/videos", accept_multiple_files=True, type=["png", "jpg", "jpeg", "mp4", "mov"], key="media_upload")
        if st.button("Analyze Media", key="analyze_media"):
            if not uploaded_files:
                st.warning("Please upload at least one image or video.")
            else:
                st.info("Running media analysis (placeholder)")
                for f in uploaded_files:
                    st.markdown(f"**File:** {f.name}")
                    # Placeholder metrics
                    st.metric(label="Clarity", value="N/A")
                    st.metric(label="Content score", value="N/A")
                    st.metric(label="Overall media score", value="N/A")

    with col_right:
        st.subheader("Consolidated Scorecard")
 # need to integrate the API and show the response
        
        user_query = st.text_area("What would you like to know?")
        if st.button('Submit', key="submit_store_wise"):
            with st.spinner("Retrieving information"):
                payload = json.dumps({
                    "query": user_query
                })
                response = requests.request("POST", url+'query', headers=headers, data=payload, timeout=30)
                store_result = response.json()["result"].strip(" ")
                st.text_area(label="Store Wise", value=store_result, height=100, key="store_wise_result")
        st.markdown("---")
        st.subheader("Backend Health Check")
        if st.button("Check Backend Health", key="health_check_btn"):
            try:
                health_url = url + "health_check"
                resp = requests.get(health_url, timeout=10)
                if resp.status_code == 200:
                    health_result = resp.json() if resp.headers.get('Content-Type','').startswith('application/json') else resp.text
                    st.success(f"Health check passed: {health_result}")
                else:
                    st.error(f"Health check failed: {resp.status_code} {resp.text}")
            except Exception as e:
                st.error(f"Health check error: {e}")

with tab_all:
    user_query = st.text_area("What would you like to know about all stores?")
    if st.button('Submit', key="submit_all_stores"):
        with st.spinner("Retrieving information"):
            payload = json.dumps({
                "query": user_query
            })
            response = requests.request("POST", url+'query', headers=headers, data=payload, timeout=30)
            all_stores_result = response.json()["result"].strip(" ")
            st.text_area(label="All Stores", value=all_stores_result, height=100, key="all_stores_result")