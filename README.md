# Subtrix

Subtrix is a substitution module for Python, providing powerful tools for text manipulation through substitutions. The
main interface is the Mechanism class, which allows for standard substitution, term expansion and variable
substitution.

## Features

- Provides a basic substitution mechanism
- Supports variable substitution
- Supports lists of variables to generate multiple documents from a single template
- Supports term expansion by using term looping substitution all combinations of a list of terms can be generated
- Provides Prefix and Suffix Support with controls for trailing suffix

## Installation

You can install Subtrix via pip:

```bash
pip install subtrix
```

Alternatively, clone the repository and install from source:

```bash
git clone https://github.com/solubrew/subtrix.git
cd subtrix
pip install -e .
```

### Requirements

- Python 3.<MIN_VERSION> or higher
- Dependencies: re, <EVAL_LIB> (automatically installed via pip where applicable)

## Quick Start

Import the module and use the Mechanism class for substitutions:

## Standard Patterns

### Substitution:

    <[token]>: basic substitution
    <~[token]~>: optional token substituion (is removed if unused in template render)
    <[prefix.:token]>: token substitution with prefix
    <[token:.suffix]>: token substitution with suffix

### Variable Substitution:

    <(token)>: registerd variable lookup for things like TODAY, USER, etc.
    <(prefix.:token)>: optional variable token substituion
    <(token:.suffix)>: optional variable token substituion

### Looped Variable Substitution:

    token: ['point0', 'point1']
    <@[token]@>: [['point0'], ['point1'], ['point0', 'point1']

```python
from subtrix import Mechanism

# Initialize Mechanism
template = 'Hello, <[name]>!'
data = {'name': 'World'}
mech = Mechanism(template, data)

# Perform standard substitution
result = mech.run()
print(result)  # Output: Hello, World!
```

## Usage


### Variable Substitution

Inject variables from various sources:


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