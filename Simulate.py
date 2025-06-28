from dataclasses import dataclass

@dataclass
class SimulationResult:
    command: str
    description: str
    severity: str
    mitre_attack_tag: str
    succeeded: bool
    error_message: str = ""


