# PharmaOps AI

PharmaOps AI is an agentic AI system designed to analyze pharmaceutical inventory and supply chain operations using Claude, specialized skills, tool calling, and structured data analysis.

The project combines an LLM-based agent with deterministic Python analysis tools, allowing users to ask operational questions in natural language while keeping numerical analysis grounded in the underlying dataset.

## Project Overview

Pharmaceutical supply chain teams need to monitor inventory levels, stockout events, expiration risk, shipment performance, and carrier activity across operational data.

PharmaOps AI provides a natural-language interface for these tasks.

Instead of asking the language model to calculate operational metrics directly, the system allows Claude to select specialized tools that perform the analysis using Python and Pandas.

The results are then returned to Claude to generate a clear, business-focused response.

Example questions include:

- Give me an inventory summary.
- Which products have the highest stockout activity?
- Show products with low inventory.
- Which products are approaching expiration?
- Give me a shipment summary.
- How many shipments were delivered on time?
- Compare carrier performance.
- Show shipment completeness.

---

## Business Problem

Pharmaceutical inventory and supply chain data can contain information across orders, products, batches, facilities, inventory levels, expiration dates, shipments, carriers, and delivery dates.

Analyzing this data manually can make it difficult to quickly identify operational issues such as:

- Stockout activity
- Low inventory levels
- Expiration risk
- Shipment completeness
- Delivery performance
- Carrier performance

PharmaOps AI provides an agent-based analysis layer that connects natural-language questions with deterministic analytical tools.

This allows the LLM to focus on understanding the user's intent and communicating findings, while Python handles the underlying calculations.

---

## Architecture

```text
User Question
      |
      v
+-------------------+
|    ClaudeAgent    |
+-------------------+
      |
      v
+-------------------+
|    SkillRouter    |
+-------------------+
      |
      v
+-------------------+
|    SkillLoader    |
+-------------------+
      |
      +------------------------+
      |                        |
      v                        v
Inventory Skill          Shipment Skill
   SKILL.md                 SKILL.md
      |                        |
      +-----------+------------+
                  |
                  v
             Claude API
                  |
                  v
              Tool Call
                  |
          +-------+-------+
          |               |
          v               v
InventoryController   ShipmentController
          |               |
          v               v
Inventory Analysis    Shipment Analysis
          |               |
          +-------+-------+
                  |
                  v
                Pandas
                  |
                  v
                 CSV
                  |
                  v
            Analysis Result
                  |
                  v
                Claude
                  |
                  v
       Business-Focused Response
```

### Component Responsibilities

**ClaudeAgent**

The main orchestration layer. It communicates with the Anthropic API, exposes available tools to Claude, executes requested tool calls, and sends tool results back to the model.

**SkillRouter**

Examines the user's question and determines which domain skill is relevant.

Current skills:

- `inventory-analysis`
- `shipment-analysis`

**SkillLoader**

Loads the relevant `SKILL.md` instructions dynamically. Only the skill required for the current question is added to the agent context.

**Skills**

Skills contain domain-specific instructions that guide how Claude should interpret analysis results, apply operational rules, and communicate findings.

**Controllers**

Controllers expose Python analysis capabilities as Claude-compatible tools and route Claude's tool requests to the appropriate analysis functions.

**Analysis Tools**

The analysis layer uses Pandas to calculate metrics directly from the pharmaceutical supply chain dataset.

This keeps quantitative results deterministic rather than relying on the LLM to calculate or invent values.

---

## Capabilities

### Inventory Analysis

The Inventory Skill supports:

- Overall inventory summaries
- Stockout analysis
- Low inventory detection
- Expiration risk analysis
- Product-level inventory analysis
- Inventory-related operational recommendations

The inventory analysis tool currently exposes:

```text
summary
stockout
low_inventory
expiration_risk
```

### Shipment Analysis

The Shipment Skill supports:

- Shipment summaries
- Delivery performance
- On-time, early, and delayed shipment analysis
- Carrier performance
- Shipment completeness
- Shipment-related operational recommendations

The shipment analysis tool currently exposes:

```text
summary
delivery_performance
carrier_performance
shipment_status
```

---

## Agent Tool Calling

PharmaOps AI separates reasoning from deterministic data analysis.

For example, when a user asks:

```text
Compare carrier performance.
```

The system follows this flow:

```text
Question
   |
   v
SkillRouter
   |
   v
shipment-analysis
   |
   v
Shipment SKILL.md
   |
   v
Claude
   |
   v
analyze_shipment
   |
   v
ShipmentController
   |
   v
carrier_performance()
   |
   v
Pandas analysis
   |
   v
Structured result
   |
   v
Claude final response
```

Claude decides which analysis is required, while Python performs the actual calculations.

---

## Project Structure

```text
pharmaops-ai/
|
|-- .env.example
|-- .gitignore
|-- README.md
|-- requirements.txt
|
|-- skills/
|   |-- inventory-analysis/
|   |   `-- SKILL.md
|   |
|   `-- shipment-analysis/
|       `-- SKILL.md
|
|-- src/
|   |-- __init__.py
|   |-- main.py
|   |
|   |-- agents/
|   |   |-- __init__.py
|   |   `-- claudeagent.py
|   |
|   |-- controllers/
|   |   |-- __init__.py
|   |   |-- inventorycontroller.py
|   |   `-- shipmentcontroller.py
|   |
|   |-- skills/
|   |   |-- __init__.py
|   |   |-- skill_loader.py
|   |   `-- skill_router.py
|   |
|   |-- tool/
|   |   |-- __init__.py
|   |   |-- inventory_analysis.py
|   |   `-- shipment_analysis.py
|   |
|   `-- assets/
|       `-- data/
|           `-- pharmaceutical-inventory-supply-chains.csv
|
`-- tests/
    |-- __init__.py
    |-- test_inventory.py
    `-- test_shipment.py
```

The project intentionally separates domain instructions from Python skill-management code:

```text
skills/
```

contains the domain-specific `SKILL.md` files.

```text
src/skills/
```

contains the Python components responsible for routing and loading those skills.

---

## Dataset

This project uses the **Pharmaceutical Inventory & Supply Chains** dataset published on the GoMask AI Marketplace.

The dataset contains pharmaceutical supply chain information including:

- Orders
- Suppliers
- Products
- Batch information
- Expiration dates
- Shipment information
- Carriers
- Expected and actual delivery dates
- Destination facilities
- Storage information
- Current inventory levels
- Stockout flags

The dataset used in this project contains **200 records and 31 columns**.

### Dataset Source

[Pharmaceutical Inventory & Supply Chains — GoMask AI Marketplace](https://gomask.ai/marketplace/datasets/pharmaceutical-inventory-supply-chains)

The dataset is used for educational and portfolio demonstration purposes. Please refer to the original source for dataset details and applicable usage terms.

---

## Tech Stack

- Python
- Anthropic Claude API
- Claude Tool Calling
- Pandas
- python-dotenv
- Pytest
- Git / GitHub

---

## Installation

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd pharmaops-ai
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Linux or macOS:

```bash
source .venv/bin/activate
```

On Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the Anthropic API key

Copy the environment template:

```bash
cp .env.example .env
```

Then edit `.env`:

```env
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

Do not commit the `.env` file or expose your API key publicly.

---

## Running PharmaOps AI

Start the command-line application:

```bash
python -m src.main
```

You can then ask questions such as:

```text
You: Give me an inventory summary.

You: Which products have the highest stockout activity?

You: Show shipment delivery performance.

You: Compare carrier performance.
```

To stop the application:

```text
exit
```

or:

```text
quit
```

---

## Testing

The project includes automated tests for the Inventory and Shipment analysis layers and controllers.

Run all tests with:

```bash
pytest -v
```

Current test coverage includes:

- Inventory summary
- Stockout analysis
- Low inventory detection
- Expiration risk
- Inventory controller execution
- Shipment summary
- Delivery performance
- Carrier performance
- Shipment completeness/status
- Shipment controller execution

The current test suite contains **10 automated tests**.

---

## Design Principles

### Deterministic Analysis

Operational metrics are calculated using Python and Pandas rather than generated directly by the language model.

### Dynamic Skill Loading

The agent loads only the skill relevant to the user's question instead of injecting every domain instruction into every request.

### Separation of Responsibilities

The project separates:

```text
Agent       -> orchestration
Skill       -> domain instructions
Router      -> skill selection
Controller  -> tool interface
Tool        -> data analysis
Pandas      -> deterministic computation
CSV         -> data layer
```

This makes the architecture easier to extend and maintain.

### Evidence-Based Responses

The agent is instructed to base factual conclusions on tool results and avoid inventing values that are not present in the analysis.

---

## Future Improvements

Potential future extensions include:

- Replace the CSV data layer with a database or data warehouse
- Integrate with ERP systems such as SAP
- Connect to cloud data services
- Add REST API endpoints
- Build a web-based operational dashboard
- Add authentication and role-based access
- Add conversation history and persistent sessions
- Expand automated integration testing
- Containerize the application with Docker
- Deploy the agent as a cloud service

---

## Disclaimer

PharmaOps AI is an educational and portfolio project built to demonstrate agentic AI, tool calling, skill-based routing, and pharmaceutical supply chain analytics.

It is not intended to make clinical, medical, regulatory, or production supply chain decisions without appropriate validation and human oversight.
