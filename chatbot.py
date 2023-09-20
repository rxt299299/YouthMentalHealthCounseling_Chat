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
class IntentExplainedClassifier:
 
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
            if '具体化' in answer or '内容与情感反应' in answer:
                if '具体化' in answer:
                    save_infos.append(self.answer_and_save(input, '(请概况一下这句话里面求助者遇到了什么问题, 控制在一句话内)', '具体化保存： '))               
                if '内容与情感反应' in answer:
                    save_infos.append(self.answer_and_save(input, '(请概况一下这句话里面反应了求助者正经历什么样的情绪,如果有涉及到产生此情绪的原因一并概括, 控制在一句话内)', '内容与情感反应保存： '))
            else:
                save_infos.append(self.answer_and_save(input, '(请记录这句话里面的重要信息, 控制在一句话内)', '信息保存： '))                 
            
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




    

