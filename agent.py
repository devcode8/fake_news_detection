from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low
from typing import List
import httpx
import json
import os
from dotenv import load_dotenv

load_dotenv()

class NewsRequest(Model):
    query: str

class NewsResult(Model):
    response: str

class NewsResponse(Model):
    msg: str

class WebSearchRequest(Model):
    query: str

class WebSearchResult(Model):
    title: str
    url: str
    content: str

class WebSearchResponse(Model):
    query: str
    results: List[WebSearchResult]

class ASI1miniRequest(Model):
    query: str

class ASI1miniResponse(Model):
    response: str

agent=Agent(name="News Agent", seed="Test Agen", port=8080, endpoint="http://localhost:8080/submit")



prompt_string = """
Analyze the following headline and the corresponding web search data to verify whether the event mentioned in the headline is factually correct, regardless of when it occurred.

Headline: "{headline}"

Web Search Data: "{web_data}"

Criteria for analysis:
Authenticity: Check if the event in the headline actually occurred, based on trusted sources.
Date Detection: Identify when the event took place, if possible.
Location Verification: Ensure that the location mentioned in the headline matches the real event.
Misinformation Check: If the event never occurred, mark it as fake.

Important Instructions:
1. If the event occurred (even if it was earlier than 5 days ago), mark the headline as Valid.
2. Only mark the headline as Fake if the event did not happen at all or is fabricated.
3. Base your answer solely on the provided web search data. Do not use your own knowledge or assumptions.
4. Be precise and clear.

Format of Output:
1. The headline "{headline}" is Valid/Fake. (Choose one based on your analysis)
2. A brief report explaining your validation reasoning.
3. If the news is Valid, add a one-line summary of the incident in 60 words or less. The summary must mention the actual date when the event occurred.

Note: If the news is Fake, skip the summary section.
"""

news_agent = 'agent1qdc95a7qpyy5cef3e3g9xfkplnfkaw8046cdzasgmp2jzsltza50ch59s7f'

fund_agent_if_low(agent.wallet.address()) #type:ignore

@agent.on_event('startup')
async def startup(ctx: Context):
    print("News Agent is starting up...")

@agent.on_rest_get('/', NewsResult)
async def index(ctx: Context) -> NewsResponse:
    return NewsResponse(msg="Welcome to the News Agent!")

async def call_tavily_api(query: str):
    try:
        async with httpx.AsyncClient() as client:
            tavily_payload = {
                "api_key": os.getenv("TAVILY_API_KEY"),
                "query": query,
                "search_depth": "advanced",
                "include_answer": True,
                "max_results": 5
            }
            response = await client.post(
                "https://api.tavily.com/search",
                json=tavily_payload,
                timeout=30.0
            )
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Tavily API error: {response.status_code}")
                return None
    except Exception as e:
        print(f"Error calling Tavily API: {e}")
        return None

async def call_asi_one_api(prompt: str):
    try:
        async with httpx.AsyncClient() as client:
            asi_payload = {
                "model": "asi1-mini",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0,
                "stream": False,
                "max_tokens": 1000
            }
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Authorization': f'Bearer {os.getenv("ASI_ONE_API_KEY")}'
            }
            response = await client.post(
                "https://api.asi1.ai/v1/chat/completions",
                json=asi_payload,
                headers=headers,
                timeout=30.0
            )
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"]
            else:
                print(f"ASI:One API error: {response.status_code}")
                print(f"Response: {response.text}")
                return None
    except Exception as e:
        print(f"Error calling ASI:One API: {e}")
        return None

@agent.on_rest_post('/news', NewsRequest, NewsResponse)
async def get_news(ctx: Context, request: NewsRequest) -> NewsResponse:
    print(f"Received news request: {request.query}")
    
    tavily_result = await call_tavily_api(request.query)
    
    if tavily_result:
        print(f"Results for {request.query}\n")
        data = []
        
        if "results" in tavily_result:
            for result in tavily_result["results"]:
                data.append(result.get("content", ""))
                print(f"Title: {result.get('title', 'N/A')} - {result.get('url', 'N/A')}")
                print(result.get("content", ""))
        
        web_data = f"Search results summary from Tavily: {data}"
        final_string = prompt_string.format(headline=request.query, web_data=web_data)
        
        asi_result = await call_asi_one_api(final_string)
        
        if asi_result:
            print(f"Results for {request.query}\n")
            print(asi_result)
            return NewsResponse(msg=asi_result)
        else:
            return NewsResponse(msg="No response received from ASI:One API.")
    else:
        return NewsResponse(msg="No response received from Tavily API.")

if __name__ == "__main__":
    agent.run()