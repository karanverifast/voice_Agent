import streamlit as st
import requests
import json
from datetime import datetime, timedelta, timezone

# Hardcoded Bolna API credentials
BOLNA_API_KEY = "bn-e947064ac0e041948e5fe78a59a5a3c1"
BOLNA_AGENT_ID = "87f0e234-fa36-45d4-9297-b2097709636d"

# Streamlit page configuration
st.set_page_config(
    page_title="Abandoned Cart Recovery",
    page_icon="📞",
    layout="centered"
)

# Title and description
st.title("📞 Abandoned Cart Recovery Call System")
st.markdown("Enter the customer's phone number to initiate a call")

# Sidebar with credentials status
with st.sidebar:
    st.header("⚙️ Configuration")
    
    st.success("✅ API Key configured")
    st.success("✅ Agent ID configured")
    
    st.markdown("---")
    st.markdown("### About")
    st.markdown("This app initiates AI-powered calls to customers who abandoned their shopping carts.")

# Main content
st.markdown("---")

# Input for phone number
col1, col2 = st.columns([3, 1])

with col1:
    phone_number = st.text_input(
        "Customer Phone Number",
        placeholder="+1234567890",
        help="Enter phone number with country code (e.g., +1234567890 or +919876543210)"
    )

with col2:
    st.markdown("<div style='padding-top: 28px;'></div>", unsafe_allow_html=True)
    initiate_call = st.button("📞 Initiate Call", type="primary", use_container_width=True)


# Function to initiate Bolna call
def initiate_bolna_call(phone, api_key, agent_id):
    """
    Initiate a call using Bolna API
    Returns: (response_json, error_string)
    """
    # Bolna API endpoint for initiating calls
    # (you can switch .ai to .dev if your account is on that host)
    url = "https://api.bolna.ai/call"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "agent_id": agent_id,
        "recipient_phone_number": phone,
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        response.raise_for_status()
        return response.json(), None
    except requests.exceptions.HTTPError as e:
        error_msg = f"HTTP Error: {e.response.status_code}"
        try:
            error_detail = e.response.json()
            error_msg += f" - {error_detail}"
        except Exception:
            error_msg += f" - {e.response.text}"
        return None, error_msg
    except requests.exceptions.RequestException as e:
        return None, str(e)


# 🔎 Helper: fetch all executions (call logs) for this agent
def get_agent_executions(api_key, agent_id, page_number=1, page_size=20):
    """
    Use Bolna's /v2/agent/{agent_id}/executions API to get call history.
    """
    url = f"https://api.bolna.ai/v2/agent/{agent_id}/executions"
    headers = {
        "Authorization": f"Bearer {api_key}",
    }
    params = {
        "page_number": page_number,
        "page_size": page_size,
        # you can also add filters like status, call_type, provider, etc.
    }
    try:
        resp = requests.get(url, headers=headers, params=params, timeout=15)
        resp.raise_for_status()
        return resp.json(), None
    except requests.exceptions.HTTPError as e:
        msg = f"HTTP Error: {e.response.status_code}"
        try:
            detail = e.response.json()
            msg += f" - {detail}"
        except Exception:
            msg += f" - {e.response.text}"
        return None, msg
    except requests.exceptions.RequestException as e:
        return None, str(e)


def format_timestamp(ts: str) -> str:
    """Nicely format ISO datetimes from Bolna and convert to IST."""
    if not ts:
        return "-"
    try:
        # Parse the datetime (handles both ...Z and plain ISO with microseconds)
        dt_utc = datetime.fromisoformat(ts.replace("Z", "+00:00"))

        # If it’s naive (no tzinfo), assume it is UTC
        if dt_utc.tzinfo is None:
            dt_utc = dt_utc.replace(tzinfo=timezone.utc)

        # Convert to IST (UTC+5:30)
        dt_ist = dt_utc.astimezone(timezone(timedelta(hours=5, minutes=30)))

        return dt_ist.strftime("%Y-%m-%d %H:%M:%S IST")
    except Exception:
        # If anything goes wrong, just return the original string
        return ts



def connection_state_from_status(status: str) -> str:
    """
    Map Bolna call status to a simple connection state:
    - Trying to connect
    - Connected
    - Failed / Not connected
    """
    if status in ["queued", "initiate", "ringing", "in-progress"]:
        return "Trying to connect"
    if status in ["completed"]:
        return "Connected"
    if not status:
        return "-"
    return "Failed / Not connected"


# Handle call initiation
last_execution_id = None

if initiate_call:
    if not phone_number:
        st.error("❌ Please enter a phone number")
    else:
        with st.spinner("Initiating call..."):
            result, error = initiate_bolna_call(
                phone_number,
                BOLNA_API_KEY,
                BOLNA_AGENT_ID
            )
        
        if error:
            st.error(f"❌ Error initiating call: {error}")
            st.info("💡 Tip: Make sure the phone number is in international format (e.g., +1234567890)")
        else:
            st.success(f"✅ Call initiated successfully to {phone_number}!")
            
            with st.expander("📋 Raw API Response", expanded=False):
                st.json(result)
            
            execution_id = result.get("execution_id") or result.get("call_id")
            if execution_id:
                st.info(f"📝 Execution ID: `{execution_id}`")
                last_execution_id = execution_id


# =========================
# 📊 Call logs instead of "Recent Calls"
# =========================
st.markdown("---")
st.markdown("### 📊 Call Logs (Agent History)")

with st.spinner("Fetching call logs from Bolna..."):
    executions_payload, exec_error = get_agent_executions(BOLNA_API_KEY, BOLNA_AGENT_ID)

if exec_error:
    st.error(f"Couldn't load call logs: {exec_error}")
else:
    executions = executions_payload.get("data", []) if executions_payload else []

    if not executions:
        st.info("No calls found yet for this agent.")
    else:
        rows = []
        for e in executions:
            telephony = e.get("telephony_data") or {}
            batch_run = e.get("batch_run_details") or {}
            # `retried` = how many times this execution was retried; attempts = retries + 1
            retries = batch_run.get("retried", 0) or 0
            attempts = retries + 1

            status = e.get("status", "-")
            rows.append(
                {
                    "Time (IST)": format_timestamp(e.get("created_at")),
                    "Customer Number": telephony.get("to_number", "-"),
                    "Status": status,
                    "Connection State": connection_state_from_status(status),
                    "Duration (sec)": telephony.get("duration"),
                    "Attempts": attempts,
                    "Execution ID": e.get("id", "-"),
                }
            )

        # If a phone number is typed, show those calls first
        if phone_number:
            filtered = [r for r in rows if r["Customer Number"] == phone_number]
            if filtered:
                st.markdown("#### Calls to this customer")
                st.dataframe(filtered, use_container_width=True)

        st.markdown("#### All Calls for this Agent")
        st.dataframe(rows, use_container_width=True)


# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; font-size: 0.8em;'>
        Powered by Verifast
    </div>
    """,
    unsafe_allow_html=True
)
