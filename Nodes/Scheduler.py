class Scheduler:

    def __init__(self, nodes):
        self._nodes = nodes

    def run_graph(self):
        # Update each nodes internal state
        for i in self._nodes:
            i.update_dependencies_status()

        # Run any nodes which can & should be run
        for i in self._nodes:
            if i.should_run():
                if i.can_run():
                    i.run()
