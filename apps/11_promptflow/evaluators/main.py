import argparse
import logging
from enum import Enum
from os import getenv
from pathlib import Path

from dotenv import load_dotenv
from promptflow.client import load_flow
from promptflow.core import AzureOpenAIModelConfiguration
from promptflow.evals.evaluate import evaluate
from promptflow.evals.evaluators import RelevanceEvaluator

BASE_DIR = Path(__file__).absolute().parent


class EvaluatorType(Enum):
    RELEVANCE = "relevance"
    ANSWER_LENGTH = "answer_length"
    APOLOGY = "apology"
    DATASET = "dataset"


def init_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="run_evaluators",
        description="Evaluate with the prompt flow SDK",
    )
    parser.add_argument(
        "-t",
        "--type",
        default=EvaluatorType.RELEVANCE.value,
        choices=[t.value for t in EvaluatorType],
        help="Evaluator type",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose mode",
    )
    return parser.parse_args()


def run_relevance_evaluator(model_config):
    relevance_eval = RelevanceEvaluator(model_config)

    relevance_score = relevance_eval(
        answer="The Alpine Explorer Tent is the most waterproof.",
        context="From the our product list,"
        " the alpine explorer tent is the most waterproof."
        " The Adventure Dining Table has higher weight.",
        question="Which tent is the most waterproof?",
    )

    print(relevance_score)


class AnswerLengthEvaluator:
    def __init__(self):
        pass

    def __call__(self, *, answer: str, **kwargs):
        return {"answer_length": len(answer)}


def run_answer_length_evaluator():
    evaluator = AnswerLengthEvaluator()
    answer_length = evaluator(answer="What is the speed of light?")
    print(answer_length)


def get_apology_evaluator(model_config):
    return load_flow(
        source=f"{BASE_DIR}/apology.prompty",
        model={"configuration": model_config},
    )


def run_apology_evaluator(model_config):
    apology_eval = get_apology_evaluator(model_config)

    # load apology evaluator from prompty file using promptflow
    apology_score = apology_eval(
        question="Where can I get my car fixed?",
        answer="I'm sorry, I don't know that. Would you like me to look it up for you? Sorry for the inconvenience.",
    )
    print(apology_score)


def run_test_dataset(model_config):
    result = evaluate(
        data=f"{BASE_DIR}/data.jsonl",  # provide your data here
        evaluators={
            EvaluatorType.RELEVANCE.value: RelevanceEvaluator(model_config),
            EvaluatorType.ANSWER_LENGTH.value: AnswerLengthEvaluator(),
            EvaluatorType.APOLOGY.value: get_apology_evaluator(model_config),
        },
        # column mapping
        evaluator_config={
            "default": {"ground_truth": "${data.ground_truth}"},
        },
        # Optionally provide an output path to dump a json of metric summary, row level data and metric and studio URL
        output_path=f"{BASE_DIR}/results.json",
    )
    print(result)


if __name__ == "__main__":
    args = init_args()

    # Set verbose mode
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)

    load_dotenv()

    model_config = AzureOpenAIModelConfiguration(
        azure_endpoint=getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=getenv("AZURE_OPENAI_API_KEY"),
        azure_deployment=getenv("AZURE_OPENAI_GPT_MODEL"),
        api_version=getenv("AZURE_OPENAI_API_VERSION"),
    )

    if args.type == EvaluatorType.RELEVANCE.value:
        run_relevance_evaluator(model_config)
    elif args.type == EvaluatorType.ANSWER_LENGTH.value:
        run_answer_length_evaluator()
    elif args.type == EvaluatorType.APOLOGY.value:
        run_apology_evaluator(model_config)
    elif args.type == EvaluatorType.DATASET.value:
        run_test_dataset(model_config)
    else:
        print(f"Invalid evaluator type {args.type}")
        print(f"Please choose from {', '.join([t.value for t in EvaluatorType])}")
        exit(1)
