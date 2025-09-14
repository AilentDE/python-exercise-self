import re
import json
import sys
from typing import Generator


MD_FILE = "from.md"
JSON_FILE = "to.json"

# ["Compute", "Storage", "Networking", "Security", "Monitoring", "AI", "Other"]

CATEGORY = "Other"
SOURCE = "Udemy"


class Question:

    def split_questions(md_text: str) -> Generator[str, None, None]:
        # Split by questions that start with "- " at the beginning of a line
        # Each question includes everything until the next question starts
        questions = re.split(r"\n(?=- [^-])", md_text.strip())
        for question in questions:
            if question.strip():
                yield question.strip()

    def parse_md_to_json(md_text: str) -> str:
        # 正則表達式匹配主題和選項
        topic_match = re.search(r"- (.*?)\n", md_text)
        options = re.findall(r"  - (.*?)\n", md_text)

        # 找出備註（縮排更深的行）
        memo_match = re.search(r"    - (.*?)$", md_text)

        result = {
            "topic": topic_match.group(1) if topic_match else "",
            "category": CATEGORY,
            "option1": options[0] if len(options) > 0 else "",
            "option2": options[1] if len(options) > 1 else "",
            "option3": options[2] if len(options) > 2 else "",
            "option4": options[3] if len(options) > 3 else "",
            "option5": options[4] if len(options) > 4 else "",
            "answer": "",
            "memo": memo_match.group(1) if memo_match else "",
            "source": SOURCE,
        }

        return result


if __name__ == "__main__":
    button = input(
        f"The Questions would be save with the category: {CATEGORY} and source: {SOURCE}? (y/n): "
    )
    # y or enter
    if button.lower() == "y" or button == "":
        pass
    else:
        sys.exit(1)

    with open(MD_FILE, "r", encoding="utf-8") as file:
        md_content = file.read()

    json_results: list[str] = []
    questions = Question.split_questions(md_content)
    for question in questions:
        json_result = Question.parse_md_to_json(question)
        json_results.append(json_result)

    with open(JSON_FILE, "w", encoding="utf-8") as file:
        file.write(json.dumps(json_results, indent=2))
