import reflex as rx
from app.states.data_state import AppState
from app.components.kpi_section import kpi_section
from app.components.charts_section import charts_section
from app.components.data_table_component import (
    data_table_component,
)
from app.components.download_button import download_button


def main_content_area() -> rx.Component:
    return rx.el.main(
        rx.el.div(
            rx.el.h1(
                "Dashboard d'Analyse des Pièces Critiques",
                class_name="text-2xl font-bold text-gray-800 mb-6",
            ),
            rx.cond(
                AppState.is_loading,
                rx.el.div(
                    rx.el.div(
                        class_name="animate-spin rounded-full h-8 w-8 border-4 border-gray-300 border-t-indigo-600"
                    ),
                    rx.el.p(
                        "Chargement des données...",
                        class_name="text-gray-600 ml-2",
                    ),
                    class_name="flex items-center justify-center h-32",
                ),
                rx.el.div(
                    rx.cond(
                        AppState.data_load_error_message
                        != "",
                        rx.el.div(
                            rx.el.p(
                                "Erreur de chargement initial:",
                                class_name="font-semibold text-red-600",
                            ),
                            rx.el.p(
                                AppState.data_load_error_message,
                                class_name="text-red-500",
                            ),
                            class_name="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-4",
                            role="alert",
                        ),
                    ),
                    kpi_section(),
                    charts_section(),
                    rx.el.div(
                        download_button(),
                        class_name="my-4 flex justify-end",
                    ),
                    data_table_component(),
                ),
            ),
            class_name="p-6",
        ),
        class_name="flex-1 h-screen overflow-y-auto bg-gray-50",
    )