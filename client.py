"""
Enterprise Executive Briefing & Strategic Memo Deliverable Synthesizer (Zero External Dependencies)
Provides structured executive memos, decision options matrices, risk registers, and word-budget analytics.
"""
import time
import math
import hashlib
import json
from typing import Dict, Any, List, Optional

class EnterpriseExecutiveBriefingDocSynthesizer:
    def __init__(self, reading_words_per_minute: int = 220):
        self.wpm = reading_words_per_minute

    def compile_risk_matrix(self, risks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculates composite risk scores: Score = Likelihood (1-5) * Severity (1-5)."""
        scored_risks = []
        for r in risks:
            name = r.get("risk_name", "Operational Risk")
            lh = int(r.get("likelihood", 3))
            sev = int(r.get("severity", 3))
            composite = lh * sev

            tier = "LOW"
            if composite >= 15:
                tier = "CRITICAL"
            elif composite >= 8:
                tier = "MODERATE"

            scored_risks.append({
                "risk_name": name,
                "likelihood": lh,
                "severity": sev,
                "composite_score": composite,
                "tier": tier,
                "mitigation": r.get("mitigation", "Continuous monitoring and guardrails.")
            })

        scored_risks.sort(key=lambda x: x["composite_score"], reverse=True)
        return {
            "total_risks_analyzed": len(scored_risks),
            "highest_risk_tier": scored_risks[0]["tier"] if scored_risks else "NONE",
            "risk_matrix": scored_risks
        }

    def synthesize_executive_briefing(
        self,
        memo_title: str,
        author_role: str,
        raw_findings_text: str,
        decision_options: Optional[List[Dict[str, Any]]] = None,
        risks: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Transforms raw text findings into a polished, professional C-suite Executive Briefing Memo.
        Includes Executive Summary, Strategic Context, Decision Matrix, Risk Register, and Recommendations.
        """
        decision_options = decision_options or [
            {"option": "Option A: Accelerate Autonomous Agent Deployment", "cost_usd": 250000, "pros": ["Immediate 40% efficiency gains"], "cons": ["High upfront capital"]},
            {"option": "Option B: Phased Divisional Pilot", "cost_usd": 75000, "pros": ["Controlled risk profile"], "cons": ["Slower time to market"]}
        ]
        risks = risks or [
            {"risk_name": "API Rate Limit & Vendor Lock-in", "likelihood": 4, "severity": 3, "mitigation": "Multi-provider model fallback architecture"},
            {"risk_name": "Cross-Boundary Clearance Leakage", "likelihood": 2, "severity": 5, "mitigation": "Automated zero-leakage PII sentinel"}
        ]

        risk_analysis = self.compile_risk_matrix(risks)

        # Word count & reading time
        words = len(raw_findings_text.split())
        est_read_min = max(1.0, round(words / self.wpm, 1))

        now_str = time.strftime("%Y-%m-%d")
        doc_id = "MEMO-" + hashlib.sha256(f"{memo_title}{now_str}".encode("utf-8")).hexdigest()[:12]

        markdown_memo = (
            f"# EXECUTIVE BRIEFING MEMO: {memo_title.upper()}\n\n"
            f"**TO:** Executive Leadership Committee\n"
            f"**FROM:** {author_role} (Autonomous Enterprise Work Agent)\n"
            f"**DATE:** {now_str}\n"
            f"**DOCUMENT ID:** {doc_id}\n"
            f"**ESTIMATED READING TIME:** {est_read_min} minutes ({words} words)\n\n"
            f"---\n\n"
            f"## 1. Executive Summary\n"
            f"{raw_findings_text[:300]}...\n\n"
            f"## 2. Core Operational Findings & Evidence\n"
            f"{raw_findings_text}\n\n"
            f"## 3. Decision Matrix & Strategic Alternatives\n"
        )

        for opt in decision_options:
            markdown_memo += f"- **{opt.get('option')}** (Est. Cost: ${opt.get('cost_usd', 0):,}):\n"
            markdown_memo += f"  - *Advantages:* {', '.join(opt.get('pros', []))}\n"
            markdown_memo += f"  - *Trade-offs:* {', '.join(opt.get('cons', []))}\n"

        markdown_memo += "\n## 4. Key Risk Register & Guardrails\n"
        for r in risk_analysis["risk_matrix"]:
            markdown_memo += f"- **[{r['tier']}] {r['risk_name']}** (Severity {r['composite_score']}/25): {r['mitigation']}\n"

        markdown_memo += (
            f"\n## 5. Immediate Recommended Action\n"
            f"Leadership sign-off requested on {decision_options[0].get('option')} by end of sprint.\n"
        )

        return {
            "document_id": doc_id,
            "title": memo_title,
            "author": author_role,
            "date": now_str,
            "metrics": {
                "word_count": words,
                "reading_time_minutes": est_read_min
            },
            "risk_summary": risk_analysis,
            "decision_options_count": len(decision_options),
            "formatted_markdown": markdown_memo,
            "deliverable_ready": True
        }
