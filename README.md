# agentic-stack-pml
-----------------------------------------------------------------------------------------------------

######################## part 1 ###########################

-----------------------------------------------------------------------------------------------------
#cloning github
-----------------------------------------------------------------------------------------------------
git clone https://github.com/Soniprincy/agentic-stack-pml.git

-----------------------------------------------------------------------------------------------------
#setting environment
------------------------------------------------------------------------------------------------------
irm https://astral.sh/uv/install.ps1|iex

uv init matscout 

cd matscout

uv run crawl4ai-setup

uv run crawl4ai-doctor

-------------------------------------------------------------------------------------------------------
#running ollama model
-------------------------------------------------------------------------------------------------------

uv run ollama pull qwen3:8b

uv run ollama run qwen3:8b "say hello" #this is a big model that my pc take too much time to respond so i tried smaller model

uv run ollama pull qwen3:4b

uv run ollama run qwen3:4b "say hello"

############################ Part 2 ##################################

------------------------------------------------------------------------------------------------------
created ask.py file inside src/matscout
------------------------------------------------------------------------------------------------------

uv run python -m matscout.ask "what is carbon fibre"   -- for code executed my llama library

uv run python -m matscout.ask "what is carbon fibre"   -- for code executed by api

uv run python -m matscout.ask "what is carbon fibre" --model qwen2.5:3b # i tried 7b and 8b model but they are taking lots of time, sometimes not working.

uv run python -m matscout.ask "what is carbon fibre" --model qwen3:4b  

ollama list # it shows qwen3:4b, qwen3:8b, qwen2.5:3 models

############################ Part 3 ##################################

------------------------------------------------------------------------------------------------------
created model.py file to keep material base model

created extract.py file 

------------------------------------------------------------------------------------------------------

 uv run python -m matscout.extract

 ########################### Part 4 ##################################

 ------------------------------------------------------------------------------------------------------
 created crawl.py for crawl model
 
 created compare.py to compare raw vs transformed data
 
 -------------------------------------------------------------------------------------------------------

 uv run python -m matscout.crawl

 uv run python -m matscout.compare

 ######################### Part 5 #####################################

 ------------------------------------------------------------------------------------------------------

 create pipeline.py

 create test_pipeline.py

 uv run python matscout.pipeline https://en.wikipedia.org/wiki/Titanium

 uv run python -m matscout.test_pipeline

 ######################### Part 6 #####################################

 -------------------------------------------------------------------------------------------------------

 create a file ghaph_pipeline.py

 create a file test_retry.py

 uv run python -m matscout.test_retry

 uv run python -m matscout.graph_pipeline https://en.wikipedia.org/wiki/Titanium

########################### Part 7 #####################################

---------------------------------------------------------------------------------------------------------

pip install fastapi uvicorn

pip install requests

uv sync

uv add crawl4ai

uv run crawl4ai-setup

uv run crawl4ai-doctor

uv run python server.py  # 1st terminal

uv run python client.py  # 2nd terminal

after extension:

uv run python server.py

uv run python extractor_server.py

uv run python client.py

######################### Part 8 #####################################

uv run python extractor_server.pu

uv run python server.py

uv run uvicorn main:app --reload --port 8000             # then open http://127.0.0.1:8000


