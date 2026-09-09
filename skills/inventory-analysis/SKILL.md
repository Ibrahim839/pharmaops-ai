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

