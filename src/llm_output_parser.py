import torch
from transformers import StoppingCriteriaList, StoppingCriteria


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
        return None

    return source[start_index:end_index]

def is_tensor_at_end(main_tensor, sub_tensor):
    # Convert scalar tensor to tensor
    if torch.is_tensor(sub_tensor):
        sub_tensor = sub_tensor.view(-1)
    else:
        sub_tensor = torch.tensor([sub_tensor])
    # Check if sub_tensor is at the end of main_tensor
    if sub_tensor.size() > main_tensor.size():
        return False
    else:
        return torch.all(main_tensor[-len(sub_tensor):] == sub_tensor)

class StoppingCriteriaSub(StoppingCriteria):
    def __init__(self, tokenizer, device, stops=[], encounters=1, completion=False):
        super().__init__()
        self.stops = ["}"] if completion else "```" # stops if completion else [torch.Tensor([28956]).to(device)]
        self.in_code = 0
        self.tokenizer = tokenizer
        self.in_code_token = "{" if completion else "```"
        self.old_input_ids = torch.Tensor()
        self.completion = completion

    def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor):
        #print('#'*100)
        #print('new inputs: ', input_ids)
        if self.old_input_ids.size()[0] == 0:
            self.old_input_ids = input_ids[0]
            return False
        else: 

            tokens = input_ids[0][self.old_input_ids.size(0): input_ids[0].size(0)]
            new_tokens = self.tokenizer.decode(tokens)
            self.old_input_ids = input_ids[0]

        if  self.in_code_token in new_tokens and not self.completion and not self.in_code:
            # print(self.in_code_token, "is in ", new_tokens)
            self.in_code += 1
            # print('Info: got in code', self.in_code)
            return False
        
        elif self.in_code_token in new_tokens and self.completion:
            self.in_code += 1


        # print()
        # print('stops', self.stops)
        # print('new token ', new_tokens)
        # print('IN code value', self.in_code)
        
        for stop in self.stops:
            if stop in new_tokens:

                if self.in_code:
                    # print('last token is stop', new_tokens)
                    # print('Info: in code value', self.in_code)
                    self.in_code -= 1
                #     if self.completion :
                #         print('INFO: Stopped generation')
                #         self.in_code = 0
                #         return True
                    
                return True if self.in_code==0 else False
        return False

def stopping_criteria(tokenizer, device, completion):
    stop_words = ["}", "```"] # Redundant if not completion
    stop_words_ids = [tokenizer(stop_word, return_tensors='pt')['input_ids'].squeeze() for stop_word in stop_words]
    stopping_criteria = StoppingCriteriaList([StoppingCriteriaSub(tokenizer, device, stops=stop_words_ids, completion=completion)])
    return stopping_criteria
