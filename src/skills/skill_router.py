import keyword


class SkillRouter:
    """
    Router user question to the most relevant skill
    """

    def route(self, user_question):
        question = user_question.lower()


        if any(
            keyword in question
            for keyword in [
                "inventory",
                "stock",
                "stockout",
                "low inventory",
                "expiration",
                "expiry",
                "batch",
                ]
        ):

            return "inventory-analysis"
        

        if any(
            keyword in question
            for keyword in [
                "shipment",
                "delivery",
                "carrier",
                "tracking",
                "delay",
            ]
        ):
            return "shipment-analysis"

