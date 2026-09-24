# PharmaOps AI

PharmaOps AI is an **Agentic AI system for pharmaceutical inventory and shipment analysis** built with Claude, tool calling, Python, and Pandas.

The system allows users to ask operational questions in natural language while deterministic Python tools perform the actual data analysis.

## Architecture

```text
User Question
      ↓
Claude Agent
      ↓
Skill Router
      ↓
Inventory / Shipment Skill
      ↓
Skill Loader
      ↓
Controller
      ↓
Analysis Tool
      ↓
Pandas
      ↓
Supply Chain Data
      ↓
Business Response
```

The architecture separates responsibilities:

- **Agent** — orchestrates the workflow and tool calling.
- **Skill** — provides domain-specific instructions.
- **Controller** — connects Claude tool requests to analysis functions.
- **Tool** — performs deterministic analysis using Pandas.

## Features

### Inventory Analysis
- Inventory summary
- Stockout analysis
- Low inventory detection
- Expiration risk

### Shipment Analysis
- Shipment summary
- Delivery performance
- Carrier performance
- Shipment completeness

## Example Questions

```text
Give me an inventory summary.

Which products have the highest stockout activity?

Show shipment delivery performance.

Compare carrier performance.
```

## Project Structure

```text
pharmaops-ai/
├── skills/
│   ├── inventory-analysis/
│   └── shipment-analysis/
├── src/
│   ├── agents/
│   ├── controllers/
│   ├── skills/
│   ├── tool/
│   ├── assets/data/
│   └── main.py
├── tests/
├── requirements.txt
└── .env.example
```

## Dataset

The project uses the **Pharmaceutical Inventory & Supply Chains** dataset from GoMask AI Marketplace.

The dataset contains **200 records and 31 columns**, covering inventory, products, orders, suppliers, shipments, carriers, facilities, storage, and stockout information.

**Source:** [GoMask AI — Pharmaceutical Inventory & Supply Chains](https://gomask.ai/marketplace/datasets/pharmaceutical-inventory-supply-chains)

Please refer to the original source for dataset details and applicable usage terms.

## Tech Stack

`Python` • `Claude API` • `Tool Calling` • `Pandas` • `Pytest`

## Setup

```bash
git clone https://github.com/Ibrahim839/pharmaops-ai.git
cd pharmaops-ai

python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
```

Add your Anthropic API key to `.env`:

```env
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

Run the application:

```bash
python -m src.main
```

## Testing

```bash
pytest -v
```

The project currently includes **10 automated tests** covering inventory analysis, shipment analysis, and controller execution.

## Future Work

The current implementation is a prototype using CSV data and Pandas.

Future development can extend the architecture with:

- Microsoft Fabric / Lakehouse
- Microsoft Copilot Studio
- SAP / ERP integration
- REST APIs
- Cloud deployment

## Disclaimer

PharmaOps AI is an educational and portfolio project demonstrating Agentic AI, tool calling, and pharmaceutical supply-chain analytics. It is not intended for production, clinical, or regulatory decision-making without appropriate validation.