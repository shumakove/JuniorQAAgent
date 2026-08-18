from dataclasses import dataclass

@dataclass
class AgentAction:
    tool: str
    arguments: dict
    reasoning: str

    