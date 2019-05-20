from typing import TypeVar

SchedulerType = TypeVar("SchedulerType")


class Scheduler(SchedulerType):

    def __init__(self, nodes):
        self._nodes = nodes

    # Basic initial implementation
    # TODO: Change execution order so dependencies come first
    # TODO: Change Node so update_dependencies_status doesn't need running constantly
    # TODO: Change execution order so nodes with time-dependent dependencies are run first
    # TODO: Change execution order based on priority + time spent (maybe fastest first is a good rule of thumb?)
    def run_graph(self):
        # Update each nodes internal state
        for i in self._nodes:
            i.update_dependencies_status()

        # Run any nodes which can & should be run
        for i in self._nodes:
            if i.should_run():
                if i.can_run():
                    i.run()
