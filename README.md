# AutoMLPipeline

Represent a Python / R project as if it were a node-graph.

## Benefits (which should be maximised)
- Encapsulation of TEMPLATE/PROCESS vs PROJECT
  - Automatically roll out improvements to the TEMPLATE to every PROJECT with no extra copy/pasting
- Naturally split different tasks into different scripts without having to write much boilerplate to get it all working
- Split TEMPLATE's into smaller subprocesses, allowing further encapsulation and automagic rollout of improvements
  - NO duplication of code!
- Encapsulating objects in nodes encourages a flexible & robust structure
  - A node having more than one way to generate its contents (eg: loading from save, from backup, or rebuilding), combined with the schedulers automagic time prioritisation means the system is robust against partial failures & will be rebuilt as quickly as possible.

## Differences to just encapsulating different bits of the project in functions
- Encourages further encapsulation with needsToRun checks, leading to more modular code
  - Re-running long projects after identifying an error will naturally only re-run the needed bits without you adding more boilerplate
- Automatic project invalidation & re-run
- Easy paralellism, laying out the project in terms of dependencies allows an automatic task scheduler to easily identify situations where multiple nodes can be run at once
- Easy namespacing, each node can have arbitrary data attached to it so there are less worries about name collisions in large projects
- Easy handling of resources, if a given object/node can be saved/loaded vs regenerated, a scheduler can easily check which is fastest. For large objects/nodes a scheduler can then decide when to load/unload it intelligently.
- Easy optimisation, giving a node multiple ways to be generated with equivalent outputs (eg: loading from several potential locations), the scheduler can optimise it over time by testing each approach (no more than needed) and sticking with the fastest. No wasted time.

## Changes in thought process
- Nodes should represent objects, connections should represent ways to construct those objects
