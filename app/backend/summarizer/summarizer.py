from abc import ABC, abstractmethod
# from openai import OpenAI
from chatgpt_selenium_automation.handler import ChatGPTAutomation


class SummarizerStrategy(ABC):
    """
    Strategy pattern for general ease of use and creation of new summarizers
    """
    @abstractmethod
    def summarize_topic_from_name(self, text) -> str:
        pass


class ChatGPTScraperSummarizerStrategy(SummarizerStrategy):
    """
    Used Singleton here, since this library barely can keep up with 1 window as is
    """
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            chrome_driver_path = r'"C:\\Apps\\chromedriver.exe"'
            chrome_path = r'"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"'
            cls._instance.chatgpt = ChatGPTAutomation(chrome_path, chrome_driver_path)
        return cls._instance

    def summarize_topic_from_name(self, text) -> str:
        self.chatgpt.send_prompt_to_chatgpt(f"Summarize the concept of {text} and it`s applications.Be as short and concise as possible. Give me only summary without any introductions, extra replies. Be as short as you physically can")
        res = self.chatgpt.return_last_response()
        res = res.replace('ChatGPT\n', "")
        return res
    
    def end_connection(self):
        self.chatgpt.quit()


class Context:
    """
    Context for use with SummarizerStrategy pattern
    """
    def __init__(self, strategy: SummarizerStrategy) -> None:
        self._strategy = strategy

    def set_strategy(self, strategy: SummarizerStrategy) -> None:
        self._strategy = strategy

    def summarize_topic_from_name(self, text) -> str:
        return self._strategy.summarize_topic_from_name(text)


# class OpenAISummarizerStrategy(SummarizerStrategy):
#     def __init__(self) -> None:
#         self.client = OpenAI()

#     def summarize_topic_from_name(self, text) -> str:
#         completion = self.client.chat.completions.create(
#             model="gpt-3.5-turbo",
#             messages=[
#                 {"role": "system", "content": """You are a assistant, that can in few words give brief and consise summary for ML concepts. 
#                                                 You respond with a summary only and avoid any extra text."""},
#                 {"role": "user", "content": "Summarize the concept of convolutional neural networks and their applications. Be as short and concise as possible. Give me only summary without any introductions, extra replies. Be as short as you physically can"}
#             ]
#         )

#         print(completion.choices[0].message)

