import json
import os
from pathlib import Path

from anthropic import Anthropic
from dotenv import load_dotenv

from src.skills import skill_router
from src.skills.skill_loader import SkillLoader
from src.skills.skill_router import SkillRouter


class ClaudeAgent:
    """
    generic Claude agent responsible for

    1. connecting to the Anthropic API
    2. sending user question to claude
    3. exposing controller toole to Claude
    4. excuting requesstedtoole
    5. sending tool result back to claude
    6. returning Claude final response
    """

    def __init__(
        self,
        controllers,
        model="claude-sonnet-4-5",
        max_tokens=1500,
    ):

        self.project_root = Path(__file__).resolve().parents[2]

        self.model = model
        self.max_tokens = max_tokens

        self.controllers = controllers

        self.skill_loader = SkillLoader()
        self,skill_router = SkillRouter()
            

        self._load_environment()

        self.client = self._create_client()

        self.tools = self._collect_tools()

        self.controllers_map = self._build_controller_map()

    """
    Build Configuration
    """

    def _load_environment(self):
        """
        load ebviroment variable from the project .env file
        """
        env_path = self.project_root / ".env"

        load_dotenv(env_path)

    def _create_client(self):
        """
        creat the anthropic client
        """
        api_key = os.getenv(f"ANTHROPIC_API_KEY")

        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY is not set " "ADD it to thr .env file ")
        return Anthropic(api_key=api_key)

    """
    Build Conteollers 
    """

    def _collect_tools(self):
        """
        collect claude tool defination from controllers
        """
        return [controller.tool_definition for controller in self.controllers]

    def _build_controller_map(self):
        """
        creat a mappingbetween tool name and controllers

        example:
        {
            "analyze_inventory": InventoryController(...)
        }
        """

        return {
            controller.tool_definition["name"]: controller
            for controller in self.controllers
        }

    """
    build system Prompt
    """

    def _build_system_prompt(self, skill_content=""):

        base_prompt =  """
        you are PharmaOps AI, an AI assistant for pharmaceutical
        inventory and supply chanin opreation

        you have access to sepecialized tools that analyze company date 

        Rules:

        1. use the avalibale tools whenever a question requires information
        frome the pharmaceutical dataseys 

        2. Never invent values that are not prvided by the tools

        3. Base factual conclusion on tool result 

        4. Clearly distinguish:
            - findings
            - risks 
            - recommendarion

        5. Provide practical business recommendation when appropiate

        6. keep responses clear, concies, and business focused

        """
        if skill_content:
            return f"""{base_prompt}
                # Relevant Skill Instructions

                {skill_content}
                """
        return base_prompt 

    """
    Public Agent Interface

    """

    def ask(self, user_question):
        """
        process a users question through claude and execute toole calls until claude produces final answer
        """

        messages = [
            {
                "role": "user",
                "content": user_question,
            }
        ]

        skill_name = self.skill_router.route(user_question)

        skill_content = ""        

        if skill_content:
            skill_content = self.skill_loader.load(skill_name)
        
        system_prompt = self._build_system_prompt(skill_content)


        while True:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                system=system_prompt,
                tools=self.tools,
                messages=messages,
            )

            if response.stop_reason == "end_turn":
                return self._extract_text(response.content)

            if response.stop_reason == "tool_use":
                messages.append(
                    {
                        "role": "assistant",
                        "content": response.content,
                    }
                )

                tool_results = self._handle_tool_calls(response.content)

                messages.append(
                    {
                        "role": "user",
                        "content": tool_results,
                    }
                )

                continue
            raise RuntimeError(
                "Unexpexted Claude stop reason:" f"{response.stop_reason}"
            )

    """
    Build tool excution

    """

    def _handle_tool_calls(self, content):
        """
        Excute every too; requested by claude
        """
        tool_results = []

        for block in content:

            if block.type != "tool_use":
                continue

            tool_name = block.name
            tool_input = block.input

            print(f"\n[Claude requested tool: {tool_name}]")

            print(f"Toole input: {tool_input}")

            result = self._execute_tool(tool_name, tool_input)

            result_json = json.dumps(result, ensure_ascii=False, default=str)

            tool_results.append(
                {"type": "tool_result", "tool_use_id": block.id, "content": result_json}
            )
        return tool_results

    def _execute_tool(self, tool_name, tool_input):
        """
        route a tool request to the correct controller
        """

        controller = self.controllers_map.get(tool_name)

        if controller is None:
            return {"error": (f"NO controller registered" f"for tool: {tool_name}")}

        try:
            return controller.execute(tool_input)

        except Exception as error:
            return {"error": str(error), "tool": tool_name}

    """
    Build Response helpers 
    """

    def _extract_text(self, content):
        """
        Extract text blocks from Claude's response.
        """

        text_parts = []

        for block in content:

            if block.type == "text":
                text_parts.append(block.text)
        return "\n".join(text_parts)
