--- 
name: inventory-analysis
description: Analyze pharmaceutical inventory levels, stockouts, product, quantites, expiration risk, and inventory-related issues using the pharmaceutical supply-chaine dataset.
---


# Inventory Analysis Skill

## Purpose

This skill analyzes pharmaceutical inventory data and provides actionat inventory insights and recommendation.

Use this skill when the user aske about:

- Current inventory levels
- Stockouts
- Products at risk od stockout 
- Inventory shortage 
- Producte quantities 
- Inventory by product
- Inventory by facility
- Inventory by supplier 
- Expiration risk 
- Batch information 
- Storage conditions 
- Inventory-related recommendation 

Do NOT use this skill as the primary skill for:

- Shipment delivery performance 
- Carrier performance 
- Suuplier reliability 
- Supplier risk 

Thos request should be handled bt thr appropriate specialized skill.


---

##  Dataset 

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
- `stoukout_flag`

### Order

- `order_id`
- `order_date`
- `quantity_ordered`
- `order_statue`

### Expiration

- `storage_location_id`
- `storage_condation`
- `storage_entry_date`
- `storage_exit_data`

### Facility

- `destination_facility_id`
- `destination_facility_name`
- `destination_city`
- `destination_state`
- `destination_county`

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
- Group results by producte, facility, supplier, or other dimentions requested by the user 

Do NOT invent inventory thresholds that do not exists in the dataset.

If a threshold is required but is not provided, clearly state the assumption used.

---

## 2. Stockout Analysis

Use:

to identify recorded stockout events.

Calculate when useful:

- Total stockout events 
- stockouts rate
- Stockouts by product 
- Stockouts by facility 
- Stockouts by subblier
- Stockouts over time 

Always distinguish between:

- Recorded stockouts 
- Potential future inventory risk

Do not claim that a product will stock in the futur unless the available data supports that conclusion

---


## 3. Product Analysis 

For product-level question:

1. Group records by `product_id` and/or `product_name`.
2. Analyze:
	- Inventory level
	- Quantity ordered
	- stockout frequency 
	- Expiration information
3. Rank products when ranking is useful.
4. Explain the reason behind the ranking 

-- 

## 4. Expiration Risk

Use:

`expiration_date`

to identify product or batches approaching expiration.

When analyzing expiration:

- Convert dates to proper datatime values.
- compare expiration dates against the relvent analysis date .
- Clearly state rhe referance date used.

Do not assume that an expired profuct is unusable unless the busniss rules  explicity say so .


## 5. storage Analysis 

Use:

- `storage_condation`
- `storage_entry_date`
- `storage_exist_date`

to identify storage-related pattern. 

Examples:

- Inventory stored under different conditions
- Storage duration
- Products associated with specific storage conditions

Do not calim that a storage condation is unsafe unless thw dataset contains an explicit pharmaceutical requirment supporting that claim.

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

# Recommendations must be based on observed data.

use structure :

### Finding 

Describe the important inventory issue.

### Evidance 

Provide the potential operational impact.

### Recommendation

Give a practocal action.

### confidence 

State whether the recommendation is:

- High confidence
- Medium confidence
- Low confidence

based on the amount and quality of available evidence.

# Response 

Keep responses business-focused and concies .

Prefer tablble for ranking and comaprisons.

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

