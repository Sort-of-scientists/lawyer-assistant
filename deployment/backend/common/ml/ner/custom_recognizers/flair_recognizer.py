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
            self
    ):
        self.model = SequenceTagger.load("./models/final-model.pt")

    def load(self) -> None:
        """Load the model, not used. Model is loaded during initialization."""
        pass

    # Class to use Flair with Presidio as an external recognizer.
    def analyze(self, text: str):
        """
        Analyze text using Text Analytics.

        :param text: The text for analysis.
        :return: predictions
        """

        results = []
        split_symbol = "\n"
        texts = text.replace('\n', "").split(split_symbol)
        sentences = [Sentence(text, use_tokenizer=CustomTokenizer()) for text in texts]

        self.model.predict(sentences, verbose=True)

        text_skip = 0
        for text, sentence in zip(texts, sentences):
            for ent in sentence.get_spans("ner"):

                if ent.score < 0.7:  # отсекаем сомнительные сущности
                    continue

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
