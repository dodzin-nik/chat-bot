import flet as ft
import flet_material as fm
from bot import ChatBot

class Message():
    def __init__(self, user_name: str, text: str, message_type: str):
        self.user_name = user_name
        self.text = text
        self.message_type = message_type

class ChatMessage(ft.Row):
    def __init__(self, message: Message):
        super().__init__()
        self.vertical_alignment="start"
        self.controls=[
                ft.CircleAvatar(
                    content=ft.Text(self.get_initials(message.user_name)),
                    color=ft.colors.WHITE,
                    bgcolor=self.get_avatar_color(message.user_name),
                ),
                ft.Column(
                    [
                        ft.Text(message.user_name, weight="bold", color="#87703E", bgcolor="#87703E"),
                        ft.Text(message.text, selectable=True, width=500, color="#87703E"),
                    ],
                    tight=True,
                    spacing=5,
                ),
            ]

    def get_initials(self, user_name: str):
        return user_name[:1].capitalize()

    def get_avatar_color(self, user_name: str):
        colors_lookup = [
            ft.colors.CYAN,
            ft.colors.GREEN,
            ft.colors.LIME,
            ft.colors.TEAL,
        ]
        return colors_lookup[hash(user_name) % len(colors_lookup)]

def main(page: ft.Page):
    page.horizontal_alignment = "stretch"
    page.title = "Техподдержка"
    page.theme_mode = "dark"
    page.bgcolor = "#E9D9C7"
    

    chat_bot = ChatBot()


    def send_message_click(e):
        if new_message.value != "":
            page.pubsub.send_all(Message(page.session.get("user_name"), new_message.value, message_type="chat_message"))
            page.pubsub.send_all(Message(user_name="Косуля Маша", text="", message_type="login_message"))
            answer = chat_bot.Answer(str(new_message.value))
            page.pubsub.send_all(Message("Косуля Маша", str(answer).lstrip(), message_type="chat_message"))

            new_message.value = ""
            new_message.focus()
            page.update()

    def on_message(message: Message):
        if message.message_type == "chat_message":
            m = ChatMessage(message)
        elif message.message_type == "login_message":
            m = ft.Text(message.text, italic=True, color=ft.colors.BLACK45, size=12)
        chat.controls.append(m)
        page.update()

    page.pubsub.subscribe(on_message)


    chat = ft.ListView(
        expand=True,
        spacing=10,
        auto_scroll=True,
    )


    new_message = ft.TextField(
        hint_text="Введите ваш вопрос...",
        autofocus=True,
        shift_enter=True,
        min_lines=1,
        max_lines=5,
        filled=True,
        expand=True,
        border_radius=20,
        on_submit=send_message_click,
        bgcolor='#b29362'
    )

    page.add(
        ft.Container(
            ft.Row([ft.Text("           Косуля Маша", style="headlineLarge", color="#EBECE7")], alignment="start"),
            ft.IconButton(icon='/icons/char.svg'),
            width=370,
            height= 100,
            bgcolor='#B29362', 
            border_radius=40
        ),
        ft.Container(
            content=chat,
            border_radius=20,
            padding=10,
            expand=True,
        ),
        ft.Row(
            [
                new_message,
                ft.IconButton(
                    icon=ft.icons.SEND_ROUNDED,
                    tooltip="Send message",
                    on_click=send_message_click,
                    icon_color="#B29362"
                ),
            ]
        ),
    )

ft.app(port=8080, target=main, assets_dir='assets')