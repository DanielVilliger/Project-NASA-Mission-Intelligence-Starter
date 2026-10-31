from ragas import EvaluationDataset
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from typing import Dict, List, Optional

# RAGAS imports
try:
    from ragas import SingleTurnSample
    from ragas.metrics import BleuScore, NonLLMContextPrecisionWithReference, ResponseRelevancy, Faithfulness, RougeScore
    from ragas import evaluate
    RAGAS_AVAILABLE = True
except ImportError:
    RAGAS_AVAILABLE = False

def evaluate_response_quality(question: str, answer: str, contexts: List[str]) -> Dict[str, float]:
    """Evaluate response quality using RAGAS metrics"""
    if not RAGAS_AVAILABLE:
        return {"error": "RAGAS not available"}
    
    # TODO: Create evaluator LLM with model gpt-3.5-turbo
    # TODO: Create evaluator_embeddings with model test-embedding-3-small
    # TODO: Define an instance for each metric to evaluate
    # TODO: Evaluate the response using the metrics
    # TODO: Return the evaluation results
    evaluator_llm = LangchainLLMWrapper(ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0,api_key="voc-58605238812667755290396ae080fde1b701.41181315",base_url="https://openai.vocareum.com/v1"))
    evaluator_embeddings = LangchainEmbeddingsWrapper(OpenAIEmbeddings(model="text-embedding-3-small",api_key="voc-58605238812667755290396ae080fde1b701.41181315",base_url="https://openai.vocareum.com/v1"))
    metrics = [
        BleuScore(),
        NonLLMContextPrecisionWithReference(),
        ResponseRelevancy(evaluator_llm,embeddings=evaluator_embeddings),
        Faithfulness(evaluator_llm),
        RougeScore()
        ]
    sample = SingleTurnSample(
        user_input=question,
        response=answer,
        reference_contexts=contexts,
        retrieved_contexts=contexts,
        reference=" ".join(contexts),)
    results = evaluate(dataset=EvaluationDataset(samples=[sample]), metrics=metrics)
    return results.scores[0]

scores = evaluate_response_quality("question", "answer", ["context"])
print(scores)

