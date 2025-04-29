import json
import asyncio
import os
import shutil
from typing import Dict, Any, Optional, List
from concurrent.futures import ThreadPoolExecutor


class UtilityManager:
    def __init__(self, max_workers: Optional[int] = None):
        """
        Initialize the UtilityManager with optional thread pool size.

        Args:
            max_workers: Maximum number of worker threads to use for parallel processing
        """
        self.executor = ThreadPoolExecutor(max_workers=max_workers)

    def structure_json(self, result: Optional[str]) -> Dict[str, Any]:
        """Synchronous implementation of structure_json for use with executor"""
        # Handle None result
        if result is None:
            return {"error": "No response received", "raw_response": None}

        # Try to extract JSON from the response
        try:
            # Find JSON pattern in the response
            start_idx = result.find("{")
            end_idx = result.rfind("}") + 1

            if start_idx >= 0 and end_idx > start_idx:
                json_str = result[start_idx:end_idx]
                structured_result = json.loads(json_str)
                return structured_result
            else:
                return {
                    "error": "Could not extract JSON from response",
                    "raw_response": result,
                }
        except json.JSONDecodeError:
            return {"error": "Invalid JSON in response", "raw_response": result}
        except AttributeError:
            # This handles the case where result is not a string but some other type
            return {
                "error": f"Expected string but got {type(result).__name__}",
                "raw_response": str(result),
            }

    async def structure_json_async(self, result: Optional[str]) -> Dict[str, Any]:
        """
        Asynchronously structure a JSON string response.

        Args:
            result: String containing JSON or None

        Returns:
            Structured JSON as a dictionary
        """
        # Check if result is a coroutine (happens if someone passes an awaitable)
        if asyncio.iscoroutine(result):
            raise TypeError(
                "Expected a string or None, but received a coroutine. "
                "Make sure to await any async functions before passing their results."
            )

        # Use run_in_executor to run the CPU-bound JSON parsing in a separate thread
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(self.executor, self.structure_json, result)

    async def structure_jsons_parallel(
        self, results: List[Optional[str]]
    ) -> List[Dict[str, Any]]:
        """
        Process multiple JSON responses in parallel.

        Args:
            results: List of strings containing JSON or None

        Returns:
            List of structured JSON dictionaries
        """
        # Check each item in the list to ensure none are coroutines
        for i, result in enumerate(results):
            if asyncio.iscoroutine(result):
                raise TypeError(
                    f"Item at index {i} is a coroutine. "
                    "Make sure to await any async functions before passing their results."
                )

        # Process all results in parallel using gathered tasks
        tasks = [self.structure_json_async(result) for result in results]
        return await asyncio.gather(*tasks)

    async def structure_json_batch(
        self, results: List[Optional[str]], batch_size: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Process JSON responses in batches to control concurrency.

        Args:
            results: List of strings containing JSON or None
            batch_size: Number of items to process concurrently

        Returns:
            List of structured JSON dictionaries
        """
        all_results = []

        # Process in batches to avoid overwhelming resources
        for i in range(0, len(results), batch_size):
            batch = results[i : i + batch_size]
            batch_results = await self.structure_jsons_parallel(batch)
            all_results.extend(batch_results)

        return all_results

    def delete_folder_if_exists(self, folder_path: str):
        if os.path.exists(folder_path):
            try:
                shutil.rmtree(folder_path)
                print(f"Folder '{os.path.relpath(folder_path)}' deleted successfully.")
            except Exception as e:
                print(f"Error deleting folder '{folder_path}': {e}")
        else:
            print(f"Folder '{os.path.relpath(folder_path)}' does not exist.")

    def close(self):
        """Clean up resources by shutting down the thread pool executor"""
        self.executor.shutdown(wait=True)

    async def __aenter__(self):
        """Support for async context manager"""
        return self

    async def __aexit__(self):
        """Clean up resources when exiting async context"""
        self.close()
