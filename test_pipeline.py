from config import DEFAULT_CONFIG

from agents.coordinator_agent import (
    CoordinatorAgent
)

agent = CoordinatorAgent(
    DEFAULT_CONFIG
)

result = agent.run_analysis(
    "MSFT"
)

print(
    result["memo"]
)