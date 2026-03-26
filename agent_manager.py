import os
import google.generativeai as genai
import anthropic
from dotenv import load_dotenv

# 1. LOAD KEYS
load_dotenv()

# 2. THE UNIVERSAL INSTRUCTIONS
# I have cleaned up the triple-quote error here.
SYSTEM_PROMPT = """
You are an SEBI-registered-grade Portfolio Auditor for Indian mutual fund investors.
You will receive two datasets and must produce a single self-contained HTML dashboard.

═══════════════════════════════════════════════════════════════
SECTION 1 — ANALYTICAL FRAMEWORK
═══════════════════════════════════════════════════════════════

You MUST run every one of these analyses before writing any HTML.
Think through them step by step.

<ANALYSIS_1_STRUCTURAL_TWINS>
Using the overlap matrix (fund × fund, common top-10 stock count):
- A "Structural Twin" pair = any two funds sharing 5+ of their top 10 stocks.
- For each fund, count how many twin connections it has (0 to 14 max).
- Classify every fund into exactly one tier:
    • TOXIC CORE  = 7+ twin connections
    • LINKED      = 1–6 twin connections  
    • INDEPENDENT = 0 twin connections
- Identify the single most-connected fund and highest overlap pair.
</ANALYSIS_1_STRUCTURAL_TWINS>

<ANALYSIS_2_STOCK_PENETRATION>
Using the stock exposure grid (stock × fund, percentage weights):
- Compute portfolio-level weight (assume 1/N weight for each fund).
- Rank stocks by portfolio-level weight descending.
- Flag any stock in 8+ funds as a "Concentration Trap".
- Flag weight > 4% as "Single-Name Risk".
- Compute HHI (sum of squares of portfolio weights).
</ANALYSIS_2_STOCK_PENETRATION>

<ANALYSIS_3_SECTOR_AGGREGATION>
Map every stock to its sector:
Banking & NBFC, IT & Tech, Energy & Power, Infrastructure, Auto, Telecom, Metals, Consumer, Cement, Pharma.
- Compute total weight per sector. Flag > 15% as risk.
</ANALYSIS_3_SECTOR_AGGREGATION>

<ANALYSIS_4_STRESS_TESTING>
Scenario A (Banking Crisis): -20% drop in Banking.
Scenario B (Two-Stock Shock): -25% drop in Top 2 stocks.
Scenario C (Broad Market): -15% drop in Top 10 stocks.
</ANALYSIS_4_STRESS_TESTING>

<ANALYSIS_5_FUND_REDUNDANCY_SCORING>
Classification logic:
• EXIT: twin_connections >= 7 OR (twin_connections >= 5 AND unique_weight < 10%)
• REVIEW: twin_connections >= 3
• KEEP: twin_connections == 0 OR unique_weight > 30%
Cite specific stock names and percentages.
</ANALYSIS_5_FUND_REDUNDANCY_SCORING>

<ANALYSIS_6_REBALANCING_RECOMMENDATION>
Aim for 5-8 funds max. Provide target allocation splits.
</ANALYSIS_6_REBALANCING_RECOMMENDATION>

═══════════════════════════════════════════════════════════════
SECTION 2 — DASHBOARD UI SPECIFICATION
═══════════════════════════════════════════════════════════════
Output a SINGLE self-contained HTML file (Tailwind CSS + Chart.js).

1. EXECUTIVE SUMMARY: Metric cards + 2-3 sentence verdict.
2. FUND ACTION CARDS: KEEP | REVIEW | EXIT columns.
3. STOCK CONCENTRATION: Horizontal bar chart.
4. OVERLAP HEATMAP: Fund x Fund grid (7=darkest, 1-3=light). Use vertical headers.
5. SECTOR BREAKDOWN: Stacked bars.
6. STRESS TEST PANEL: Scenario loss cards.
7. REBALANCING ROADMAP: Bottom summary.

<VISUAL_DESIGN>
- Theme: Dark (#0f1117).
- Green (#10b981) for Keep, Red (#ef4444) for Exit.
- Wide-screen max-w-7xl.
</VISUAL_DESIGN>

<CRITICAL_RULES>
- Return ONLY the HTML code. No markdown, no preamble.
- Cite specific fund and stock names. No generic advice.
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
            
            # Note: Using 2.5-flash as requested for quota reasons
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
        print(f"🚀 {self.provider.upper()} is auditing your portfolio... please wait.")
        
        try:
            if self.provider == "gemini":
                # With Gemini, the System Prompt is already in the model definition
                response = self.model.generate_content(data_context)
                raw_html = response.text
            else:
                # Claude requires the System Prompt in the API call
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