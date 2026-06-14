import datetime
import json
import os
import re
import sys
import uuid
from pathlib import Path

ASSET_REGEX = re.compile(r"https://github\.com/(?:user-attachments/assets|user-images)/[a-zA-Z0-9\-/]+")
DATE_PREFIX = re.compile(r"^\d{4}-\d{2}-\d{2}-")
DECK_DIRECTIVE = re.compile(r"^\s*Deck:\s*([a-z0-9][a-z0-9-]*)\s*$", re.IGNORECASE | re.MULTILINE)
SECTION_HEADING = re.compile(r"^##(?!#)\s+(.+?)\s*#*\s*$")
QUESTION_HEADING = re.compile(r"^###(?!#)\s+(.+?)\s*#*\s*$")
FENCE = re.compile(r"^\s*(```+|~~~+)")


def slugify(value):
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug


def deck_slug_from_path(path):
    return DATE_PREFIX.sub("", path.stem)


def extract_tags(labels, control_labels):
    tags = []
    for label in labels:
        name = label.get("name", "")
        if name not in control_labels and name not in tags:
            tags.append(name)
    return tags


def issue_labels():
    return json.loads(os.environ.get("ISSUE_LABELS", "[]"))


def build_frontmatter(fields, body):
    lines = ["---"]
    for key, value in fields.items():
        if isinstance(value, list):
            lines.append(f"{key}: {json.dumps(value)}")
        else:
            lines.append(f"{key}: {json.dumps(value)}")
    lines.extend(["---", "", body.strip(), ""])
    return "\n".join(lines)


def refuse_if_slug_exists(content_dir, slug, content_type):
    for existing_file in content_dir.glob("*.md"):
        if deck_slug_from_path(existing_file) == slug:
            print(f"Refusing to overwrite existing {content_type} URL slug: {slug}")
            print(f"Existing file: {existing_file}")
            sys.exit(1)


def find_existing_deck(flashcard_dir, deck_slug):
    for existing_file in flashcard_dir.glob("*.md"):
        if deck_slug_from_path(existing_file) == deck_slug:
            return existing_file
    return None


def ingest_images(body, slug, content_type):
    found_urls = ASSET_REGEX.findall(body)
    if not found_urls:
        return body

    import requests

    img_rel_dir = f"assets/{content_type}/{slug}"
    img_abs_dir = Path("public") / img_rel_dir
    img_abs_dir.mkdir(parents=True, exist_ok=True)

    for url in found_urls:
        try:
            print(f"Downloading {url}...")
            response = requests.get(url, stream=True, timeout=10)
            if response.status_code != 200:
                continue

            content_type_header = response.headers.get("Content-Type", "")
            ext = ".png"
            if "image/jpeg" in content_type_header:
                ext = ".jpg"
            elif "image/webp" in content_type_header:
                ext = ".webp"
            elif "image/gif" in content_type_header:
                ext = ".gif"

            img_name = f"img-{uuid.uuid4().hex[:8]}{ext}"
            img_path = img_abs_dir / img_name

            with open(img_path, "wb") as image_file:
                for chunk in response.iter_content(1024):
                    image_file.write(chunk)

            body = body.replace(url, f"/{img_rel_dir}/{img_name}")
        except Exception as error:
            print(f"Failed to ingest {url}: {error}")

    return body


def split_frontmatter(text):
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n?", text, re.DOTALL)
    if not match:
        return "", text
    return match.group(1), text[match.end():]


def parse_inline_tags(raw_value):
    raw_value = raw_value.strip()
    if not raw_value:
        return []
    try:
        parsed = json.loads(raw_value)
        if isinstance(parsed, list):
            return [str(item) for item in parsed]
    except json.JSONDecodeError:
        pass

    if raw_value.startswith("[") and raw_value.endswith("]"):
        raw_value = raw_value[1:-1]

    return [
        item.strip().strip("\"'")
        for item in raw_value.split(",")
        if item.strip()
    ]


def merge_tags_into_frontmatter(frontmatter, tags):
    if not tags:
        return frontmatter

    lines = frontmatter.splitlines()
    for index, line in enumerate(lines):
        if not re.match(r"^\s*tags\s*:", line):
            continue

        existing_tags = parse_inline_tags(line.split(":", 1)[1])
        merged_tags = existing_tags[:]
        for tag in tags:
            if tag not in merged_tags:
                merged_tags.append(tag)
        lines[index] = f"tags: {json.dumps(merged_tags)}"
        return "\n".join(lines)

    lines.append(f"tags: {json.dumps(tags)}")
    return "\n".join(lines)


def normalize_heading(value):
    return re.sub(r"\s+", " ", value.strip()).lower()


def normalize_question(value):
    value = re.sub(r"[`*_~\[\]()]", "", value)
    return re.sub(r"\s+", " ", value.strip()).lower()


def update_fence(line, fenced_by):
    match = FENCE.match(line)
    if not match:
        return fenced_by

    fence_type = match.group(1)[0]
    if not fenced_by:
        return fence_type
    if fenced_by == fence_type:
        return ""
    return fenced_by


def extract_questions(markdown):
    questions = []
    fenced_by = ""
    for line in markdown.splitlines():
        inside_fence = bool(fenced_by)
        match = None if inside_fence else QUESTION_HEADING.match(line)
        if match:
            questions.append(match.group(1).strip())
        fenced_by = update_fence(line, fenced_by)
    return questions


def validate_flashcards(markdown, existing_markdown=None):
    incoming_questions = extract_questions(markdown)
    if not incoming_questions:
        print("Flashcard issues must include at least one level-3 question heading, e.g. ### What is softmax?")
        sys.exit(1)

    seen = set()
    for question in incoming_questions:
        normalized = normalize_question(question)
        if normalized in seen:
            print(f"Duplicate question in incoming flashcards: {question}")
            sys.exit(1)
        seen.add(normalized)

    if existing_markdown is None:
        return

    existing_questions = {normalize_question(question) for question in extract_questions(existing_markdown)}
    for question in incoming_questions:
        if normalize_question(question) in existing_questions:
            print(f"Refusing to append duplicate question to existing deck: {question}")
            sys.exit(1)


def trim_blank_lines(lines):
    trimmed = lines[:]
    while trimmed and not trimmed[0].strip():
        trimmed.pop(0)
    while trimmed and not trimmed[-1].strip():
        trimmed.pop()
    return trimmed


def split_sections(markdown):
    lines = trim_blank_lines(markdown.splitlines())
    prefix = []
    sections = []
    current_section = None
    fenced_by = ""

    for line in lines:
        inside_fence = bool(fenced_by)
        section_match = None if inside_fence else SECTION_HEADING.match(line)
        if section_match:
            if current_section:
                sections.append(current_section)
            current_section = {
                "title": section_match.group(1).strip(),
                "lines": [],
            }
            continue

        if current_section is None:
            prefix.append(line)
        else:
            current_section["lines"].append(line)

        fenced_by = update_fence(line, fenced_by)

    if current_section:
        sections.append(current_section)

    if not sections and any(line.strip() for line in lines):
        return [], [{"title": "Cards", "lines": lines}]

    return prefix, sections


def append_flashcard_sections(existing_body, incoming_body):
    prefix, existing_sections = split_sections(existing_body)
    _, incoming_sections = split_sections(incoming_body)
    section_lookup = {
        normalize_heading(section["title"]): section
        for section in existing_sections
    }

    for incoming_section in incoming_sections:
        incoming_lines = trim_blank_lines(incoming_section["lines"])
        if not incoming_lines:
            continue

        key = normalize_heading(incoming_section["title"])
        existing_section = section_lookup.get(key)
        if existing_section:
            existing_section["lines"] = trim_blank_lines(existing_section["lines"])
            if existing_section["lines"]:
                existing_section["lines"].append("")
            existing_section["lines"].extend(incoming_lines)
        else:
            existing_sections.append({
                "title": incoming_section["title"],
                "lines": incoming_lines,
            })

    parts = []
    prefix = trim_blank_lines(prefix)
    if prefix:
        parts.append("\n".join(prefix))

    for section in existing_sections:
        section_lines = trim_blank_lines(section["lines"])
        section_text = f"## {section['title']}"
        if section_lines:
            section_text += "\n\n" + "\n".join(section_lines)
        parts.append(section_text)

    return "\n\n".join(part.strip() for part in parts if part.strip()) + "\n"


def extract_deck_directive(body):
    match = DECK_DIRECTIVE.search(body)
    if not match:
        return None, body.strip()

    deck_slug = match.group(1).lower()
    body_without_directive = (body[:match.start()] + body[match.end():]).strip()
    return deck_slug, body_without_directive


def create_blog_post(title, body, tags, date_str, issue_number):
    slug = slugify(title) or f"issue-{issue_number}"
    post_dir = Path("src/content/blog")
    post_dir.mkdir(parents=True, exist_ok=True)
    refuse_if_slug_exists(post_dir, slug, "post")

    body = ingest_images(body, slug, "blog")
    filename = post_dir / f"{date_str}-{slug}.md"
    if filename.exists():
        print(f"Refusing to overwrite existing post file: {filename}")
        sys.exit(1)

    filename.write_text(
        build_frontmatter({
            "title": title,
            "date": date_str,
            "description": "",
            "tags": tags,
            "categories": tags,
        }, body),
        encoding="utf-8",
    )
    return filename


def publish_flashcards(title, body, tags, date_str, issue_number):
    flashcard_dir = Path("src/content/flashcards")
    flashcard_dir.mkdir(parents=True, exist_ok=True)
    target_deck_slug, body = extract_deck_directive(body)

    if target_deck_slug:
        existing_deck = find_existing_deck(flashcard_dir, target_deck_slug)
        if not existing_deck:
            print(f"Refusing to append to missing flashcard deck: {target_deck_slug}")
            sys.exit(1)

        existing_text = existing_deck.read_text(encoding="utf-8")
        frontmatter, existing_body = split_frontmatter(existing_text)
        if not frontmatter:
            print(f"Existing flashcard deck is missing frontmatter: {existing_deck}")
            sys.exit(1)

        validate_flashcards(body, existing_body)
        body = ingest_images(body, target_deck_slug, "flashcards")
        updated_body = append_flashcard_sections(existing_body, body)
        updated_frontmatter = merge_tags_into_frontmatter(frontmatter, tags)
        existing_deck.write_text(
            f"---\n{updated_frontmatter.strip()}\n---\n\n{updated_body}",
            encoding="utf-8",
        )
        return existing_deck

    slug = slugify(title) or f"issue-{issue_number}"
    refuse_if_slug_exists(flashcard_dir, slug, "flashcard deck")
    validate_flashcards(body)
    body = ingest_images(body, slug, "flashcards")

    filename = flashcard_dir / f"{date_str}-{slug}.md"
    if filename.exists():
        print(f"Refusing to overwrite existing flashcard file: {filename}")
        sys.exit(1)

    filename.write_text(
        build_frontmatter({
            "title": title,
            "date": date_str,
            "description": "",
            "tags": tags,
        }, body),
        encoding="utf-8",
    )
    return filename


def write_github_output(filename):
    output_path = os.environ.get("GITHUB_OUTPUT")
    if not output_path:
        return

    with open(output_path, "a", encoding="utf-8") as github_output:
        github_output.write(f"filename={filename}\n")


def main():
    title = os.environ.get("ISSUE_TITLE", "Untitled")
    body = os.environ.get("ISSUE_BODY", "")
    labels = issue_labels()
    issue_number = os.environ.get("ISSUE_NUMBER", "unknown")
    label_names = {label.get("name", "") for label in labels}
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")

    if "flashcards" in label_names:
        tags = extract_tags(labels, {"publish", "flashcards"})
        filename = publish_flashcards(title, body, tags, date_str, issue_number)
    else:
        tags = extract_tags(labels, {"publish"})
        filename = create_blog_post(title, body, tags, date_str, issue_number)

    write_github_output(filename)


if __name__ == "__main__":
    main()
