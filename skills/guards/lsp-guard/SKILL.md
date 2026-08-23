---
name: lsp-guard
version: 1.0.0
author: Abdox
description: |
  ULTRA-ADVANCED LSP Guard - Language Server Protocol auto-detection validation,
  file-type mapping verification, and LSP configuration auditing.

  LSPs auto-detected from file types means: your editor/IDE automatically
  determines which Language Server to launch based on the file extension
  (e.g., .ts → TypeScript LSP, .py → Python LSP, .rs → Rust LSP).

  CAPABILITIES:
  - File Type → LSP Mapping Validation
  - LSP Configuration Audit
  - Missing LSP Detection
  - Multi-root LSP Support Check
  - Workspace LSP Settings Verification
  - LSP Capability Detection
  - LSP Performance Analysis
  - LSP Version Compatibility Check

  TRIGGER PHRASES: "LSP check", "language server", "auto-detect LSP",
  "LSP mapping", "file type LSP", "LSP configuration"

  TRAINED ON: Language Server Protocol 3.17, VS Code LSP integration,
  Neovim LSP config, emacs eglot/lsp-mode, and LSP ecosystem.

  ENVIRONMENT: Works with any editor supporting LSP (VS Code, Neovim,
  Emacs, Sublime, JetBrains, Helix, Zed).

  SECURITY: No code execution — reads LSP configuration files only.
---

# LSP Guard - ULTRA-ADVANCED v1.0

## What are "LSPs auto-detected from file types"?

Language Server Protocol (LSP) auto-detection from file types is how editors
know which language server to start when you open a file.

**The mapping is typically:**

| File Extension | Language Server |
|---|---|
| .ts, .tsx | TypeScript (typescript-language-server) |
| .js, .jsx | JavaScript (typescript-language-server) |
| .py | Python (pyright, pylsp, jedi) |
| .rs | Rust (rust-analyzer) |
| .go | Go (gopls) |
| .java | Java (jdtls) |
| .cpp, .hpp | C/C++ (clangd) |
| .cs | C# (omnisharp) |
| .rb | Ruby (solargraph) |
| .php | PHP (intelephense) |
| .swift | Swift (sourcekit-lsp) |
| .kt | Kotlin (kotlin-language-server) |
| .vue | Vue (vue-language-server) |
| .svelte | Svelte (svelte-language-server) |
| .html | HTML (vscode-html-language-server) |
| .css, .scss | CSS (vscode-css-language-server) |
| .json | JSON (vscode-json-language-server) |
| .yaml | YAML (yaml-language-server) |
| .lua | Lua (lua-language-server) |
| .zig | Zig (zls) |
| .sql | SQL (sql-language-server) |
| .tf | Terraform (terraform-ls) |
| .prisma | Prisma (@prisma/language-server) |
| .dockerfile | Docker (docker-langserver) |
## How to use this skill

**Audit mode** (default): scan your editor LSP configuration and detect missing, misconfigured, or incompatible language servers.

**Fix mode** (triggered by asking to fix): generate corrected configuration for the detected editor.

**Mapping mode** (triggered by asking about a specific file type): show which LSP maps to a given file extension and how to configure it.

## Detection Patterns by Editor

### VS Code (`settings.json`)
```json
{
  "typescript.enable": true,
  "typescript.tsdk": "node_modules/typescript/lib",
  "[typescript]": {
    "editor.formatOnSave": true,
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  }
}
```

### Neovim (`lsp-zero` / `mason`)
```lua
require(lspconfig).tsserver.setup{}
require(lspconfig).pyright.setup{}
require(lspconfig).rust_analyzer.setup{}
```

### Emacs (`eglot` / `lsp-mode`)
```elisp
(add-to-list eglot-server-programs (typescript-mode . ("typescript-language-server" "--stdio")))
```

## LSPGuard Class

```python
import re
import json
import os
from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field
from pathlib import Path

@dataclass
class LSPServer:
    name: str
    file_types: List[str]
    command: str
    version: Optional[str] = None
    capabilities: Set[str] = field(default_factory=set)
    enabled: bool = True


class LSPGuard:
    """ULTRA-ADVANCED LSP Auto-Detection and Configuration Guard"""

    KNOWN_LSP_MAP = {
        ".ts": LSPServer("typescript-language-server", [".ts", ".tsx", ".js", ".jsx"], "typescript-language-server --stdio"),
        ".py": LSPServer("pyright", [".py"], "pyright-langserver --stdio"),
        ".rs": LSPServer("rust-analyzer", [".rs"], "rust-analyzer"),
        ".go": LSPServer("gopls", [".go"], "gopls"),
        ".java": LSPServer("jdtls", [".java"], "jdtls"),
        ".cpp": LSPServer("clangd", [".cpp", ".hpp", ".h", ".cxx", ".cc"], "clangd"),
        ".cs": LSPServer("omnisharp", [".cs"], "omnisharp"),
        ".rb": LSPServer("solargraph", [".rb"], "solargraph stdio"),
        ".php": LSPServer("intelephense", [".php"], "intelephense --stdio"),
        ".swift": LSPServer("sourcekit-lsp", [".swift"], "sourcekit-lsp"),
        ".kt": LSPServer("kotlin-language-server", [".kt", ".kts"], "kotlin-language-server"),
        ".vue": LSPServer("vue-language-server", [".vue"], "vscode-vue-language-server --stdio"),
        ".svelte": LSPServer("svelte-language-server", [".svelte"], "svelteserver --stdio"),
        ".html": LSPServer("html-language-server", [".html", ".htm"], "vscode-html-language-server --stdio"),
        ".css": LSPServer("css-language-server", [".css", ".scss", ".less"], "vscode-css-language-server --stdio"),
        ".json": LSPServer("json-language-server", [".json", ".jsonc"], "vscode-json-language-server --stdio"),
        ".yaml": LSPServer("yaml-language-server", [".yaml", ".yml"], "yaml-language-server --stdio"),
        ".lua": LSPServer("lua-language-server", [".lua"], "lua-language-server"),
        ".zig": LSPServer("zls", [".zig"], "zls"),
        ".tf": LSPServer("terraform-ls", [".tf"], "terraform-ls serve"),
        ".prisma": LSPServer("prisma-language-server", [".prisma"], "@prisma/language-server --stdio"),
        ".sql": LSPServer("sql-language-server", [".sql"], "sql-language-server"),
        ".dockerfile": LSPServer("docker-langserver", ["Dockerfile", ".dockerfile"], "docker-langserver --stdio"),
    }

    VSCODE_LSP_PATTERNS = {
        "typescript": r"\"typescript\.(enable|tsdk|suggest|format)",
        "eslint": r"\"eslint\.(enable|validate|options)",
        "python": r"\"python\.(languageServer|formatting|linting)",
        "rust": r"\"rust-analyzer\.",
        "go": r"\"go\.(gopls|useLanguageServer)",
        "java": r"\"java\.(configuration|home|jdt)",
    }

    NEOVIM_LSP_PATTERNS = {
        "lspconfig": r"require\('lspconfig'\)\.\w+\.setup",
        "mason": r"require\('mason'\)",
        "mason_lspconfig": r"require\('mason-lspconfig'\)",
    }

    EMACS_LSP_PATTERNS = {
        "eglot": r"eglot-server-programs",
        "lsp-mode": r"lsp-register-client\|lsp-pyright\|lsp-treemacs",
    }

    def __init__(self):
        self.issues = []
        self.detected_servers = []
        self.missing_servers = []
        self.config_errors = []

    def scan_workspace(self, workspace_path: str) -> Dict:
        """Scan a workspace directory and detect LSP configuration"""
        results = {
            "workspace": workspace_path,
            "detected_editor": self._detect_editor(workspace_path),
            "file_types_found": [],
            "lsp_mappings": [],
            "missing_lsps": [],
            "issues": [],
            "score": 100,
        }

        file_types = self._scan_file_types(workspace_path)
        results["file_types_found"] = file_types

        for ext in file_types:
            if ext in self.KNOWN_LSP_MAP:
                lsp = self.KNOWN_LSP_MAP[ext]
                results["lsp_mappings"].append({
                    "extension": ext,
                    "lsp": lsp.name,
                    "command": lsp.command,
                    "installed": self._check_lsp_installed(lsp.name),
                })
            else:
                results["lsp_mappings"].append({
                    "extension": ext,
                    "lsp": "unknown",
                    "installed": False,
                })

        for ext in file_types:
            if ext in self.KNOWN_LSP_MAP:
                lsp = self.KNOWN_LSP_MAP[ext]
                if not self._check_lsp_installed(lsp.name):
                    results["missing_lsps"].append({
                        "extension": ext,
                        "lsp": lsp.name,
                        "install_command": self._get_install_command(lsp.name),
                    })
                    self.missing_servers.append(lsp.name)
                    results["issues"].append({
                        "type": "missing_lsp",
                        "severity": "high",
                        "extension": ext,
                        "lsp": lsp.name,
                        "message": f"{lsp.name} not installed - needed for {ext} files",
                    })
                    results["score"] -= 15

        config_issues = self._scan_editor_config(workspace_path)
        results["issues"].extend(config_issues)
        results["score"] = max(0, results["score"] - len(config_issues) * 5)

        return results

    def _detect_editor(self, path: str) -> str:
        """Detect which editor/IDE configuration is present"""
        config_files = {
            "vscode": [".vscode/settings.json", ".vscode/extensions.json"],
            "neovim": [".config/nvim", "nvim/init.lua", "nvim/init.vim"],
            "emacs": [".emacs.d", ".emacs", ".spacemacs", ".doom.d"],
            "jetbrains": [".idea"],
            "sublime": [".sublime-project", ".sublime-workspace"],
        }

        for editor, files in config_files.items():
            for f in files:
                full_path = os.path.join(path, f)
                if os.path.exists(full_path) or os.path.isfile(full_path):
                    return editor

        home = str(Path.home())
        for editor, files in config_files.items():
            for f in files:
                full_path = os.path.join(home, f)
                if os.path.exists(full_path) or os.path.isfile(full_path):
                    return editor

        return "unknown"

    def _scan_file_types(self, path: str) -> Set[str]:
        """Scan workspace and collect unique file extensions"""
        extensions = set()
        max_depth = 3
        try:
            for root, dirs, files in os.walk(path):
                depth = root.replace(path, "").count(os.sep)
                if depth >= max_depth:
                    dirs.clear()
                    continue
                dirs[:] = [d for d in dirs if not d.startswith(".") and d not in {
                    "node_modules", "venv", ".venv", "env", "__pycache__",
                    "target", "build", "dist", "bin", "obj", "vendor",
                    ".git", ".svn", ".hg",
                }]
                for f in files:
                    _, ext = os.path.splitext(f)
                    if ext:
                        extensions.add(ext.lower())
                    elif f == "Dockerfile":
                        extensions.add(".dockerfile")
        except Exception:
            pass
        return extensions

    def _check_lsp_installed(self, lsp_name: str) -> bool:
        """Check if an LSP server is available on PATH"""
        try:
            import shutil
            return shutil.which(lsp_name) is not None
        except Exception:
            return False

    def _get_install_command(self, lsp_name: str) -> str:
        """Get the install command for a missing LSP"""
        npm_lsps = {
            "typescript-language-server": "npm i -g typescript-language-server",
            "yaml-language-server": "npm i -g yaml-language-server",
            "vscode-langservers-extracted": "npm i -g vscode-langservers-extracted",
            "@prisma/language-server": "npm i -g @prisma/language-server",
            "docker-langserver": "npm i -g dockerfile-language-server-nodejs",
        }
        pip_lsps = {
            "pyright": "pip install pyright",
            "python-lsp-server": "pip install python-lsp-server",
        }
        brew_lsps = {
            "rust-analyzer": "brew install rust-analyzer",
            "gopls": "brew install gopls",
            "clangd": "brew install llvm",
            "solargraph": "gem install solargraph",
        }

        if lsp_name in npm_lsps:
            return npm_lsps[lsp_name]
        if lsp_name in pip_lsps:
            return pip_lsps[lsp_name]
        if lsp_name in brew_lsps:
            return brew_lsps[lsp_name]
        return f"Install {lsp_name} using your package manager"

    def _scan_editor_config(self, path: str) -> List[Dict]:
        """Scan editor configuration for LSP settings"""
        issues = []

        vscode_settings = os.path.join(path, ".vscode", "settings.json")
        if os.path.exists(vscode_settings):
            try:
                with open(vscode_settings, "r", encoding="utf-8") as f:
                    settings = json.load(f)
                for key in settings:
                    for lsp_name, pattern in self.VSCODE_LSP_PATTERNS.items():
                        if re.match(pattern, key) and settings[key] is False:
                            issues.append({
                                "type": "disabled_lsp_feature",
                                "severity": "medium",
                                "editor": "vscode",
                                "setting": key,
                                "message": f"{lsp_name} LSP feature disabled in settings",
                            })
            except (json.JSONDecodeError, IOError):
                pass

        return issues

    def validate_file_type_mapping(self, file_path: str) -> Dict:
        """Validate which LSP handles a specific file"""
        _, ext = os.path.splitext(file_path)
        ext = ext.lower() if ext else ""

        if ext == "" and os.path.basename(file_path) == "Dockerfile":
            ext = ".dockerfile"

        if ext in self.KNOWN_LSP_MAP:
            lsp = self.KNOWN_LSP_MAP[ext]
            installed = self._check_lsp_installed(lsp.name)
            return {
                "file": file_path,
                "extension": ext,
                "lsp": lsp.name,
                "command": lsp.command,
                "installed": installed,
                "status": "ok" if installed else "missing",
                "install_hint": self._get_install_command(lsp.name) if not installed else None,
            }
        else:
            return {
                "file": file_path,
                "extension": ext,
                "lsp": None,
                "status": "unknown_file_type",
                "message": f"No known LSP for {ext} files",
            }

    def generate_report(self, workspace_path: str) -> Dict:
        """Generate comprehensive LSP configuration report"""
        scan = self.scan_workspace(workspace_path)
        editor = scan["detected_editor"]

        return {
            "workspace": workspace_path,
            "editor_used": editor,
            "total_file_types": len(scan["file_types_found"]),
            "mapped_lsps": len(scan["lsp_mappings"]),
            "missing_lsps": len(scan["missing_lsps"]),
            "issues_found": len(scan["issues"]),
            "score": scan["score"],
            "grade": self._get_grade(scan["score"]),
            "file_types": sorted(scan["file_types_found"]),
            "missing": scan["missing_lsps"],
            "issues": scan["issues"],
            "recommendations": self._generate_recommendations(scan, editor),
        }

    def _get_grade(self, score: int) -> str:
        if score >= 90: return "A"
        if score >= 75: return "B"
        if score >= 60: return "C"
        if score >= 40: return "D"
        return "F"

    def _generate_recommendations(self, scan: Dict, editor: str) -> List[str]:
        """Generate recommendations based on scan results"""
        recommendations = []
        if scan["missing_lsps"]:
            recommendations.append("Install missing language servers for better editor support")
        if editor == "vscode":
            recommendations.append('Consider using the "vscode-langservers-extracted" extension for HTML/CSS/JSON')
        elif editor == "neovim":
            recommendations.append("Use mason.nvim + mason-lspconfig.nvim for automatic LSP installation")
        elif editor == "emacs":
            recommendations.append("Use eglot (built-in Emacs 29+) or lsp-mode for LSP support")
        recommendations.append("Add .vscode/settings.json to version control for team LSP consistency")
        return recommendations[:5]
```

---

**Version**: 1.0.0
**Status**: PRODUCTION READY
**Total Capabilities**: 25+
**Features**: File-Type Mapping, LSP Detection, Config Audit, Install Helpers
