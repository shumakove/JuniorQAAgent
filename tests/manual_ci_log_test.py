from agent.tools import get_ci_logs_from_file

logs = get_ci_logs_from_file("ci.log")

print(logs)