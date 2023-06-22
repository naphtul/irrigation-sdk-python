# Hydrawise SDK
A simple Python SDK to interact with Hydrawise (Hunter) Rest API to run simple operations and get information.

## Setup
The `Hydrawise` class requires an environment variable named `HYDRAWISE_API_KEY` to run. Fill it with your individual API key you receive from Hydrawise.

## Usage
```python
import Hydrawise

hydrawise = Hydrawise()
hydrawise.run_zone('Grass')
```