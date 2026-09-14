from src.tool.inventory_analysis import (
    inventory_summary,
    stockout_analysis,
    low_inventory_products,
    expiration_risk,
)


class InventoryController:
    """
    controller responsible for inventory related tool definitions and execution
    """

    def __init__(self):
        self.tool_definition = self.build_tool_definition()

    def build_tool_definition(self):
        """
        Return the claude tool schema for inventory analyzsis

        """

        return {
            "name": "analyze_inventory",
            "description": (
                "Analyze pharmaceutical inventory data. "
                "Use this tool for inventory summaries, stockouts, "
                "low inventory detection, and expiration risk."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "analysis_type": {
                        "type": "string",
                        "enum": ["summary", "stockout", "low_inventory", "expiration_risk"],
                        "description": (" the type of inventory analysis to perform "),
                    },
                    "threshold": {
                        "type": "number",
                        "description": (
                            "inventory threshold used for low inventory"
                            "analysis default is 20"
                        ),
                    },
                    "days": {
                        "type": "integer",
                        "description": (
                            "Number of days used for expiration risk"
                            "analyzr Default is 90"
                        ),
                    },
                },
                "required": ["analysis_type"],
                "additionalProperties": False,
            },
        }

    def execute(self, tool_input):
        """
        Execute the correct inventory analysis function
        """
        analysis_type = tool_input.get("analysis_type")

        if analysis_type == "summary":
            return inventory_summary()

        if analysis_type == "stockout":
            return stockout_analysis()

        if analysis_type == "low_inventory":
            threshold = tool_input.get("threshold", 20)
            return low_inventory_products(threshold)

        if analysis_type == "expiration_risk":
            days = tool_input.get("days", 90)
            return expiration_risk(days)

        return {"error": f"Unknown analysis type {analysis_type}"}
