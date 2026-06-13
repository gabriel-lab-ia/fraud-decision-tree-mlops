from pathlib import Path


OUTPUT_PATH = Path("docs/diagrams/fraud-mlops-big-tech-architecture.svg")


SVG = r'''<svg width="1800" height="1120" viewBox="0 0 1800 1120" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse">
      <path d="M 24 0 L 0 0 0 24" fill="none" stroke="#1f2937" stroke-width="0.8"/>
    </pattern>

    <marker id="arrow-blue" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto">
      <path d="M2,2 L10,6 L2,10 Z" fill="#38bdf8"/>
    </marker>

    <marker id="arrow-green" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto">
      <path d="M2,2 L10,6 L2,10 Z" fill="#22c55e"/>
    </marker>

    <marker id="arrow-orange" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto">
      <path d="M2,2 L10,6 L2,10 Z" fill="#fb923c"/>
    </marker>

    <marker id="arrow-purple" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto">
      <path d="M2,2 L10,6 L2,10 Z" fill="#c084fc"/>
    </marker>
  </defs>

  <style>
    .title { font: 800 32px Inter, Segoe UI, Arial, sans-serif; fill: #f8fafc; }
    .subtitle { font: 500 17px Inter, Segoe UI, Arial, sans-serif; fill: #cbd5e1; }
    .lane-title { font: 800 15px Inter, Segoe UI, Arial, sans-serif; fill: #f8fafc; }
    .box-title { font: 800 13px Inter, Segoe UI, Arial, sans-serif; fill: #f8fafc; }
    .box-subtitle { font: 500 11px Inter, Segoe UI, Arial, sans-serif; fill: #cbd5e1; }
    .legend { font: 600 12px Inter, Segoe UI, Arial, sans-serif; fill: #cbd5e1; }
  </style>

  <rect width="1800" height="1120" fill="#030712"/>
  <rect width="1800" height="1120" fill="url(#grid)" opacity="0.75"/>

  <rect x="330" y="28" width="1140" height="82" rx="18" fill="#0b1120" stroke="#94a3b8" stroke-width="1.8"/>
  <text x="900" y="64" text-anchor="middle" class="title">Fraud Decision Tree MLOps Architecture</text>
  <text x="900" y="91" text-anchor="middle" class="subtitle">Linux-first • uv • scikit-learn • MLflow • FastAPI • MongoDB • Docker • CI/CD</text>

  <!-- Lanes -->
  <rect x="55" y="150" width="370" height="840" rx="18" fill="#061826" stroke="#0284c7" stroke-width="2"/>
  <text x="240" y="184" text-anchor="middle" class="lane-title">DEVELOPMENT &amp; VERSIONING LAYER</text>

  <rect x="475" y="150" width="520" height="840" rx="18" fill="#061a10" stroke="#16a34a" stroke-width="2"/>
  <text x="735" y="184" text-anchor="middle" class="lane-title">MACHINE LEARNING LIFECYCLE LAYER</text>

  <rect x="1045" y="150" width="350" height="840" rx="18" fill="#1c1005" stroke="#f97316" stroke-width="2"/>
  <text x="1220" y="184" text-anchor="middle" class="lane-title">SERVING &amp; APPLICATION LAYER</text>

  <rect x="1445" y="150" width="300" height="840" rx="18" fill="#16081f" stroke="#9333ea" stroke-width="2"/>
  <text x="1595" y="184" text-anchor="middle" class="lane-title">TELEMETRY &amp; OBSERVABILITY LAYER</text>

  <!-- Development boxes -->
  <g fill="#101820" stroke="#38bdf8" stroke-width="2">
    <rect x="95" y="220" width="290" height="70" rx="12"/>
    <rect x="95" y="320" width="290" height="70" rx="12"/>
    <rect x="95" y="420" width="290" height="70" rx="12"/>
    <rect x="95" y="520" width="290" height="70" rx="12"/>
    <rect x="95" y="620" width="290" height="70" rx="12"/>
    <rect x="95" y="720" width="290" height="70" rx="12"/>
  </g>

  <text x="240" y="248" text-anchor="middle" class="box-title">Linux Workstation</text>
  <text x="240" y="270" text-anchor="middle" class="box-subtitle">Pop!_OS • terminal-first workflow</text>

  <text x="240" y="348" text-anchor="middle" class="box-title">VS Code</text>
  <text x="240" y="370" text-anchor="middle" class="box-subtitle">source editing • local debugging</text>

  <text x="240" y="448" text-anchor="middle" class="box-title">uv Environment</text>
  <text x="240" y="470" text-anchor="middle" class="box-subtitle">.venv • pyproject.toml • uv.lock</text>

  <text x="240" y="548" text-anchor="middle" class="box-title">Git Repository</text>
  <text x="240" y="570" text-anchor="middle" class="box-subtitle">local commits • Linux-first source</text>

  <text x="240" y="648" text-anchor="middle" class="box-title">GitHub Repository</text>
  <text x="240" y="670" text-anchor="middle" class="box-subtitle">open-source portfolio project</text>

  <text x="240" y="748" text-anchor="middle" class="box-title">GitHub Actions</text>
  <text x="240" y="770" text-anchor="middle" class="box-subtitle">CI • tests • model validation</text>

  <!-- ML boxes -->
  <g fill="#101820" stroke="#22c55e" stroke-width="2">
    <rect x="540" y="220" width="390" height="70" rx="12"/>
    <rect x="540" y="320" width="390" height="70" rx="12"/>
    <rect x="540" y="420" width="390" height="70" rx="12"/>
    <rect x="540" y="520" width="390" height="70" rx="12"/>
    <rect x="540" y="620" width="390" height="70" rx="12"/>
    <rect x="540" y="720" width="390" height="70" rx="12"/>
    <rect x="540" y="840" width="180" height="74" rx="12"/>
    <rect x="750" y="840" width="180" height="74" rx="12"/>
  </g>

  <text x="735" y="248" text-anchor="middle" class="box-title">Fraud Dataset</text>
  <text x="735" y="270" text-anchor="middle" class="box-subtitle">synthetic baseline • future real data</text>

  <text x="735" y="348" text-anchor="middle" class="box-title">Data Validation</text>
  <text x="735" y="370" text-anchor="middle" class="box-subtitle">schema • target • missing values</text>

  <text x="735" y="448" text-anchor="middle" class="box-title">Feature Engineering</text>
  <text x="735" y="470" text-anchor="middle" class="box-subtitle">risk signals • transaction features</text>

  <text x="735" y="548" text-anchor="middle" class="box-title">Decision Tree Training</text>
  <text x="735" y="570" text-anchor="middle" class="box-subtitle">scikit-learn DecisionTreeClassifier</text>

  <text x="735" y="648" text-anchor="middle" class="box-title">Model Evaluation</text>
  <text x="735" y="670" text-anchor="middle" class="box-subtitle">accuracy • precision • recall • F1 • ROC-AUC</text>

  <text x="735" y="748" text-anchor="middle" class="box-title">Model Validation Gate</text>
  <text x="735" y="770" text-anchor="middle" class="box-subtitle">minimum recall • F1 • ROC-AUC</text>

  <text x="630" y="870" text-anchor="middle" class="box-title">MLflow Tracking</text>
  <text x="630" y="892" text-anchor="middle" class="box-subtitle">params • metrics • runs</text>

  <text x="840" y="870" text-anchor="middle" class="box-title">Model Artifact</text>
  <text x="840" y="892" text-anchor="middle" class="box-subtitle">joblib • metadata</text>

  <!-- Serving boxes -->
  <g fill="#101820" stroke="#fb923c" stroke-width="2">
    <rect x="1090" y="235" width="260" height="72" rx="12"/>
    <rect x="1090" y="355" width="260" height="72" rx="12"/>
    <rect x="1090" y="475" width="260" height="72" rx="12"/>
    <rect x="1090" y="595" width="260" height="72" rx="12"/>
    <rect x="1090" y="715" width="260" height="72" rx="12"/>
    <rect x="1090" y="850" width="260" height="72" rx="12"/>
  </g>

  <text x="1220" y="264" text-anchor="middle" class="box-title">FastAPI Gateway</text>
  <text x="1220" y="286" text-anchor="middle" class="box-subtitle">REST endpoints</text>

  <text x="1220" y="384" text-anchor="middle" class="box-title">Health / Readiness</text>
  <text x="1220" y="406" text-anchor="middle" class="box-subtitle">/health • /ready</text>

  <text x="1220" y="504" text-anchor="middle" class="box-title">Prediction Endpoint</text>
  <text x="1220" y="526" text-anchor="middle" class="box-subtitle">POST /predict</text>

  <text x="1220" y="624" text-anchor="middle" class="box-title">Inference Engine</text>
  <text x="1220" y="646" text-anchor="middle" class="box-subtitle">loads tree artifact</text>

  <text x="1220" y="744" text-anchor="middle" class="box-title">Prediction Response</text>
  <text x="1220" y="766" text-anchor="middle" class="box-subtitle">label • risk_score • version</text>

  <text x="1220" y="879" text-anchor="middle" class="box-title">Docker Runtime</text>
  <text x="1220" y="901" text-anchor="middle" class="box-subtitle">containerized service</text>

  <!-- Telemetry boxes -->
  <g fill="#101820" stroke="#c084fc" stroke-width="2">
    <rect x="1485" y="225" width="220" height="70" rx="12"/>
    <rect x="1485" y="335" width="220" height="70" rx="12"/>
    <rect x="1485" y="445" width="220" height="70" rx="12"/>
    <rect x="1485" y="555" width="220" height="70" rx="12"/>
    <rect x="1485" y="685" width="220" height="70" rx="12" stroke-dasharray="7 5"/>
    <rect x="1485" y="795" width="220" height="70" rx="12" stroke-dasharray="7 5"/>
  </g>

  <text x="1595" y="254" text-anchor="middle" class="box-title">MongoDB</text>
  <text x="1595" y="276" text-anchor="middle" class="box-subtitle">prediction telemetry</text>

  <text x="1595" y="364" text-anchor="middle" class="box-title">Telemetry Events</text>
  <text x="1595" y="386" text-anchor="middle" class="box-subtitle">request • model • score</text>

  <text x="1595" y="474" text-anchor="middle" class="box-title">MLflow SQLite</text>
  <text x="1595" y="496" text-anchor="middle" class="box-subtitle">metadata backend</text>

  <text x="1595" y="584" text-anchor="middle" class="box-title">Monitoring Reports</text>
  <text x="1595" y="606" text-anchor="middle" class="box-subtitle">quality • metrics • usage</text>

  <text x="1595" y="714" text-anchor="middle" class="box-title">Prometheus / Grafana</text>
  <text x="1595" y="736" text-anchor="middle" class="box-subtitle">planned observability</text>

  <text x="1595" y="824" text-anchor="middle" class="box-title">Alerting System</text>
  <text x="1595" y="846" text-anchor="middle" class="box-subtitle">planned Slack / PagerDuty</text>

  <!-- Arrows -->
  <g stroke-width="2.4" fill="none">
    <line x1="240" y1="290" x2="240" y2="320" stroke="#38bdf8" marker-end="url(#arrow-blue)"/>
    <line x1="240" y1="390" x2="240" y2="420" stroke="#38bdf8" marker-end="url(#arrow-blue)"/>
    <line x1="240" y1="490" x2="240" y2="520" stroke="#38bdf8" marker-end="url(#arrow-blue)"/>
    <line x1="240" y1="590" x2="240" y2="620" stroke="#38bdf8" marker-end="url(#arrow-blue)"/>
    <line x1="240" y1="690" x2="240" y2="720" stroke="#38bdf8" marker-end="url(#arrow-blue)"/>

    <line x1="735" y1="290" x2="735" y2="320" stroke="#22c55e" marker-end="url(#arrow-green)"/>
    <line x1="735" y1="390" x2="735" y2="420" stroke="#22c55e" marker-end="url(#arrow-green)"/>
    <line x1="735" y1="490" x2="735" y2="520" stroke="#22c55e" marker-end="url(#arrow-green)"/>
    <line x1="735" y1="590" x2="735" y2="620" stroke="#22c55e" marker-end="url(#arrow-green)"/>
    <line x1="735" y1="690" x2="735" y2="720" stroke="#22c55e" marker-end="url(#arrow-green)"/>
    <line x1="690" y1="790" x2="630" y2="840" stroke="#22c55e" marker-end="url(#arrow-green)"/>
    <line x1="780" y1="790" x2="840" y2="840" stroke="#22c55e" marker-end="url(#arrow-green)"/>

    <line x1="1220" y1="307" x2="1220" y2="355" stroke="#fb923c" marker-end="url(#arrow-orange)"/>
    <line x1="1220" y1="427" x2="1220" y2="475" stroke="#fb923c" marker-end="url(#arrow-orange)"/>
    <line x1="1220" y1="547" x2="1220" y2="595" stroke="#fb923c" marker-end="url(#arrow-orange)"/>
    <line x1="1220" y1="667" x2="1220" y2="715" stroke="#fb923c" marker-end="url(#arrow-orange)"/>
    <line x1="1220" y1="787" x2="1220" y2="850" stroke="#fb923c" marker-end="url(#arrow-orange)"/>

    <line x1="1595" y1="295" x2="1595" y2="335" stroke="#c084fc" marker-end="url(#arrow-purple)"/>
    <line x1="1595" y1="405" x2="1595" y2="445" stroke="#c084fc" marker-end="url(#arrow-purple)"/>
    <line x1="1595" y1="515" x2="1595" y2="555" stroke="#c084fc" marker-end="url(#arrow-purple)"/>
    <line x1="1595" y1="625" x2="1595" y2="685" stroke="#c084fc" stroke-dasharray="8 6" marker-end="url(#arrow-purple)"/>
    <line x1="1595" y1="755" x2="1595" y2="795" stroke="#c084fc" stroke-dasharray="8 6" marker-end="url(#arrow-purple)"/>

    <line x1="930" y1="877" x2="1090" y2="630" stroke="#fb923c" stroke-dasharray="8 6" marker-end="url(#arrow-orange)"/>
    <line x1="1350" y1="750" x2="1485" y2="260" stroke="#c084fc" marker-end="url(#arrow-purple)"/>
    <line x1="930" y1="877" x2="1485" y2="480" stroke="#c084fc" stroke-dasharray="8 6" marker-end="url(#arrow-purple)"/>
    <line x1="385" y1="755" x2="540" y2="755" stroke="#38bdf8" stroke-dasharray="8 6" marker-end="url(#arrow-blue)"/>
  </g>

  <!-- Legend -->
  <rect x="540" y="1030" width="720" height="48" rx="16" fill="#0b1120" stroke="#334155"/>
  <text x="575" y="1060" class="legend">Solid lines = implemented flow</text>
  <text x="790" y="1060" class="legend">Dashed lines = planned or future integration</text>
  <text x="1125" y="1060" class="legend">Architecture = project map + MLOps roadmap</text>
</svg>
'''


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(SVG, encoding="utf-8")
    print(f"Generated {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
