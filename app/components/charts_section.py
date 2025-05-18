import reflex as rx
from app.components.charts.critical_parts_chart import (
    critical_parts_chart,
)
from app.components.charts.aog_nrc_chart import (
    aog_nrc_chart,
)
from app.components.charts.urgency_pie_chart import (
    urgency_pie_chart,
)
from app.components.charts.evolution_chart import (
    evolution_chart,
)
from app.states.data_state import AppState


def charts_section() -> rx.Component:
    return rx.el.div(
        rx.cond(
            AppState.filtered_data.length() > 0,
            rx.el.div(
                rx.el.div(
                    critical_parts_chart(),
                    class_name="w-full lg:w-1/2",
                ),
                rx.el.div(
                    aog_nrc_chart(),
                    class_name="w-full lg:w-1/2",
                ),
                rx.el.div(
                    urgency_pie_chart(),
                    class_name="w-full lg:w-1/2",
                ),
                rx.el.div(
                    evolution_chart(),
                    class_name="w-full lg:w-1/2",
                ),
                class_name="flex flex-wrap gap-4 mb-6",
            ),
            rx.el.div(
                rx.el.p(
                    "Aucune donnée à afficher pour les graphiques.",
                    class_name="text-gray-500 text-center p-4",
                ),
                class_name="bg-white p-4 rounded-lg shadow w-full",
            ),
        )
    )