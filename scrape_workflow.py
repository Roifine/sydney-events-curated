import streamlit as st
from datetime import datetime
import json
from dateutil import parser
import os

# --- Load Events from JSON Files ---
def load_events_with_category(file_category_map):
    all_events = []
    for filename, category in file_category_map.items():
        if not os.path.exists(filename):
            continue
        with open(filename, "r", encoding="utf-8") as f:
            try:
                events = json.load(f)
                for event in events:
                    title = event.get("event title", "").strip()
                    link = event.get("event link", "").strip()
                    if not title or not link:
                        continue

                    # Parse date or mark as 'Various'
                    raw_date = event.get("event time", "").strip()
                    try:
                        date_obj = parser.parse(raw_date, fuzzy=True)
                        date_str = date_obj.strftime("%Y-%m-%d")
                        valid_date = True
                    except Exception:
                        date_str = "Various"
                        valid_date = False

                    # Handle location
                    location = event.get("event location", "").strip()
                    if not location or location.lower() in ["unknown", ""]:
                        location = "Various"

                    description = event.get("event description", "No description provided").strip()

                    all_events.append({
                        "title": title,
                        "category": category,
                        "description": description,
                        "date": date_str,
                        "valid_date": valid_date,
                        "link": link,
                        "location": location
                    })
            except Exception as e:
                print(f"⚠️ Error loading {filename}: {e}")
    return all_events

# --- File → Category mapping ---
file_category_map = {
    "events_broadsheet.json": "General",
    "events_enmore.json": "Music",
    "events_golden.json": "Music",
    "events_film_fest.json": "Films"
}

EVENTS = load_events_with_category(file_category_map)

# --- UI Starts ---
st.set_page_config(page_title="Sydney Culture Radar", page_icon="🎉")
st.title("🎉 Sydney Culture Radar")

# Custom message block
st.markdown(
    """
    <div style="font-size: 1.15rem; line-height: 1.6; margin-bottom: 1.5rem; font-family: 'Helvetica Neue', sans-serif;">
    Roi and Therese created this curated list of events for you to check out. It includes <strong>films</strong>, <strong>music gigs</strong>, and other happenings we think you might like.  
    </div>
    """,
    unsafe_allow_html=True
)

# --- Filters ---
st.subheader("🎯 What are you into?")
selected_categories = st.multiselect(
    "Choose your category:",
    options=["General", "Music", "Films"],
    default=["General", "Music", "Films"]
)

# --- Filter and Show Events ---
if selected_categories:
    st.subheader("🎟️ Upcoming Events:")

    filtered_events = [
        e for e in EVENTS
        if e["category"] in selected_categories and (
            not e["valid_date"] or e["date"] > datetime.now().strftime("%Y-%m-%d")
        )
    ]
    filtered_events.sort(key=lambda x: x["date"] if x["valid_date"] else "9999-12-31")

    if filtered_events:
        for event in filtered_events:
            st.markdown(f"**{event['title']}** — _{event['category']}_")
            st.markdown(f"📅 {event['date']}")
            st.markdown(f"📍 {event['location']}")
            st.markdown(f"{event['description']}")
            st.markdown(f"[🔗 More Info]({event['link']})")
            st.markdown("---")
    else:
        st.info("No upcoming events match your selected filters.")
else:
    st.info("Please select at least one category to see events.")

# --- Feedback Section ---
st.markdown(
    """
    <div style="margin-top: 2rem;">
        <a href="https://docs.google.com/forms/d/e/1FAIpQLSfiAMnPRQjFI06EBROHbmkSR9LmFFFRmVSAuh7X3F4Dedz1GQ/viewform?usp=header" target="_blank" style="
            background-color: #FF4B4B;
            color: white;
            padding: 0.75rem 1.5rem;
            text-decoration: none;
            border-radius: 8px;
            font-weight: bold;
            font-size: 1rem;
            display: inline-block;
        ">💬 Give Feedback</a>
    </div>
    """,
    unsafe_allow_html=True
)
