import streamlit as st
from langgraph_backend_sqlite import workflow, get_all_threads
from langchain_core.messages import BaseMessage,HumanMessage
import uuid

# *****************************************utilitty functions ***********************

def generate_thread_id():
    thread_id = uuid.uuid4()
    return thread_id

def reset_chat():
    if st.session_state['message_history']:
        thread_id = generate_thread_id()
        st.session_state['thread_id'] = thread_id
        add_threads(thread_id)
        st.session_state['message_history'] = []
    
    
def load_conversation(thread_id):
    #  
    message = workflow.get_state(config={'configurable':{'thread_id':thread_id}}).values
    print(workflow.get_state(config={'configurable':{'thread_id':thread_id}}).values)
    print("--------------------")
    if message:
        return workflow.get_state(config={'configurable':{'thread_id':thread_id}}).values['message']
    else:
        return {}

# ****************************************session setup ***************************

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []
    
    
if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()
    
if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = get_all_threads()
    
def add_threads(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)
  
# add thread id intially when the chat start , first chat.      
add_threads(st.session_state['thread_id'])

# ***************************************sidebar UI *******************************
st.sidebar.title('Langgraph chatbot')

if st.sidebar.button('New Chat'):
    if load_conversation(st.session_state['chat_threads'][-1]):
        
        reset_chat()
    st.session_state['thread_id'] = st.session_state['chat_threads'][-1]
    st.session_state['message_history'] = []
    
    
    
st.sidebar.header('My Conversation history')

#  to show all thread_ids or chats

for thread in st.session_state['chat_threads'][::-1]:
    if st.sidebar.button(str(thread)):
    # if st.session_state['message_history']:
        
        st.session_state['thread_id'] = thread
        messages = load_conversation(thread)
        
        temp_messages = []
        
        for message in messages:
            if isinstance(message,HumanMessage):
                role = 'user'
            else:
                role = 'assistant'
                
            temp_messages.append({'role':role,'content':message.content})
        
        st.session_state['message_history'] = temp_messages
                


# ************************************

for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

prompt = st.chat_input('say something')

if prompt:
    with st.chat_message('user'):
        st.text(prompt)
    st.session_state['message_history'].append({'role':'user','content':prompt})


    with st.chat_message('assistant'):
        # here we pass our generator ,st.write_stream is generator which is used for streaming
        ai_message = st.write_stream(
            message_chunk.content for message_chunk ,metadata in  workflow.stream({'message':[HumanMessage(content=prompt)]},config={'configurable':{'thread_id':st.session_state['thread_id']}},stream_mode='messages')
        )
        
        
    st.session_state['message_history'].append({'role':'assistant','content':ai_message})
    # st.session_state['message_history'].append({'role':'assistant','content':response['message'][-1].content})
    