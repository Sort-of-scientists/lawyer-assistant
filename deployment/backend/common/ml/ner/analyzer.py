from typing import List, Dict
import re

from common.ml.ner.custom_recognizers import FlairRecognizer


class DocEntityRecognizer:
    ENTITIES = ['LOCATION',
                'MONEY',
                'KPP',
                'DATE',
                'DATA',
                'CREDIT_CARD',
                'ADDRESS',
                'PHONE_NUMBER',
                'DATE_TIME',
                'INN',
                'PERSON']

    PATTERNS = {
        'CREDIT_CARD': r'\b(?:\d{4}[\s-]?){3}\d{4}\b',
        'INN': r'\b\d{10}\b',
        'MOBILE_PHONE_RUS': r'(?:(?:\+7|8)[\s-]?)9\d{2}[\s-]?\d{3}[\s-]?\d{2}[\s-]?\d{2}'
    }

    def __init__(self) -> None:
        """
        Initializes the DocEntityRecognizer.

        Sets up the NLP engine using the provided configuration and creates an
        instance of the AnalyzerEngine with specified recognizers for
        detecting various entities from Russian text.

        Recognizers for credit cards, phone numbers, dates, and custom
        recognizers (Flair, INN, KPP) are registered for use in the analysis.
        """

        self.neural_network = FlairRecognizer()

    def regular_expression_analyze(self, text) -> List[Dict]:
        """
        Analyzes the input text to extract named entities.

        Parameters
        ----------
        text : str
            The text to be analyzed for named entity recognition with regexp

        Returns
        -------
        List[Dict]
            A list of dictionaries, each containing details of recognized entities,
            including their extracted value, entity type, start index, and end index in the text.

        The function performs the following steps:
        1. Analyzes the text using the regexp, specifying the Russian
           language and the types of entities to extract.
        2. Processes the results to remove conflicts and organize data.
        3. Constructs a list of entity information formatted as dictionaries.
        """
        results = []
        for label, pattern in self.PATTERNS.items():
            for match in re.finditer(pattern, text):
                value = match.group(0)
                start, end = match.start(), match.end()

                results.append({
                    'value': value,
                    'label': label,
                    'score': 1.0,
                    'start': start,
                    'end': end
                })

        return results

    def predict(self, text: str) -> List[Dict]:
        """
        Analyzes the input text to extract named entities.

        Parameters
        ----------
        text : str
            The text to be analyzed for named entity recognition.

        Returns
        -------
        List[Dict]
            A list of dictionaries, each containing details of recognized entities,
            including their extracted value, entity type, start index, and end index in the text.

        The function performs the following steps:
        1. Analyzes the text using the AnalyzerEngine, specifying the Russian
           language and the types of entities to extract.
        2. Processes the results to remove conflicts and organize data.
        3. Constructs a list of entity information formatted as dictionaries.
        """
        neural_network_results = self.neural_network.analyze(text)
        regular_expression_results = self.regular_expression_analyze(text)

        return neural_network_results + regular_expression_results
