import encodings
from pathlib import Path


class SkillLoader:
    """
    load skill instruction from SKILL.md files 
    """

    def __init__(self):
        self.project_root = Path(__file__).resolve().parents[2]
        self.skills_root = self.project_root / "skills"


    def load(self, skill_name):
        """
        load a skill by folder name
        """

        skill_path = (self.skills_root / skill_name /"SKILL.md")

        if not skill_path.exists():
            raise FileNotFoundError(
                f"Skill file not found: {skill_path}"
            )

        return skill_path.read_text(encoding="utf-8")