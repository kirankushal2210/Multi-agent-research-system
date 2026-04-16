import os
from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search , scrape_url 
from dotenv import load_dotenv

load_dotenv()

def get_llm():
      model_name = os.getenv("OLLAMA_MODEL", "llama3.2:3b")
      base_url = os.getenv("OLLAMA_BASE_URL")
      kwargs = {
          "model": model_name,
          "temperature": 0,
      }
      if base_url:
                kwargs["base_url"] = base_url
            return ChatOllama(**kwargs)

#1st agent 
def build_search_agent():
      return create_agent(
          model = get_llm(),
          tools= [web_search]
)

#2nd agent 
def build_reader_agent():
      return create_agent(
          model = get_llm(),
          tools = [scrape_url]
)

#writer chain 
writer_prompt = ChatPromptTemplate.from_messages([
      ("system", "You are an expert writer. Write clear, concise, and recruiter-ready answers."),
      ("human", """Write a polished response on the topic below.

      Topic: {topic}

      Use the available research or context if it is helpful, but if the research is missing or limited, rely on general knowledge to create a strong, presentable answer.

      Context:
      {research}

      Structure the response as:
      - Introduction
      - Key points
      - Conclusion
      - Practical takeaway

      Keep it professional, easy to follow, and suitable for a demo presentation."""),
])

def build_writer_chain():
      return writer_prompt | get_llm() | StrOutputParser()

#critic_chain 
critic_prompt = ChatPromptTemplate.from_messages([
       ("system", "You are a sharp and constructive research critic. Be honest and specific."),
      ("human", """Review the research report below and evaluate it strictly.

      Report:
      {report}

      Respond in this exact format:

      Score: X/10

      Strengths:
      - ...
      - ...

      Areas to Improve:
      - ...
      - ...

      One line verdict:
      ..."""),
])

def build_critic_chain():
      return critic_prompt | get_llm() | StrOutputParser()
