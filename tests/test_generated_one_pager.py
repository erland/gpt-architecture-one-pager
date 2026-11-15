"""Fixture-based checks: no model is invoked in CI."""
from __future__ import annotations
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from validate_generated_one_pager import SV, check_report

def report(source="**[OWASP – Agentic Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/)**, OWASP (2025).", recommendation="Testa", extra=""):
    sections = []
    for index, heading in enumerate(SV, 1):
        if index == 12:
            body = recommendation + "\n\nAvgränsad pilot med kontrollerad åtkomst."
        elif index == 14:
            body = source + "\n\nTillförlitlighet: bedömning separerad från källfakta."
        else:
            body = "En kort, konkret bedömning av betydelse, risker och konsekvenser."
        sections.append(f"{index}. {heading}\n\n{body}")
    return "ARCHITECTURE ONE-PAGER\n\n" + "\n\n".join(sections) + "\n" + extra

class GeneratedOnePagerTests(unittest.TestCase):
    def test_valid(self):
        self.assertEqual([], check_report(report()))
    def test_legacy_plus_one_failure(self):
        errors = check_report(report(source="OWASP Gen AI Security Project +1"))
        self.assertTrue(any("placeholder" in error.lower() for error in errors))
        self.assertTrue(any("url" in error.lower() for error in errors))
    def test_missing_source_link(self):
        self.assertTrue(any("URL" in error for error in check_report(report(source="OWASP, 2025"))))
    def test_bad_heading_order(self):
        bad = report().replace("3. Vad det är", "3. Felaktigt avsnitt")
        self.assertTrue(any("heading" in error.lower() for error in check_report(bad)))
    def test_missing_heading(self):
        self.assertTrue(any("14" in error for error in check_report(report().replace("10. Mognad och ekosystem", "Mognad och ekosystem"))))
    def test_multiple_recommendations(self):
        self.assertTrue(any("exactly one" in error for error in check_report(report(recommendation="Testa\n\nAvvakta"))))
    def test_long_text(self):
        self.assertTrue(any("too long" in error for error in check_report(report(extra="") .replace("3. Vad det är", ("Långt textstycke. " * 400) + "\n\n3. Vad det är"))))
    def test_no_live_claim(self):
        self.assertEqual([], check_report(report(source="[Källa](https://example.org/report) – endast exempel, inte verifierad.")))

if __name__ == "__main__":
    unittest.main()
