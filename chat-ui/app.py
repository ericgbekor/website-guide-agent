"""
Cloud Run ADK Agent Chat Application
====================================

This Streamlit application provides a chat interface for interacting with ADK agents
deployed on Google Cloud Run. It handles authentication and API communication with
your Cloud Run service.

Requirements:
------------
- ADK Agent deployed on Google Cloud Run
- Cloud Run service accessible without authentication
- Streamlit and related packages installed

Usage:
------
1. Configure your Cloud Run service URL
2. Create a session (optional) or start chatting directly
3. Send messages and receive responses from your deployed agent

Architecture:
------------
- HTTP requests to Cloud Run service endpoints
- Direct HTTP communication
- Session management for stateful conversations
- Response processing for ADK event format
"""

import streamlit as st
import requests
import json
import time
import uuid
from typing import Dict, List, Optional, Any
import os

# Set page config
st.set_page_config(
    page_title="Cloud Run Agent Chat",
    page_icon=":robot:",
    layout="wide",
    initial_sidebar_state="expanded"
)

class CloudRunADKClient:
    """Client for ADK agents deployed on Google Cloud Run"""
    
    def __init__(self, service_url: str):
        self.service_url = service_url.rstrip('/')
    
    
    def _get_headers(self):
        """Get appropriate headers"""
        headers = {"Content-Type": "application/json"}
        return headers
    
    def health_check(self) -> Dict:
        """Check if the Cloud Run service is healthy"""
        try:
            response = requests.get(
                f"{self.service_url}/health",
                headers=self._get_headers(),
                timeout=10
            )
            
            return {
                "success": response.status_code == 200,
                "status_code": response.status_code,
                "response": response.text[:200] if response.text else "No response"
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def create_session(self, user_id: str, app_name: str = "agent") -> Dict:
        """Create a new session with the agent"""
        session_id = f"session-{int(time.time())}"
        
        try:
            # Try standard ADK session creation
            response = requests.post(
                f"{self.service_url}/apps/{app_name}/users/{user_id}/sessions/{session_id}",
                headers=self._get_headers(),
                json={},
                timeout=30
            )
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "session_id": session_id,
                    "user_id": user_id,
                    "response": response.json() if response.content else {}
                }
            else:
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}: {response.text}"
                }
                
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": f"Connection error: {str(e)}"
            }
    
    def send_message_run_endpoint(self, message: str, user_id: Optional[str] = None, session_id: Optional[str] = None, app_name: str = "agent") -> Dict:
        """Send message using the /run endpoint"""
        try:
            payload = {
                "appName": app_name,
                "userId": user_id or f"user-{int(time.time())}",
                "sessionId": session_id,
                "newMessage": {
                    "role": "user",
                    "parts": [{"text": message}]
                }
            }
            
            response = requests.post(
                f"{self.service_url}/run",
                headers=self._get_headers(),
                json=payload,
                timeout=120
            )
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "response": response.json()
                }
            else:
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}: {response.text}"
                }
                
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": f"Connection error: {str(e)}"
            }
    
    def send_message_run_sse(self, message: str, user_id: Optional[str] = None, session_id: Optional[str] = None, app_name: str = "agent") -> Dict:
        """Send message using the /run_sse endpoint (Server-Sent Events)"""
        try:
            payload = {
                "appName": app_name,
                "userId": user_id or f"user-{int(time.time())}",
                "sessionId": session_id,
                "newMessage": {
                    "role": "user",
                    "parts": [{"text": message}]
                }
            }
            
            # For SSE, we'll get a streaming response
            response = requests.post(
                f"{self.service_url}/run_sse",
                headers=self._get_headers(),
                json=payload,
                timeout=120,
                stream=True
            )
            
            if response.status_code == 200:
                # Collect all SSE events
                events = []
                for line in response.iter_lines(decode_unicode=True):
                    if line.startswith('data: '):
                        try:
                            event_data = json.loads(line[6:])  # Remove 'data: ' prefix
                            events.append(event_data)
                        except json.JSONDecodeError:
                            continue
                
                return {
                    "success": True,
                    "response": events
                }
            else:
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}: {response.text}"
                }
                
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": f"Connection error: {str(e)}"
            }
    
    def send_message_simple(self, message: str, user_id: Optional[str] = None, session_id: Optional[str] = None) -> Dict:
        """Send message using simple chat endpoint"""
        try:
            payload = {"message": message}
            
            if user_id:
                payload["user_id"] = user_id
            if session_id:
                payload["session_id"] = session_id
            
            response = requests.post(
                f"{self.service_url}/chat",
                headers=self._get_headers(),
                json=payload,
                timeout=120
            )
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "response": response.json()
                }
            else:
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}: {response.text}"
                }
                
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": f"Connection error: {str(e)}"
            }
    
    def send_message_direct(self, message: str, user_id: Optional[str] = None, session_id: Optional[str] = None) -> Dict:
        """Send message to root endpoint (some Cloud Run services use this)"""
        try:
            payload = {
                "query": message,
                "user_id": user_id or f"user-{int(time.time())}",
                "session_id": session_id
            }
            
            response = requests.post(
                f"{self.service_url}/",
                headers=self._get_headers(),
                json=payload,
                timeout=120
            )
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "response": response.json()
                }
            else:
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}: {response.text}"
                }
                
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": f"Connection error: {str(e)}"
            }
    
    def process_response(self, response_data: Any) -> Dict:
        """Process Cloud Run response to extract text and tool information"""
        result = {
            'final_text': '',
            'tool_calls': [],
            'tool_responses': [],
            'events': [],
            'status': 'success',
            'raw_response': response_data
        }
        
        try:
            # Handle ADK-style event list
            if isinstance(response_data, list):
                result['events'] = response_data
                
                for event in response_data:
                    if isinstance(event, dict):
                        content = event.get("content", {})
                        
                        # Extract model responses
                        if content.get("role") == "model":
                            parts = content.get("parts", [])
                            for part in parts:
                                if "text" in part and part["text"]:
                                    result['final_text'] += part["text"] + " "
                        
                        # Extract function calls
                        parts = content.get("parts", [])
                        for part in parts:
                            if "functionCall" in part:
                                func_call = part["functionCall"]
                                result['tool_calls'].append({
                                    'name': func_call.get('name', 'unknown'),
                                    'args': func_call.get('args', {})
                                })
                            
                            # Extract function responses
                            elif "functionResponse" in part:
                                func_response = part["functionResponse"]
                                result['tool_responses'].append({
                                    'name': func_response.get('name', 'unknown'),
                                    'response': func_response.get('response', {})
                                })
            
            # Handle direct response object
            elif isinstance(response_data, dict):
                # Direct text fields
                for text_field in ['text', 'response', 'message', 'output', 'result']:
                    if text_field in response_data and response_data[text_field]:
                        result['final_text'] = str(response_data[text_field])
                        break
                
                # Handle nested content
                if 'content' in response_data:
                    content = response_data['content']
                    if isinstance(content, str):
                        result['final_text'] = content
                    elif isinstance(content, dict) and 'text' in content:
                        result['final_text'] = content['text']
                
                # Handle events field
                if 'events' in response_data:
                    result['events'] = response_data['events']
                    # Process events recursively
                    events_result = self.process_response(response_data['events'])
                    if events_result['final_text']:
                        result['final_text'] = events_result['final_text']
                    result['tool_calls'].extend(events_result['tool_calls'])
                    result['tool_responses'].extend(events_result['tool_responses'])
                
                # If no text found, try to stringify the response nicely
                if not result['final_text']:
                    # Remove common metadata fields before stringifying
                    clean_response = {k: v for k, v in response_data.items() 
                                    if k not in ['timestamp', 'request_id', 'metadata', 'status']}
                    if clean_response:
                        result['final_text'] = json.dumps(clean_response, indent=2)
            
            # Handle string response
            elif isinstance(response_data, str):
                result['final_text'] = response_data
            
            # Handle other types
            else:
                result['final_text'] = str(response_data)
            
            # Clean up final text
            result['final_text'] = result['final_text'].strip()
            
            return result
            
        except Exception as e:
            return {
                'final_text': f"Error processing response: {str(e)}",
                'tool_calls': [],
                'tool_responses': [],
                'events': [],
                'status': 'error',
                'raw_response': response_data
            }

# Initialize session state
def initialize_session_state():
    """Initialize Streamlit session state variables"""
    if "user_id" not in st.session_state:
        st.session_state.user_id = f"user-{uuid.uuid4()}"
    
    if "session_id" not in st.session_state:
        st.session_state.session_id = None
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "client" not in st.session_state:
        st.session_state.client = None

def send_message_with_streaming(client: CloudRunADKClient, message: str, app_name: str, thinking_placeholder):
    """Send message using streaming with thinking indicator"""
    
    # Get user and session IDs
    user_id = st.session_state.user_id
    session_id = st.session_state.session_id or f"temp-session-{int(time.time())}"
    
    # Show initial thinking indicator
    with thinking_placeholder.container():
        with st.chat_message("assistant"):
            with st.spinner("🤖 Agent is thinking..."):
                time.sleep(0.5)  # Show spinner for a moment
    
    # Try SSE endpoint first for streaming, then fallback to regular endpoints
    endpoints_to_try = [
        ("POST /run_sse", lambda: client.send_message_run_sse(message, user_id, session_id, app_name), True),
        ("POST /run", lambda: client.send_message_run_endpoint(message, user_id, session_id, app_name), False),
        ("/chat", lambda: client.send_message_simple(message, user_id), False),
        ("root /", lambda: client.send_message_direct(message, user_id), False)
    ]
    
    for endpoint_name, endpoint_func, is_streaming in endpoints_to_try:
        try:
            # Update thinking indicator for current endpoint
            with thinking_placeholder.container():
                with st.chat_message("assistant"):
                    # st.write(f"🔄 Trying {endpoint_name}...")
                    with st.spinner("Agent Thinking..."):
                        response = endpoint_func()
            
            if response.get("success"):
                # Clear thinking indicator
                thinking_placeholder.empty()
                
                # Process response
                processed = client.process_response(response["response"])
                
                # Create assistant message
                assistant_content = processed['final_text'] or "Task completed."
                
                # Add tool information if available
                if processed['tool_calls']:
                    tool_info = f"\n\n**Tools used:** {', '.join([call['name'] for call in processed['tool_calls']])}"
                    assistant_content += tool_info
                
                # Add assistant response to chat
                assistant_message = {
                    "role": "assistant",
                    "content": assistant_content,
                    "timestamp": time.strftime("%H:%M:%S"),
                    "tool_calls": processed['tool_calls'],
                    "tool_responses": processed['tool_responses'],
                    "events": processed['events'],
                    "endpoint_used": endpoint_name,
                    "raw_response": processed['raw_response'],
                    "status": processed['status']
                }
                
                st.session_state.messages.append(assistant_message)
                
                # Display the response with streaming effect
                display_streaming_response(assistant_message)
                
                return True
                
        except Exception as e:
            # Show error in thinking placeholder briefly
            with thinking_placeholder.container():
                with st.chat_message("assistant"):
                    st.error(f"❌ {endpoint_name} failed: {str(e)}")
                    time.sleep(1)  # Brief delay to show error
            continue
    
    # If all endpoints failed
    thinking_placeholder.empty()
    error_msg = "All endpoints failed. Please check your configuration and try again."
    st.session_state.messages.append({
        "role": "assistant",
        "content": error_msg,
        "timestamp": time.strftime("%H:%M:%S"),
        "status": "error"
    })
    
    # Display error message
    with st.chat_message("assistant"):
        st.error(error_msg)
        st.caption(f"🕒 {time.strftime('%H:%M:%S')}")
    
    return False

def display_streaming_response(message):
    """Display response with streaming effect"""
    with st.chat_message("assistant"):
        # Show initial processing indicator
        response_container = st.empty()
        
        with response_container.container():
            st.write("💭 Processing response...")
            time.sleep(1)
        
        content = message["content"]
        
        # If content is short, show it all at once
        if len(content) < 100:
            response_container.markdown(content)
        else:
            # Stream the text word by word for longer content
            words = content.split()
            displayed_text = ""
            
            for i, word in enumerate(words):
                displayed_text += word + " "
                
                # Update every few words for better performance
                if i % 3 == 0 or i == len(words) - 1:
                    response_container.markdown(displayed_text + "▌")  # Show cursor
                    time.sleep(0.08)  # Adjust speed as needed
            
            # Final display without cursor
            response_container.markdown(content)
        
        # Show timestamp and endpoint info
        caption_parts = [f"🕒 {message['timestamp']}"]
        if message.get("endpoint_used"):
            caption_parts.append(f"📡 {message['endpoint_used']}")
        st.caption(" | ".join(caption_parts))
        
        # Show tool details if available
        if (message.get("tool_calls") and len(message["tool_calls"]) > 0):
            with st.expander(f"🔧 Tool Details ({len(message['tool_calls'])} calls)"):
                for j, tool_call in enumerate(message["tool_calls"]):
                    st.write(f"**Call {j+1}:** {tool_call['name']}")
                    if tool_call.get('args'):
                        st.json(tool_call['args'])
                
                if message.get("tool_responses"):
                    st.write("**Responses:**")
                    for j, tool_response in enumerate(message["tool_responses"]):
                        st.write(f"**Response {j+1}:** {tool_response['name']}")
                        if tool_response.get('response'):
                            st.json(tool_response['response'])
        
        # Show raw response for debugging
        if (message.get("raw_response") and st.session_state.get("show_debug", False)):
            with st.expander("🐛 Debug: Raw Response"):
                st.json(message["raw_response"])

def main():
    """Main application function"""
    
    initialize_session_state()
    
    # Sidebar for configuration
    with st.sidebar:
        st.title(":robot: Cloud Run Agent")

        # Configuration form
        with st.form("config_form"):
            st.subheader("Service Configuration")
            
            service_url = st.text_input(
                "Cloud Run Service URL",
                value=st.session_state.get("service_url", ""),
                help="Your Cloud Run service URL (e.g., https://your-service-123abc-uc.a.run.app)",
                placeholder="https://your-service-123abc-uc.a.run.app"
            )
            
            app_name = st.text_input(
                "App Name",
                value=st.session_state.get("app_name", ""),
                help="Name of your ADK agent application deployed",
                placeholder="Your App Name"
            )
            
            
            submitted = st.form_submit_button("💾 Save Configuration")
            
            if submitted and service_url:
                try:
                    st.session_state.client = CloudRunADKClient(
                        service_url=service_url
                    )
                    st.session_state.service_url = service_url
                    st.session_state.app_name = app_name
                    st.success("✅ Configuration saved!")
                except Exception as e:
                    st.error(f"❌ Configuration failed: {str(e)}")
        
        st.divider()
        
        # Session management
        if st.session_state.client:
            st.subheader("Session Management")
            
            if st.session_state.session_id:
                st.success("🟢 Session Active")
                st.caption(f"Session: {st.session_state.session_id}")
                
                if st.button("🔄 New Session"):
                    result = st.session_state.client.create_session(
                        st.session_state.user_id, 
                        st.session_state.get("app_name", "agent")
                    )
                    if result.get("success"):
                        st.session_state.session_id = result["session_id"]
                        st.session_state.messages = []
                        st.rerun()
                    else:
                        st.error(f"Failed to create session: {result.get('error')}")
            else:
                st.warning("🔴 No Active Session")
                
                if st.button("➕ Create Session"):
                    result = st.session_state.client.create_session(
                        st.session_state.user_id, 
                        st.session_state.get("app_name", "agent")
                    )
                    if result.get("success"):
                        st.session_state.session_id = result["session_id"]
                        st.rerun()
                    else:
                        st.error(f"Failed to create session: {result.get('error')}")
                
                st.info("💡 You can chat without a session too")
        
        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = []
            st.rerun()
        
        st.divider()
        
        # Session info
        st.subheader("Session Info")
        st.caption(f"User ID: {st.session_state.user_id}")
        st.caption(f"Messages: {len(st.session_state.messages)}")
        if st.session_state.get("service_url"):
            st.caption(f"Service: {st.session_state.service_url}")
    
    # Main chat interface
    st.title(":robot: Cloud Run Agent Chat")

    # Check if client is configured
    if not st.session_state.client:
        st.info("👈 Please configure your Cloud Run service URL in the sidebar to get started.")
        return
    
    # Display chat messages (excluding the last assistant message if it will be streamed)
    messages_to_display = st.session_state.messages.copy()
    
    for message in messages_to_display:
        if message["role"] == "user":
            with st.chat_message("user"):
                st.markdown(message["content"])
                st.caption(f"🕒 {message['timestamp']}")
        elif message["role"] == "assistant":
            with st.chat_message("assistant"):
                st.markdown(message["content"])
                
                # Show timestamp and endpoint info
                caption_parts = [f"🕒 {message['timestamp']}"]
                if message.get("endpoint_used"):
                    caption_parts.append(f"📡 {message['endpoint_used']}")
                st.caption(" | ".join(caption_parts))
                
                # Show tool details for assistant messages
                if (message.get("tool_calls") and len(message["tool_calls"]) > 0):
                    with st.expander(f"🔧 Tool Details ({len(message['tool_calls'])} calls)"):
                        for j, tool_call in enumerate(message["tool_calls"]):
                            st.write(f"**Call {j+1}:** {tool_call['name']}")
                            if tool_call.get('args'):
                                st.json(tool_call['args'])
                        
                        if message.get("tool_responses"):
                            st.write("**Responses:**")
                            for j, tool_response in enumerate(message["tool_responses"]):
                                st.write(f"**Response {j+1}:** {tool_response['name']}")
                                if tool_response.get('response'):
                                    st.json(tool_response['response'])
                
                # Show raw response for debugging
                if (message.get("raw_response") and st.session_state.get("show_debug", False)):
                    with st.expander("🐛 Debug: Raw Response"):
                        st.json(message["raw_response"])
    
    # Debug toggle
    if st.session_state.messages:
        st.session_state.show_debug = st.checkbox("Show debug info", value=False)
    
    # Chat input
    if user_input := st.chat_input("Type your message here..."):
        # Add user message to chat immediately
        st.session_state.messages.append({
            "role": "user", 
            "content": user_input,
            "timestamp": time.strftime("%H:%M:%S")
        })
        
        # Display user message immediately
        with st.chat_message("user"):
            st.markdown(user_input)
            st.caption(f"🕒 {time.strftime('%H:%M:%S')}")
        
        # Create placeholder for thinking indicator
        thinking_placeholder = st.empty()
        
        # Send message with streaming
        send_message_with_streaming(
            st.session_state.client, 
            user_input, 
            st.session_state.get("app_name", "agent"),
            thinking_placeholder
        )
        
        st.rerun()

if __name__ == "__main__":
    main()