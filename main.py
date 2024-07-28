import sys
import hyperdiv as hd
import requests
from ollama import Client
import time

"""
    Set the location for where ollama is running, default is based on default install
"""
ollama_url = 'http://localhost:11434'

# create an empty list to store all the models we have installed.
model_list = []

if requests.get(ollama_url).status_code == 200:
    client = Client(host=ollama_url)
    api_return = client.list()
    for model in api_return['models']:
        model_list.append(model['name'])
else:
    print("Ollama is not running")
    sys.exit(1)


"""
Ollama Chat
"""

def add_message(role, content, state, gpt_model):
    """
    Add a message to the state.

    Args:
        role (str): The role of the message (e.g., 'user', 'assistant').
        content (str): The content of the message.
        state (hd.state): The state object.
        gpt_model (str): The GPT model used for generating the message.
    """
    state.messages += (
        dict(role=role, content=content, id=state.message_id, gpt_model=gpt_model),
    )
    state.message_id += 1


def request(gpt_model, state , imessage):
    """
    Send a request to the Ollama chatbot API.

    Args:
        gpt_model (str): The GPT model to use for the request.
        state (hd.state): The state object.

    """
    #print(gpt_model,imessage,"A")
    response = client.chat(
        model=gpt_model,
        #messages=[dict(role=m["role"], content=m["content"]) for m in state.messages],
        messages=[imessage],
        stream=True,
    )

    for chunk in response:
        message = chunk['message']
        state.current_reply += message.get("content", "")
    add_message("assistant", state.current_reply, state, gpt_model)
    #print(state.current_reply,"B")
    state.current_reply = ""
    state.running = False



"""
Global configuration of bots

"""


bot1 = {'name': 'kimi', 
        'question': None,
        'answer' : None,
        'model':"llama",
        'talking':False
        }

bot2 = {'name': 'Fiona', 
        'question': None,
        'answer' : None,
        'model':"Yi",
        'talking':False
        }

bots = []
bots.append(bot1)
bots.append(bot2)

def config(state):
     with hd.box(
         gap=1,
         padding=1,
         border="2px solid gray-50",
         max_width = 20
     ):
         # Agent 1
         bots[0]['name'] = hd.text_input("Agent 1 name: ", placeholder="name").value
         bots[0]['model'] = hd.select(options=model_list, placeholder="Choose model:").value 

         # Agent 2
         bots[1]['name'] = hd.text_input("Agent 2 name: ", placeholder="name").value
         bots[1]['model'] = hd.select( options=model_list, placeholder="Choose model:").value
         state.topics = hd.text_input("Topic: ", placeholder="topic").value 





def renderhistory(state):
    for e in reversed(state.messages):
        name = bots[e['id']%2]['name']
        if(e['id']%2==0):position = 'end'
        if(e['id']%2==1):position = 'start'
        with hd.scope(e['id']):
            with hd.box(align=position, wrap = 'wrap',padding=(0, 0, 0, 0) ):
                hd.icon('person',font_size=2)
                with hd.box(
                    padding=1,
                    gap=1,
                    border="1px solid neutral-100",
                    background_color="neutral-50",
                    border_radius="large",
                    max_width=20,
                ):
                    hd.markdown(f"### {name}:{e['gpt_model']}")
                    hd.markdown("Answer:  ")
                    hd.markdown(e['content'],white_space = "normal")


def AIsay(name,answer,model,ibot,stateLLM,task):
    '''
        Render AI model and message to webpage
    '''
    if (ibot != stateLLM.irun ):
        return

    task = hd.task()

    if(ibot ==0):
        position = 'end'
    if(ibot ==1):
        position = "start"

    with hd.box(align=position, wrap = 'wrap',padding=(0, 0, 0, 0) ):
        hd.icon('person',font_size=2)
        with hd.box(
            padding=1,
            gap=1,
            border="1px solid neutral-100",
            background_color="neutral-50",
            border_radius="large",
            max_width=20,
        ):
            if (bots[ibot]['talking']==False ):
                bots[ibot]['talking'] =  True
                print("SSSSSSSSSSSSSSS",ibot,stateLLM.irun)
                prompt =  dict(role='user', content=bots[ibot]['question'])
                stateLLM.running = True
                task.rerun(request,bots[ibot]['model'],stateLLM,prompt)
            # Render history messages:

            if stateLLM.running:
                hd.markdown(f"### {name}:{model}")
                hd.markdown("Answer:  ")
                hd.markdown(stateLLM.current_reply,white_space = "normal")
            else:
                hd.markdown(stateLLM.messages[-1]['content'],white_space = "normal")

                bots[1-ibot]['question'] = stateLLM.messages[-1]['content']+"，言辞激烈反驳我，一段话，不超过30字）"
                bots[ibot]['talking'] =  False

                stateLLM.irun = 1-ibot


                #print(gpt_model,state.current_reply)
                #print(bots[0]['question'],"000",stateLLM.message_id)
                #print(bots[1]['question'],"111",stateLLM.message_id)


def main():
    # Config AI agents
    # Outer container that centers the title and inner container.
    template = hd.template(title="Ollama Basic Chatbot", sidebar=False)
    template.body.align = 'center'

    # Globale state
    # Clicked: chat begin
    # Topics: chat topic
    task = hd.task()
    state = hd.state(clicked=False,topics="")

    # State for LLM
    state_LLM = hd.state(messages=(), current_reply="", irun=0, running=False, message_id=0)

    with template.body:
        # Initialize
        #print(state.clicked,state.topics, state_LLM.messages, state_LLM.current_reply, state_LLM.message_id,state_LLM.running)
        if (not state.clicked):
            config(state)
            state.clicked = hd.button( "ssss",size='large').clicked
        # Chat
        else:
            #with hd.box(direction='vertical',gap=1.5, vertical_scroll=True):
            with hd.box(direction='vertical-reverse',gap=1.5, vertical_scroll=True):
                 if (state_LLM.message_id ==0):
                     bots[0]['question'] = state.topics+"，（讨论这个话题，一段话，不超过10字）"
                 AIsay(bots[0]['name'],bots[0]['answer'],bots[0]['model'],0,state_LLM,task)
                 AIsay(bots[1]['name'],bots[1]['answer'],bots[1]['model'],1,state_LLM,task)
                 renderhistory(state_LLM)

        with hd.box(direction='vertical-reverse',gap=1.5):
            hd.markdown("[Status]   " + "Current topic: " + state.topics)

if __name__ == "__main__":
    hd.run(main)
