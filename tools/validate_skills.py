import os
import re
import sys
from pathlib import Path

SKILLS_DIR = Path("skills")
REGISTRY_FILE = Path("registry.yaml")

REQUIRED_FRONTMATTER = {"name", "description", "version", "status"}
REQUIRED_HEADINGS = [
    "Purpose",
    "Use When",
    "Do Not Use When",
    "Inputs To Check",
    "Procedure",
    "Output Format",
    "Rules",
    "Global Skill Change Policy"
]

def check_local_content(content, filepath):
    errors = []
    lines = content.split('\n')
    for i, line in enumerate(lines, 1):
        if "/Users/" in line:
            errors.append(f"Line {i}: Found local path '/Users/'")
        if "/home/" in line:
            errors.append(f"Line {i}: Found local path '/home/'")
        if re.search(r'\bTODO\s*$', line) or re.search(r'\bTODO\s*:?\s*$', line):
            errors.append(f"Line {i}: Found TODO without explanation")
        # simple check for hardcoded private repo paths, e.g. private bitbucket or internal github
        if "git@" in line or "github.com/private" in line or "internal.repo" in line:
            errors.append(f"Line {i}: Possible hardcoded private repo path")
    return errors

def parse_frontmatter(frontmatter_str):
    data = {}
    for line in frontmatter_str.strip().split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            data[key.strip()] = value.strip()
    return data

def main():
    errors = []
    
    if not SKILLS_DIR.exists():
        print(f"Error: {SKILLS_DIR} not found")
        return 1

    if not REGISTRY_FILE.exists():
        print(f"Error: {REGISTRY_FILE} not found")
        return 1

    with open(REGISTRY_FILE, "r", encoding="utf-8") as f:
        registry_content = f.read()

    registry_names = []
    registry_paths = []
    for line in registry_content.split('\n'):
        line = line.strip()
        if line.startswith('- name:') or line.startswith('name:'):
            registry_names.append(line.split('name:', 1)[1].strip())
        elif line.startswith('path:'):
            registry_paths.append(line.split('path:', 1)[1].strip())

    for p in registry_paths:
        if not Path(p).exists():
            errors.append(f"Registry path does not exist: {p}")

    skill_folders = [f for f in SKILLS_DIR.iterdir() if f.is_dir() and not f.name.startswith('.')]

    for folder in skill_folders:
        skill_name = folder.name
        
        if skill_name not in registry_names:
            errors.append(f"Skill folder '{skill_name}' not found in registry.yaml")

        skill_md = folder / "SKILL.md"
        changelog_md = folder / "CHANGELOG.md"

        if not skill_md.exists():
            errors.append(f"Missing SKILL.md in {folder}")
            continue
            
        if not changelog_md.exists():
            errors.append(f"Missing CHANGELOG.md in {folder}")

        with open(skill_md, "r", encoding="utf-8") as f:
            content = f.read()

        if not content.startswith("---"):
            errors.append(f"{skill_md} missing YAML frontmatter")
            continue

        parts = content.split("---", 2)
        if len(parts) < 3:
            errors.append(f"{skill_md} invalid YAML frontmatter")
            continue

        frontmatter_str = parts[1]
        body = parts[2]

        frontmatter = parse_frontmatter(frontmatter_str)

        for req in REQUIRED_FRONTMATTER:
            if req not in frontmatter:
                errors.append(f"{skill_md} frontmatter missing '{req}'")

        if frontmatter.get("name") != skill_name:
            errors.append(f"{skill_md} name '{frontmatter.get('name')}' does not match folder '{skill_name}'")

        for heading in REQUIRED_HEADINGS:
            if not re.search(rf'^#+\s+{heading}\s*$', body, re.MULTILINE):
                errors.append(f"{skill_md} missing heading '{heading}'")
                
        local_errors = check_local_content(content, skill_md)
        errors.extend(local_errors)

    if errors:
        print("Validation errors found:")
        for e in errors:
            print(f"- {e}")
        return 1
    else:
        print("Validation passed. All skills are compliant.")
        return 0

if __name__ == "__main__":
    sys.exit(main())
