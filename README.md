# Subtrix

Subtrix is a substitution module for Python, providing powerful tools for text manipulation through substitutions. The
main interface is the Mechanism class, which allows for standard substitution, formula expansion, and variable
substitution. It enables developers to perform complex string replacements, evaluate embedded formulas, and inject
variables dynamically, making it ideal for templating, configuration processing, and data transformation tasks.

## Features

- **Mechanism Class**: Core interface for handling substitutions with support for standard regex-based replacements,
  mathematical formula expansion, and variable injection.
- **Standard Substitution**: Perform simple or regex-based string replacements.
- **Formula Expansion**: Evaluate and expand embedded mathematical or logical formulas within strings.
- **Variable Substitution**: Replace placeholders with values from dictionaries, environments, or custom sources.
- **Extensible**: Easily extend the Mechanism class for custom substitution logic or additional evaluators.
- **Error Handling**: Robust validation and error reporting for substitution operations.
- **Performance Optimized**: Efficient processing for large strings or batch operations.
- **Cross-Platform Compatibility**: Works on Windows, macOS, and Linux.

## Installation

You can install Subtrix via pip:

```bash
pip install subtrix
```

Alternatively, clone the repository and install from source:

```bash
git clone https://github.com/<USER_OR_ORG>/subtrix.git
cd subtrix
pip install -e .
```

### Requirements

- Python 3.<MIN_VERSION> or higher
- Dependencies: re, <EVAL_LIB> (automatically installed via pip where applicable)

## Quick Start

Import the module and use the Mechanism class for substitutions:

```python
from subtrix import Mechanism

# Initialize Mechanism
mech = Mechanism()

# Perform standard substitution
result = mech.substitute('Hello, {name}!', variables={'name': 'World'})
print(result)  # Output: Hello, World!
```

## Usage

### Standard Substitution

Use regex or simple string replacements:

```python
# Simple replacement
result = mech.substitute('apple banana apple', replace={'apple': 'orange'})
print(result)  # Output: orange banana orange

# Regex-based
result = mech.substitute('123-456-789', pattern=r'\d{3}', replacement='XXX')
print(result)  # Output: XXX-XXX-XXX
```

### Formula Expansion

Expand embedded formulas:

```python
# Evaluate math formulas
result = mech.expand_formula('The sum is {2 + 3 * 4}.')
print(result)  # Output: The sum is 14.

# Custom formula support
result = mech.expand_formula('Area: {pi * r**2}', variables={'r': 5}, globals={'pi': 3.14159})
print(result)  # Output: Area: 78.53975
```

### Variable Substitution

Inject variables from various sources:

```python
# From dictionary
result = mech.substitute('User: {username}, Age: {age}', variables={'username': 'alice', 'age': 30})

# From environment variables
import os

os.environ['APP_ENV'] = 'production'
result = mech.substitute('Environment: {APP_ENV}', use_env=True)
```

## Examples

### Example 1: Templating Configuration Files

```python
from subtrix import Mechanism

mech = Mechanism()
template = """
server: {host}
port: {port}
debug: {debug_mode}
calculated: {10 + port * 2}
"""
variables = {'host': 'localhost', 'port': 8080, 'debug_mode': True}
result = mech.substitute(template, variables=variables)
print(result)
```

### Example 2: Batch Processing Strings

```python
from subtrix import Mechanism

mech = Mechanism()
strings = ['Item {i}: {value}' for i in range(3)]
variables_list = [{'i': 0, 'value': 'A'}, {'i': 1, 'value': 'B'}, {'i': 2, 'value': 'C'}]

results = [mech.substitute(s, variables=v) for s, v in zip(strings, variables_list)]
for res in results:
    print(res)
```

## Configuration Guide

The Mechanism class can be configured with options like:

- `safe_eval`: Boolean to enable safe evaluation for formulas (default: True)
- `delimiter`: Custom delimiters for variables/formulas (e.g., '{{ }}')
- `custom_evaluators`: Dictionary of user-defined functions for expansion

For example:

```python
mech = Mechanism(safe_eval=True, delimiter=('{{', '}}'))
```

For advanced customization, refer to the [docs/config-reference.md](docs/config-reference.md).

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/<FEATURE_NAME>`).
3. Commit your changes (`git commit -am 'Add some feature'`).
4. Push to the branch (`git push origin feature/<FEATURE_NAME>`).
5. Open a Pull Request.

See [CONTRIBUTING.md](CONTRIBUTING.md) for more details.

## License

This project is licensed under the <LICENSE_TYPE> License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with inspiration from open-source templating and substitution libraries.
- Thanks to contributors of underlying libraries like re, <EVAL_LIB>.