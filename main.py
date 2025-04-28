import os
import argparse

from modules.agent import ArticleProcessorAgent
from config import INPUT_FOLDER, PROCESSED_FOLDER, RESPONSE_STRUCTURE
from utils import UtilityManager


class ArticleProcessor:
    def __init__(self):
        self.agent = ArticleProcessorAgent()
        self.utility_manager = UtilityManager()


def main():

    parser = argparse.ArgumentParser(
        prog="Article Processor",
    )
    parser.add_argument("-n", "--name", type=str, default="article")
    args = parser.parse_args()

    # Choose whether to use the agent or not
    processor = ArticleProcessor()

    # Cleanup
    processor.utility_manager.delete_folder_if_exists(PROCESSED_FOLDER)

    processor.agent.process_article(
        os.path.join(INPUT_FOLDER, f"{args.name}.png"),
        os.path.join(INPUT_FOLDER, f"{args.name}.xml"),
        RESPONSE_STRUCTURE,
        PROCESSED_FOLDER,
    )

    print("Processing complete. Output saved to the artifacts folder.")


if __name__ == "__main__":
    main()
