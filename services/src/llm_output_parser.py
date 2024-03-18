import torch
from llama_cpp import StoppingCriteria


class StopOnTokens(StoppingCriteria):
    def __init__(self, tokenizer):
        super().__init__()
        self.stop_word = '}'
        self.in_code = 0
        self.incode_words = "{"
        self.old_input_ids = None
        self.tokenizer = tokenizer

    def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor):

        if self.old_input_ids is None:
            self.old_input_ids = input_ids
            return False
        elif len(input_ids) == len(self.old_input_ids):
            return True # no generation anymore
        
        new_token_word = self.tokenizer.decode(input_ids[len(self.old_input_ids):])
        self.old_input_ids = input_ids

        if self.incode_words in new_token_word:
            self.in_code += 1

        if self.stop_word in new_token_word:
            self.in_code -= 1
            return True if self.in_code == 0 else False
        return False
  


def remove_after_last_occurrence(source, char):
    last_occurrence_index = source.rfind(char)

    if last_occurrence_index != -1:
        result = source[:last_occurrence_index+2]
        return result
    else:
        return source

def get_string_between(source, start_str, end_str):
    start_index = source.find(start_str)
    if start_index == -1:
        return None

    start_index += len(start_str)
    end_index = source.find(end_str, start_index)

    if end_index == -1:
        return source[start_index:len(source)]

    return source[start_index:end_index]