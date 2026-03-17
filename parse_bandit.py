import json

with open("bandit_output.json", encoding="utf-8") as f:
    data = json.load(f)

with open("parsed_bandit.txt", "w", encoding="utf-8") as out:
    for r in data["results"]:
        if r["issue_severity"] in ["HIGH", "MEDIUM"]:
            out.write(f"SEVERITY: {r['issue_severity']} | FILE: {r['filename']} | LINE: {r['line_number']}\n")
            out.write(f"TEXT: {r['issue_text']}\n")
            out.write("-" * 50 + "\n")
