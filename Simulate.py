import subprocess
from dataclasses import dataclass
from jinja2 import Template
from datetime import datetime

@dataclass
class SimulationResult:
    command: str
    description: str
    severity: str
    mitre_attack_tag: str
    succeeded: bool
    error_message: str = ""



def run_command(command, description, severity, mitre_tag):
    try:
        subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return SimulationResult(command, description, severity, mitre_tag, True)
    except subprocess.CalledProcessError as e:
        return SimulationResult(command, description, severity, mitre_tag, False, error_message=e.stderr.decode('utf-8'))


def generate_html_report(simulation_results):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    total = len(simulation_results)
    passed = sum(1 for r in simulation_results if r.succeeded)
    failed = total - passed
    success_rate = round((passed / total) * 100, 2) if total else 0

    with open("Template.html", "r") as file:
        template = Template(file.read())

    return template.render(
        timestamp=timestamp,
        total=total,
        passed=passed,
        failed=failed,
        success_rate=success_rate,
        results=simulation_results
    )



if __name__ == "__main__":
    tests = [
        ("whoami", "Check user identity", "Low", "T1033"),
        ("invalidcommand123", "Deliberate failure", "Medium", "T1059")
    ]

    results = [run_command(*test) for test in tests]
    html = generate_html_report(results)

    with open("simulation_report.html", "w") as report_file:
        report_file.write(html)

    print("Report generated: simulation_report.html")