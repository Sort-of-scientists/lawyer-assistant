from typing import Optional, List, Tuple, Set
from presidio_analyzer import (
    RecognizerResult,
    EntityRecognizer,
    AnalysisExplanation,
)
from presidio_analyzer.nlp_engine import NlpArtifacts
from flair.models import SequenceTagger
from flair.data import Sentence

from common.ml.ner.custom_recognizers.recognizers_utils import CustomTokenizer


class FlairRecognizer(EntityRecognizer):
    """
    Wrapper for a flair model, if needed to be used within Presidio Analyzer.
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
        self.model = SequenceTagger.load(
            r"models/final-model.pt")

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

    def get_supported_entities(self) -> List[str]:
        """
        Return supported entities by this model.

        :return: List of the supported entities.
        """
        return self.supported_entities

    # Class to use Flair with Presidio as an external recognizer.
    def analyze(
            self, text: str, entities: List[str], nlp_artifacts: NlpArtifacts = None
    ) -> List[RecognizerResult]:
        """
        Analyze text using Text Analytics.

        :param text: The text for analysis.
        :param entities: Not working properly for this recognizer.
        :param nlp_artifacts: Not used by this recognizer.
        :param language: Text language. Supported languages in MODEL_LANGUAGES
        :return: The list of Presidio RecognizerResult constructed from the recognized
            Flair detections.
        """

        results = []
        split_symbol = "\n\n"
        texts = text.split(split_symbol)
        sentences = [Sentence(text, use_tokenizer=CustomTokenizer()) for text in texts]

        self.model.predict(sentences, verbose=True)

        # If there are no specific list of entities, we will look for all of it.
        if not entities:
            entities = self.supported_entities

        text_skip = 0
        for text, sentence in zip(texts, sentences):
            for ent in sentence.get_spans("ner"):
                textual_explanation = self.DEFAULT_EXPLANATION.format(
                    ent.labels[0].value
                )
                explanation = self.build_flair_explanation(
                    round(ent.score, 2), textual_explanation
                )
                flair_result = self._convert_to_recognizer_result(ent, explanation, text_skip)
                results.append(flair_result)
            text_skip += len(text) + len(split_symbol)
        return results

    def _convert_to_recognizer_result(self, entity, explanation, text_skip) -> RecognizerResult:

        entity_type = self.PRESIDIO_EQUIVALENCES.get(entity.tag, entity.tag)
        flair_score = round(entity.score, 2)

        flair_results = RecognizerResult(
            entity_type=entity_type,
            start=entity.start_position + text_skip,
            end=entity.end_position + text_skip,
            score=flair_score,
            analysis_explanation=explanation,
        )

        return flair_results

    def build_flair_explanation(
            self, original_score: float, explanation: str
    ) -> AnalysisExplanation:
        """
        Create explanation for why this result was detected.

        :param original_score: Score given by this recognizer
        :param explanation: Explanation string
        :return:
        """
        explanation = AnalysisExplanation(
            recognizer=self.__class__.__name__,
            original_score=original_score,
            textual_explanation=explanation,
        )
        return explanation

    @staticmethod
    def __check_label(
            entity: str, label: str, check_label_groups: Tuple[Set, Set]
    ) -> bool:
        return any(
            [entity in egrp and label in lgrp for egrp, lgrp in check_label_groups]
        )
