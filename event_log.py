from event_templates import render_event


def process_event_log(history: list, output_file: str = None) -> None:
    lines = []
    for event in history:
        text = render_event(event)
        if text:
            lines.append(text)

    output = "\n".join(lines)
    print(output)

    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"\nHistory saved to {output_file}")
