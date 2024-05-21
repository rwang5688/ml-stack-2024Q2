#!/bin/bash
export AWS_PROFILE="default"
export AWS_REGION="us-west-2"
export KENDRA_INDEX_ID="f3774bdc-92c7-4110-a0da-5d6410099213"
export FALCON_40B_ENDPOINT="jumpstart-dft-hf-llm-falcon-40b-instruct-bf16"
export LLAMA_2_ENDPOINT="jumpstart-dft-meta-textgeneration-llama-2-70b-f"

export OPENAI_API_KEY="<YOUR-OPEN-AI-API-KEY>"
export ANTHROPIC_API_KEY="<YOUR-ANTHROPIC-APIKEY>"

# Usage: streamlit run app.py <anthropic|openai|falcon40b|llama2|llama2_n|bedrock_titan|bedrock_claudev2|bedrock_claudev3_haiku|bedrock_claudev3_sonnet|bedrock_llama2_13b|bedrock_llama2_70b>
streamlit run app.py bedrock_llama2_70b --server.port 8080
