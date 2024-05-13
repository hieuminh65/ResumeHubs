import replicate
from api.utils import clean_bullet_points

import os
from dotenv import load_dotenv

load_dotenv()
replicate_api_key = os.getenv("REPLICATE_API_KEY")
client = replicate.Client(api_token=replicate_api_key)

system_prompt = "You're a dataset generator. Your response should be a list of resume bullet points, each separated by a new line character ('\n'). There's no need to add a '-' or a bullet point symbol at the start of each line. Please follow the prompt and generate at least 7 bullet points. Each bullet point should include the keywords and relevant, quantified information, and be single sentence They should be concise, unique, professional, and written in the third person, past tense, and active voice. Use the X-Y-Z formula: 'Accomplished [X] as measured by [Y], by doing [Z]'. The keyword should be bolded in each bullet point. Maintain the same tense throughout. There may be more than one keyword in the prompt. You must not repeat the same bullet point."

example = """Developed a new **NoSQL** database structure which improved data retrieval time by 45%.\nSuccessfully integrated **MongoDB (NoSQL)** with the existing MySQL database, resulting in a 30% increase in data storage capacity.\nConducted comprehensive training sessions on **NoSQL** for the technical team and increased their proficiency from 60% to 90%.\nAnalyzed and optimized complex query performance on **Couchbase (NoSQL)**, reducing query execution time by 25%.\nEnhanced application scalability by implementing **Cassandra's (NoSQL)** distributed architecture, supporting an additional 1 million users per month.\nStreamlined database management processes using **Amazon DynamoDB (NoSQL)**, saving the company over $50,000 annually in maintenance costs.\nSpearheaded the migration of a legacy SQL system to a modern **NoSQL** solution, successfully improving overall system efficiency by 35%.\nImplemented **Redis (NoSQL)** as a caching layer, reducing server load by 40% and improving response times.\nLed a project to transition to **Google Cloud Firestore (NoSQL)**, increasing data reliability and reducing costs by 20%.\nOptimized **Apache HBase (NoSQL)** configurations, resulting in a 50% increase in data processing speed."""

example2 = """Leveraged **Python** to develop a **data analytics** pipeline, resulting in a 30% increase in processing speed.\nUsed **Python** and **data analytics** techniques to identify key market trends, leading to a 20% increase in sales.\nImplemented a **data analytics** solution in **Python** to automate report generation, saving 10 hours of manual work per week.\nConducted comprehensive training sessions on **Python** and **data analytics**, increasing team proficiency by 40%.\nDeveloped a **Python** script to automate **data analytics** tasks, improving efficiency by 25%.\nUsed **Python** to perform **data analytics** on customer data, leading to a 15% increase in customer retention.\nCreated a **Python**-based **data analytics** tool to predict future sales trends, improving inventory management and reducing costs by 20%."""

example3 = """Utilized **Python** and **Microsoft Excel** to perform **data analytics**, resulting in a 20% increase in operational efficiency.\nLeveraged **Python** to automate **data analytics** tasks and presented findings using **Microsoft Excel**, leading to a 15% increase in sales.\nConducted comprehensive training sessions on **Python**, **data analytics**, and **Microsoft Excel**, enhancing team proficiency by 50%.\nDeveloped a **Python** script to automate **data analytics** tasks and export results to **Microsoft Excel**, improving efficiency by 30%.\nUsed **Python** and **Microsoft Excel** to perform **data analytics** on customer data, leading to a 10% increase in customer retention.\nCreated a **Python**-based **data analytics** tool to predict future sales trends and presented findings using **Microsoft Excel**, improving inventory management and reducing costs by 25%."""

preprompt = f"""Example keywords: NoSQL\n\n{example}\n\nExample keywords: Python, data analytics\n\n{example2}\n\nExample keywords Python, data analytics, Microsoft Excel\n\n{example3}\n\n"""

def generate_bulletpoints(keywords: list[str], previous_bullet_points: list[str] = []):
    previous_bullet_points = "\n".join(previous_bullet_points)
    global system_prompt, preprompt
    keywords = ", ".join(keywords)
    prompt = f"""{preprompt}Generate 10 resume bullet points for the keyword: {keywords}.\n\n{previous_bullet_points}\n\nGenerate 10 more resume bullet points:\n"""
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