# Route-Linter

A command-line tool to analyze source code directories, specifically designed to examine backend and frontend paths.

## Overview

Route-Linter is a Python utility that helps developers analyze their codebase by examining specified backend and frontend directories. This tool is useful for ensuring consistency between API routes and frontend requests.

## Installation

No installation is required beyond having Python 3.x installed. Simply clone or download this repository.

## Usage

```bash
python route_linter.py --backend /path/to/backend --frontend /path/to/frontend
```

### Required Arguments

- `--backend`: Path to the backend directory
- `--frontend`: Path to the frontend directory

## Example

```bash
python route_linter.py --backend ./server/src --frontend ./client/src
```

## Requirements

- Python 3.x
- No external dependencies required for basic functionality