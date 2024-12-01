from typing import Optional, List, Tuple, Set

from flair.models import SequenceTagger
from flair.data import Sentence

from common.ml.ner.custom_recognizers.recognizers_utils import CustomTokenizer


class FlairRecognizer:
    """
    Wrapper for a flair model
    """

    ENTITIES = ["PERSON", "LOCATION", "ADDRESS", "DATA", "MONEY", "DATE"]

    DEFAULT_EXPLANATION = "Identified as {} by Flair's Named Entity Recognition"

    CHECK_LABEL_GROUPS = [
        ({"PERSON"}, {"PERSON"}),
        ({"LOCATION"}, {"LOCATION"}),
        ({"ADDRESS"}, {"ADDRESS"}),
        ({"DATA"}, {"DATA"}),
        ({"MONEY"}, {"MONEY"})
    ]

    PRESIDIO_EQUIVALENCES = {
        "DATA": "DATE_TIME",
    }

    def __init__(
            self,
            supported_language: str = "en",
            supported_entities: Optional[List[str]] = None,
            check_label_groups: Optional[Tuple[Set, Set]] = None,
    ):
        self.model = SequenceTagger.load("./models/final-model.pt")

        self.check_label_groups = (
            check_label_groups if check_label_groups else self.CHECK_LABEL_GROUPS
        )

        supported_entities = supported_entities if supported_entities else self.ENTITIES

        super().__init__(
            supported_entities=supported_entities,
            supported_language=supported_language,
            name="Flair Analytics",
        )

    def load(self) -> None:
        """Load the model, not used. Model is loaded during initialization."""
        pass

    # Class to use Flair with Presidio as an external recognizer.
    def analyze(self, text: str, entities: List[str]):
        """
        Analyze text using Text Analytics.

        :param text: The text for analysis.
        :param entities: Not working properly for this recognizer.
        :return: predictions
        """

        results = []
        split_symbol = "\n\n"
        texts = text.split(split_symbol)
        sentences = [Sentence(text, use_tokenizer=CustomTokenizer()) for text in texts]

        self.model.predict(sentences, verbose=True)

        text_skip = 0
        for text, sentence in zip(texts, sentences):
            for ent in sentence.get_spans("ner"):
                flair_result = self._convert_to_recognizer_result(ent, text_skip)
                results.append(flair_result)
            text_skip += len(text) + len(split_symbol)
        return results

    def _convert_to_recognizer_result(self, entity, text_skip):

        entity_type = self.PRESIDIO_EQUIVALENCES.get(entity.tag, entity.tag)
        flair_score = round(entity.score, 2)

        flair_results = {
            "value": entity.text,
            "label": entity_type,
            "start": entity.start_position + text_skip,
            "end": entity.end_position + text_skip,
            "score": flair_score,
        }
        return flair_results
