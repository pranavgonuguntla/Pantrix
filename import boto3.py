import boto3
import json

# Sample ingredient list from grocery API
ingredients = ["chicken breast", "broccoli", "olive oil", "garlic", "rice"]

# Convert list to string for prompt
ingredient_str = ', '.join(f'"{item}"' for item in ingredients)

# Create the prompt with dynamic ingredient input
prompt = f"""
You are a helpful chef. Create 2 dinner recipes using ONLY these ingredients:
[{ingredient_str}]

Constraints:
- Total cook time under 30 minutes
- High protein
- Avoid dairy
- Output in structured JSON format with:
  - title
  - ingredients (list)
  - instructions (list of steps)
  - prep_time
  - estimated_calories
"""

bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')

response = bedrock.invoke_model(
    modelId="anthropic.claude-v2",  # or another Bedrock-supported model
    contentType="application/json",
    accept="application/json",
    body=json.dumps({
        "prompt": prompt,
        "max_tokens_to_sample": 1024,
        "temperature": 0.7,
        "stop_sequences": ["\n\nHuman:"]
    })
)

response_body = json.loads(response['body'].read())
recipes = response_body['completion']