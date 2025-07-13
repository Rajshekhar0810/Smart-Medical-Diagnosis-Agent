from config.config_loader import load_config
from langchain_openai import ChatOpenAI


def test_llm():
    config = load_config()

    if config['llm']['provider'].lower() == "openai":
        print("✅ LLM provider is OpenAI")
        
        # Load the LLM model
        llm = ChatOpenAI(
            model_name=config['llm']['model_name'],
            
        )
        
        # Create a simple prompt
        prompt = "What is the capital of France?"

        # Run the LLM
        response = llm.invoke(prompt)

        print("\n✅ Model Response:")
        print(response.content)
    else:
        print("⚠️ Only OpenAI provider is supported in this test.")

if __name__ == "__main__":
    test_llm()