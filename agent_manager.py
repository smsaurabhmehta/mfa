import os
import google.generativeai as genai
import anthropic
from dotenv import load_dotenv

# 1. LOAD KEYS
load_dotenv()

# 2. THE UNIVERSAL INSTRUCTIONS (Refined for Static Fintech UI)
SYSTEM_PROMPT = """
You are a Senior Portfolio Auditor. Your task is to transform complex mutual fund data into a professional, static HTML "X-Ray" Report. 

<STYLE_GUIDE>
- Aesthetic: High-end Fintech (Bloomberg Terminal meets Stripe Dashboard).
- Interactivity: NONE. No sliders, no dropdowns, no hidden tabs. Everything must be visible on the "printed" page.
- Typography: Clean sans-serif (Inter/System-UI). 
- Layout: Structured cards with subtle borders. Avoid "busy" shadows.
- Color Palette: Deep Charcoal (#0f1117) background, Slate cards (#1a1d27), and Emerald/Rose/Amber accents.
</STYLE_GUIDE>

═══════════════════════════════════════════════════════════════
SECTION 1 — ANALYTICAL FRAMEWORK (The "Brain")
═══════════════════════════════════════════════════════════════

Perform these steps before coding the HTML:
1. ANALYSIS_STRUCTURAL_TWINS: Identify funds sharing 5+ top-10 stocks. Tier them: Toxic Core (7+), Linked (1-6), Independent (0).
2. ANALYSIS_STOCK_PENETRATION: Rank stocks by portfolio weight. Flag "Concentration Traps" (in 8+ funds) or "Single-Name Risk" (>4% weight).
3. ANALYSIS_SECTOR_AGGREGATION: Group by Banking, IT, Energy, etc. Flag sectors > 15%.
4. ANALYSIS_STRESS_TESTING: Calculate % loss for Banking Crisis (-20%), Top-2 Shock (-25%), and Market Shock (-15%).
5. ANALYSIS_REDUNDANCY_SCORING: Classify every fund as KEEP, REVIEW, or EXIT based on twin counts and unique stock weights.

═══════════════════════════════════════════════════════════════
SECTION 2 — STATIC UI SPECIFICATION (The "Body")
═══════════════════════════════════════════════════════════════

The HTML must be a single file using Tailwind CSS and Chart.js.

1. EXECUTIVE SUMMARY: 4-6 large Metric Cards (Total Funds, Twin Pairs, HHI Score, Exit Count). Below them, a "Verdicts" box with 3 bullet points naming specific funds/stocks.
2. ACTIONABLE CLASSIFICATION: A 3-column grid (KEEP | REVIEW | EXIT). Each fund gets a high-contrast card listing its "Structural Twin Count" and its 2 most "Unique" stock picks.
3. CONCENTRATION CHART: A static horizontal bar chart of the Top 15 stocks. Color bars by "Fund Penetration" (Dark Red for stocks held by 10+ funds).
4. THE 25-FUND HEATMAP: 
   - Use a fixed-layout table. 
   - Rotated headers (vertical) to prevent overlap.
   - Small, crisp font (10px). 
   - Direct color mapping (Red for 5+ overlap, Grey for low overlap).
5. SECTOR EXPOSURE: A clean bar chart comparing your portfolio vs. Nifty 50 benchmarks.
6. RISK SCENARIOS: 3 static cards showing "Estimated Portfolio Value Loss" in large, bold red percentages.
7. REBALANCING ROADMAP: A final "Target Portfolio" table showing recommended funds and weightage.

<CRITICAL_RULES>
1. DO NOT USE TEMPLATE TAGS (no {{ }} or {% %}).
2. PERFORM THE MATH: You must calculate every percentage, HHI score, and overlap count yourself.
3. HARDCODE THE VALUES: Write the actual numbers and fund names directly into the HTML text. 
   - WRONG: <div>{{ fund.name }}</div>
   - RIGHT: <div>Parag Parikh Flexi Cap Fund</div>
4. FULL ENUMERATION: If I provide 25 funds, you must generate 25 individual "Action Cards" and a 25x25 Heatmap. No truncating.
5. NO PREAMBLE: Return ONLY the raw <html> code.
</CRITICAL_RULES>
"""

class PortfolioAgent:
    def __init__(self, provider="gemini"):
        self.provider = provider
        
        if provider == "gemini":
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                raise ValueError("GEMINI_API_KEY not found in .env file")
            genai.configure(api_key=api_key)
            
            # Using 2.5-flash for speed/quota, with the high-end fintech system prompt
            self.model = genai.GenerativeModel(
                model_name="models/gemini-2.5-flash",
                system_instruction=SYSTEM_PROMPT
            )
            
        elif provider == "claude":
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                raise ValueError("ANTHROPIC_API_KEY not found in .env file")
            self.client = anthropic.Anthropic(api_key=api_key)

    def generate_report(self, data_context):
        print(f" {self.provider.upper()} is auditing your portfolio (Static Mode)... please wait.")
        
        try:
            if self.provider == "gemini":
                response = self.model.generate_content(
                    f"ACTUAL PORTFOLIO DATA TO ANALYZE:\n{data_context}\n\n"
                    "Generate the final, hardcoded HTML report now."
                )
                raw_html = response.text
            else:
                response = self.client.messages.create(
                    model="claude-3-5-sonnet-20240620",
                    max_tokens=8000,
                    system=SYSTEM_PROMPT,
                    messages=[{"role": "user", "content": data_context}]
                )
                raw_html = response.content[0].text

            # Clean up Markdown artifacts
            clean_html = raw_html.replace("```html", "").replace("```", "").strip()
            return clean_html

        except Exception as e:
            raise Exception(f"AI Generation Error ({self.provider}): {str(e)}")