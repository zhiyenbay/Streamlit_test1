import streamlit as st
from langchain.llms import OpenAI

from openai import OpenAI
import json

from bokeh.models.widgets import Button
from bokeh.models import CustomJS

text = st.text_input("Say what ?")

tts_button = Button(label="Speak", width=100)

tts_button.js_on_event("button_click", CustomJS(code=f"""
    var u = new SpeechSynthesisUtterance();
    u.text = "{text}";
    u.lang = 'en-US';

    speechSynthesis.speak(u);
    """))

st.bokeh_chart(tts_button)

schema = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "Document",
    "type": "object",
    "properties": {
        "document": {
            "type": "object",
            "properties": {
                "falling_down_in_3_month": {"type": "string", "enum": ["Да", "Нет"],"description": "This field answers to the question if the patient has fallen recently or not"},
                "accompanying_illness":  {"type": "string", "enum": ["Да", "Нет"], "description": "are there any signs of concomitant diseasess"},
                "walking_difficulties": {"type": "string", "enum": ["ходит сам (даже если при помощи кого-то) или строгий постельный режим (неподвжино)", "Костыли/ходунки/трость", "Опирается о мебель или стены для поддержания"], "description":"This field answers to the question: does patient walk independently?"},
                "intravenous_drip": {"type": "string", "enum": ["Да", "Нет"], "description":"This field answers to the question: if the patient is taking intravenous infusion?" },
                "mobility":  {"type": "string", "enum": ["Нормально (ходи свободно)", "Слегка несвободная (ходит с остановками, шаги короткие, иногда с зарежкой)", "Нарушения (не может встать, ходит опираясь, смотрит вниз)"], "description": "Does the patient have walking problems?"},
                "psychology": {"type": "string", "enum": ["Осознает свою способность двигаться", "Не знает или забывает, что нужна помощь при движении"], "description" : "what is the patient's mental state?"},
              }
          },
    "required": ["document"]
    }
}


st.title('Quickstart App')

openai_api_key = st.sidebar.text_input('OpenAI API Key')

# def generate_response(input_text):
#   llm = OpenAI(temperature=0.7, openai_api_key=openai_api_key)
#   st.info(llm(input_text))

with st.form('my_form'):
  text = st.text_area('Enter text:', 'What are the three key pieces of advice for learning how to code?')
  prompt = "Map information to a valid  JSON output according to the provided JSON Schema. Information: " + text
  submitted = st.form_submit_button('Submit')
  
  if not openai_api_key.startswith('sk-'):
    st.warning('Please enter your OpenAI API key!', icon='⚠')
  if submitted and openai_api_key.startswith('sk-'):
    client = OpenAI(
      api_key = openai_api_key
    )
    chat_completion = client.chat.completions.create(
    model="gpt-3.5-turbo-1106",
    response_format={"type":"json_object"},
    messages=[
        {"role":"system","content":"Answer according to following Json Schema: "+ json.dumps(schema)},
        {"role":"user","content":prompt}
    ],
    temperature = 0
    )

    finish_reason = chat_completion.choices[0].finish_reason

    if(finish_reason == "stop"):
        data = chat_completion.choices[0].message.content
        st.info(data)

    else :
        st.info("Error! provide more tokens please")
