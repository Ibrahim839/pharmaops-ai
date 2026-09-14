from src.tool.shipment_analysis import(
    shipment_summary,
    shipment_status_analysis,
    delivery_performance,
    carrier_performance
)

class ShipmentController:
    def __init__(self):
        self.tool_definition  = self.build_tool_definition()


    def build_tool_definition(self):
        return {
            "name": "analyze_shipment",
            "description": (
                "Analyze pharmaceutical shipment date"
                "Use this tool for shipment summeries, delivery performance "
                "carrier  performance, and shipment completness analysis"
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "analysis_type": {
                        "type": "string",
                        "enum": [
                            "summary",
                            "delivery_performance",
                            "carrier_performance",
                            "shipment_status"
                        ],
                        "description": (
                            "the type of shipment analysis to perform"
                        ),
                    },
                },
                "required": ["analysis_type"],
                "additionalProperties": False,
            }
        }
    

    def execute(self, tool_input):
        analysis_type = tool_input.get("analysis_type")

        if analysis_type =="summary":
            return shipment_summary()
        
        if analysis_type == "delivery_performance":
            return delivery_performance()

        if analysis_type == "carrier_performance":
            return carrier_performance()

        if analysis_type == "shipment_status":
            return shipment_status_analysis()

        return {
            "error": f"Unknown analysis type: {analysis_type}"
        }
