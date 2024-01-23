# VidioPy's Contribution Guidelines

## Communication on GitHub

- Keep discussions on GitHub issues and pull requests focused and concise. Remember that each comment triggers a notification for multiple people.
- Before making significant changes to the core codebase, discuss them with the team.

## Setting Up Your Development Environment

- Fork the official VidioPy repository to your own GitHub account.
- Clone the forked repository to your local machine.
- Create and activate a Python virtual environment to isolate the project dependencies.
- Navigate to the cloned directory and run `pip install -e .` to install the project dependencies.
- Regularly sync your local repository with the main repository to stay up-to-date with the latest changes.

## Coding Standards and Code Quality

- Adhere to the [PEP8](https://www.python.org/dev/peps/pep-0008/) coding conventions for Python.
- Use comments judiciously and only when necessary. Aim to write self-explanatory code.
- Choose clear and descriptive names for variables, functions, and classes.
- Document new features or bug fixes with docstring. Update the documentation in the `docs/markdown/` directory as needed.
- Use Prettier to maintain consistent code formatting.
- Review your code in PyCharm or VSCode to catch potential edge cases.
- When adding new functions or features, update the corresponding unit tests or mention the need for new tests in your pull request.

## Submitting Pull Requests

- You can submit a pull request (PR) even if your work is still in progress; it doesn't have to be fully finished.
- Before submitting your PR, run the test suite using pytest to ensure your changes haven't broken anything.
- Provide a clear and detailed description of your changes when submitting your PR. This will help the reviewers understand your work and expedite the review process.
