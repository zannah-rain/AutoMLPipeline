import Classes.Node


# *Node* assumes that the output of a Node will be overwritten next time the node is run
# This class is for tasks which when run again may *improve* the previous result rather than starting again
# Eg: Continuing a grid search if the Scheduler has nothing urgent to do
class RepeatableNode(Classes.Node):
    pass
