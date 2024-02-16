import argparse
import logging
from abc import ABC, abstractmethod

class BaseScript(ABC):
    def __init__(self):
        self.setup_logging()
        self.parser = argparse.ArgumentParser(description=self.description())
        self.define_arguments()
        self.args = self.parser.parse_args()
    
    @abstractmethod
    def description(self):
        """Return a description of the script."""
        pass

    @abstractmethod
    def define_arguments(self):
        """Define command-line arguments the script accepts."""
        pass
    
    @abstractmethod
    def run(self):
        """The main logic of the script."""
        pass

    def setup_logging(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def execute(self):
        """Execute the script based on the parsed arguments."""
        self.run()
