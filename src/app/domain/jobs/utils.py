import os
import json
import structlog
from typing import Any
from openai import AsyncOpenAI


logger = structlog.get_logger()

model = os.environ["OPENAI_MODEL_NAME"]
client = AsyncOpenAI(api_key=os.environ["OPENAI_API_KEY"])
prompt = """
    Extract the following information from the given job post in the form of HTML/JS code:
    - Company Name
    - Company URL
    - Company LinkedIn URL
    - Job title
    - Job Location
    - Tech stack such as tools, programming languages, frameworks, and technologies, along with the certainty(Low, Medium or High) that the company is likely using the tool

    Rules for assigning certainty to tools:
    - If the candidate experience with a tool is preferred or considered a bonus, the certainty should be High.
    - If a tool is explicitely mentioned as part of company's tech stack, the certainty  should be High.
    - If a tool is mentioned as part of a list of similar tools, the certainty should be Low.
    - Else, use Medium.

    Format the extracted information into the following short JSON object:
    {{
        "company": {{
            "name": "company name",
            "url": "https://company.tld",
            "linkedin_url": "https://company/linkedin/url",
        }}
        title: "Job title",
        location: {{"country": "country name", "region": "state or provience name", "city": "city name"}},
        tools: [ {{"name": "tool name 1", "certainty": "High"}}, {{"name": "tool name 2", "certainty": "Medium"}} ]
    }}

    Note: Use null if you're unable to extract any information.

    Here is the code:
    {html_content}
"""


async def extract_job_details_from_html(html_content: str) -> dict[str, Any]:
    """Extracts job post from the html using an LLM."""
    messages = [
        {
            "role": "user",
            "content": prompt.format(html_content=html_content),
        }
    ]
    chat_response = await client.chat.completions.create(
        model=model,
        messages=messages,
        response_format={
            "type": "json_object",
        },
    )

    job_details = json.loads(chat_response.choices[0].message.content)
    print(job_details)
    if (
        not "title" in job_details
        or "name" not in job_details.get("company")
        and ("url" not in job_details.get("company") or "linkedin_url" not in job_details.get("company"))
    ):
        logger.warn("Failed to extract necessary information from job post", job_details=job_details)

    return job_details