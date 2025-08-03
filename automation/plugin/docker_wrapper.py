"""
DockerWrapper Utility

This module provides a utility class for managing Docker containers used in pytest sessions or tests.

Functions:
    _with_retry(retry_on_result, function, *func_args, **func_kwargs):
        Retry a function call with exponential backoff based on result or exception.
        
        Args:
            retry_on_result (Callable[[Any], bool]): Function to determine if a retry is needed based on result.
            function (Callable): The function to call.
            *func_args: Positional arguments for the function.
            **func_kwargs: Keyword arguments for the function.
        Returns:
            Any: The result of the function call.
    
    _run_command(args):
        Run a shell command and return its output as a string.
        
        Args:
            args (list[str]): Bash command as list of strings.
        Returns:
            str: The command output.

Classes:
    DockerWrapper:
        Encapsulates Docker container management logic (start, stop, status).
        
        Args:
            container_name (str): Name of the Docker image/container to manage.
            port (str, optional): Port mapping for the container (default: "8000:8000").
        
        Methods:
            _get_container_id():
                Get the container ID of the running container.
                Returns:
                    str: The container ID or empty string if not running.
            _run_container():
                Run the Docker container.
                Returns:
                    str: The container ID of the started container.
            _stop_container(container_id):
                Stop the running Docker container.
                Args:
                    container_id (str): The ID of the container to stop.
                Returns:
                    str: The output of the stop command.
            start():
                Start the container if not already running.
                Returns:
                    str: The container ID.
            stop():
                Stop the container if running.
                Returns:
                    str: The container ID.
"""

import logging
import subprocess
from collections.abc import Callable
import time
from typing import Any

from retrying import Retrying

PLUGIN_NAME = "docker_manage_plugin"


def _with_retry(retry_on_result: Callable[[Any], bool], function: Callable, *func_args, **func_kwargs) -> Any:
    """
    Retry a function call with exponential backoff based on result or exception.

    Args:
        retry_on_result (Callable[[Any], bool]): Function to determine if a retry is needed based on result.
        function (Callable): The function to call.
        *func_args: Positional arguments for the function.
        **func_kwargs: Keyword arguments for the function.
    Returns:
        Any: The result of the function call.
    """
    retry_func: Retrying = Retrying(
        retry_on_exception=lambda err: isinstance(err, ValueError),
        retry_on_result=retry_on_result,
        wait_exponential_multiplier=1000,
        wait_exponential_max=10000,
        before_attempts=lambda *args, **kwargs: logging.debug("Before attempts Data args={args}, kwargs={kwargs}")
    )

    return retry_func.call(function, *func_args, **func_kwargs)


def _run_command(args: list[str]) -> str:
    """
    Run a shell command and return its output as a string.

    Args:
        args (list[str]): Bash command as list of strings.
    Returns:
        str: The command output.
    """
    try:
        result = subprocess.run(args, check=True, capture_output=True, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        logging.error(f"Command failed: {' '.join(args)}\nError: {e.stderr.strip()}", exc_info=True)
    
    return ""


class DockerWrapper:

    def __init__(self, container_name: str, port: str = "8000:8000"):
        """
        Initialize the DockerWrapper.

        Args:
            container_name (str): Name of the Docker image/container to manage.
            port (str, optional): Port mapping for the container (default: "8000:8000").
        """
        self.container_name = container_name
        self.port = port
       
    def _get_container_id(self) -> str:
        """
        Get the container ID of the running container for the specified image.

        Returns:
            str: The container ID if running, otherwise an empty string.
        """

        return _run_command(["docker", "ps", "-q", "--filter", f"ancestor={self.container_name}"])

    def _run_container(self) -> str:
        """
        Run the Docker container for the specified image and port.

        Returns:
            str: The container ID of the started container.
        """

        return _run_command(["docker", "run", "-d", "-p", self.port, self.container_name])

    def _stop_container(self, container_id: str) -> str:
        """
        Stop the running Docker container.

        Args:
            container_id (str): The ID of the container to stop.
        Returns:
            str: The output of the stop command.
        """

        return _run_command(["docker", "stop", container_id])

    def start(self) -> str:
        """
        Start the Docker container if not already running.

        Returns:
            str: The container ID.
        """
        container_id: str = self._get_container_id()

        if not container_id:
            logging.debug(f"Starting new docker {self.container_name}")
            self._run_container()
            time.sleep(2.5)  # Wait for the container to be fully up
            _with_retry(lambda result: result == '', self._get_container_id)
            logging.debug(f"=== Docker container '{self.container_name}' started with ID: {container_id} ===")
        else:
            logging.debug(f"=== Docker container '{self.container_name}' already running ID: {container_id} ===")

        return container_id

    def stop(self) -> str:
        """
        Stop the Docker container if running.

        Returns:
            str: The container ID.
        """
        logging.debug("=== Stopping Docker container management ===")
        container_id = self._get_container_id()

        if container_id:
            logging.debug(f"=== Sending topt to '{self.container_name}'")
            self._stop_container(container_id)
            time.sleep(1.5)  # Wait for the container to be fully up
            logging.debug(f"=== Wait for container {container_id} to stop ===")
            _with_retry(lambda result: result != '', self._get_container_id)
            logging.debug(f"=== Docker container '{self.container_name}' stopped with ID: {container_id} ===")
        else:
            logging.debug(f"=== No running Docker container found with name '{self.container_name}' ===")
    
        return container_id
