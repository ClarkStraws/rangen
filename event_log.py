from event_templates import render_event, TemplateChooser


def process_event_log(history: list, output_file: str = None) -> None:
    chooser = TemplateChooser()
    lines = []
    for event in history:
        text = render_event(event, chooser)
        if text:
            lines.append(text)

    output = "\n".join(lines)

    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"History saved to {output_file}")
