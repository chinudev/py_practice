from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import CSVLoader
from langchain.vectorstores import DocArrayInMemorySearch
from IPython.display import display, Markdown
from langchain.llms import OpenAI

llm_model = "gpt-3.5-turbo"

file = 'OutdoorClothingCatalog_1000.csv'
loader = CSVLoader(file_path=file)
docs = loader.load()
print(docs[0])

from langchain.embeddings import OpenAIEmbeddings
embeddings = OpenAIEmbeddings()

# Create an embedding for a simple text
#embed = embeddings.embed_query("What is the capital of France?")
#print(len(embed), embed[0:5])    # Note we have 1536 dimensions in the embedding.

# Let's convert all the entries in the docs to embeddings and store in a db
db = DocArrayInMemorySearch.from_documents(
    docs, 
    embeddings
)

# Let's find entries in db that have similar embedding score 
query = "Please suggest a shirt with sunblocking"

# If we were doing this manually, we can find documents with similar embeddings and feed them 
#  to the LLM for a response.
def manual_run():
    docs = db.similarity_search(query)
    print(len(docs), docs[0])
    llm = ChatOpenAI(temperature = 0.0, model=llm_model)
    qdocs = "".join([docs[i].page_content for i in range(len(docs))])
    response = llm.call_as_llm(f"{qdocs} Question: Please list all your \
    shirts with sun protection in a table in markdown and summarize each one.") 
    display(Markdown(response))

#manual_run()   # didn't display a table.. probably markdown doesn't work on command line. may need Jupyter lab 

def retrieval_qa():
    retriever = db.as_retriever()
    llm = ChatOpenAI(temperature = 0.0, model=llm_model)
    qa_stuff = RetrievalQA.from_chain_type(
        llm=llm, 
        chain_type="stuff", 
        retriever=retriever, 
        verbose=True
    )
    query =  "Please list all your shirts with sun protection in a table and summarize each one."
    response = qa_stuff.run(query)
    print(response)
    
    qa = RetrievalQA.from_chain_type(llm=ChatOpenAI(temperature=0.0, model=llm_model), chain_type="stuff", retriever=retriever)
    response = qa.run(query)
    display(Markdown(response))

exit()

# We are going to use an in-memory vector store 
from langchain.indexes import VectorstoreIndexCreator
from langchain.embeddings import OpenAIEmbeddings


# Create embeddings using OpenAI's model. I picked the cheapest but you can 
#  see the other models at https://platform.openai.com/docs/guides/embeddings/embedding-models
embeddings = OpenAIEmbeddings(model="text-embedding3-small")  
# Create the vector store index
index = VectorstoreIndexCreator(embedding=embeddings, vectorstore_cls=DocArrayInMemorySearch).from_loaders([loader])
query ="Please list all your shirts with sun protection \
in a table in markdown and summarize each one."

llm_replacement_model = OpenAI(temperature=0, model='gpt-3.5-turbo-instruct')
response = index.query(query, llm = llm_replacement_model)
print(display(Markdown(response)))  # Display the response in markdown format

