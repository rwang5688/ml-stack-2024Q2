import json
import boto3

model_id = 'meta.llama3-8b-instruct-v1:0'
bedrock = boto3.client(service_name='bedrock-runtime')

def lambda_handler(event, context):
    if (event['httpMethod'] == 'GET'):
        output = load_html()
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'text/html'},
            'body': output
        }
    elif (event['httpMethod'] == "POST"):
        body = json.loads(event['body'])
        messages = body['messages']
        print(messages)
        output = chat(messages)
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'text/html'},
            'body': output
        }
    else:
         return {
            'statusCode': 200,
            'headers': {'Content-Type': 'text/html'},
            'body': "OK"
        }

def load_html():
    html = ''
    with open('index.html', 'r') as file:
        html = file.read()
    return html

def chat(messages):
    inference_config = {'temperature': 1.0, 'topP': 1.0, 'maxTokens': 1024}
    response = bedrock.converse(
        modelId=model_id,
        messages=messages,
        inferenceConfig=inference_config
    )
    content = response['output']['message']['content']
    output = ''
    for item in content:
        output = output + item['text'] + '\n'
    return output
