"""MCP Server for Enterprise Executive Briefing Doc Synthesizer."""
import sys
import json
import time
from client import EnterpriseExecutiveBriefingDocSynthesizer

synthesizer = EnterpriseExecutiveBriefingDocSynthesizer()

def handle_call_tool(params):
    name = params.get("name")
    args = params.get("arguments", {})
    if name != "synthesize_executive_briefing_memo":
        raise ValueError(f"Unknown tool: {name}")

    action = args.get("action", "synthesize_executive_briefing")
    if action == "synthesize_executive_briefing":
        return synthesizer.synthesize_executive_briefing(
            memo_title=args.get("memo_title", "Q3 Strategic Memo"),
            author_role=args.get("author_role", "WorkBuddy Agent"),
            raw_findings_text=args.get("raw_findings_text", "Operational findings summarized."),
            decision_options=args.get("decision_options"),
            risks=args.get("risks")
        )
    elif action == "compile_risk_matrix":
        return synthesizer.compile_risk_matrix(args.get("risks", []))
    else:
        raise ValueError(f"Invalid action: {action}")

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print("Running self-test...")
        memo = synthesizer.synthesize_executive_briefing(
            "Test Strategy", "Chief Agent", "Testing core enterprise doc deliverable synthesis."
        )
        assert memo["deliverable_ready"] is True
        assert len(memo["formatted_markdown"]) > 100
        print("Self-test PASSED!")
        sys.exit(0)

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            msg_id = req.get("id")
            method = req.get("method")
            if method == "initialize":
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "serverInfo": {"name": "EnterpriseExecutiveBriefingDocSynthesizer", "version": "1.0.0"},
                        "capabilities": {"tools": {}}
                    }
                }
            elif method == "tools/list":
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "tools": [{
                            "name": "synthesize_executive_briefing_memo",
                            "description": "Synthesize goal-to-document deliverables: compile structured executive briefing memos, auto-format risk registers, synthesize decision options, and compute reading time budgets.",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "action": {"type": "string", "enum": ["synthesize_executive_briefing", "compile_risk_matrix"]},
                                    "memo_title": {"type": "string"},
                                    "author_role": {"type": "string"},
                                    "raw_findings_text": {"type": "string"},
                                    "decision_options": {"type": "array"},
                                    "risks": {"type": "array"}
                                },
                                "required": ["action"]
                            }
                        }]
                    }
                }
            elif method == "tools/call":
                res = handle_call_tool(req.get("params", {}))
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
                }
            else:
                resp = {"jsonrpc": "2.0", "id": msg_id, "result": {}}
            print(json.dumps(resp), flush=True)
        except Exception as e:
            err_resp = {"jsonrpc": "2.0", "id": None, "error": {"code": -32000, "message": str(e)}}
            print(json.dumps(err_resp), flush=True)

if __name__ == "__main__":
    main()
