import os
import argparse
import time

import asyncio
from modules.agent import ArticleProcessorAgent
from config import INPUT_FOLDER, PROCESSED_FOLDER, RESPONSE_STRUCTURE
from utils import UtilityManager


class ArticleProcessor:
    def __init__(self):
        self.agent = ArticleProcessorAgent()
        self.utility_manager = UtilityManager()


async def main():
    start_time = time.perf_counter()  # ⏱ Start timing
    parser = argparse.ArgumentParser(
        prog="Article Processor",
    )
    parser.add_argument("-n", "--name", type=str, default="article")
    parser.add_argument(
        "-p",
        "--parallel",
        type=int,
        default=1,
        help="Number of articles to process in parallel",
    )
    args = parser.parse_args()

    processor = ArticleProcessor()

    # Cleanup
    processor.utility_manager.delete_folder_if_exists(PROCESSED_FOLDER)

    if args.parallel > 1 and os.path.isdir(os.path.join(INPUT_FOLDER, args.name)):
        # Process multiple articles in parallel
        article_dir = os.path.join(INPUT_FOLDER, args.name)
        tasks = []

        for file in os.listdir(article_dir):
            if file.endswith(".png"):
                base_name = file[:-4]  # Remove .png extension
                image_path = os.path.join(article_dir, file)
                xml_path = os.path.join(article_dir, f"{base_name}.xml")

                if os.path.exists(xml_path):
                    # Create a task for each article
                    task = processor.agent.process_article(
                        image_path,
                        xml_path,
                        args.name,
                        RESPONSE_STRUCTURE,
                        PROCESSED_FOLDER,
                    )
                    tasks.append(task)

                    # Process in batches based on parallel argument
                    if len(tasks) >= args.parallel:
                        await asyncio.gather(*tasks)
                        tasks = []
                else:
                    print("Associate XML file not found")

        # Process any remaining tasks
        if tasks:
            await asyncio.gather(*tasks)
    else:
        # Process single article
        await processor.agent.process_article(
            os.path.join(INPUT_FOLDER, f"{args.name}.png"),
            os.path.join(INPUT_FOLDER, f"{args.name}.xml"),
            args.name,
            RESPONSE_STRUCTURE,
            PROCESSED_FOLDER,
        )

    end_time = time.perf_counter()  # ⏱ End timing
    elapsed_time = end_time - start_time

    print(
        f"✅ Processing complete in {elapsed_time:.2f} seconds.\nOutput saved to the artifacts folder."
    )


if __name__ == "__main__":
    asyncio.run(main())
