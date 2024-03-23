import boto3
from botocore.exceptions import ClientError
import json
import logging
import pprint


# bedrock: list foundation models for Anthropic
#aws bedrock list-foundation-models \
#    --by-provider anthropic \
#    --query "modelSummaries[*].modelId"
bedrock = boto3.client("bedrock")
response = bedrock.list_foundation_models(
    byProvider='anthropic'
)

# response is a Python dictionary
print ("response from bedrock.list_foundation_models() byProvider='anthropic'")
print ("==")
pprint.pprint (response)
print ("==")

# bedrock-runtime: invoke_model
# reference: https://github.com/langchain-ai/langchain/issues/18514#issuecomment-1978606147
bedrock_runtime = boto3.client("bedrock-runtime")

message = "\n\nHuman: Who are you?\n\nAssistant:"
body = json.dumps({
    "max_tokens": 256,
    "messages": [{"role": "user", "content": message}],
    "anthropic_version": "bedrock-2023-05-31"
})
model_id = "anthropic.claude-3-sonnet-20240229-v1:0"

response = bedrock_runtime.invoke_model(body=body, modelId=model_id)
response_body = json.loads(response.get("body").read())
content = response_body.get("content")

input_token_count = response["ResponseMetadata"]["HTTPHeaders"][
    "x-amzn-bedrock-input-token-count"
]

output_token_count = response["ResponseMetadata"]["HTTPHeaders"][
    "x-amzn-bedrock-output-token-count"
]

# response is a Python dictionary
print ("response from bedrock-runtime.invoke_model()")
print ("==")
pprint.pprint (response)
print ("==")

# response.body is a stream
print ("response_body")
print ("==")
print (json.dumps(response_body, indent=4))
print ("==")

# response.body.content is a Python dictionary
print ("content")
print ("==")
pprint.pprint (content)
print ("==")

# input and output token counts are strings; need to convert to ints
print ("input_token_count: %d" % int(input_token_count))
print ("output_token_count: %d" % int(output_token_count))

