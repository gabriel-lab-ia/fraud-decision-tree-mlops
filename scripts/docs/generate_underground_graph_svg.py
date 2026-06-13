from pathlib import Path

NODES = [
    ("Raw data", 80, 170, "#4285f4"),
    ("DAO", 220, 105, "#34a853"),
    ("Cleaning", 220, 235, "#fbbc05"),
    ("Validation", 370, 105, "#ea4335"),
    ("Preprocessing", 370, 235, "#4285f4"),
    ("Features", 530, 170, "#34a853"),
    ("Decision Tree", 700, 170, "#fbbc05"),
    ("MLflow", 860, 95, "#ea4335"),
    ("Artifacts", 860, 245, "#4285f4"),
    ("FastAPI", 1030, 170, "#34a853"),
    ("MongoDB", 1190, 95, "#fbbc05"),
    ("Monitoring", 1190, 245, "#ea4335"),
    ("Tests", 530, 335, "#4285f4"),
    ("CI/CD", 700, 335, "#34a853"),
    ("uv", 860, 335, "#fbbc05"),
    ("Docker", 1030, 335, "#ea4335"),
]


def generate_svg() -> str:
    node_markup = "\n".join(
        f'<g><circle cx="{x}" cy="{y}" r="24" fill="{color}"/>'
        f'<text x="{x}" y="{y + 43}" text-anchor="middle">{label}</text></g>'
        for label, x, y, color in NODES
    )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 430">
<defs>
  <pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse">
    <path d="M20 0H0V20" fill="none" stroke="#171717" stroke-width="1"/>
  </pattern>
  <style>text{{fill:#d8d8d8;font:13px Arial,sans-serif}} .edge{{fill:none;stroke:#444;stroke-width:2}}</style>
</defs>
<rect width="1280" height="430" fill="#050505"/><rect width="1280" height="430" fill="url(#grid)"/>
<g class="edge">
<path d="M104 170C145 170 170 105 196 105"/><path d="M104 170C145 170 170 235 196 235"/>
<path d="M244 105C290 105 315 105 346 105"/><path d="M244 235C290 235 315 235 346 235"/>
<path d="M394 105C450 105 465 170 506 170"/><path d="M394 235C450 235 465 170 506 170"/>
<path d="M554 170H676"/><path d="M724 170C775 170 790 95 836 95"/>
<path d="M724 170C775 170 790 245 836 245"/><path d="M884 245C945 245 950 170 1006 170"/>
<path d="M1054 170C1100 170 1115 95 1166 95"/><path d="M1054 170C1100 170 1115 245 1166 245"/>
<path d="M554 335H676"/><path d="M724 335H836"/><path d="M884 335H1006"/>
</g>
{node_markup}
<text x="40" y="45" font-size="24">FRAUD MLOPS / SYSTEM GRAPH</text>
</svg>"""


if __name__ == "__main__":
    output = Path("docs/diagrams/fraud-mlops-underground-graph.svg")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(generate_svg(), encoding="utf-8")
