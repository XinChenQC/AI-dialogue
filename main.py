import sys
import hyperdiv as hd
import requests
from ollama import Client

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

print(model_list)



"""
Global configuration of bots

"""

bot1 = {'name': 'kimi', 
        'question': None,
        'answer' : "Sdfsdf:eeeeeeeeeeeeeeee  eeeeeeeeee  eee eeeeeeee  eeeeeeeeeee  eeeee eeeeee",
        'model':"llama"
        }

bot2 = {'name': 'Fiona', 
        'question': None,
        'answer' : None,
        'model':"Yi"
        }

bots = []
bots.append(bot1)
bots.append(bot2)



def config():
    with hd.hbox(
        gap=2,
        padding=1,
        justify="center" 
    ):
        # Agent 1
        with hd.box(
            gap=1,
            padding=1,
            border="2px solid gray-50"
        ):
            bots[0]['name'] = hd.text_input("Agent 1 name: ", placeholder="name").value
            bots[0]['model'] = hd.select(options=model_list, placeholder="Choose model:").value 

        # Agent 2
        with hd.box(
            gap=1,
            padding=1,
            border="2px solid gray-50"
        ):
            bots[1]['name'] = hd.text_input("Agent 2 name: ", placeholder="name").value
            bots[1]['model'] = hd.select( options=model_list, placeholder="Choose model:").value

def AIsay(name,answer,model,position):
    '''
        Render AI model and message to webpage
    '''

    with hd.box(align=position, wrap = 'wrap',padding=(0, 3, 1, 3) ):

        with hd.box(
            padding=1,
            gap=1,
            border="1px solid neutral-100",
            background_color="neutral-50",
            border_radius="large",
            max_width=30,
        ):
            hd.markdown(f"### {name}:{model}")
            hd.markdown("Answer:  ")
            hd.markdown(answer,white_space = "normal")



def main():
    # Config AI agents
    # Outer container that centers the title and inner container.
    config()

    AIsay(bots[0]['name'],bots[0]['answer'],bots[0]['model'],'end') 
    AIsay(bots[1]['name'],bots[1]['answer'],bots[1]['model'],'start') 

if __name__ == "__main__":
    hd.run(main)
