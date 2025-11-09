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

def fetch_store_metrics(api_url, store_id):
    try:
        # FastAPI endpoint expects a raw string body. Send the store_id as a JSON string
        # (i.e. body = "Store1") so Body(str) on the server will parse it.
        resp = requests.post(api_url, json=store_id, headers=headers, timeout=30)
        if resp.status_code == 200:
            data = resp.json()
            print("store review data ", data)
            return data

        # If server rejects JSON string (422), try a plain text fallback
        if resp.status_code == 422:
            try:
                resp2 = requests.post(api_url, data=store_id, headers={"Content-Type": "text/plain"}, timeout=30)
                if resp2.status_code == 200:
                    return resp2.json()
                else:
                    st.error(f"Failed to fetch store reviews (fallback): {resp2.status_code} {resp2.text}")
                    return []
            except Exception as e:
                st.error(f"Error fetching store reviews (fallback): {e}")
                return []

        # other non-200 responses
        st.error(f"Failed to fetch store reviews: {resp.status_code} {resp.text}")
        return []
    except Exception as e:
        st.error(f"Error fetching store reviews: {e}")
        return []

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
.metric-good { color: #28a745; font-weight: 700; font-size: 1.8rem; }
.metric-bad { color: #dc3545; font-weight: 700; font-size: 1.8rem; }
.metric-neutral { color: #ffc107; font-weight: 700; font-size: 1.8rem; }
.metric-label { font-size: 0.95rem; color: #333; margin-bottom: 0.2rem; }
.metric-block { padding: 0.25rem 0.5rem; }
.font-bold { font-weight: 700; font-size: 1.8rem;}
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

def get_color_class(score):
    # Accepts numeric scores (1-5) or returns neutral for non-numeric values
    try:
        score = float(score)
        if score >= 4:
            return "metric-good"
        elif score <= 2:
            return "metric-bad"
        return "metric-neutral"
    except (ValueError, TypeError):
        return "metric-neutral"

def format_metric(label, value, text_class=None, label_class=None):
    # For non-numeric text values (like overall sentiment) allow explicit class
    if text_class:
        cls = text_class
    else:
        cls = get_color_class(value)
    return f"""
        <div class='metric-block'>
          <div class='metric-label {label_class}'>{label}</div>
          <div class='{cls}'>{value}</div>
        </div>
    """

def render_metrics_grid(metrics, cols=3, text_class=None):
    """Render a list of (label, value) pairs into a grid of columns.
    metrics: list of (label, value)
    """
    if not metrics:
        return
    columns = st.columns(cols)
    for idx, (label, value) in enumerate(metrics):
        col = columns[idx % cols]
        print("col", col)
        with col:
            st.markdown(format_metric(label, value, text_class), unsafe_allow_html=True)



tab_store_wise, tab_all = st.tabs(["Store Wise Analysis", "Complete Analysis"])

with tab_store_wise:
    # Three-column layout: left (60%), divider (thin), right (40%)
    col_left, col_div, col_right = st.columns([3, 0.08, 2])

    # vertical divider in the middle column
    with col_div:
        st.markdown(
            "<div style='border-left:1px solid #ddd; height:calc(100vh - 20px); position:sticky; top:80px; margin-left:10px;'></div>",
            unsafe_allow_html=True,
        )

    with col_left:

        # Dropdown (selectbox) for choosing a store (shows human-friendly names)
        store_names = [s["name"] for s in stores_list]
        selected_name = st.selectbox("Choose a store", store_names)
        # find the selected store dict (fallback to first)
        selected_store = next((s for s in stores_list if s["name"] == selected_name), stores_list[0])
        # st.write(f"Selected store: {selected_store['name']} (id: {selected_store['id']})")

        # Per-store cache: only fetch from backend if we haven't already fetched for this store
        if 'store_cache' not in st.session_state:
            st.session_state.store_cache = {}

        store_id = selected_store['id']

        # Helper to perform fetch and update cache
        def _fetch_and_cache(sid, sname):
            with st.spinner(f"Agent is running for {sname}..."):
                store_reviews = fetch_store_metrics(url + "fetch_mi_for_oniline_reveiws", sid)
                store_media = fetch_store_metrics(url + "fetch_mi_for_media_description", sid)
                store_structured_data = fetch_store_metrics(url + "fetch_mi_for_structured_data", sid)
                st.session_state.store_cache[sid] = {
                    'reviews': store_reviews,
                    'media': store_media,
                    'structured': store_structured_data,
                }

        # Always check cache for the selected store; fetch only on cache miss
        if store_id in st.session_state.store_cache:
            st.session_state['last_fetch_from_cache'] = True
        else:
            # Cache miss — fetch now and store
            _fetch_and_cache(store_id, selected_store['name'])
            st.session_state['last_fetch_from_cache'] = False
        # record the selection
        st.session_state['selected_store_id'] = store_id

        # Populate the current display slots from the cache (exists now whether freshly fetched or previously present)
        cached = st.session_state.store_cache.get(store_id)
        if cached:
            st.session_state.store_reviews = cached.get('reviews')
            st.session_state.store_media = cached.get('media')
            st.session_state.store_structured_data = cached.get('structured')
        else:
            # No data available (e.g., fetch failed); ensure variables are present but empty
            st.session_state.store_reviews = None
            st.session_state.store_media = None
            st.session_state.store_structured_data = None

        # Small UI helpers: show whether we loaded from cache or fetched just now, and allow manual refresh
        if st.session_state.get('last_fetch_from_cache'):
            st.info("Loaded data from cache for the selected store.")
        else:
            st.success("Fetched fresh data for the selected store.")

        # Allow user to force-refresh the selected store's cached data
        if st.button("Refresh Store Analysis", key=f"refresh_{store_id}"):
            _fetch_and_cache(store_id, selected_store['name'])
            st.session_state['last_fetch_from_cache'] = False
            st.rerun()

        tab_sentiment, tab_media, tab_structured = st.tabs(["Reviews", "Video & Image Scorecard", "Structured Data Analysis"])

        with tab_sentiment:
                    # Show fetched data if available
            reviews = st.session_state.get('store_reviews')
            if reviews:
                st.subheader("Store Reviews Analysis")
                
                # Render review metrics using shared helpers
                review_metrics = [
                    ("Staff Behavior",reviews.get('Staff_behaviour_score', 'N/A')),
                    ("Cleanliness",reviews.get('Cleanliness_score', 'N/A')),
                    ("Product Availability",reviews.get('Product_availability_score', 'N/A')),
                    ("Parking",reviews.get('Parking_score', 'N/A')),
                    ("Discounts",reviews.get('Discount', 'N/A')),
                ]
                render_metrics_grid(review_metrics, cols=3)

                # Overall sentiment (text) - color by explicit mapping
                sentiment =reviews.get('overall_sentiment', 'N/A')
                sentiment_class = {
                    'positive': 'metric-good',
                    'negative': 'metric-bad',
                    'neutral': 'metric-neutral'
                }.get(str(sentiment).lower(), 'metric-neutral')
                st.markdown(format_metric("Overall Sentiment", str(sentiment).title(), text_class=sentiment_class, label_class='font-bold'), unsafe_allow_html=True)

                # Display detailed insights
                st.subheader("Detailed Insights")
                st.markdown("**Key Findings:**")
                st.write(st.session_state.store_reviews.get('insights_para', ''))
                
                st.markdown("**Improvement Suggestions:**")
                st.write(st.session_state.store_reviews.get('improvements_para', ''))
        with tab_media:
            # Media (video & image) analysis results
            media = st.session_state.get('store_media')
            if media:
                st.subheader("Video & Image Reviews Analysis")

                # Use shared metric renderer for media metrics
                media_metrics = [
                    ("Cleanliness", media.get('Cleanliness_score', 'N/A')),
                    ("Waiting Queue", media.get('Waiting Queue_score', 'N/A')),
                    ("Staff Behavior", media.get('Staff_behaviour_score', 'N/A')),
                    ("Misplaced Inventory", media.get('Misplaced_inventory_score', 'N/A')),
                    ("Empty Shelves", media.get('empty_shelves_score', 'N/A')),
                ]
                render_metrics_grid(media_metrics, cols=3)

                # Display detailed insights
                st.subheader("Detailed Insights")
                st.markdown("**Key Findings:**")
                st.write(media.get('insights_para', ''))
                
                st.markdown("**Improvement Suggestions:**")
                st.write(media.get('improvements_para', ''))
            else:
                st.info("No media analysis available for the selected store.")
      

        with tab_structured:
            # Structured data analysis results
            structured = st.session_state.get('store_structured_data')
            if structured:
                st.subheader("Structured Data Analysis")

                # Pick key numeric metrics to show in a grid
                structured_metrics = [
                    ("Total Sales", structured.get('total sales', 'N/A')),
                    ("MoM Sales Growth", structured.get('MoM sales growth', 'N/A')),
                    ("Average Order Value (AOV)", structured.get('Average Order Value (AOV)', 'N/A')),
                    ("Employee Utilization (%)", structured.get('Employee Utilization', 'N/A')),
                    ("Avg Employee Rating", structured.get('Average employee rating', 'N/A')),
                ]
                render_metrics_grid(structured_metrics, cols=3, text_class="font-bold")

                 # Display detailed insights
                st.subheader("Detailed Insights")
                st.markdown("**Key Findings:**")
                st.write(structured.get('insights_para', ''))
                
                st.markdown("**Improvement Suggestions:**")
                st.write(structured.get('improvements_para', ''))
            else:
                st.info("No structured data analysis available for the selected store.")


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