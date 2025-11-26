import os
from typing import List
from langchain_community.document_loaders import UnstructuredMarkdownLoader, TextLoader, JSONLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

class KnowledgeBase:
    def __init__(self):
        self.vectorstore = None
        self.retriever = None
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0) 

    def build_knowledge_base(self, file_paths: List[str]):
        documents = []
        for path in file_paths:
            if path.endswith(".md"):
                loader = UnstructuredMarkdownLoader(path)
            elif path.endswith(".json"):
                loader = TextLoader(path)
            else:
                loader = TextLoader(path)
            documents.extend(loader.load())

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splits = text_splitter.split_documents(documents)

        persist_directory = "chroma_db"
        self.vectorstore = Chroma.from_documents(
            documents=splits, 
            embedding=GoogleGenerativeAIEmbeddings(model="models/embedding-001"),
            persist_directory=persist_directory
        )
        self.retriever = self.vectorstore.as_retriever()

    def generate_test_cases(self, query: str):
        if not self.retriever:
            return "Error: Knowledge Base not built. Please upload documents first."

        template = """You are an expert QA Engineer.
        Based on the following context from project documentation, generate comprehensive test cases for the user's request.
        
        Context:
        {context}
        
        Request: {question}
        
        Output Format:
        Provide a list of test cases in Markdown format. Each test case should include:
        - Test ID
        - Feature
        - Test Scenario
        - Expected Result
        - Grounded In (Reference the specific document or rule)
        
        Strictly base your test cases on the provided context. Do not hallucinate features.
        """
        prompt = ChatPromptTemplate.from_template(template)
        
        rag_chain = (
            {"context": self.retriever, "question": RunnablePassthrough()}
            | prompt
            | self.llm
            | StrOutputParser()
        )
        
        return rag_chain.invoke(query)

    def generate_selenium_script(self, test_case: str, html_content: str):
        if not self.retriever:
             # Even for script gen, we might want to retrieve context, but the prompt says 
             # "Retrieve relevant documentation snippets from the vector DB"
             pass

        # Retrieve relevant docs for the test case to ensure we know the rules (e.g. what is a valid input)
        # We can use the test case description itself as a query
        docs = self.retriever.get_relevant_documents(test_case)
        context_text = "\n\n".join([d.page_content for d in docs])

        template = """You are an expert Selenium Automation Engineer using Python.
        
        Task: Generate a robust, runnable Selenium Python script for the following test case.
        
        Test Case:
        {test_case}
        
        Target HTML Page Source:
        {html_content}
        
        Relevant Documentation Context:
        {context}
        
        Requirements:
        1. Use `webdriver.Chrome()` (assume chromedriver is in PATH).
        2. Use explicit waits (`WebDriverWait`) for stability.
        3. Use appropriate selectors based on the provided HTML (ID, CSS, XPath).
        4. Include assertions to verify the Expected Result.
        5. The script should be complete and runnable.
        6. Handle potential errors gracefully.
        
        Output only the Python code block.
        """
        prompt = ChatPromptTemplate.from_template(template)
        
        chain = (
            prompt 
            | self.llm 
            | StrOutputParser()
        )
        
        return chain.invoke({
            "test_case": test_case,
            "html_content": html_content,
            "context": context_text
        })
