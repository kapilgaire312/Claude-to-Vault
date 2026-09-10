import frontmatter


def split_main_content_and_manual_notes(contents: str, delimiter: str):
    if delimiter in contents:
        parts = contents.split(delimiter, 1)
        main_content = parts[0].strip()
        manual_notes = parts[1].strip()

    else:
        main_content = contents.strip()
        manual_notes = ""

    return main_content, manual_notes


def add_metadata_to_md(md_file: str, metadata: dict[str, str | int]):
    post = frontmatter.loads(md_file)
    post.metadata.update(metadata)
    return frontmatter.dumps(post)
