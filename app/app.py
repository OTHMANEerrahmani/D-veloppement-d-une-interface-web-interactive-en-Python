import reflex as rx
from app.states.data_state import AppState
from app.components.sidebar import sidebar
from app.components.main_content_area import (
    main_content_area,
)


def index() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            sidebar(),
            main_content_area(),
            class_name="flex flex-row w-full min-h-screen",
        ),
        class_name="bg-gray-100 text-gray-800",
    )


app = rx.App(theme=rx.theme(appearance="light"))
app.add_page(index, on_load=AppState.load_data)