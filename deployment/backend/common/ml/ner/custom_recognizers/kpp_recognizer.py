from presidio_analyzer import Pattern, PatternRecognizer


KppRecognizer = PatternRecognizer(
    supported_entity="KPP",
    patterns=[Pattern("КПП", r"\b\d{9}\b", 0.9)],
    supported_language="ru"
)
