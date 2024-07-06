### Amazon Bedrock Development Workshop

Conversational Chatbot lab: https://catalog.us-east-1.prod.workshops.aws/workshops/0b6e72fe-77ee-4777-98cc-237eec795fdb/en-US/fm/06-chatbot

Installation instructions:

1. Create a bucket with name: bedrock-workshop-${AWS::AccountId}-${AWS::Region}.

2. Create a Lambda function with latest Python runtime and name: BedrockWorkshopChatbot.
- Navigate to Configuration > General Configuration.
- Set max values for timeout (15 min.), memory (10240 MB), and ephemeral storage (10240 MB).
- Navigate to Configuration > Permissions.
- Navigate to Lambda function exeuction role.
- Add a custom inline policy to the Lambda fucntion execution role with policy name: AmazonBedrockWorkshopStackLambdaFunctionPolicy.

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

3. Change working directory to: bedrock-workshop-chatbot.

4. Follow the deployment instructions in "The Deployment Package" and "Deployment" sections.

5. Create an API Gateway API with name: BedrockWorkshopChatbot and stage: demo.
- Create an `ANY` method of Lambda function type with Lambda proxy integration set to `True`.
- Set Lambda function to the ARN for BedrockWorkshopChatbot Lambda function.
- Deploy the API with a new `demo` stage.

6. Follow the test instructions in the "Deployment" section.
