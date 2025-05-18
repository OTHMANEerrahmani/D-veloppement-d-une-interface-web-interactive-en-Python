import reflex as rx
from app.states.data_state import AppState


def download_button() -> rx.Component:
    return rx.el.button(
        "Télécharger les Données Filtrées (CSV)",
        on_click=AppState.download_filtered_data,
        class_name="px-4 py-2 bg-green-600 text-white font-semibold rounded-lg shadow hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-opacity-50 transition ease-in-out duration-150 disabled:opacity-50",
        disabled=AppState.filtered_data.length() == 0,
    )