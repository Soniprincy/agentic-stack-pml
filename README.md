# agentic-stack-pml
-----------------------------------------------------------------------------------------------------

############### part 1 ###########################
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

