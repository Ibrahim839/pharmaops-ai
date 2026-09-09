---
name: inventory-analysis
description: Analyze pharmaceutical inventory levels, stockouts, product quantities, expiration risk, and inventory-related issues using the pharmaceutical supply-chain dataset.
---

# Inventory Analysis Skill

## Purpose

This skill analyzes pharmaceutical inventory data and provides actionable
inventory insights and recommendations.

Use this skill when the user asks about:

- Current inventory levels
- Stockouts
- Products at risk of stockout
- Inventory shortages
- Product quantities
- Inventory by product
- Inventory by facility
- Inventory by supplier
- Expiration risk
- Batch information
- Storage conditions
- Inventory-related recommendations

Do NOT use this skill as the primary skill for:

- Shipment delivery performance
- Carrier performance
- Supplier reliability
- Supplier risk

Those requests should be handled by the appropriate specialized skill.

---

## Dataset

The primary data source is:

`data/pharmaceutical-inventory-supply-chains.csv`

The dataset contains pharmaceutical orders, products, suppliers,
shipments, facilities, storage information, inventory levels,
and stockout information.

---

## Relevant Fields

### Product

- `product_id`
- `product_name`
- `batch_number`
- `unit_of_measure`

### Inventory

- `current_inventory_level`
- `stockout_flag`

### Order

- `order_id`
- `order_date`
- `quantity_ordered`
- `order_status`

### Expiration

- `expiration_date`

### Storage

- `storage_location_id`
- `storage_condition`
- `storage_entry_date`
- `storage_exit_date`

### Facility

- `destination_facility_id`
- `destination_facility_name`
- `destination_city`
- `destination_state`
- `destination_country`

### Supplier

- `supplier_id`
- `supplier_name`

---

# Analysis Rules

## 1. Inventory Level Analysis

When analyzing inventory:

- Calculate total inventory when appropriate.
- Calculate average inventory when appropriate.
- Identify products or facilities with unusually low inventory.
- Group results by product, facility, supplier, or other dimensions
  requested by the user.

Do not invent inventory thresholds that do not exist in the dataset.

If a threshold is required but is not provided, clearly state the
assumption used.

---

## 2. Stockout Analysis

Use:

`stockout_flag`

to identify recorded stockout events.

Calculate when useful:

- Total stockout events
- Stockout rate
- Stockouts by product
- Stockouts by facility
- Stockouts by supplier
- Stockouts over time

Always distinguish between:

- Recorded stockouts
- Potential future inventory risk

Do not claim that a product will stock out in the future unless the
available data supports that conclusion.

---

## 3. Product Analysis

For product-level questions:

1. Group records by `product_id` and/or `product_name`.
2. Analyze:
   - Inventory level
   - Quantity ordered
   - Stockout frequency
   - Expiration information
3. Rank products when ranking is useful.
4. Explain the reason behind the ranking.

---

## 4. Expiration Risk

Use:

`expiration_date`

to identify products or batches approaching expiration.

When analyzing expiration:

- Convert dates to proper datetime values.
- Compare expiration dates against the relevant analysis date.
- Clearly state the reference date used.

Do not assume that an expired product is unusable unless the business
rules explicitly say so.

---

## 5. Storage Analysis

Use:

- `storage_condition`
- `storage_entry_date`
- `storage_exit_date`

to identify storage-related patterns.

Examples:

- Inventory stored under different conditions
- Storage duration
- Products associated with specific storage conditions

Do not claim that a storage condition is unsafe unless the dataset
contains an explicit pharmaceutical requirement supporting that claim.

---

# Data Quality

Before performing an important analysis:

1. Check that the requested columns exist.
2. Handle missing values appropriately.
3. Convert date columns to datetime.
4. Check for duplicate records when relevant.
5. Report important data-quality limitations.

Never silently fabricate missing values.

---

# Recommendation Framework

Recommendations must be based on observed data.

Use this structure:

### Finding

Describe the important inventory issue.

### Evidence

Provide the relevant numbers or records.

### Risk

Explain the potential operational impact.

### Recommendation

Give a practical action.

### Confidence

State whether the recommendation is:

- High confidence
- Medium confidence
- Low confidence

based on the amount and quality of available evidence.

---

# Response Style

Keep responses business-focused and concise.

Prefer tables for rankings and comparisons.

For example:

| Product | Inventory | Stockouts | Risk |
|---|---:|---:|---|
| Product A | 12 | 4 | High |
| Product B | 25 | 2 | Medium |
| Product C | 80 | 0 | Low |

Always explain the reasoning behind important conclusions.

Do not expose internal reasoning or hidden chain-of-thought.

---

# Example Questions

This skill should be able to answer questions such as:

- Which products have the most stockouts?
- Which facilities have inventory problems?
- What products currently have low inventory?
- Which products appear to be at the highest inventory risk?
- Which batches are approaching expiration?
- What is the stockout rate?
- Which products have the highest quantity ordered?
- Which supplier is associated with the most stockouts?
- Give me recommendations to reduce stockouts.