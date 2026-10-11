import json
from datetime import datetime
from pathlib import Path
import streamlit as st
from gemma_client import GemmaClient

st.set_page_config(page_title="PlantCare Adventure AI", page_icon="🌿", layout="centered")
st.title("🌿 PlantCare Adventure AI")
st.caption("AI gives you a small mission. The real adventure happens away from the screen.")

MISSIONS = {
    "Nature walk": ("Leaf detective", "Walk slowly for five minutes. Find three leaves that differ in shape or texture without picking them.", ["leaf shapes", "textures", "different shades of green"]),
    "Plant care": ("Plant check-up", "Observe one safe outdoor plant. Look at its newest leaf, soil surface, sunlight, and visible signs of stress.", ["new growth", "soil surface", "sunlight", "spots or insects"]),
    "Photography": ("One-detail challenge", "Find one plant detail worth photographing. Observe it for one full minute before using the camera.", ["tiny patterns", "light and shadow", "texture"]),
    "Quiet time": ("Sit and notice", "Sit near a plant for five minutes. Notice sound, movement, light, and one detail you normally overlook.", ["movement", "sound", "light", "one overlooked detail"]),
}

def make_prompt(activity, location, preference):
    return f"""Create a short, safe 3-10 minute outdoor observation mission.
Activity: {activity}
Environment: {location or 'not provided'}
Preference: {preference or 'not provided'}
Return only JSON with keys: title, mission, look_for (array of 3-5 short strings), safety_note.
Avoid asking users to pick/eat unknown plants or enter unsafe/private places. Keep instructions concise and encourage putting the phone away."""

def parse_json(text):
    text=text.strip().replace("```json","").replace("```","").strip()
    start,end=text.find("{"),text.rfind("}")
    if start<0 or end<0: raise ValueError("Gemma response did not contain JSON")
    return json.loads(text[start:end+1])

def fallback(activity):
    title, mission, look_for = MISSIONS[activity]
    return {"title":title,"mission":mission,"look_for":look_for,"safety_note":"Observe only. Do not pick or eat unknown plants; avoid unsafe areas and respect private property."}

def save_journal(entry):
    p=Path("data"); p.mkdir(exist_ok=True); file=p/"journal.json"
    entries=[]
    if file.exists():
        try: entries=json.loads(file.read_text(encoding="utf-8"))
        except (ValueError,OSError): entries=[]
    entries.append(entry)
    file.write_text(json.dumps(entries[-30:],indent=2,ensure_ascii=False),encoding="utf-8")

with st.sidebar:
    st.header("Mission preferences")
    activity=st.selectbox("Outdoor activity",list(MISSIONS))
    location=st.text_input("Environment (optional)",placeholder="garden, park, campus…")
    preference=st.text_input("Preference (optional)",placeholder="easy, quiet, 5 minutes…")
    use_gemma=st.checkbox("Try Gemma if configured",value=True)

if "mission" not in st.session_state:
    st.session_state.mission=None

if st.button("🌱 Generate my outdoor mission",use_container_width=True):
    mission=None
    client=GemmaClient()
    if use_gemma and client.is_configured:
        try:
            mission=parse_json(client.chat(make_prompt(activity,location,preference)))
        except Exception as exc:
            st.warning(f"Gemma was unavailable; using the built-in fallback. Details: {exc}")
    st.session_state.mission=mission or fallback(activity)

mission=st.session_state.mission
if mission:
    st.divider()
    st.success("Mission ready")
    st.header(mission.get("title","Outdoor mission"))
    st.write(mission.get("mission",""))
    st.subheader("👀 Things to look for")
    for i,item in enumerate(mission.get("look_for",[])):
        st.checkbox(item,key=f"mission_{i}_{item}")
    st.warning("📵 Put your phone away now. Come back when you are finished.")
    st.caption(mission.get("safety_note","Observe safely and do not damage plants."))
    note=st.text_area("📝 What did you notice?",placeholder="Write a short observation after you return.")
    photo=st.file_uploader("Optional photo",type=["jpg","jpeg","png","webp"])
    if st.button("📖 Create Plant Adventure Journal",use_container_width=True):
        entry={"created_at":datetime.now().isoformat(timespec="seconds"),"mission":mission,"observation":note.strip(),"photo_name":photo.name if photo else None}
        save_journal(entry)
        st.success("Journal entry saved to data/journal.json.")
        st.markdown("### 🌳 Latest journal")
        st.write("**Mission:** "+mission.get("title","Outdoor mission"))
        st.write("**Observation:** "+(note.strip() or "No note added."))
else:
    st.info("Choose an activity and generate a mission. Then take the smallest possible step: go outside.")
