# -*- coding: utf-8 -*-
"""st12.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1SKr0asnqqr6emHtQbxDp1SrFUvpCtXyU
"""


from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.agents import load_tools, Tool, AgentExecutor, LLMSingleActionAgent, AgentOutputParser
from langchain.prompts import StringPromptTemplate

from langchain import OpenAI, LLMChain
from langchain.tools import DuckDuckGoSearchRun

from typing import List, Union
from langchain.schema import AgentAction, AgentFinish


from langchain.agents import initialize_agent
from langchain.llms.openai import OpenAI
import re
import langchain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser

from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

import streamlit as st
import os
import openai

os.environ['OPENAI_API_KEY'] = st.secrets['key1]



llm = ChatOpenAI(model = "gpt-4-1106-preview", temperature = 0.5)
template_ask = """

First, understand the meaning of an individual's beliefs. An individual's beliefs is the key ideas that underpin the decisions of oneself and can be generalized to almost anything. They are one's personal interpretation of conventions in the world, and are unspecific. For example, one core belief could be 'money is useless'. These beliefs can be generalized to any scenario.

Then, outline the 5 ABSTRACT, UNSPECIFIC beliefs of the input, in the form of a rubric.
The rubric can be used to assess anything based on the beliefs you evaluated. The extent to which the subject meets a belief provides the score for the belief (out of 3); the total score is the sum of the scores of the 5 beliefs.

The input is here: ""{input}""
"""

prompt_ask = ChatPromptTemplate.from_template(template_ask)
chain_ask = (
    prompt_ask | llm | StrOutputParser()

)


template1 = """


Part 1:
First, evaluate the subject of the input. For example, the subject of 'i hate school', is school. Output your answer.
Then, interpret the subject as what the general public sees it as.
Then, answer the following questions:
1. Who was a contemporary predecessor of the subject?
2. Who was the most famous hero/system that took the subject's role in the past, that is well known and praised by the public?
3. Who is the most competent counterpart of the subject (what the public strongly associates with the input subject; what alternative is MOST COMPETENT of replacing the subject)?

You will identify the questions that cannot be answered. For example, there is no 'most famous hero/system' for the input subject 'sleeping'; hence, you will not be answering this question.
Your output should  ONLY be your answer to the questions as 4 subjects. Label the attribute (predecessor, counterpart...) for each subject




Part 2:
answer the following questions on EVERY SINGLE ONE OF THE FOUR subjects you evaluated previously.
You will use your rubric to assess any type of subject, from individual to a system.
For a subject that is a pure concept/not yet implemented, answer the following questions on it as if it is already implemented.
You will EXAPLAIN your chain of thought for the REASONS/WHY behind your mark allocations, providing CLEAR EVIDENCE and EXAMPLES as you do so.


The questions are here:

{question}

Finally, calculate the total score for each of the FOUR subjects.



The input is here: ""{input}""



"""

prompt1 = ChatPromptTemplate.from_template(template1)
chain1 = (

           prompt1 | llm | StrOutputParser()

)

from langchain.schema import StrOutputParser
llmx = ChatOpenAI(model = "gpt-3.5-turbo")
templatex = """
Make sure to complete part 1 and part 2.



Part 1:

First, evaluate the subject of the input.
Using the text,  summarize all the advantages and disadvantages the input subject has over others in detail.  Then, explicitly mention which of the other subjects it has the advantages and disadvantages on.
Then, provide real world, specific, examples for every generic term you mentioned.



Part 2:
First, identify the input subject, the predecessor, the counterpart, and the most famous hero from the start o the text.
Then, carefully analyzing the text; if the input subject scored the highest overall, choose option 1; if the input subject scored the lowest overall, choose option 2; if the input subject scored in the middle, choose option 3.

option 1:
you will overwhelmingly praise the input subject.
write an opinion that favors the input subject, sounding very personal and opinionated by using the 1st person narrative. Make sure to sound like a teenager, who is blunt.
In your opinion, highlight the KEY advantages that the input subject has over the other subjects (mentioning the names of the others), incorporating the real world examples you provided.
You will mention key ideas from the rubric but not providing specific scoring.
Structure your opinion for someone that has no idea about the scoring and the areas mentioned in the text, using 6th grade vocabulary.
Use 2 sentences to do this.
Begin by stating phrases similar to the 'input subject' is 'the best!'.


option 2:
you will overwhelmingly reprove the input subject.
write an opinion that denigrates the input subject, sounding very personal and opinionated by using the 1st person narrative. Make sure to sound like the  a teengaer, who is blunt.
You will mention key ideas from the rubric but not providing specific scoring.
In your opinion, highlight the KEY disadvantages that the input subject has over the other subjects (mentioning the names of the others), incorporating the real world examples you provided.
Structure your opinion for someone that has no idea about the scoring and the areas mentioned in the text, using 6th grade vocabulary.
Use 2 sentences to do this.
Begin by stating phrases similar to the 'input subject' is 'garbage'.

option 3:
you will write an opinion towards the input subject.
write an opinion on the input subject, sounding very personal and opinionated by using the 1st person narrative. Make sure to sound like a teenager that uses lots of slang and is super lazy/succinct.
In your opinion, highlight the disadvantages and advantages that the input subject has over the other subjects (mentioning the names of the others), incorporating the real world examples you provided.
When you show the advantages, be overwhelmingly positive; when showing disadvantages, be overwhelmingly negative.
You will mention key ideas from the rubric but not providing specific scoring.
Structure your opinion for someone that has no idea about the scoring and the areas mentioned in the text, using 6th grade vocabulary.
You will use TWO sentences to do this.
Begin by stating phrases similar to the 'input subject' is mediocre'.

The text is here: ""
{input1}
""

the input is here: ""
{input2}
""


"""
from langchain.schema.runnable import RunnablePassthrough
promptx = ChatPromptTemplate.from_template(templatex)


chainy = (
    promptx | llmx|StrOutputParser()
)


st.set_page_config(page_title = "Hazel", page_icon = ":penguin:")

st.header("Say Anything!")



def get_person():
  person = st.text_area(label = "", placeholder = "who do you praise? : ", key = "person")
  return person
retrieved_person = get_person()

def get_subject():
  subject = st.text_area(label = "", placeholder = "Say Anything! :", key = "subject")
  return subject
retrieved_subject = get_subject()

llm = ChatOpenAI(model = "gpt-4-1106-preview", temperature = 0.5)



template_ask = """

First, understand the meaning of an individual's beliefs. An individual's beliefs is the key ideas that underpin the decisions of oneself and can be generalized to almost anything. They are one's personal interpretation of conventions in the world, and are unspecific. For example, one core belief could be 'money is useless'. These beliefs can be generalized to any scenario.

Then, outline the 5 ABSTRACT, UNSPECIFIC beliefs of the input, in the form of a rubric.
The rubric can be used to assess anything based on the beliefs you evaluated. The extent to which the subject meets a belief provides the score for the belief (out of 3); the total score is the sum of the scores of the 5 beliefs.

The input is here: ""{input}""
"""

prompt_ask = ChatPromptTemplate.from_template(template_ask)
chain_ask = (
    prompt_ask | llm | StrOutputParser()

)

if retrieved_person:
  questions = chain_ask.invoke({"input": retrieved_person})
  st.write(questions)
if retrieved_subject:
  analysis = chain1.invoke({"question":questions, "input": retrieved_subject})
  result = chainy.invoke({"input1": analysis, "input2": retrieved_subject})
  st.write(result)
  st.write(analysis)

