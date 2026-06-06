window.PORTFOLIO_PROJECTS = [
  {
    title: "AppSec Automation Platform",
    repo: "https://github.com/bhadra19/appsec-automation-platform",
    category: "Security Automation",
    rating: 5,
    status: "Runnable",
    tech: ["Python", "Flask", "SQLite"],
    keywords: ["Application Security", "SSDLC", "Security Automation", "Vulnerability Management"],
    summary: "Upload source code, run security checks, track vulnerability severity, and generate SQLite-backed reports.",
    run: "python app.py"
  },
  {
    title: "Secure SDLC Dashboard",
    repo: "https://github.com/bhadra19/secure-sdlc-dashboard",
    category: "Secure SDLC",
    rating: 5,
    status: "Runnable",
    tech: ["Python", "SQLite", "Dashboard"],
    keywords: ["Secure SDLC", "Security Metrics", "Reporting Dashboard", "Remediation Tracking"],
    summary: "Realtime SQLite-backed dashboard for vulnerability tracking, ownership, remediation status, and metrics.",
    run: "python app.py"
  },
  {
    title: "DevSecOps Pipeline",
    repo: "https://github.com/bhadra19/devsecops-pipeline",
    category: "DevSecOps",
    rating: 5,
    status: "Runnable",
    tech: ["GitHub Actions", "Python", "CI/CD"],
    keywords: ["CI/CD", "DevSecOps", "Automation", "SAST", "Secret Detection"],
    summary: "Local and GitHub Actions pipeline for SAST-style checks, dependency review, secret detection, and reports.",
    run: "python run_pipeline.py"
  },
  {
    title: "API Security Testing Framework",
    repo: "https://github.com/bhadra19/api-security-testing-framework",
    category: "API Security",
    rating: 5,
    status: "Runnable",
    tech: ["Python", "HTTP", "JWT"],
    keywords: ["API Security", "Authentication", "Authorization", "Rate Limit Testing"],
    summary: "Authorized tester for JWT behavior, broken authorization, rate-limit observation, and API fuzzing.",
    run: "python demo_api.py, then python api_tester.py"
  },
  {
    title: "Docker Security Scanner",
    repo: "https://github.com/bhadra19/docker-security-scanner",
    category: "Container Security",
    rating: 4,
    status: "Runnable",
    tech: ["Python", "Docker"],
    keywords: ["Container Security", "Docker", "Misconfiguration Checks"],
    summary: "Scanner for risky Dockerfile patterns such as root containers, latest tags, broad COPY, and sensitive ports.",
    run: "python docker_scan.py --dockerfile sample.Dockerfile"
  },
  {
    title: "Kubernetes Security Auditor",
    repo: "https://github.com/bhadra19/kubernetes-security-auditor",
    category: "Cloud Native",
    rating: 4,
    status: "Runnable",
    tech: ["Python", "Kubernetes", "YAML"],
    keywords: ["Kubernetes", "Cloud Security", "RBAC", "Pod Security"],
    summary: "Audits manifests for RBAC wildcard permissions, privileged pods, hostPath usage, and missing limits.",
    run: "python kube_audit.py --path sample_deployment.yaml"
  },
  {
    title: "Secure Coding Review Assistant",
    repo: "https://github.com/bhadra19/secure-coding-review-assistant",
    category: "Secure Coding",
    rating: 4,
    status: "Runnable",
    tech: ["Python", "SAST"],
    keywords: ["Secure Coding", "Application Security", "SQL Injection", "XSS", "Secrets"],
    summary: "Rule-based code reviewer that detects SQL injection, XSS sinks, hardcoded secrets, and recommends fixes.",
    run: "python review.py --path ."
  },
  {
    title: "Cloud Security Scanner",
    repo: "https://github.com/bhadra19/cloud-security-scanner",
    category: "Cloud Security",
    rating: 4,
    status: "Runnable",
    tech: ["Python", "AWS", "JSON"],
    keywords: ["AWS", "Cloud Security", "S3 Bucket Analysis", "IAM Review"],
    summary: "Scans local AWS-style S3 and IAM inventory JSON for public exposure and overly broad permissions.",
    run: "python cloud_scan.py --input sample_aws_inventory.json"
  },
  {
    title: "Vulnerability Management Portal",
    repo: "https://github.com/bhadra19/vulnerability-management-portal",
    category: "Vulnerability Management",
    rating: 4,
    status: "Runnable",
    tech: ["Java", "Spring Boot", "REST"],
    keywords: ["Vulnerability Management", "CVE Tracking", "Risk Prioritization", "Assignment Workflow"],
    summary: "Spring Boot REST portal for CVE tracking, assignment workflow, SLA state, and risk prioritization.",
    run: "mvn spring-boot:run"
  },
  {
    title: "AI-Powered Secure Code Analyzer",
    repo: "https://github.com/bhadra19/ai-secure-code-analyzer",
    category: "AI Security",
    rating: 5,
    status: "Runnable",
    tech: ["Python", "LLM-style", "SAST"],
    keywords: ["AI Security", "LLM", "Secure Code Analyzer", "Remediation Guidance"],
    summary: "Secure code analyzer with deterministic rules and AI-style vulnerability explanation and remediation output.",
    run: "python ai_analyzer.py --file sample_vulnerable.py"
  }
];
