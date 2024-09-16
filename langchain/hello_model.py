import os
import pprint 
from openai import OpenAI

llm_model = "gpt-3.5-turbo"

# There are 3 ways to use OpenAI API in this file 
# 1. Use OpenAI directly
# 2. Use LangChain with a simple prompt
# 3. Use LangChain with a parser


def use_openai_directly():
    client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

    # Not needed since I am setting the values in .zshrc. 
    #from dotenv import load_dotenv, find_dotenv
    #_ = load_dotenv(find_dotenv()) # read local .env file
    def get_completion(prompt, model=llm_model):
        messages = [{"role": "user", "content": prompt}]
        response = client.chat.completions.create(model=model,
        messages=messages,
        temperature=0)       # set temperature to 0 for deterministic output
        return response.choices[0].message.content

    print(get_completion("what is one plus one ?"))  # Test the function

    customer_email = "Arrr, I be fuming that me blender lid flew off and splattered me kitchen walls with smoothie! And to make matters worse, the warranty don't cover the cost of cleaning up me kitchen. I need yer help right now, matey!"
    style = "Jamaican English in a fun playful manner"

    prompt = f"""Translate the text that is delimited by triple backticks into a style that is {style}.  text: ```{customer_email}``` """

    print(f'prompt = {prompt}')
    response = get_completion(prompt)
    print(f'response = "{response}')

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import ResponseSchema
from langchain.output_parsers import StructuredOutputParser
    
def use_langchain_simple():
    chat = ChatOpenAI(temperature=0.0, model=llm_model)
    print('Chat client = ')
    pprint.pprint(str(chat))
    print('\n')

    template_string = """Translate the text that is delimited by triple backticks into a style that is {style}. text: ```{text}``` """

    prompt_template = ChatPromptTemplate.from_template(template_string)
    #print(prompt_template.messages[0].prompt)
    customer_style = 'American English in a calm and respectful tone'
    customer_email = "Arrr, I be fuming that me blender lid flew off and splattered me kitchen walls with smoothie! And to make matters worse, the warranty don't cover the cost of cleaning up me kitchen. I need yer help right now, matey!"

    # Fill in the input varaibles for the prompt template 
    print('input variable for the prompt template = ', prompt_template.messages[0].prompt.input_variables)
    customer_messages = prompt_template.format_messages(style=customer_style, text=customer_email)
    print(customer_messages)

    # Now invoke the chat model
    response = chat(messages=customer_messages)
    print(response.content)
    print('\n')
    print(response)

def langchain_parser():
    customer_review = """\
    This leaf blower is pretty amazing.  It has four settings:\
    candle blower, gentle breeze, windy city, and tornado. \
    It arrived in two days, just in time for my wife's \
    anniversary present. \
    I think my wife liked it so much she was speechless. \
    So far I've been the only one using it, and I've been \
    using it every other morning to clear the leaves on our lawn. \
    It's slightly more expensive than the other leaf blowers \
    out there, but I think it's worth it for the extra features.
    """

    review_template = """\
    For the following text, extract the following information:

    gift: Was the item purchased as a gift for someone else? \
    Answer True if yes, False if not or unknown.

    delivery_days: How many days did it take for the product \
    to arrive? If this information is not found, output -1.

    price_value: Extract any sentences about the value or price,\
    and output them as a comma separated Python list.

    Format the output as JSON with the following keys:
    gift
    delivery_days
    price_value

    text: {text}
    """    
    chat = ChatOpenAI(temperature=0.0, model=llm_model)

    # when you run this function, you will see the output of the model 
    # is in a json format, but it is a string, not a dictionary. In next step we will 
    #  define a schema and convert the output to a dictionary.
    def with_no_parser():
        prompt_template = ChatPromptTemplate.from_template(review_template)
        #print(prompt_template)
        messages = prompt_template.format_messages(text=customer_review)
        response = chat.invoke(messages)
        print(response.content)
        print(type(response.content))  # note the type of response is a string, not a dictionary
    
    #with_no_parser()

    # Now let's see how we can use a schema and parser. 
    #


    gift_schema = ResponseSchema(name="gift", 
                                 description="Was the item purchased as a gift for someone else? Answer True if yes, False if not or unknown.")
    delivery_days_schema = ResponseSchema(name="delivery_days", 
                                          description="How many days did it take for the product to arrive? If this information is not found, output -1.")
    price_value_schema = ResponseSchema(name="price_value", 
                                        description="Extract any sentences about the value or price, and output them as a comma separated Python list.")

    response_schemas = [gift_schema, delivery_days_schema, price_value_schema]

    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
    format_instructions = output_parser.get_format_instructions()
    #print(format_instructions)


    # Note that there is some duplication in the following template. gift is explainedin the main text and again in the format instructions.
    # There must be a way to avoid it but let's not worry about that for now. 
    review_template_2 = """\
    For the following text, extract the following information:

    gift: Was the item purchased as a gift for someone else? \
    Answer True if yes, False if not or unknown.

    delivery_days: How many days did it take for the product\
    to arrive? If this information is not found, output -1.

    price_value: Extract any sentences about the value or price,\
    and output them as a comma separated Python list.

    text: {text}

    {format_instructions}
    """

    # Finally we build a prompt that includes text and format instructions
    prompt = ChatPromptTemplate.from_template(template=review_template_2)
    messages = prompt.format_messages(text=customer_review, 
                                      format_instructions=format_instructions)

    #print(messages[0].content)  # This is the final prompt that will be sent to the model
    response = chat(messages)
    print(response.content)
    output_dict = output_parser.parse(response.content)  # This will convert the string response to a dictionary
    print('\nDictionary output:')
    pprint.pprint(output_dict)
    print(output_dict.get('delivery_days'))  # Accessing a specific key in the dictionary


#use_openai_directly()
#use_langchain_simple()
langchain_parser()