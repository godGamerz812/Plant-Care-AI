import streamlit as st

st.set_page_config(page_title="PlantCare Adventure AI", page_icon="🌿")

st.title("PlantCare Adventure AI")
st.write("Touch Grass: go outside, observe nature, and make an Adventure Journal.")

activity = st.selectbox("Choose an outdoor activity", ["Nature walk", "Plant care", "Photography", "Quiet time"])
location = st.text_input("Location / environment", placeholder="park, garden, campus...")
preference = st.text_input("Preference", placeholder="easy, quiet, 5 minutes...")

missions = {
    "Nature walk": "Walk slowly for 5 minutes and compare three leaves without touching them.",
    "Plant care": "Observe a safe plant: newest leaf, soil surface, sunlight, and visible signs of stress.",
    "Photography": "Find one plant detail and observe it for one minute before taking a photo.",
    "Quiet time": "Sit near a plant for 5 minutes with the phone away. Notice sound, movement, and light."
}

if st.button("Generate outdoor mission"):
    st.subheader("Mission")
    st.write(missions[activity])
    st.subheader("Things to look for")
    for x in ["leaf shapes", "textures", "light and shadow", "tiny movement", "a sound you normally ignore"]:
        st.checkbox(x)
    st.info("Put your phone away while you explore, then return here.")
    st.warning("Observe only. Do not pick, eat, or damage unknown plants.")
    st.text_area("Record an observation")
    st.file_uploader("Optional photo", type=["jpg","jpeg","png","webp"])
    st.success("After the walk, create your small Adventure Journal from your observation.")
else:
    st.info("Choose your outdoor activity, location/preferences, and generate a mission.")
