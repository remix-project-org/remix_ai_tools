from llama_cpp import StoppingCriteria


class StopOnTokens(StoppingCriteria):
    def __init__(self, tokenizer):
        super().__init__()
        self.stop_word = '}'
        self.in_code = 0
        self.incode_words = "{"
        self.old_input_ids = None
        self.tokenizer = tokenizer

    def __call__(self, input_ids, scores):

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
    
# Stop on new line token
class StopOnTokensNL(StoppingCriteria):
    def __init__(self, tokenizer):
        super().__init__()
        self.stop_word = ['\n', ';']
        self.old_input_ids = None
        self.tokenizer = tokenizer
        self.n_tokens = 0

    def __call__(self, input_ids, scores):
        self.n_tokens += 1
        if self.old_input_ids is None:
            self.old_input_ids = input_ids
            return False
        elif len(input_ids) == len(self.old_input_ids):
            return True # no generation anymore
        
        new_token_word = self.tokenizer.decode(input_ids[len(self.old_input_ids):])
        self.old_input_ids = input_ids

        for sw in self.stop_word:
            if sw in new_token_word and self.n_tokens >=3: # avoid stopping on the first character as it is a new line
                return True
        return False