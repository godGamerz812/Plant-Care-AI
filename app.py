import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

import streamlit as st
from gemma_client import GemmaClient

st.set_page_config(page_title='PlantCare AI', page_icon='🌱', layout='centered')

MISSIONS = {
    'Plant care': {'title':'Plant check-up','mission':'Choose one outdoor plant. Inspect its newest leaf, soil surface, sunlight, and visible signs of stress. Do not pick or eat unknown plants.','look_for':['new growth','soil moisture','sunlight','spots or insects']},
    'Nature walk': {'title':'Leaf detective','mission':'Find three leaves that differ in shape or texture. Spend two minutes comparing them, then return to the app.','look_for':['leaf shape','leaf texture','different shades of green']},
    'Photography': {'title':'One-photo observation','mission':'Choose one plant detail worth photographing. Before taking the photo, observe it for one minute and notice a detail the camera might miss.','look_for':['tiny patterns','texture','light and shadow']},
    'Quiet time': {'title':'Sit and notice','mission':'Sit near an outdoor plant for five minutes. Notice movement, sound, light changes, and one detail you would normally overlook.','look_for':['movement','sound','light','one overlooked detail']}
}

def prompt_for(activity: str, context: str, preference: str) -> str:
    return f'''Create a short 3-10 minute outdoor plant observation mission.\nActivity: {activity}\nLocation/context: {context or 'not provided'}\nPreference: {preference or 'not provided'}\nReturn only JSON with keys: title, mission, look_for, safety_note.\nRules: practical, simple, no picking/eating/damaging plants, encourage the user to put the phone away, and do not claim exact identification from limited information.'''

def fallback(activity: str) -> Dict[str, Any]:
    d=MISSIONS[activity]
    return {'title':d['title'],'mission':d['mission'],'look_for':d['look_for'],'safety_note':'Observe without picking or eating unknown plants. Avoid unsafe areas and respect public/private spaces.'}

def parse_json(text: str) -> Dict[str, Any]:
    text=text.strip()
    if text.startswith('```'):
        text=text.replace('```json','',1).replace('```','',1).strip()
    start,end=text.find('{'),text.rfind('}')
    if start<0 or end<0: raise ValueError('Gemma did not return JSON.')
    return json.loads(text[start:end+1])

def save_entry(entry: Dict[str, Any]) -> None:
    p=Path('data'); p.mkdir(exist_ok=True); f=p/'journal.json'
    items=[]
    if f.exists():
        try: items=json.loads(f.read_text(encoding='utf-8'))
        except Exception: items=[]
    items.append(entry)
    f.write_text(json.dumps(items[-20:],indent=2,ensure_ascii=False),encoding='utf-8')

st.title('🌱 PlantCare AI')
st.caption('Get a small outdoor plant mission, then put your phone away.')
with st.sidebar:
    st.header('Mission setup')
    activity=st.selectbox('Outdoor moment',list(MISSIONS))
    context=st.text_input('Location / environment',placeholder='park, garden, campus…')
    preference=st.text_input('Preference',placeholder='5 minutes, easy, quiet…')
    use_gemma=st.checkbox('Use Gemma when configured',value=True)

client=GemmaClient()
if 'mission' not in st.session_state: st.session_state.mission=None
if st.button('🌿 Generate my mission',use_container_width=True):
    mission=None
    if use_gemma and client.is_configured:
        try: mission=parse_json(client.chat(prompt_for(activity,context,preference)))
        except Exception as exc: st.warning(f'Gemma could not be reached, so the local fallback was used. ({exc})')
    st.session_state.mission=mission or fallback(activity)

mission=st.session_state.mission
if mission:
    st.divider(); st.success('Mission ready'); st.header(mission.get('title','Outdoor mission')); st.write(mission.get('mission',''))
    st.subheader('👀 Look for')
    for item in mission.get('look_for',[]): st.checkbox(item,key='check_'+item)
    st.warning('📵 Put your phone away now. Come back when you are finished.')
    st.caption(mission.get('safety_note',''))
    note=st.text_area('📝 What did you notice?',placeholder='Write a short observation after you return.')
    photo=st.file_uploader('Optional photo',type=['jpg','jpeg','png','webp'])
    if st.button('📖 Create Plant Adventure Journal',use_container_width=True):
        save_entry({'created_at':datetime.now().isoformat(timespec='seconds'),'mission':mission,'observation':note.strip(),'photo_name':photo.name if photo else None})
        st.success('Journal entry saved.'); st.markdown('### 🌳 Latest journal'); st.write('**Mission:** '+mission.get('title','Outdoor mission')); st.write('**Observation:** '+(note.strip() or 'No note added.'))
else:
    st.info('Generate a mission and take the smallest possible step: go outside.')
