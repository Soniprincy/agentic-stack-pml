import time
import ollama
import sys
import httpx
import argparse

#---------------------------------------------------------------------------------

# def main():
#     question = sys.argv[1] if len(sys.argv) > 1 else "Hello"

#     start = time.time()
#     response = ollama.chat(
#         model="qwen3:4b",
#         messages=[{"role": "user", "content": question}],
#     )
#     elapsed = time.time() - start

#     print(response["message"]["content"])
#     print(f"\n[model: qwen3:4b | time: {elapsed:.2f}s]")

# ---------------------------------------------------------------------------------

# def main():
#     question = sys.argv[1] if len(sys.argv) > 1 else "Hello"

#     start = time.time()
#     response = httpx.post(
#         "http://localhost:11434/api/chat",
#         json={
#             "model": "qwen3:4b",
#             "messages": [{"role": "user", "content": question}],
#             "stream": False,  # output in batch or not
#         },
#         timeout=None, # before 120, then 300 but sometimes doesn't execute fast
#     )
#     elapsed = time.time() - start

#     print(response.json()["message"]["content"])
#     print(f"\n[model: qwen3:4b | time: {elapsed:.2f}s]")

#---------------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("question")
    parser.add_argument("--model", default="qwen2.5:3b")
    args = parser.parse_args()

    start = time.time()
    response = httpx.post(
        "http://localhost:11434/api/chat",
        json={
            "model": args.model,
            "messages": [{"role": "user", "content": args.question}],
            "stream": False,
        },
        timeout=None, # before 120, then 300 but sometimes break
    )
    elapsed = time.time() - start

    print(response.json()["message"]["content"])
    print(f"\n[model: {args.model} | time: {elapsed:.2f}s]")

#--------------------------------------------------------------------------------

if __name__ == "__main__":
    main()