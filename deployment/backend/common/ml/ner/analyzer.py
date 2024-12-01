from typing import List, Dict

from presidio_analyzer import AnalyzerEngine, RecognizerRegistry
from presidio_analyzer.predefined_recognizers import CreditCardRecognizer, PhoneRecognizer, DateRecognizer
from presidio_analyzer.nlp_engine import NlpEngineProvider

from common.ml.ner.custom_recognizers import FlairRecognizer, InnRecognizer, KppRecognizer
from common.ml.ner.custom_recognizers.recognizers_utils import remove_conflicts_and_get_text_manipulation_data


class DocEntityRecognizer:
    CONFIGURATION = {
        "nlp_engine_name": "spacy",
        "models": [{"lang_code": "ru", "model_name": "ru_core_news_sm"}],
    }

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

    def __init__(self) -> None:
        """
        Initializes the DocEntityRecognizer.

        Sets up the NLP engine using the provided configuration and creates an
        instance of the AnalyzerEngine with specified recognizers for
        detecting various entities from Russian text.

        Recognizers for credit cards, phone numbers, dates, and custom
        recognizers (Flair, INN, KPP) are registered for use in the analysis.
        """
        provider = NlpEngineProvider(nlp_configuration=self.CONFIGURATION)
        nlp_engine = provider.create_engine()

        registry = RecognizerRegistry()
        registry.add_recognizer(CreditCardRecognizer(supported_language='ru'))
        registry.add_recognizer(PhoneRecognizer(supported_language='ru'))
        registry.add_recognizer(DateRecognizer(supported_language='ru'))
        registry.add_recognizer(FlairRecognizer(supported_language='ru'))
        registry.add_recognizer(InnRecognizer)
        registry.add_recognizer(KppRecognizer)

        self.analyzer = AnalyzerEngine(registry=registry, nlp_engine=nlp_engine)

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
        result = self.analyzer.analyze(text, language='ru', entities=self.ENTITIES)
        result = remove_conflicts_and_get_text_manipulation_data(result)

        entity_list = []
        for entity in result:
            entity_text = text[entity.start: entity.end]
            entity_list.append({"value": entity_text,
                                "score": entity.score,
                                "label": entity.entity_type,
                                "start": entity.start,
                                "end": entity.end})

        return entity_list
