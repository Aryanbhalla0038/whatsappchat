# Contributing to WhatsApp Chat Analyzer

We love your input! We want to make contributing to this project as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

## Development Process

We use GitHub to host code, to track issues and feature requests, as well as accept pull requests.

### Pull Requests

1. Fork the repo and create your branch from `main`
2. If you've added code that should be tested, add tests
3. Ensure the test suite passes
4. Make sure your code lints
5. Issue that pull request!

### Local Development Setup

1. Clone your fork:
```bash
git clone https://github.com/your-username/whatsappchat.git
cd whatsappchat
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. Install development dependencies:
```bash
pip install -r requirements.txt
pip install pytest black flake8
```

4. Create a feature branch:
```bash
git checkout -b feature/your-feature-name
```

5. Make your changes and test locally:
```bash
streamlit run app.py
```

6. Format your code:
```bash
black src/ app.py
flake8 src/ app.py
```

7. Commit your changes:
```bash
git commit -m "Add your message here"
```

8. Push to your fork and submit a pull request

## Code Style

- Follow PEP 8 guidelines
- Use meaningful variable names
- Add docstrings to functions and classes
- Add comments for complex logic
- Keep functions focused and small

## New Feature Checklist

- [ ] Code follows PEP 8 style guide
- [ ] Docstrings added to functions/classes
- [ ] Code is tested locally
- [ ] README updated if needed
- [ ] Commit messages are clear

## Bug Report Template

```
**Describe the bug**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. See error

**Expected behavior**
What you expected to happen.

**Screenshots**
If applicable, add screenshots.

**Environment**
- OS: [e.g. Windows 10]
- Python version: [e.g. 3.9]
- Chat file format: [e.g. Android export]

**Additional context**
Any other context about the problem.
```

## Feature Request Template

```
**Is your feature request related to a problem?**
Description of the problem.

**Describe the solution**
Clear description of what you want to happen.

**Describe alternatives considered**
Other solutions you've considered.

**Additional context**
Any other context or screenshots.
```

## Questions?

Feel free to open an issue or discussion. We're here to help!

## License

By contributing, you agree that your contributions will be licensed under its MIT License.
