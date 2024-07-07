### Bedrock Converse API: Amazon Bedrock Development Workshop - Conversational Chatbot

Lab content: https://catalog.us-east-1.prod.workshops.aws/workshops/0b6e72fe-77ee-4777-98cc-237eec795fdb/en-US/fm/06-chatbot

Deployment and Test instructions:

1. Create a deployment S3 bucket with name: `bedrock-workshop-${AWS::AccountId}-${AWS::Region}``.

2. Create and configure a Lambda function with latest Python runtime and name: `BedrockWorkshopChatbot`.

- Navigate to Configuration > General Configuration.
- Set max values for timeout (15 minutes), memory (10240 MB), and ephemeral storage (10240 MB).
- Navigate to Configuration > Permissions.
- Navigate to Lambda function exeuction role.
- Add the following custom inline policy to the Lambda fucntion execution role.
- Set policy name, e.g.: `AmazonBedrockWorkshopStackLambdaFunctionPolicy`.

```
{
	"Version": "2012-10-17",
	"Statement": [
		{
			"Action": [
				"bedrock:InvokeModel",
				"bedrock:InvokeModelWithResponseStream",
				"bedrock:ListFoundationModels"
			],
			"Resource": "*",
			"Effect": "Allow"
		},
		{
			"Action": [
				"aoss:APIAccessAll"
			],
			"Resource": "*",
			"Effect": "Allow"
		},
		{
			"Action": [
				"secretsmanager:GetSecretValue"
			],
			"Resource": "*",
			"Effect": "Allow"
		},
		{
			"Action": [
				"ec2:CreateNetworkInterface",
				"ec2:DeleteNetworkInterface",
				"ec2:DescribeNetworkInterfaces"
			],
			"Resource": "*",
			"Effect": "Allow"
		},
		{
			"Action": [
				"logs:CreateLogGroup",
				"logs:CreateLogStream",
				"logs:PutLogEvents"
			],
			"Resource": "*",
			"Effect": "Allow"
		}
	]
}
```

3. Create and configure an API Gateway API with name: `BedrockWorkshopChatbot` and stage: `demo`.

- Create an `ANY` method of Lambda function type.
- Set Lambda proxy integration to `True`.
- Set Lambda function to the ARN of the `BedrockWorkshopChatbot` Lambda function.
- Deploy the API with a new `demo` stage.
 
4. Change working directory to: `bedrock_workshop_chatbot`.

5. Execute deployment instructions in `The Deployment Package` and `Deployment` sections of the Conversational Chatbot lab: https://catalog.us-east-1.prod.workshops.aws/workshops/0b6e72fe-77ee-4777-98cc-237eec795fdb/en-US/fm/06-chatbot ...

6. Execute test instructions in the `Deployment` section.
