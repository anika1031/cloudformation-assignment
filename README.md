# cloudformation-assignment

## Objective
 
Build a serverless Birthday Reminder application using AWS services.
The application should allow users to:
 
-  Add birthdays
-  View birthdays
-  Access via a frontend hosted on S3
 
---
 
##  Services Used
 
| Service | Purpose |
|---|---|
| AWS CloudFormation | Infrastructure as Code |
| AWS Lambda | Serverless compute |
| Amazon API Gateway | REST API layer |
| Amazon DynamoDB | NoSQL database |
| Amazon S3 | Frontend hosting |
| IAM | Permissions & security |
 
---

## Example Assignment Deployment

You can refer to a sample working project below:

Mohan's Deployment (Staging):
---> https://staging.d304zajv3i3izo.amplifyapp.com/

---

##  Architecture Overview
 
```
Frontend (S3)
     ↓
API Gateway
     ↓
Lambda Functions
     ↓
DynamoDB
```
 ### Dashboard
<img width="1014" height="909" alt="image" src="https://github.com/user-attachments/assets/45484370-d3fe-497e-9304-420e24e7c8d0" />

---
 
##  Part 1: Deploy Infrastructure (CloudFormation)
 
1. Go to **AWS Console**
2. Open **CloudFormation**
3. Click **Create Stack → With new resources**
4. Upload the provided YAML template
5. Click **Next**
6. Enter stack name:
 
```
birthday-reminder-stack
```
 
7. Keep default settings → Click **Next → Create Stack**
8. Wait until status becomes:
 
```
CREATE_COMPLETE
```
 
---
 
##  Part 2: API Gateway Setup
 
1. Go to **API Gateway**
2. Open your API
3. Check if resources are created:
   - `/birthdays` OR `/test`
 
###  Deploy API
 
- Click **Deploy API**
- Create/select stage:
 
```
dev
```
 
- Copy the **Invoke URL**
 
Example:
 
```
https://abc123.execute-api.region.amazonaws.com/dev
```
 
---
 
##  Part 3: Fix IAM Permissions
 
>  The application will **NOT** work fully at this stage.
 
###  Expected Issue
 
- Adding a birthday fails due to missing DynamoDB permissions
 
###  Your Task
 
- Identify the error
- Fix the Lambda execution role permissions
 
###  Steps
 
1. Go to **IAM → Roles**
2. Find the Lambda execution role
3. Attach a policy to allow DynamoDB access
 
### Required Permissions
 
```json
{
  "Effect": "Allow",
  "Action": [
    "dynamodb:PutItem",
    "dynamodb:GetItem",
    "dynamodb:Scan",
    "dynamodb:Query"
  ],
  "Resource": "*"
}
```
 
---
 
##  Part 4: Fix CORS Issue
 
When connecting the frontend, you may see:
 
```
blocked by CORS policy
``` 
###  Step 1: Add CORS Headers in Lambda
 
Modify your Lambda response to include the following headers:
 
```python
return {
    'statusCode': 200,
    'headers': {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type'
    },
    'body': json.dumps(data)
}
```
Note: If you still face CORS issues, ensure your API supports OPTIONS method.
---
 
##  Part 5: Test the API
 
###  GET Request
 
Open in your browser:
 
```
<api-url>/birthdays
```
 
###  POST Request (using curl)
 
```bash
curl -X POST <api-url>/birthdays \
  -H "Content-Type: application/json" \
  -d '{"name":"Anika","birthDate":"2000-01-01"}'
```
 
---
 
##  Part 6: Host Frontend on S3
 
1. Go to **S3**
2. Create a new bucket
3. Disable **Block all public access**
4. Upload `index.html`
 
### Enable Static Website Hosting
 
- Go to **Properties**
- Enable **Static Website Hosting**
- Copy the **Website Endpoint URL**
 
### Make Bucket Public
 
Add the following bucket policy (replace `YOUR-BUCKET-NAME`):
 
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::YOUR-BUCKET-NAME/*"
    }
  ]
}
```
 
---
 
##  Part 7: Connect Frontend to API
 
1. Open your `index.html`
2. Paste your **API Gateway Invoke URL**
3. Save the file
4. Re-upload to S3 if already hosted
 
---
 
##  Final Checklist
 
- [ ] CloudFormation stack status: `CREATE_COMPLETE`
- [ ] API Gateway deployed to `dev` stage
- [ ] IAM role has DynamoDB permissions
- [ ] Lambda returns CORS headers
- [ ] GET `/birthdays` returns data
- [ ] POST `/birthdays` adds a record
- [ ] `index.html` hosted on S3
- [ ] Frontend connected to API URL
