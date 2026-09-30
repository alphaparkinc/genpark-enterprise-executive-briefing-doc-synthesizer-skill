"""Example usage for EnterpriseExecutiveBriefingDocSynthesizer."""
import sys
import json
from client import EnterpriseExecutiveBriefingDocSynthesizer

sys.stdout.reconfigure(encoding='utf-8')

def main():
    print("=== Enterprise Executive Briefing Memo Synthesizer Demo (WorkBuddy Goal-to-Doc) ===")
    synthesizer = EnterpriseExecutiveBriefingDocSynthesizer()

    findings = """
    Q3 Enterprise Transformation Audit:
    - 420 autonomous agent workflows now live across customer support, finance, and engineering.
    - Employee time saved reached an aggregate 12,400 hours per month.
    - Cloud infrastructure inference expenses grew by 18%, but offset by a 62% decrease in external contractor fees.
    """

    print("\n--- Synthesizing C-Suite Strategic Memo ---")
    memo = synthesizer.synthesize_executive_briefing(
        memo_title="Enterprise Autonomous Agent ROI & Scalability Review",
        author_role="WorkBuddy Senior Agentic PM",
        raw_findings_text=findings
    )
    print(f"Document ID: {memo['document_id']}")
    print(f"Word Count: {memo['metrics']['word_count']}, Reading Time: {memo['metrics']['reading_time_minutes']} min")
    print("\n--- Generated Executive Memo Preview ---")
    print(memo["formatted_markdown"])

if __name__ == "__main__":
    main()
