# langchain-python-parsers

Demo of various custom parsers for the Python version of langchain

## Setup

```sh
pip install langchain
pip install openai
pip install python-dotenv
pip install fix-busted-json
```

Create a .env file with the following contents:

```ini
OPENAI_API_KEY="sk-xyz..."
```

Check installation

```sh
python hello_world.py
.
Hallo Welt!
```

NB. Need to use Python 3.8 or higher, so activate an appropriate virtual environment if necessary.

```sh
conda activate nnseries
```

## Custom Agent Chat

Using gpt-4, should output something like:

```sh
cd custom_agent_chat
python custom_agent_chat.py
.
I now know the final answer.
Final Answer: Here are 5 Test Engineer jobs in London:

1. ITS Testing Services (UK) Ltd - Test Engineer - Electrical Safety
   Location: SL7, Marlow, SL7 1LW
   Salary: Competitive salary and package

2. Harris Crawley - Instrument Test Engineer
   Location: London

3. Associate QA/Test Engineer - Shopper Technology
   Location: London

4. Portable Appliance Test Engineer
   Location: SW11, South West London, SW11 4NJ
   Salary: £21,750

5. Portable Appliance Test Engineer
   Location: Shadwell, E1 0hx
   Salary: £21,750
```

## Three Underscore Parser

```sh
cd ThreeUnderscoreParser
python agent_chat.py
```

## Json Parser

```sh
cd JsonParser
python agent_chat.py
```
