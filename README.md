# AutoMLPipeline

Represent a Python / R project as if it were a node-graph.

# Benefits (which should be maximised)
- Encapsulation of TEMPLATE/PROCESS vs PROJECT
  - Automatically roll out improvements to the TEMPLATE to every PROJECT with no extra copy/pasting
- Naturally split different tasks into different scripts without having to write much boilerplate to get it all working
- Split TEMPLATE's into smaller subprocesses, allowing further encapsulation and automagic rollout of improvements
  - NO duplication of code!

# Differences to just encapsulating different bits of the project in functions
- Encourages further encapsulation with needsToRun checks, leading to more modular code
  - Re-running long projects after identifying an error will naturally only re-run the needed bits without you adding more boilerplate
- Automatic project invalidation & re-run
- Easy paralellism, laying out the project in terms of dependencies allows an automatic task scheduler to easily identify situations where multiple nodes can be run at once
- Easy namespacing, each node can have arbitrary data attached to it so there are less worries about name collisions in large projects
