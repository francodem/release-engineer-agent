Contributing
============

Thank you for your interest in contributing to Release Engineer Agent! 
This document provides guidelines and instructions for contributing.

Getting Started
---------------

1. Fork the repository
2. Clone your fork::

      git clone https://github.com/your-username/release-engineer-agent.git
      cd release-engineer-agent

3. Create a branch for your changes::

      git checkout -b feature/your-feature-name

4. Make your changes
5. Test your changes
6. Submit a pull request

Development Setup
----------------

1. Create a virtual environment::

      python -m venv venv
      source venv/bin/activate  # On Windows: venv\Scripts\activate

2. Install dependencies::

      pip install -r requirements.txt

3. Install development dependencies::

      pip install -r requirements-dev.txt

4. Run tests::

      pytest

Code Style
----------

* Follow PEP 8 style guidelines
* Use type hints where appropriate
* Write docstrings for all public functions and classes
* Keep functions focused and single-purpose
* Write meaningful variable and function names

Commit Messages
---------------

Write clear, descriptive commit messages:

* Use the present tense ("Add feature" not "Added feature")
* Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
* Limit the first line to 72 characters or less
* Reference issues and pull requests liberally after the first line

Example::

   Add deployment validation endpoint

   Implements POST /deployments/{id}/validate endpoint that runs
   health checks and custom validation rules. Fixes #123.

Pull Request Process
--------------------

1. Update the documentation if you're adding or changing functionality
2. Add tests for new features or bug fixes
3. Ensure all tests pass
4. Update CHANGELOG.md with your changes
5. Ensure your code follows the project's style guidelines
6. Request review from maintainers

Testing
-------

* Write unit tests for new features
* Ensure all existing tests pass
* Aim for high test coverage
* Test edge cases and error conditions

Documentation
-------------

* Update relevant documentation when adding features
* Add docstrings to new functions and classes
* Update API documentation if endpoints change
* Include examples in documentation when helpful

Reporting Bugs
--------------

When reporting bugs, please include:

* Description of the bug
* Steps to reproduce
* Expected behavior
* Actual behavior
* Environment details (OS, Python version, etc.)
* Relevant logs or error messages

Feature Requests
----------------

For feature requests, please include:

* Clear description of the feature
* Use case and motivation
* Proposed implementation approach (if you have ideas)
* Any alternatives you've considered

Code Review
-----------

All submissions require review. We use GitHub pull requests for this purpose. 
The review process helps ensure code quality and consistency.

Questions?
----------

If you have questions, please:

* Check existing issues and pull requests
* Open a new issue with the "question" label
* Reach out to maintainers

Thank you for contributing!

