---
name: shipment-analysis

description: Analyze pharmaceutical shipment activity, delivery performance, carrier performance, shipment completeness, delays, and shipment-related issues using the pharmaceutical supply-chain dataset.
---



# shipment Analysis

## Purpose

Use this skill to analyze pharmaceutical shipment and delivery data.

This skill supports questions about:

- shipment activity
- delivery performance 
- delayed shipments
- early shipments 
- on-time shipments
- carrier performance 
- shipment completeness
- expected and acrual delivery dates 
- shipment destinations

## Available Data 

The shipment analysis uses data from:

`src/assets/data/pharmaceutical-inventory-supply-chains.csv`

Relevant shipment fields include 

- shipment_id
- shipment_date 
- carrier_name
- tracking_number
- expected_delivery_date
- actual_delivery_date
- destination_facility_id
- destination_facility_name
- destination_city
- destination_state
- destination_country
- order_status

## Shipment Evaluation Rule

A shipment can be evaluted for delivery performance only when both:

- expected_delivery_data is available
- actual_delivery_date is available

calculate delivery timing using:

`actual_delivery_date - expected_delivery_date`

Interpret the result as:

- greater than 0 days -> delayed
- equal to 0 days -> on time
- less than 0 days -> early

Do not classify a shipment as delayed when the actual delivery date is missing.

## shipment Completeness

A shipment is considered completed for this  analysis when both expected and actual delivery dates are available.

If one or both dates are missing, treat the shipment as incomplete for delivery performance analysis

Do not assume that in complete means delayed or faild

## carrier analysis 

when comparing carriers:

- use only shipments that have both expected and actual delivery dates 
- report the number of evaluated shipment
- consider delayed, on time and early shupments
- ise delay rate and on time rate when relevant

Carrier names may contain naming inconsistencies

Do not automatically merge carriers with similar names unless there is clear evidence that they represent the same carrier

Mention this limitation when it could materially affect the comparison

## Data Quality 

Check For:

- missing shipment id
- missing carrier names
- missing exoected delivery dates 
- inconsistent carrier names 

Dot not invent missing shipment information

## Recommendations 

Recommendation must be based only on observed shipment date 

Do not claim that a carrier is un rekiable when there is insufficient evaluable shipment date.

When comparing carriers with very different number of shipment, mention the difference in sample size

## Suggested Response Structure

When appropriate, structure the answer as:

1. finding
2. evidence
3. operational imapct 
4. Recommendation
5. data limitation or confidance 

Prefer table when comparig multiple carriers or shipments.