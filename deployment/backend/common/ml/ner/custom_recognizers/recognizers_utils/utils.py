from flair.tokenization import Tokenizer
from segtok.tokenizer import symbol_tokenizer


class CustomTokenizer(Tokenizer):
    def __init__(self):
        pass

    def tokenize(self, text: str) -> list[str]:
        tokens = symbol_tokenizer(text)
        final_tokens = []
        for token in tokens:
            if token == ".,":
                final_tokens.extend([".", ","])
            else:
                final_tokens.append(token)
        return final_tokens

    def name(self) -> str:
        return self.__class__.__name__
