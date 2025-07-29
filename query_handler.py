import requests
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

GROQ_API_KEY = os.getenv('GROQ_API_KEY')
client = Groq(api_key=GROQ_API_KEY)

def query_groq(user_query, system_prompt="You are a helpful assistant that aggregates info from tech docs and APIs."):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",  # Updated, stable model
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_query}
        ],
        max_tokens=512,
        temperature=0.7
    )
    return response.choices[0].message.content

STACK_OVERFLOW_ENDPOINT = 'https://api.stackexchange.com/2.3/search/advanced'
GITHUB_ENDPOINT = 'https://api.github.com/search/repositories'

def fetch_stack_overflow(query, api_key=None):
    params = {
        'order': 'desc',
        'sort': 'relevance',
        'q': query,
        'site': 'stackoverflow',
        'key': api_key if api_key else None
    }
    response = requests.get(STACK_OVERFLOW_ENDPOINT, params=params)
    if response.status_code == 200:
        items = response.json().get('items', [])
        return [item['title'] + ": " + item['link'] for item in items[:3]]
    return []

def fetch_github(query, token):
    headers = {'Authorization': f'token {token}'}
    params = {'q': query, 'sort': 'stars', 'order': 'desc'}
    response = requests.get(GITHUB_ENDPOINT, params=params, headers=headers)
    if response.status_code == 200:
        items = response.json().get('items', [])
        return [item['full_name'] + ": " + item['html_url'] for item in items[:3]]
    return []

def aggregate_and_query(user_query):
    stack_results = fetch_stack_overflow(user_query, os.getenv('STACK_OVERFLOW_KEY'))
    github_results = fetch_github(user_query, os.getenv('GITHUB_TOKEN'))
    aggregated_context = f"Stack Overflow results: {stack_results}\nGitHub results: {github_results}"
    full_query = f"{user_query}\nContext: {aggregated_context}"
    return query_groq(full_query, "Summarize and present concise answers based on the provided context.")
