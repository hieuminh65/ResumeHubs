import replicate
from api.utils import clean_bullet_points
import streamlit as st

replicate_api_key = st.secrets['API_KEY']["REPLICATE_API_KEY"]
client = replicate.Client(api_token=replicate_api_key)


example = """Developed a new **NoSQL** database structure which improved data retrieval time by 45%.\nSuccessfully integrated **MongoDB (NoSQL)** with the existing MySQL database, resulting in a 30% increase in data storage capacity.\nConducted comprehensive training sessions on **NoSQL** for the technical team and increased their proficiency from 60% to 90%.\nAnalyzed and optimized complex query performance on **Couchbase (NoSQL)**, reducing query execution time by 25%.\nEnhanced application scalability by implementing **Cassandra's (NoSQL)** distributed architecture, supporting an additional 1 million users per month.\nStreamlined database management processes using **Amazon DynamoDB (NoSQL)**, saving the company over $50,000 annually in maintenance costs.\nSpearheaded the migration of a legacy SQL system to a modern **NoSQL** solution, successfully improving overall system efficiency by 35%.\nImplemented **Redis (NoSQL)** as a caching layer, reducing server load by 40% and improving response times.\nLed a project to transition to **Google Cloud Firestore (NoSQL)**, increasing data reliability and reducing costs by 20%.\nOptimized **Apache HBase (NoSQL)** configurations, resulting in a 50% increase in data processing speed."""

example2 = """Leveraged **Python** to develop a **data analytics** pipeline, resulting in a 30% increase in processing speed.\nUsed **Python** and **data analytics** techniques to identify key market trends, leading to a 20% increase in sales.\nImplemented a **data analytics** solution in **Python** to automate report generation, saving 10 hours of manual work per week.\nConducted comprehensive training sessions on **Python** and **data analytics**, increasing team proficiency by 40%.\nDeveloped a **Python** script to automate **data analytics** tasks, improving efficiency by 25%.\nUsed **Python** to perform **data analytics** on customer data, leading to a 15% increase in customer retention.\nCreated a **Python**-based **data analytics** tool to predict future sales trends, improving inventory management and reducing costs by 20%."""

example3 = """Utilized **Python** and **Microsoft Excel** to perform **data analytics**, resulting in a 20% increase in operational efficiency.\nLeveraged **Python** to automate **data analytics** tasks and presented findings using **Microsoft Excel**, leading to a 15% increase in sales.\nConducted comprehensive training sessions on **Python**, **data analytics**, and **Microsoft Excel**, enhancing team proficiency by 50%.\nDeveloped a **Python** script to automate **data analytics** tasks and export results to **Microsoft Excel**, improving efficiency by 30%.\nUsed **Python** and **Microsoft Excel** to perform **data analytics** on customer data, leading to a 10% increase in customer retention.\nCreated a **Python**-based **data analytics** tool to predict future sales trends and presented findings using **Microsoft Excel**, improving inventory management and reducing costs by 25%."""

system_prompt = "# Role\n\nYou're a dataset generator of resume bullet points base on resume keywords\n\n# Response format:\n\nYour response should be only a list of resume bullet points, each separated by a new line character ('\\n'). There's no need to add a '-', a bullet point symbol, or index number at the start of each line. \n\n# Task:\n\nPlease follow the prompt and generate at least 7 bullet points. Each bullet point should include the keywords and relevant, quantified information, and be single sentence. They should be concise, unique, professional, and written in the third person, past tense, and active voice. Use the X-Y-Z formula: 'Accomplished [X] as measured by [Y], by doing [Z]'. The keyword should be bolded in each bullet point. Maintain the same tense throughout. There may be more than one keyword in the prompt. You must not repeat the same bullet point.\n\n# Example:\n\n"

example_prompt = f"""\n\nExample keywords: NoSQL\n\n{example}\n\nExample keywords: Python, data analytics\n\n{example2}\n\nExample keywords Python, data analytics, Microsoft Excel\n\n{example3}\n\n"""

system_prompt += example_prompt

def generate_bulletpoints(keywords: list[str], previous_bullet_points: list[str] = []):
    global system_prompt

    if previous_bullet_points:
        previous_bullet_points.reverse()
        previous_bullet_points = "These are the previous bullet points generated that you should not repeat:\n\n" + "\n\n".join(previous_bullet_points)

    keywords = ", ".join(keywords)
    
    prompt = f"""## Generate resume bullet points for the keyword(s): {keywords}.\n\n{previous_bullet_points}\n\n## Generate exactly 9 more resume bullet points here:\n\n"""
    
    output = ""
    for event in client.stream(
        "snowflake/snowflake-arctic-instruct",
        input={
            "top_k": 50,
            "top_p": 0.9,
            "prompt": prompt,
            "temperature": 1,
            "max_new_tokens": 4096,
            "min_new_tokens": 0,
            "stop_sequences": "<|im_end|>",
            "prompt_template": f"<|im_start|>system\n\n{system_prompt}<|im_end|>\n<|im_start|>user\n\n{prompt}<|im_end|>\n\n<|im_start|>assistant\n\n",
            "presence_penalty": 2,
            "frequency_penalty": 0.2
        },
    ):
        output += str(event)
        # print(str(event), end="")

    number = output.count("\n") + 1
    print("\nThere are", number, "bullet points generated.")
    st.session_state.num_bullet_points_generated = number

    output = clean_bullet_points(output)
    return output