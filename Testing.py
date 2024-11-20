import streamlit as st
import google.generativeai as genai
from datetime import datetime, timedelta
import numpy as np

GOOGLE_API_KEY = "AIzaSyAJbE8Twn7MGQXcyvNfmJCGrewGFVt93NI"



genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

if "messages" not in st.session_state:
    st.session_state.messages = []
    
if "greeting_displayed" not in st.session_state:
    st.session_state.greeting_displayed = False

# Sample tracking data
sample_tracking_data = [
    {
        "tracking_number": "1Z999AA1234567890",
        "status": "In Transit",
        "location": "New York, NY",
        "gps": (40.730610, -73.935242),
        "weather": "Partly Cloudy",
        "eta": datetime.now() + timedelta(days=2),
        "last_updated": datetime.now() - timedelta(hours=2)
    },
    {
        "tracking_number": "1Z777BB0987654321",
        "status": "Delivered",
        "location": "Los Angeles, CA",
        "gps": (34.052235, -118.243683),
        "weather": "Sunny",
        "eta": datetime.now() - timedelta(days=1),
        "last_updated": datetime.now() - timedelta(minutes=30)
    },
    {
        "tracking_number": "1Z666CC5432109876",
        "status": "Out for Delivery",
        "location": "Chicago, IL",
        "gps": (41.878113, -87.629799),
        "weather": "Rainy",
        "eta": datetime.now() + timedelta(hours=6),
        "last_updated": datetime.now() - timedelta(minutes=15)
    },
    {
        "tracking_number": "1Z555DD4321098765",
        "status": "Delayed",
        "location": "Miami, FL",
        "gps": (25.761681, -80.191788),
        "weather": "Thunderstorms",
        "eta": datetime.now() + timedelta(days=3),
        "last_updated": datetime.now() - timedelta(hours=1)
    },
    {
        "tracking_number": "1Z444EE0987654321",
        "status": "Delivered",
        "location": "Seattle, WA",
        "gps": (47.606209, -122.332071),
        "weather": "Cloudy",
        "eta": datetime.now() - timedelta(days=2),
        "last_updated": datetime.now() - timedelta(days=2)
    }
]


def get_help_message():
    """Return an enhanced help message with available commands and features."""
    return """
    🤖 **Welcome to Your Smart Shipping Assistant!**
    
    I'm here to help you track and manage your shipments. Here's everything I can do for you:
    
    📦 **Tracking Commands**
    • Simply type a tracking number to get complete details
    • Example: "1Z999AA1234567890"
    
    🔍 **Specific Information Queries**
    1. **Track** - Get comprehensive tracking details
       • Command: `track <tracking_number>`
       • Example: "track 1Z999AA1234567890"
       • Returns: Full shipment status, location, weather, and ETA
    
    2. **Status** - Quick status check
       • Command: `status <tracking_number>`
       • Example: "status 1Z999AA1234567890"
       • Returns: Current shipment status
    
    3. **Location** - Real-time location tracking
       • Command: `location <tracking_number>`
       • Example: "location 1Z999AA1234567890"
       • Returns: Current location with GPS coordinates
    
    4. **Weather** - Weather conditions at package location
       • Command: `weather <tracking_number>`
       • Example: "weather 1Z999AA1234567890"
       • Returns: Current weather at package location
    
    5. **ETA** - Estimated delivery time
       • Command: `eta <tracking_number>`
       • Example: "eta 1Z999AA1234567890"
       • Returns: Expected delivery date and time
    
    📱 **Additional Features**
    • `samples` - View sample tracking numbers
    • `history` - View your recent tracking history
    • `clear` - Clear your chat history
    
    💡 **Pro Tips**
    • You can ask questions in natural language
    • Example: "Where is my package with tracking number 1Z999AA1234567890?"
    • Example: "What's the weather like where my package is?"
    • Example: "When will my shipment arrive?"
    
    🔔 **Notifications**
    • Use `notify <tracking_number>` to get alerts for:
      - Delivery status changes
      - Weather delays
      - Updated ETAs
    
    📊 **Tracking Multiple Packages**
    • Use `list` to see all your active trackings
    • Track multiple packages at once by separating tracking numbers with commas
    • Example: "track 1Z999AA1234567890, 1Z777BB0987654321"
    
    🌐 **Coverage Information**
    • Works with major carriers worldwide
    • Supports domestic and international shipments
    • Real-time updates where available
    
    ⚡ **Quick Commands**
    • `latest` - View your most recent tracking
    • `delayed` - Check for any delayed packages
    • `delivered` - List recently delivered packages
    
    Need more specific help? Just ask me anything about your shipments! 
    Remember, I'm here 24/7 to assist you with your tracking needs. 🚚✨
    """

# Update the process_message function to handle new commands
def process_message(message):
    """Process user message and return appropriate response."""
    message = message.lower().strip()
    
    # Help command
    if message == "help":
        return get_help_message()
    
    # New commands handler
    if message == "history":
        return "Here's your recent tracking history: [Would display recent tracking history]"
    
    if message == "clear":
        st.session_state.messages = []
        return "Chat history has been cleared!"
    
    if message == "list":
        return "Here are your active trackings: [Would display active trackings]"
    
    if message == "latest":
        return "Your most recent tracking: [Would display most recent tracking]"
    
    if message == "delayed":
        delayed_packages = [data for data in sample_tracking_data if data["status"] == "Delayed"]
        if delayed_packages:
            response = "📦 Delayed Packages:\n\n"
            for package in delayed_packages:
                response += f"• Tracking: {package['tracking_number']}\n"
                response += f"  Location: {package['location']}\n"
                response += f"  New ETA: {package['eta'].strftime('%B %d, %Y')}\n\n"
            return response
        return "No delayed packages found!"
    
    if message == "delivered":
        delivered_packages = [data for data in sample_tracking_data if data["status"] == "Delivered"]
        if delivered_packages:
            response = "✅ Recently Delivered Packages:\n\n"
            for package in delivered_packages:
                response += f"• Tracking: {package['tracking_number']}\n"
                response += f"  Location: {package['location']}\n"
                response += f"  Delivered: {package['last_updated'].strftime('%B %d, %Y')}\n\n"
            return response
        return "No recently delivered packages found!"
    
    if message.startswith("notify"):
        tracking_number = message.split("notify")[1].strip()
        return f"🔔 Notifications enabled for tracking number: {tracking_number}\nYou'll receive updates for status changes, delays, and ETA updates."
    """Process user message and return appropriate response."""
    message = message.lower().strip()
    
    # Help command
    if message == "help":
        return get_help_message()
    
    # Sample tracking numbers command
    if message == "samples":
        samples = "\n".join([f"- {data['tracking_number']}" for data in sample_tracking_data])
        return f"Here are some sample tracking numbers you can try:\n{samples}"
    
    # Check if message contains a tracking number
    for data in sample_tracking_data:
        if data["tracking_number"].lower() in message:
            tracking_data = data
            
            # Process specific commands
            if message.startswith("status"):
                return f"Status for {tracking_data['tracking_number']}: {tracking_data['status']}"
            
            elif message.startswith("location"):
                return f"Current location of {tracking_data['tracking_number']}: {tracking_data['location']}\nGPS: {tracking_data['gps']}"
            
            elif message.startswith("weather"):
                return f"Weather at package location ({tracking_data['location']}): {tracking_data['weather']}"
            
            elif message.startswith("eta"):
                return f"Estimated delivery time for {tracking_data['tracking_number']}: {tracking_data['eta'].strftime('%B %d, %Y at %I:%M %p')}"
            
            # Default to full tracking info
            return f"""
            📦 Tracking Information for {tracking_data['tracking_number']}:
            
            📍 Status: {tracking_data['status']}
            📍 Current Location: {tracking_data['location']}
            📍 GPS Coordinates: {tracking_data['gps']}
            🌤️ Weather: {tracking_data['weather']}
            🕒 Estimated Delivery: {tracking_data['eta'].strftime('%B %d, %Y at %I:%M %p')}
            ⏰ Last Updated: {tracking_data['last_updated'].strftime('%B %d, %Y at %I:%M %p')}
            """
    
    # If no tracking number found, use Gemini API for general conversation
    try:
        response = model.generate_content(message)
        return response.text
    except Exception as e:
        return "I'm sorry, I couldn't process your request. Please try again or type 'help' for available commands."

# Streamlit UI
st.title("🚚 Smart Shipment Assistant")

# Display initial greeting only once
if not st.session_state.greeting_displayed:
    initial_greeting = """
    👋 Hello! I'm your Smart Shipment Assistant. I can help you track packages, check delivery status, 
    and provide real-time updates on your shipments.
    
    Type 'help' to see what I can do for you!
    """
    st.session_state.messages.append({"role": "assistant", "content": initial_greeting})
    st.session_state.greeting_displayed = True

# Chat interface
if "messages" in st.session_state:
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"🧑 **You:** {message['content']}")
        else:
            st.markdown(f"🤖 **Assistant:** {message['content']}")

# Message input
message = st.chat_input("Type your message here...")

if message:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": message})
    
    # Get and add assistant response to chat history
    response = process_message(message)
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Rerun to update the chat display
    st.rerun()

# Sidebar with additional information
with st.sidebar:
    st.subheader("About")
    st.markdown("""
    This Smart Shipment Assistant helps you track packages and get real-time updates. 
    It uses advanced AI to understand your queries and provide accurate shipping information.
    
    **Quick Tips:**
    - Type 'help' to see available commands
    - Type 'samples' to see sample tracking numbers
    - You can ask questions in natural language
    """)
    
    # Add timestamp for last update
    st.markdown(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")