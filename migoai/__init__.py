from .chat import ChatWithMigoAI
from .update import check_update

def start_chat():
    check_update()
    chat_app = ChatWithMigoAI()
    chat_app.run()