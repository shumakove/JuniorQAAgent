from dataclasses import dataclass, field

@dataclass
class AgentState:
    test_name: str
    initial_error: str = ""
    ci_logs: str = ""
    git_diff: str = ""

    test_runs: list[dict] = field(default_factory=list)
    test_history: list[dict] = field(default_factory=list)
    related_tests: list[dict] = field(default_factory=list)

    hypothesis: str = ""
    confidence: float = 0.0
    actions_taken: list[str] = field(default_factory=list)
    evidence: list[str] = field(default_factory=list)

    final_classification: str | None = None
    human_escalation: bool = False

    iteration: int = 0
    finished: bool = False