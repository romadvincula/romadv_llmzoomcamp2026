"""Starter code for the monitoring homework.

Sets up the text-search RAG from homework 1 and a shared OpenAI client.
"""

from openai import OpenAI

from gitsource import GithubRepositoryDataReader
from minsearch import Index

from rag_helper import RAGBase


class RAGTraced(RAGBase):
    def __init__(self, tracer, **kwargs):
        super().__init__(**kwargs)
        self.tracer = tracer

    def search(self, **kwargs):
        # extend search method a tracer
        with self.tracer.start_as_current_span("search") as span:
            return super().search(**kwargs)
        
    def llm(self, prompt):
        # extend llm
        with self.tracer.start_as_current_span("llm") as span:
            response = super().llm(prompt)
            usage = response.usage
            total_cost = self.calc_total_cost(usage)
            span.set_attribute("input_tokens", usage.input_tokens)
            span.set_attribute("output_tokens", usage.output_tokens)
            span.set_attribute("cost", total_cost)
            return response

    def rag(self, query):
        with self.tracer.start_as_current_span("rag") as span:
            search_results = self.search(query=query)
            prompt = super().build_prompt(query, search_results)
            response = self.llm(prompt)
            span.set_attribute("output_text", response.output_text)
            return response.output_text
        
    def calc_total_cost(self, usage):
        input_price_per_million = 0.75
        output_price_per_million = 4.50

        input_cost = (usage.input_tokens / 1_000_000) * input_price_per_million
        output_cost = (usage.output_tokens / 1_000_000) * output_price_per_million
        total_cost = input_cost + output_cost

        return total_cost


COMMIT = "8c1834d"

# --- Load the course lessons (same as HW1, HW2, HW4) ---
reader = GithubRepositoryDataReader(
    repo_owner="DataTalksClub",
    repo_name="llm-zoomcamp",
    commit_id=COMMIT,
    allowed_extensions={"md"},
    filename_filter=lambda path: "/lessons/" in path,
)
documents = [file.parse() for file in reader.read()]

index = Index(text_fields=["content"], keyword_fields=["filename"])
index.fit(documents)

client = OpenAI()
rag = RAGBase(index=index, llm_client=client)

if __name__ == "__main__":
    query = "How does the agentic loop keep calling the model until it stops?"
    answer = rag.rag(query)
    print(answer)
