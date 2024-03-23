import boto3
from botocore.exceptions import ClientError
import json
import logging


# list foundation models for Anthropic
#aws bedrock list-foundation-models \
#    --by-provider anthropic \
#    --query "modelSummaries[*].modelId"
bedrock = boto3.client("bedrock")
response = bedrock.list_foundation_models(
    byProvider='anthropic'
)

print(response)

# get input and output token counts
# reference: https://github.com/langchain-ai/langchain/issues/18514#issuecomment-1978606147
bedrock_runtime = boto3.client("bedrock-runtime")

message = "\n\nHuman: Who are you?\n\nAssistant:"

bedrock = boto3.client(service_name="bedrock-runtime")
body = json.dumps({
    "max_tokens": 256,
    "messages": [{"role": "user", "content": message}],
    "anthropic_version": "bedrock-2023-05-31"
})

response = bedrock.invoke_model(body=body, modelId="anthropic.claude-3-sonnet-20240229-v1:0")

response_body = json.loads(response.get("body").read())
content = response_body.get("content")

input_token_count = response["ResponseMetadata"]["HTTPHeaders"][
    "x-amzn-bedrock-input-token-count"
]

output_token_count = response["ResponseMetadata"]["HTTPHeaders"][
    "x-amzn-bedrock-output-token-count"
]

print(content, input_token_count, output_token_count, sep="\n")

