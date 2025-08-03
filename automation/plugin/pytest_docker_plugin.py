import logging

import pytest

from pytest import Config, Parser
from pytest import Session, ExitCode

from automation.plugin.docker_wrapper import DockerWrapper

PLUGIN_NAME: str = "docker_manage_plugin"


class DockerMangePlugin:
    def __init__(self, config: Config) -> None:
        """
        Initialize the DockerMangePlugin.

        Args:
            config (Config): The pytest configuration object.
        """
        self.config: Config = config
        self.container_name: str = config.getoption("--container-name")
        self.with_docker: str = config.getoption("--with-docker")
        self.action_scope: str = config.getoption("--container-scope")
        self.docker = DockerWrapper(self.container_name)

    def pytest_sessionstart(self, session: Session) -> None:
        """
        Called before the pytest session starts.

        Args:
            session (Session): The pytest session object.
        """
        if self.with_docker and self.action_scope == 'session':
            self.docker.start()
        
        logging.info("=== Pytest session started ===")

    def pytest_sessionfinish(self, session: Session, exitstatus: ExitCode) -> None:
        """
        Called after the pytest session finishes.

        Args:
            session (Session): The pytest session object.
            exitstatus (ExitCode): The exit status of the session.
        """
        if self.with_docker and self.action_scope == 'session':
            self.docker.stop()
        
        logging.info(f"=== Pytest session finished with exit --- status {exitstatus} ===")


    def pytest_runtest_setup(self, item: pytest.Item) -> None:
        """
        Called before each test is run. Used to set up any necessary state or resources.

        Args:
            item (pytest.Item): The test item about to be run.
        """
        logging.info(f"=== Setting up test: {item.name} ===")

        if self.with_docker and self.action_scope == 'test':
            logging.debug(f"=== Setting up test: {item.name} ===")
            self.docker.start()
                
    def pytest_runtest_teardown(self, item: pytest.Item) -> None:
        """
        Called after each test is run. Used to clean up any state or resources.

        Args:
            item (pytest.Item): The test item that was run.
        """
        logging.info(f"=== Tearing down test: {item.name} ===")

        if self.with_docker and self.action_scope == 'test':
            logging.debug(f"=== Setting up test: {item.name} ===")
            self.docker.stop()
            

def pytest_addoption(parser: Parser) -> None:
    parser.addoption(
        "--container-name",
        action="store",
        default='flask-reverse-api',
        help="Enable request debugging output."
    )
    parser.addoption(
        "--with-docker",
        action="store_true",
        default=False,
        help="Run tests with Docker container management."
    )
    parser.addoption(
        "--container-scope",
        choices=['session', 'test'],
        action="store",
        default='session',
        help="Run tests with Docker container management."
    )


def pytest_configure(config: Config) -> None:
    if config.getoption("--with-docker"):
        logging.debug("=== Docker management plugin enabled ===")
        config.pluginmanager.register(DockerMangePlugin(config=config), PLUGIN_NAME)


def pytest_unconfigure(config: Config) -> None:
    plugin = config.pluginmanager.getplugin(PLUGIN_NAME)
    if plugin:
        logging.debug("=== Unregistering Docker management plugin ===")
        config.pluginmanager.unregister(plugin)
