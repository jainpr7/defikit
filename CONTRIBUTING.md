# Contributing to DeFiKit

Thank you for your interest in contributing to DeFiKit! This document provides guidelines and instructions for contributing.

## Code of Conduct

Please be respectful and considerate in all interactions. We aim to foster an inclusive and welcoming community.

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue with:
- A clear, descriptive title
- Steps to reproduce the issue
- Expected behavior
- Actual behavior
- Your environment (Python version, OS, etc.)

### Suggesting Features

Feature requests are welcome! Please open an issue with:
- A clear description of the feature
- Use cases and motivation
- Any implementation ideas you have

### Pull Requests

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature-name`)
3. Make your changes
4. Add tests for your changes
5. Run the test suite (`pytest`)
6. Run linting (`ruff check src tests`)
7. Run type checking (`mypy src`)
8. Commit your changes (`git commit -am 'Add some feature'`)
9. Push to the branch (`git push origin feature/your-feature-name`)
10. Open a Pull Request

## Development Setup

```bash
# Clone the repository
git clone https://github.com/jainpr7/defikit.git
cd defikit

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

## Code Style

- Follow PEP 8
- Use type hints for all functions
- Write docstrings for public APIs
- Keep line length under 100 characters
- Use ruff for linting and formatting

## Testing

- Write tests for all new features
- Maintain or improve code coverage
- Run `pytest` before submitting PRs
- Use async/await for async code

## Documentation

- Update docstrings for modified functions
- Add examples for new features
- Update README.md if needed

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
