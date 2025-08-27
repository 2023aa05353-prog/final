from langgraph_sdk import get_sync_client

def test_assistant():
    client = get_sync_client(url="http://localhost:2024")
    
    # Test with a complex query that requires multiple agents
    query = "For customer Jane Doe (ID 74829), check if she can get the 'Pro' fiber plan, find the installation clause in the policy doc, and suggest a sales pitch based on her past interest in premium services."
    
    print("Sending query to assistant...")
    for chunk in client.runs.stream(
        None,  # Threadless run
        "agent",  # Name of assistant defined in langgraph.json
        input={
            "messages": [{
                "role": "human",
                "content": query,
            }],
        },
        stream_mode="messages-tuple",
    ):
        print(f"\nReceiving new event of type: {chunk.event}...")
        print(chunk.data)
        print("\n" + "-"*50)

if __name__ == "__main__":
    test_assistant()
