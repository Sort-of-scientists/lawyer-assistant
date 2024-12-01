from presidio_analyzer import Pattern, PatternRecognizer


InnRecognizer = PatternRecognizer(
    supported_entity="INN",
    patterns=[Pattern("ИНН (10 digits)", r"\b\d{10}(\d{2})?\b", 0.9)],
    supported_language="ru"
)