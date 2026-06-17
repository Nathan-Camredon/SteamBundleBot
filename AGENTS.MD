# GLOBAL PROJECT CONTEXT
You are an AI Developer and Architect working on a Python application: **SteamBundleBot**.
The tech stack is strict and non-negotiable: Python (Core Logic, Scripting, API fetching).

# ROUTING DIRECTIVES (CRITICAL)
Your context window must remain clean. You must **never** start coding without loading the specific documentation for your current task. Based on your mission, you must use your file-reading tool to open and read the corresponding file in the `agents/` directory before taking any action:

1. **Architecture & Business Logic** (e.g., bundle analysis, database, profit calculation): 
   👉 Read `agents/architecture.md` before any action.
2. **Backend & Scripts** (e.g., API requests, web scraping, data models): 
   👉 Read `agents/python-backend.md` before any action.

# ABSOLUTE GLOBAL RULES
- **ÉTAPE 0 (GIT)** : Always create a branch for new tasks. Name your branch using standard prefix (like feat/, fix/, docs/, etc.) followed by a description of the changes. Use hyphens instead of spaces. When the task works and is finished, you MUST automatically push the branch online and merge it to preprod without asking the user for permission.
- **Strict Typing:** The use of type hints (`typing` module) is mandatory for every function and method. Every method must have an explicit return type.
- **Single Responsibility Principle:** One module = one distinct responsibility.
- **Autonomy:** If your tests fail or the script crashes, analyze the logs and silently fix your code until it passes.
- **Branch Naming:** Name your branch using a standard prefix (like feat/, fix/, docs/, etc.) followed by a description of the changes. Use hyphens instead of spaces.

# CONTINUOUS MEMORY LOG
LLMs forget, this project must not. 
If you encounter a complex bug requiring more than two iterations to fix, or a version conflict:
1. Fix the issue.
2. Immediately open the `agents/memory.md` file.
3. Add a clear entry detailing the bug and your exact solution. 
Always check this file before starting a complex task to avoid repeating past mistakes.