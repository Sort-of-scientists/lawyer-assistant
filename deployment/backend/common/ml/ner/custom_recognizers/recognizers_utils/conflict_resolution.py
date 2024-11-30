from typing import List
from presidio_analyzer import RecognizerResult


def is_result_conflicted_with_other_elements(other_elements, result):
    return any(
        [result.has_conflict(other_element) for other_element in other_elements]
    )


def remove_conflicts_and_get_text_manipulation_data(
            analyzer_results: List[RecognizerResult],
    ) -> List[RecognizerResult]:
        """
        Iterate the list and create a sorted unique results list from it.

        Only insert results which are:
        1. Indices are not contained in other result.
        2. Have the same indices as other results but with larger score.
        :return: List
        """
        tmp_analyzer_results = []
        # This list contains all elements which we need to check a single result
        # against. If a result is dropped, it can also be dropped from this list
        # since it is intersecting with another result and we selected the other one.
        other_elements = analyzer_results.copy()
        for result in analyzer_results:
            other_elements.remove(result)

            is_merge_same_entity_type = False
            for other_element in other_elements:
                if other_element.entity_type != result.entity_type:
                    continue
                if result.intersects(other_element) == 0:
                    continue

                other_element.start = min(result.start, other_element.start)
                other_element.end = max(result.end, other_element.end)
                other_element.score = max(result.score, other_element.score)
                is_merge_same_entity_type = True
                break
            if not is_merge_same_entity_type:
                other_elements.append(result)
                tmp_analyzer_results.append(result)

        unique_text_metadata_elements = []
        # This list contains all elements which we need to check a single result
        # against. If a result is dropped, it can also be dropped from this list
        # since it is intersecting with another result and we selected the other one.
        other_elements = tmp_analyzer_results.copy()
        for result in tmp_analyzer_results:
            other_elements.remove(result)
            result_conflicted = is_result_conflicted_with_other_elements(
                other_elements, result
            )
            if not result_conflicted:
                other_elements.append(result)
                unique_text_metadata_elements.append(result)

        # This further improves the quality of handling the conflict between the
        # various entities overlapping. This will not drop the results insted
        # it adjust the start and end positions of overlapping results and removes
        # All types of conflicts among entities as well as text.
        unique_text_metadata_elements.sort(key=lambda element: element.start)
        elements_length = len(unique_text_metadata_elements)
        index = 0
        while index < elements_length - 1:
            current_entity = unique_text_metadata_elements[index]
            next_entity = unique_text_metadata_elements[index + 1]
            if current_entity.end <= next_entity.start:
                index += 1
            else:
                if current_entity.score >= next_entity.score:
                    next_entity.start = current_entity.end
                else:
                    current_entity.end = next_entity.start
                unique_text_metadata_elements.sort(
                    key=lambda element: element.start
                )
        unique_text_metadata_elements = [
            element for element in unique_text_metadata_elements
            if element.start <= element.end
            ]
        return unique_text_metadata_elements