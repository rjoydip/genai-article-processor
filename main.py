import os
import argparse

from modules.agent import ArticleProcessorAgent
from config import INPUT_FOLDER, PROCESSED_FOLDER, RESPONSE_STRUCTURE


class ArticleProcessor:
    def __init__(self):
        self.agent = ArticleProcessorAgent()


def main():
    parser = argparse.ArgumentParser(
        prog="Article Processor",
    )

    parser.add_argument("-n", "--name", type=str, default="article")

    args = parser.parse_args()

    # Choose whether to use the agent or not
    processor = ArticleProcessor()

    processor.agent.process_article(
        os.path.join(INPUT_FOLDER, f"{args.name}.png"),
        os.path.join(INPUT_FOLDER, f"{args.name}.xml"),
        RESPONSE_STRUCTURE,
        PROCESSED_FOLDER,
    )

    print("Processing complete. Output saved to the artifacts folder.")


if __name__ == "__main__":
    main()
