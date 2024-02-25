def active_button(button_text: str, active_text: str | None = None, is_front: bool = True) -> str:
    if not active_text:
        active_text = "✅"
    button_text = f"{active_text} {button_text}" if is_front else f"{button_text} {active_text}"
    return button_text
