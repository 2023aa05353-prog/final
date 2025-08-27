from setuptools import setup, find_packages

setup(
    name="verizon-assistant",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "langgraph-supervisor",
        "langchain",
        "langchain-google-genai",
        "langchain_community",
        "faiss-cpu",
        "sentence-transformers",
        "python-dotenv",
        "langgraph-cli",
        "langgraph-sdk"
    ],
)
