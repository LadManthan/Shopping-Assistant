# Shopping Assistant

A Python-based Shopping Assistant that leverages AI agents and external APIs to help users analyze, compare, and rank products from various online sources. The project is modular, with dedicated agents for product analysis and comparison, and tools for integrating with platforms like Rainforest and SerpAPI.

## Features
- Product analysis and comparison using AI agents
- Integration with Rainforest for product data
- Ranking services for enhanced recommendations
- Modular architecture for easy extension

## Project Structure
```
app.py                  # Main application entry point
graph.py                # Graph-related utilities
requirements.txt        # Python dependencies

agents
|---> analyzer.py           # Product analysis agent
|---> comperator.py         # Product comparison agent

models
|---> schemas.py            # Data schemas and models

services
|---> ranking.py            # Product ranking service

tools
|---> rainforest_tool.py    # Rainforest API integration
```

## Getting Started

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Installation
1. Clone the repository:
   ```sh
   git clone <repo-url>
   cd Shopping Assistant
   ```
2. (Optional) Create and activate a virtual environment:
   ```sh
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On Unix/Mac
   source venv/bin/activate
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

### Usage
Run the main application:
```sh
python app.py
```
