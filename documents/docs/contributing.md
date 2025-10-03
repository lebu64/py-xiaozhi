---
title: Contribution Guide
description: How to contribute code to the py-xiaozhi project
sidebar: false
outline: deep
---

<div class="contributing-page">

# Contribution Guide

<div class="header-content">
  <h2>How to Contribute Code to py-xiaozhi Project 🚀</h2>
</div>

## Introduction

Thank you for your interest in the py-xiaozhi project! We warmly welcome community members to participate in contributions, whether it's fixing bugs, improving documentation, or adding new features. This guide will help you understand how to submit contributions to the project.

## Development Environment Setup

### Basic Requirements

- Python 3.9 or higher
- Git version control system
- Basic Python development tools (recommended to use Visual Studio Code)

### Get Source Code

1. First, Fork this project to your own account on GitHub
   - Visit [py-xiaozhi project page](https://github.com/huangjunsen0406/py-xiaozhi)
   - Click the "Fork" button in the top right corner
   - Wait for the Fork to complete, you will be redirected to your repository copy

2. Clone your forked repository locally:

```bash
git clone https://github.com/YOUR_USERNAME/py-xiaozhi.git
cd py-xiaozhi
```

3. Add the upstream repository as a remote source:

```bash
git remote add upstream https://github.com/huangjunsen0406/py-xiaozhi.git
```

You can use the `git remote -v` command to confirm the remote repositories are correctly configured:

```bash
git remote -v
# Should display:
# origin    https://github.com/YOUR_USERNAME/py-xiaozhi.git (fetch)
# origin    https://github.com/YOUR_USERNAME/py-xiaozhi.git (push)
# upstream  https://github.com/huangjunsen0406/py-xiaozhi.git (fetch)
# upstream  https://github.com/huangjunsen0406/py-xiaozhi.git (push)
```

### Install Development Dependencies
- Other dependencies need to be checked in the relevant documentation under the guide
```bash
# Create and activate virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install project dependencies
pip install -r requirements.txt
```

## Development Process

### Keep in Sync with Main Repository

Before starting work, it's important to ensure your local repository stays synchronized with the main project. Here are the steps to sync your local repository:

1. Switch to your main branch (`main`):

```bash
git checkout main
```

2. Pull the latest changes from the upstream repository:

```bash
git fetch upstream
```

3. Merge the upstream main branch changes into your local main branch:

```bash
git merge upstream/main
```

4. Push the updated local main branch to your GitHub repository:

```bash
git push origin main
```

### Create Branch

Before starting any work, make sure to create a new branch from the latest upstream main branch:

```bash
# Get the latest upstream code (as described in the previous section)
git fetch upstream
git checkout -b feature/your-feature-name upstream/main
```

When naming branches, you can follow these conventions:
- `feature/xxx`: New feature development
- `fix/xxx`: Bug fixes
- `docs/xxx`: Documentation updates
- `test/xxx`: Testing related work
- `refactor/xxx`: Code refactoring

### Coding Standards

We use [PEP 8](https://www.python.org/dev/peps/pep-0008/) as the Python code style guide. Before submitting code, make sure your code meets the following requirements:

- Use 4 spaces for indentation
- Line length should not exceed 120 characters
- Use meaningful variable and function names
- Add docstrings for public APIs
- Use type hints (Type Hints)

We recommend using static code analysis tools to help you follow coding standards:

```bash
# Use flake8 to check code style
flake8 .

# Use mypy for type checking
mypy .
```

### Testing

Before submitting, make sure all tests pass

## Submitting Changes

### Pre-Submission Checklist

Before submitting your code, make sure to complete the following checks:

1. Does the code comply with PEP 8 standards?
2. Have necessary test cases been added?
3. Do all tests pass?
4. Has appropriate documentation been added?
5. Has the problem you planned to solve been resolved?
6. Is it synchronized with the latest upstream code?

### Submit Changes

During development, develop the habit of making small, frequent commits. This makes your changes easier to track and understand:

```bash
# View changed files
git status

# Stage changes
git add file1.py file2.py

# Commit changes
git commit -m "feat: add new feature X"
```

### Resolve Conflicts

If you encounter conflicts when trying to merge upstream changes, follow these steps to resolve them:

1. First understand where the conflicts are:

```bash
git status
```

2. Open the conflicting file, you will see markers like:

```
<<<<<<< HEAD
Your code
=======
Upstream code
>>>>>>> upstream/main
```

3. Modify the file to resolve conflicts, remove conflict markers
4. After resolving all conflicts, stage and commit:

```bash
git add .
git commit -m "fix: resolve merge conflicts"
```

### Commit Specification

We use [Conventional Commits](https://www.conventionalcommits.org/) specification to format Git commit messages. Commit messages should follow this format:

```
<type>[optional scope]: <description>

[optional body]

[optional footer]
```

Common commit types include:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Changes that don't affect code meaning (like whitespace, formatting, etc.)
- `refactor`: Code refactoring that neither fixes bugs nor adds features
- `perf`: Code changes that improve performance
- `test`: Adding or correcting tests
- `chore`: Changes to the build process or auxiliary tools and libraries

For example:

```
feat(tts): Add new speech synthesis engine support

Add support for Baidu speech synthesis API, including the following features:
- Support for multiple voice options
- Support for speech rate and volume adjustment
- Support for mixed Chinese-English synthesis

Fixes #123
```

### Push Changes

After completing code changes, push your branch to your GitHub repository:

```bash
git push origin feature/your-feature-name
```

If you have already created a Pull Request and need to update it, simply push to the same branch again:

```bash
# After making more changes
git add .
git commit -m "refactor: improve code based on feedback"
git push origin feature/your-feature-name
```

### Sync Latest Code Before Creating Pull Request

Before creating a Pull Request, it's recommended to sync with the upstream repository again to avoid potential conflicts:

```bash
# Get latest upstream code
git fetch upstream

# Rebase upstream latest code onto your feature branch
git rebase upstream/main

# If conflicts occur, resolve conflicts and continue rebase
git add .
git rebase --continue

# Force push updated branch to your repository
git push --force-with-lease origin feature/your-feature-name
```

Note: Using `--force-with-lease` is safer than directly using `--force`, as it prevents overwriting changes pushed by others.

### Create Pull Request

When you complete feature development or issue fixing, follow these steps to create a Pull Request:

1. Push your changes to GitHub:

```bash
git push origin feature/your-feature-name
```

2. Visit your forked repository page on GitHub, click the "Compare & pull request" button

3. Fill out the Pull Request form:
   - Use a clear title, following the commit message format
   - Provide detailed information in the description
   - Reference related issues (using `#issue-number` format)
   - If this is work in progress, add `[WIP]` prefix to the title

4. Submit the Pull Request and wait for project maintainers to review

### Pull Request Lifecycle

1. **Creation**: Submit your PR
2. **CI Checks**: Automated testing and code style checks
3. **Code Review**: Maintainers will review your code and provide feedback
4. **Revision**: Modify your code based on feedback
5. **Approval**: Once your PR is approved
6. **Merge**: Maintainers will merge your PR into the main branch

## Documentation Contribution

If you want to improve project documentation, follow these steps:

1. Fork the project and clone locally following the steps above

2. Documentation is located in the `documents/docs` directory, using Markdown format

3. Install documentation development dependencies:

```bash
cd documents
pnpm install
```

4. Start local documentation server:

```bash
pnpm docs:dev
```

5. Visit `http://localhost:5173/py-xiaozhi/` in your browser to preview your changes

6. After completing changes, submit your contribution and create a Pull Request

### Documentation Writing Guidelines

- Use clear, concise language
- Provide practical examples
- Explain complex concepts in detail
- Include appropriate screenshots or diagrams (when needed)
- Avoid excessive technical terminology, provide explanations when necessary
- Maintain consistent documentation structure

## Issue Reporting

If you discover an issue but cannot fix it temporarily, please [create an Issue](https://github.com/huangjunsen0406/py-xiaozhi/issues/new) on GitHub. When creating an Issue, include the following information:

- Detailed description of the problem
- Steps to reproduce the problem
- Expected behavior and actual behavior
- Your operating system and Python version
- Relevant log output or error information

## Code Review

After submitting a Pull Request, project maintainers will review your code. During the code review process:

- Please wait patiently for feedback
- Respond promptly to comments and suggestions
- Make modifications and update your Pull Request when necessary
- Maintain polite and constructive discussion

### Handling Code Review Feedback

1. Carefully read all comments and suggestions
2. Respond to or change each point
3. If you disagree with a suggestion, politely explain your reasoning
4. After completing modifications, leave a comment in the PR to notify the reviewer

## Becoming a Project Maintainer

If you consistently make valuable contributions to the project, you may be invited to become a project maintainer. As a maintainer, you will have permission to review and merge others' Pull Requests.

### Maintainer Responsibilities

- Review Pull Requests
- Manage issues
- Participate in project planning
- Answer community questions
- Help guide new contributors

## Code of Conduct

Please respect all project participants and follow this code of conduct:

- Use inclusive language
- Respect different perspectives and experiences
- Gracefully accept constructive criticism
- Focus on the best interests of the community
- Show empathy towards other community members

## Frequently Asked Questions

### Where should I start contributing?

1. Check issues labeled "good first issue"
2. Fix errors or unclear parts in documentation
3. Add more test cases
4. Solve problems you discover during your own usage

### My submitted PR hasn't received a response for a long time, what should I do?

Leave a comment in the PR, politely asking if further improvements or clarifications are needed. Please understand that maintainers may be busy and need some time to review your contribution.

### What types of changes can I contribute?

- Bug fixes
- New features
- Performance improvements
- Documentation updates
- Test cases
- Code refactoring

## Acknowledgments

Thank you again for contributing to the project! Your participation is very important to us, let's work together to make py-xiaozhi better!

</div>

<style>
.contributing-page {
  max-width: 900px;
  margin: 0 auto;
  padding: 2rem 1.5rem;
}

.contributing-page h1 {
  text-align: center;
  margin-bottom: 1rem;
}

.header-content {
  text-align: center;
}

.header-content h2 {
  color: var(--vp-c-brand);
  margin-bottom: 1rem;
}

.contributing-page h2 {
  margin-top: 3rem;
  padding-top: 1rem;
  border-top: 1px solid var(--vp-c-divider);
}

.contributing-page h3 {
  margin-top: 2rem;
}

.contributing-page code {
  background-color: var(--vp-c-bg-soft);
  padding: 0.2em 0.4em;
  border-radius: 3px;
}

.contributing-page pre {
  margin: 1rem 0;
  border-radius: 8px;
  overflow: auto;
}
</style>
