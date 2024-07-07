### Bedrock Agents API: Amazon Bedrock (Agents and Knowledge Base) Workshop - Higher Education

Workshop content: https://catalog.us-east-1.prod.workshops.aws/workshops/3008d94a-eaf7-477f-8b70-bc694f3589fc/en-US

Deployment and Test instructions:

1. Set up Bedrock

https://catalog.us-east-1.prod.workshops.aws/workshops/3008d94a-eaf7-477f-8b70-bc694f3589fc/en-US/01-getting-started/self-paced-lab/1-bedrock-setup

2. Download source code and set up SageMaker Studio Notebook

https://catalog.us-east-1.prod.workshops.aws/workshops/3008d94a-eaf7-477f-8b70-bc694f3589fc/en-US/01-getting-started/self-paced-lab/2-sagemaker-notebook-setup

Detailed Steps:

- Download source:
  - https://static.us-east-1.prod.workshops.aws/public/e54460c6-1688-421f-8800-4123d98f509a/static/workshop-labs.zip

- IGNORE CloudFormation template: `Code/workshop-stack.yaml`.
  - This template deploys a SageMaker Domain, and then adds SageMaker Studio Classic app.  We do not want this app.

- Deploy Cloudormation template: `Code/workshop-stack-s3-buckets.yaml`.
  - This template will create a bucket with name: `workshop-stack-s3-buckets-${AWS::AccountId}-bedrock-courses-cat`.
  - Plus this template will add three prefixes: `course-registration`, `course-reviews`, `knowledge-base`.

- Make sure SageMaker Execution Role has sufficient access for:
  - Amazon Bedrock (bedrock:*)
  - Amazon OpenSearch Service (aFoss:*)
  - Amazon SageMaker (AmazonSageMakerFullAccess)
  - Amazon S3 (AmazonS3FullAccess)
  - AWS CloudFormation (AWSCloudFormationFullAccess)
  - AWS IAM (IAMFullAccess)
  - AWS Lambda (AWSLambdaFullAccess)
- OR:
  - PowerUserAccess
  - AWS IAM (IAMFullAccess)

- Create, run, and open JupyterLab space, e.g., `bedrock-agents-and-kb-workshop`.

- Upload `bedrock_basics.ipynb`.

- Select cell: `Invoking Bedrock Agents`, and **Run All Above Selected Cell**.

- This confirms that we have the proper permissions to invoke Bedrock Agents API later.

3. Create Bedrock Knowledge Base for Course Catalog

https://catalog.us-east-1.prod.workshops.aws/workshops/3008d94a-eaf7-477f-8b70-bc694f3589fc/en-US/04-agents/1-knowledge-base/1-course-catalog

4. Create DynamoDB Tables for Course Reviews and Course Registrations

https://catalog.us-east-1.prod.workshops.aws/workshops/3008d94a-eaf7-477f-8b70-bc694f3589fc/en-US/04-agents/2-action-groups/1-create-db

5. Create Bedrock Agent; add Knowledge Base for Course Catalog and Course Review Action to Agent

https://catalog.us-east-1.prod.workshops.aws/workshops/3008d94a-eaf7-477f-8b70-bc694f3589fc/en-US/04-agents/2-action-groups/2-courses-review

Detailed Steps:

- When creating Course Review Action, make sure `Description` fields are NON-EMPTY for the Action Group and Lambda Function.  Or the creation may fail.

- When updating Lambda function code, we must upload a zip file.  Copy and paste code, and clicking **Deploy** will result in failure.

- It is easiest to zip up the Python file (`courses-agent-group-courses-review.py`) into a zip file (`courses-agent-group-courses-review.zip`), and then upload the zip file.

- Make sure to change the following:
  - Under Code: Change the Lambda handler to `courses-agent-group-courses-review.lambda_handler`.
  - Under Configuration > General Configuration: Change to max value timeout (15 minutes), memory (10240 MB), ephemeral storage (10240 MB).
  - Under Configuration > Permissions: Add to Lambda function execution role the custom inline policy:`dynamodb_lambda_permissions`.
  - In the `dynamodb_lambda_permissions` policy, make sure Resources statements have the correct ${AWS::AccountId}.
  - UNder Configuration > Permissions: Add to `agentInvokeFunction`, Source ARN: <Bedrock Agent ARN> and Action: `lambda:invokeFunction`.

- In order to trigger another **Prepare** cycle, go through another **Edit in Agent Builder** and **Save and exit** cycle.

- Prompt 2: `Show me reviews for CS 441 course` will fail to retrieve the course review because Lambda function will try to match `courseName` to `CS 441 Machine Learning`.

- Change Prompt 2 to: `Show me reviews for course CS 441`, and Course Review Agent will retrieve the appropriate course review.

6. Add Course Registration Action to Agent

https://catalog.us-east-1.prod.workshops.aws/workshops/3008d94a-eaf7-477f-8b70-bc694f3589fc/en-US/04-agents/2-action-groups/3-courses-registration

Detailed Steps:

- When updating Lambda function code, we must upload a zip file.  Copy and paste code, and clicking **Deploy** will result in failure.

- It is easiest to zip up the Python file (`courses-agent-group-courses-registration.py`) into a zip file (`courses-agent-group-courses-registration.zip`), and then upload the zip file.

- Make sure to change the following:
  - Under Code: Change the Lambda handler to `courses-agent-group-courses-registration.lambda_handler`.
  - Under Configuration > General Configuration: Change to max value timeout (15 minutes), memory (10240 MB), ephemeral storage (10240 MB).
  - Under Configuration > Permissions: Add to Lambda function execution role the custom inline policy:`dynamodb_lambda_permissions`.
  - In the `dynamodb_lambda_permissions` policy, make sure Resources statements have the correct ${AWS::AccountId}.
  - UNder Configuration > Permissions: Add to `agentInvokeFunction`, Source ARN: <Bedrock Agent ARN> and Action: `lambda:invokeFunction`.

- In order to trigger another **Prepare** cycle, go through another **Edit in Agent Builder** and **Save and exit** cycle.

7. Create, test, and add Guardrails to Agent

https://catalog.us-east-1.prod.workshops.aws/workshops/3008d94a-eaf7-477f-8b70-bc694f3589fc/en-US/05-guardrails

Detailed Steps:

- Message for blocked prompts and responses have moved to Page 1 of the **Create Guardrails** wizard.

- Sample message: `Please ask questions related to course catalog.  Please refrain from asking questions that: 1) compare institutions; 2) are related to employment prospects; or 3) are inappropriate in language or manner.`

8. Deploy Bedrock Agent; use SageMaker Studio Notebook to test Agent

https://catalog.us-east-1.prod.workshops.aws/workshops/3008d94a-eaf7-477f-8b70-bc694f3589fc/en-US/06-deploying-bedrock-agent

Detailed Steps:

- From Bedrock Agents console, create an Alias with name: `demo`.

- In SageMaker Studio Notebook `bedrock_basic.ipynb`, under **Invoking Bedrock Agents** section, replace:
  - agentId = `<Bedrock Agent Id>`
  - alias_id = `<Bedrock Agent Alias Id>`
