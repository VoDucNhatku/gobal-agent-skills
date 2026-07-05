import os
import re

skills_dir = r"D:\Gobal-AI Agent\.agents\skills"

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
    
    # We will quote the 'description' value if it's not already quoted.
    # It might contain colons which break YAML parsing.
    def replacer(m):
        val = m.group(1).strip()
        # If it's already properly quoted with double quotes, leave it alone (basic check)
        if val.startswith('"') and val.endswith('"'):
            return f"description: {val}"
        
        # Escape any existing double quotes in the string
        val_escaped = val.replace('"', '\\"')
        return f'description: "{val_escaped}"'

    new_frontmatter = re.sub(r"^description:\s+(.+)$", replacer, frontmatter, flags=re.MULTILINE)
    
    if new_frontmatter != frontmatter:
        new_content = content.replace(frontmatter, new_frontmatter, 1)
        with open(skill_md, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Fixed quotes for: {skill_folder}")

print("Done fixing descriptions!")
