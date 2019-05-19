import datetime
from typing import TypeVar

NodeType = TypeVar("NodeType")


class Node(NodeType):

    def __init__(self):
        # Can have an arbitrary number of dependencies (other nodes):
        self._dependencies = {}  # Dependencies should be accessible by name
        self._dependencies_last_run_time = {}  # Tracks when each dependency was last run
        self._dependencies_last_run_time_used = {}  # Tracks when the last version this Node actually used was
        self._dependencies_maximum_oldness = {}  # If they're older than this -> re-run them
        self._dependencies_changed_since_last_run = {}  # If they've changed since we've last run
        self._dependencies_change_triggers_run = {}  # Whether each dependency changes means we should re-run this node

        # Contains code to do *something* with those inputs
        self._input_validation = None  # A function to check any non Node dependencies look correct (False if wrong)
        self._action = None  # A function to call when it should run
        self._output_validation = None  # A function to check if the output is as expected
        self._result = None  # The result of _action (or a node which points to the result, eg: a file)
        self.last_run_time = None  # When _action was run last
        self.last_run_successful = False  # Whether _output_validation passed last time we attempted to run this node

        # Contains an internal "Schedule" determining when it will try to run _action
        self._run_repeatedly = False
        self._run_delay = None
        self._next_scheduled_run = None

        # Contains an internal *history* of stuff it's done / tried to do (and how long it took)
        self._historic_run_times = []  # When each run was done before
        self._historic_run_durations = []  # How long each run took
        self._historic_run_successes = []  # Whether each historic run was a success or not

    # Add another Node as a dependency
    def add_dependency(self, name: str, x: NodeType, max_oldness: str, change_triggers_run: bool) -> None:
        self._dependencies[name] = x
        self._dependencies_last_run_time[name] = x.last_run_time
        self._dependencies_last_run_time_used[name] = None
        self._dependencies_maximum_oldness[name] = max_oldness
        self._dependencies_changed_since_last_run[name] = None
        self._dependencies_change_triggers_run[name] = change_triggers_run

    # Check if any dependencies have changed since our last run
    def update_dependencies_status(self):
        for i in self._dependencies.keys():
            if self._dependencies[i].last_run_time != self._dependencies_last_run_time[i]:
                self._dependencies_changed_since_last_run[i] = True
                self._dependencies_last_run_time[i] = self._dependencies[i].last_run_timea

    # Check if this node CAN run (dependencies have run successfully and inputs are valid
    def can_run(self):
        # Check each dependency has run successfully
        for i in self._dependencies.keys():
            if not self._dependencies[i].last_run_successful:
                return False
        # Check the _input_validation function also passes True
        return self._input_validation()

    # Check if this node SHOULD be run according to its triggers / schedule
    def should_run(self):
        for i in self._dependencies.keys():
            # If any dependencies are too old, we shouldn't update this node until they get re-run
            if self._dependencies_last_run_time_used[i] < \
                    datetime.datetime.now() - self._dependencies_maximum_oldness[i]:
                return False
            # If we have a run scheduled
            if self._next_scheduled_run <= datetime.datetime.now():
                return True
            # Any dependencies which have changed + trigger a re-run
            if self._dependencies_change_triggers_run[i] and self._dependencies_changed_since_last_run[i]:
                return True
        return False

    # Run the actual task :)
    def run(self):
        run_time_start = datetime.datetime.now()  # For calculating how long the run takes
        self._result = self._action()  # Actually run the node
        self.last_run_time = datetime.datetime.now()  # Set last run time to AFTER the process has finished
        self.last_run_successful = self._output_validation(self._result)  # Record whether the result passes validation
        run_time_duration = self.last_run_time - run_time_start  # Calculate how long the run took

        self._historic_run_times = self._historic_run_times.append(self.last_run_time)
        self._historic_run_durations = self._historic_run_durations.append(run_time_duration)
        self._historic_run_successes = self.last_run_successful

        # Schedule the next run
        if self._run_repeatedly:
            self._next_scheduled_run = self.last_run_time + self._run_delay
