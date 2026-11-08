from langchain_ollama import ChatOllama

# Local model served by Ollama (http://localhost:11434). See `ollama list` for options.
# reasoning=False turns off qwen's "thinking" step, which is slow on a laptop.
llm = ChatOllama(model="qwen3.5:4b", temperature=0, reasoning=False)


if __name__ == "__main__":
    response = llm.invoke("Say hello in one sentence.what is the day to day and time in uganda")
    print(response.content)
