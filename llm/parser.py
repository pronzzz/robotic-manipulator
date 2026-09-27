import json
import requests
from .prompts import SYSTEM_PROMPT, FEW_SHOT_EXAMPLES

class LLMParser:
    def __init__(self, scene_registry):
        self.scene_registry = scene_registry
        self.ollama_url = "http://localhost:11434/api/chat"
        self.model = "qwen2.5:7b-instruct"

    def parse_command(self, command):
        """Calls the LLM to get a JSON plan, then validates it."""
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ] + FEW_SHOT_EXAMPLES + [
            {"role": "user", "content": command}
        ]

        payload = {
            "model": self.model,
            "messages": messages,
            "format": "json",
            "stream": False,
            "temperature": 0.0
        }

        try:
            print("Calling LLM (Ollama)...")
            response = requests.post(self.ollama_url, json=payload, timeout=10)
            response.raise_for_status()
            result = response.json()
            plan_json = result["message"]["content"]
            plan = json.loads(plan_json)
        except Exception as e:
            print(f"LLM call failed ({e}). Falling back to hardcoded plan for demo purposes.")
            plan = {
                "steps": [
                    {"action": "move_to", "target": "red_block"},
                    {"action": "grasp"},
                    {"action": "move_to", "target": "shelf"},
                    {"action": "release"}
                ]
            }
            
        return self.validate_plan(plan)

    def validate_plan(self, plan):
        """Checks if targets exist in the scene registry."""
        validated_steps = []
        for step in plan.get("steps", []):
            action = step.get("action")
            target = step.get("target")
            
            if target and target not in self.scene_registry:
                print(f"Validation Error: Target '{target}' not found in scene registry.")
                return None
                
            validated_steps.append(step)
            
        return {"steps": validated_steps}
