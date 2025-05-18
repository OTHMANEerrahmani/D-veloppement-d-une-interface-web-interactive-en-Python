import reflex as rx
from app.states.data_state import AppState


def kpi_card(
    title: str, value: rx.Var | str, unit: str = ""
) -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            title,
            class_name="text-sm font-medium text-gray-500",
        ),
        rx.el.p(
            value,
            rx.el.span(unit, class_name="text-lg ml-1"),
            class_name="text-2xl font-semibold text-indigo-600 mt-1",
        ),
        class_name="bg-white p-4 rounded-lg shadow",
    )


def kpi_section() -> rx.Component:
    return rx.el.div(
        kpi_card(
            "Références Suivies",
            AppState.total_references_tracked,
        ),
        kpi_card(
            "Score Criticité Moyen",
            AppState.avg_score_criticite.to_string(),
        ),
        kpi_card(
            "% Moyen AOG",
            AppState.avg_percent_aog.to_string(),
            unit="%",
        ),
        kpi_card(
            "% Moyen NRC",
            AppState.avg_percent_nrc.to_string(),
            unit="%",
        ),
        class_name="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-6",
    )