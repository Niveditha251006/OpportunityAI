import json
import os
import re
import time

from dotenv import load_dotenv
from google import genai
from google.genai import errors

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def _fallback_extract_student_profile(text: str) -> dict:
    """Extract common profile details without calling an AI service."""
    lower_text = text.lower()

    profile = {
        "education_level": None,
        "field": None,
        "annual_income": None,
        "state": None,
        "rural": None,
        "first_generation": None,
        "interests": [],
    }

    # Education level
    if any(term in lower_text for term in [
        "undergraduate", "btech", "b.tech", "b.e.", "bachelor"
    ]):
        profile["education_level"] = "undergraduate"
    elif any(term in lower_text for term in [
        "postgraduate", "post-graduate", "master's", "m.tech", "mba"
    ]):
        profile["education_level"] = "postgraduate"
    elif any(term in lower_text for term in [
        "phd", "doctoral", "doctorate"
    ]):
        profile["education_level"] = "doctoral"

    # Field of study
    if any(term in lower_text for term in [
        "computer science", "cse", "software engineering"
    ]):
        profile["field"] = "computer science"
    elif "engineering" in lower_text:
        profile["field"] = "engineering"
    elif "medicine" in lower_text or "medical student" in lower_text:
        profile["field"] = "medicine"
    elif "commerce" in lower_text:
        profile["field"] = "commerce"
    elif "arts" in lower_text:
        profile["field"] = "arts"
    elif "science" in lower_text:
        profile["field"] = "science"

    # State: recognize only a limited set of explicitly named states.
    states = [
        "Andhra Pradesh", "Telangana", "Karnataka", "Tamil Nadu",
        "Kerala", "Maharashtra", "Delhi", "Uttar Pradesh",
        "Madhya Pradesh", "Rajasthan", "Gujarat", "West Bengal",
        "Bihar", "Odisha", "Punjab", "Haryana", "Assam",
        "Jharkhand", "Chhattisgarh", "Goa", "Himachal Pradesh",
        "Uttarakhand", "Sikkim", "Tripura", "Meghalaya",
        "Manipur", "Mizoram", "Nagaland", "Arunachal Pradesh"
    ]

    for state in states:
        if state.lower() in lower_text:
            profile["state"] = state
            break

    # Annual family income, for example: â‚¹250000 or 250,000 rupees.
    income_patterns = [
        r"(?:annual|yearly|family)\s+(?:family\s+)?income"
        r"\s*(?:is|of|:|=)?\s*(?:â‚¹|rs\.?|inr)?\s*"
        r"([\d,]+(?:\.\d+)?)",

        r"(?:â‚¹|rs\.?|inr)\s*([\d,]+(?:\.\d+)?)"
        r"\s*(?:per\s+year|annually|yearly)?",

        r"([\d,]+(?:\.\d+)?)\s*rupees"
        r"\s*(?:per\s+year|annually|yearly)?",
    ]

    for pattern in income_patterns:
        match = re.search(pattern, lower_text)
        if match:
            try:
                profile["annual_income"] = float(
                    match.group(1).replace(",", "")
                )
                break
            except ValueError:
                pass



    # Explicitly stated background indicators.
    rural_no = re.search(
        r"\b(not rural|non[- ]rural|urban)\b", lower_text
    )
    rural_yes = re.search(
        r"\b(rural|village|villager)\b", lower_text
    )

    # Explicit negative statements take priority over keyword matches.
    if rural_no:
        profile["rural"] = False
    elif rural_yes:
        profile["rural"] = True

    first_gen_no = re.search(
        r"\b(not a first[- ]generation|not first[- ]generation|"
        r"my parent[s]? attended college)\b",
        lower_text,
    )
    first_gen_yes = re.search(
        r"\b(first[- ]generation|first person in my family to attend college|"
        r"first in my family to attend college)\b",
        lower_text,
    )

    if first_gen_no:
        profile["first_generation"] = False
    elif first_gen_yes:
        profile["first_generation"] = True


    # Basic keyword fallback for interests.
    interest_keywords = [
        "python", "artificial intelligence", "machine learning",
        "software development", "web development", "data science",
        "cybersecurity", "programming", "robotics", "cloud computing",
        "app development", "research"
    ]

    profile["interests"] = [
        interest for interest in interest_keywords
        if interest in lower_text
    ]

    return profile


def extract_student_profile(text: str) -> dict:
    prompt = f"""
Extract a student's profile from the text below.

Return ONLY valid JSON with these fields:

- education_level
- field
- annual_income
- state
- rural
- first_generation
- interests

Rules:
- education_level should be a simple value such as "undergraduate"
- annual_income should be a number in Indian rupees
- rural and first_generation must be true, false, or null
- Use true only when the student explicitly indicates the condition is true.
- Use false only when the student explicitly indicates the condition is false.
- If rural or first_generation is not stated or is ambiguous, use null.
- For other missing text/number fields, use null, and use [] for missing interests.
- Do not invent information.
- interests must be a list of strings
- Do not invent information.

Student text:
{text}
"""

    max_retries = 3

    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt
            )

            if not response.text:
                raise ValueError("Gemini returned an empty response.")

            cleaned_response = response.text.strip()

            if cleaned_response.startswith("```json"):
                cleaned_response = cleaned_response[7:]

            if cleaned_response.endswith("```"):
                cleaned_response = cleaned_response[:-3]

            profile = json.loads(cleaned_response.strip())

            expected_fields = {
                "education_level", "field", "annual_income", "state",
                "rural", "first_generation", "interests"
            }

            if not isinstance(profile, dict):
                raise ValueError("Gemini response must be a JSON object.")

            if not expected_fields.issubset(profile):
                raise ValueError("Gemini response is missing profile fields.")

            return profile

        except (errors.ServerError, errors.ClientError) as error:
            if attempt == max_retries - 1:
                print(
                    "Gemini remained unavailable after retries. "
                    "Using the basic Python fallback."
                )
                return _fallback_extract_student_profile(text)

            wait_time = 2 ** attempt
            print(
                f"Gemini temporarily unavailable. "
                f"Retrying in {wait_time} seconds..."
            )
            time.sleep(wait_time)
