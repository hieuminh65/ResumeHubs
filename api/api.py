import replicate
from api.utils import clean_bullet_points

import os
from dotenv import load_dotenv

load_dotenv()
replicate_api_key = os.getenv("REPLICATE_API_KEY")
client = replicate.Client(api_token=replicate_api_key)

system_prompt = "You're a dataset generator. Your response should be a list of resume bullet points, each separated by a new line character ('\n'). There's no need to add a '-' or a bullet point symbol at the start of each line. Please follow the prompt and generate at least 7 bullet points. Each bullet point should include the keyword and relevant, quantified information, and be single sentence They should be concise, unique, professional, and written in the third person, past tense, and active voice. Use the X-Y-Z formula: 'Accomplished [X] as measured by [Y], by doing [Z]'. The keyword should be bolded in each bullet point. Maintain the same tense throughout."
example = """Developed a new **NoSQL** database structure which improved data retrieval time by 45%.\nSuccessfully integrated **MongoDB (NoSQL)** with the existing MySQL database, resulting in a 30% increase in data storage capacity.\nConducted comprehensive training sessions on **NoSQL** for the technical team and increased their proficiency from 60% to 90%.\nAnalyzed and optimized complex query performance on **Couchbase (NoSQL)**, reducing query execution time by 25%.\nEnhanced application scalability by implementing **Cassandra's (NoSQL)** distributed architecture, supporting an additional 1 million users per month.\nStreamlined database management processes using **Amazon DynamoDB (NoSQL)**, saving the company over $50,000 annually in maintenance costs.\nSpearheaded the migration of a legacy SQL system to a modern **NoSQL** solution, successfully improving overall system efficiency by 35%.\nImplemented **Redis (NoSQL)** as a caching layer, reducing server load by 40% and improving response times.\nLed a project to transition to **Google Cloud Firestore (NoSQL)**, increasing data reliability and reducing costs by 20%.\nOptimized **Apache HBase (NoSQL)** configurations, resulting in a 50% increase in data processing speed."
"""

def generate_bulletpoints(keyword):
    prompt = f"""Example keywords: NoSQL\n\n{example}\n\nGenerate 10 resume bullet points for the keyword: {keyword}."""
    global system_prompt
    output = ""
    for event in client.stream(
        "snowflake/snowflake-arctic-instruct",
        input={
            "top_k": 50,
            "top_p": 0.9,
            "prompt": prompt,
            "temperature": 0.7,
            "max_new_tokens": 1028,
            "min_new_tokens": 0,
            "stop_sequences": "<|im_end|>",
            "prompt_template": f"<|im_start|>system\n{system_prompt}<|im_end|>\n<|im_start|>user\n{prompt}<|im_end|>\n\n<|im_start|>assistant\n",
            "presence_penalty": 2,
            "frequency_penalty": 0.2
        },
    ):
        output += str(event)
        # print(str(event), end="")
    number = output.count("\n")
    print("\nThere are", number, "bullet points generated.")
    output = clean_bullet_points(output)
    return output