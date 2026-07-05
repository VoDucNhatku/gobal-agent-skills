import os
import re

skills_dir = r"D:\GOBAL AGENT & SKILL\.claude\skills"
fixed_files = []

for skill_folder in os.listdir(skills_dir):
    folder_path = os.path.join(skills_dir, skill_folder)
    if not os.path.isdir(folder_path):
        continue
    
    skill_md = os.path.join(folder_path, "SKILL.md")
    if not os.path.exists(skill_md):
        continue

    with open(skill_md, "r", encoding="utf-8") as f:
        content = f.read()

    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        continue

    frontmatter = match.group(1)
    
    # We will find every key-value pair and quote the value.
    def replacer(m):
        key = m.group(1)
        val = m.group(2).strip()
        
        # Already properly quoted?
        if val.startswith('"') and val.endswith('"') and val.count('"') - val.count('\\"') == 2:
            return f"{key}: {val}"
        if val.startswith("'") and val.endswith("'") and val.count("'") - val.count("\\'") == 2:
            return f"{key}: {val}"
            
        # Escape any existing double quotes in the string
        val_escaped = val.replace('"', '\\"')
        return f'{key}: "{val_escaped}"'

    new_frontmatter = re.sub(r"^([a-zA-Z0-9_-]+):\s+(.+)$", replacer, frontmatter, flags=re.MULTILINE)
    
    if new_frontmatter != frontmatter:
        new_content = content.replace(frontmatter, new_frontmatter, 1)
        with open(skill_md, "w", encoding="utf-8") as f:
            f.write(new_content)
        fixed_files.append(skill_folder)

print(f"Fixed {len(fixed_files)} files.")
for f in fixed_files:
    print(f" - {f}")
