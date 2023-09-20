import openai
import tiktoken

#load system messages
def load_sys_message(sys_message_path):
    file1 = open(sys_message_path, 'r')
    Lines = file1.readlines()
    sys_content = ' '.join([item[:-1] for item in Lines])

    sys_message = [{'role':'system',
                'content':sys_content}]
    return sys_message

#load QA messages
def QA_messages(QA_path):
    file1 = open(QA_path, 'r')
    Lines = file1.readlines()
    examples = [item[:-1] for item in Lines]
    Q_contents = []
    A_contents = []
    for i in range(len(examples)):
        example = examples[i]
        if example.startswith('Q'):
            Q_contents.append(example)
        elif example.startswith('A'):
            A_contents.append(example)

    messages = []
    for i in range(len(Q_contents)):
        Q_content = Q_contents[i]
        A_content = A_contents[i]
        messages += [{'role': 'system', 'name': 'user', 'content':   Q_content},
                    {'role': 'system', 'name': 'assistant', 'content': A_content}]
    return messages

def post_process_resonpse(resonpse):
    if resonpse.startswith('A: Counselor: '):
        resonpse = resonpse[14:]
    if ' (Explanation: ' in resonpse:
        resonpse = resonpse.split(' (Explanation: ')[0]
    return resonpse


def post_process_resonpse_open_question(resonpse):
    if resonpse.startswith('A: Counselor: '):
        resonpse = resonpse[14:]
    if ' (Background investigation: ' in resonpse:
        resonpse = resonpse.split(' (Background investigation: ')[0]
    return resonpse

#模块一：开场白
class OpenStatementChat:
 
    def __init__(self, system_chat_example, temperature):
        self.messages = system_chat_example
        self.temperature = temperature

    def chat(self):
            prompt = "Could you please provide an open-ended question as an opening statement for the following psychological counseling?"
            
            messages = self.messages+[{ "role": "user", "content": prompt}]
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages = messages,
                temperature = self.temperature
            )
            
            answer = response.choices[0]['message']['content']
            
            return answer

#模块四：心理技术判断
class StrategyExplainedClassifier:
 
    def __init__(self, system_chat_example, temperature):
        self.messages = system_chat_example
        self.temperature = temperature
    
    def answer_and_save(self, input, explain_txt, save_txt):
        input_details = input+ explain_txt
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages = [{ "role": "user", "content": input_details}],
            temperature = self.temperature
        )
        answer_details = response.choices[0]['message']['content']
        return save_txt+answer_details     

    def chat(self, input):            
            messages = self.messages+[{ "role": "user", "content": input}]
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages = messages,
                temperature = self.temperature
            )
            
            answer = response.choices[0]['message']['content']
            save_infos = []
            if 'Specific techniques' in answer or 'Content and emotional response' in answer:
                if 'Specific techniques' in answer:
                    save_infos.append(self.answer_and_save(input, '(Summarize the problem the person is experiencing in this sentence and keep it to one sentence.)', 'Specific techniques and save：'))               
                if 'Content and emotional response' in answer:
                    save_infos.append(self.answer_and_save(input, '(Please summarize what kind of emotion the person is experiencing in this sentence, and if there is a reason for this emotion, summarize it, and keep it to one sentence.)', 'Content and Emotional Response and save: '))
            else:
                save_infos.append(self.answer_and_save(input, '(Record the important information in this sentence, keeping it to one sentence.)', 'Information save： '))                 
            
            return answer, save_infos


class ChatAnswer:
 
    def __init__(self, system_chat_example, temperature):
        self.messages = system_chat_example
        self.temperature = temperature

    def chat(self, input):
            prompt = input
            
            messages = self.messages+[{ "role": "user", "content": prompt}]
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages = messages,
                temperature = self.temperature
            )
            
            answer = response.choices[0]['message']['content']
            
            #print(answer)
            return answer

class ChatBot:
 
    def __init__(self, system_chat_example, temperature):
        self.messages = system_chat_example
        self.temperature = temperature

    def chat(self, input):
            prompt = input
            
            messages = self.messages+[{ "role": "user", "content": prompt}]
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages = messages,
                temperature = self.temperature
            )
            
            answer = response.choices[0]['message']['content']
            
            print(answer)
    
            tokens = self.num_tokens_from_messages(messages)
            print(f"Total tokens: {tokens}")
    
            if tokens > 4000:
                print("WARNING: Number of tokens exceeds 4000. Truncating messages.")
                messages = messages[2:]

    def num_tokens_from_messages(self, messages, model="gpt-3.5-turbo"):
        try:
            encoding = tiktoken.encoding_for_model(model)
        except KeyError:
            encoding = tiktoken.get_encoding("cl100k_base")
        if model == "gpt-3.5-turbo":  # note: future models may deviate from this
            num_tokens = 0
            for message in messages:
                num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
                for key, value in message.items():
                    num_tokens += len(encoding.encode(value))
                    if key == "name":  # if there's a name, the role is omitted
                        num_tokens += -1  # role is always required and always 1 token
            num_tokens += 2  # every reply is primed with <im_start>assistant
            return num_tokens
        else:
            raise NotImplementedError(f"""num_tokens_from_messages() is not presently implemented for model {model}.""")




    

