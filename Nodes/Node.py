from typing import TypeVar

NodeType = TypeVar("NodeType")


class Node(NodeType):

    def __init__(self):
        # Can have an arbitrary number of dependencies (other nodes):
        self._dependencies = {}  # Dependencies should be accessible by name
        self._dependencies_last_run_time = {}  # Tracks when each dependency was last run
        self._dependencies_maximum_oldness = {}  # If they're older than this -> re-run them

        # Contains code to do *something* with those inputs
        self._input_validation = None  # A function to check any non Node dependencies look correct
        self._action = None  # A function to call when it should run
        self._output_validation = None  # A function to check if the output is as expected
        self._result = None  # The result of _action (or a node which points to the result, eg: a file)
        self.last_run_time = None  # When _action was run last

        # Contains an internal "Schedule" determining when it will try to run _action
        self._run_on_dependency_change = False
        self._run_repeatedly = False
        self._run_delay = None
        self._next_scheduled_run = None

        # Contains an internal *history* of stuff it's done / tried to do (and how long it took)
        self._historic_run_times = None  # When each run was done before
        self._historic_run_durations = None  # How long each run took
        self._historic_run_successes = None  # Whether each historic run was a success or not

    # Add another Node as a dependency
    def add_dependency(self, name: str, x: NodeType, max_oldness: str) -> None:
        self._dependencies[name] = x
        self._dependencies_last_run_time[name] = x.last_run_time
        self._dependencies_maximum_oldness = max_oldness

    def check_dependencies(self):
        for i in self._dependencies.keys():


    def run(self):
        self.check_dependencies()
        # TODO: RUN IF VALID DEPENDENCIES