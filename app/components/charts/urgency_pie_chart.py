import reflex as rx
from app.states.data_state import AppState

PIE_COLORS = [
    "#0088FE",
    "#00C49F",
    "#FFBB28",
    "#FF8042",
    "#AF19FF",
    "#FF4560",
]


def urgency_pie_chart() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "Répartition des Niveaux d'Urgence",
            class_name="text-lg font-semibold text-gray-700 mb-2",
        ),
        rx.recharts.pie_chart(
            rx.recharts.pie(
                rx.foreach(
                    AppState.urgency_distribution_data,
                    lambda item, index: rx.recharts.cell(
                        fill=rx.Var.create(PIE_COLORS).at(
                            index % len(PIE_COLORS)
                        )
                    ),
                ),
                data_key="value",
                name_key="name",
                data=AppState.urgency_distribution_data,
                cx="50%",
                cy="50%",
                outer_radius=80,
                label=True,
            ),
            rx.recharts.tooltip(),
            rx.recharts.legend(),
            height=300,
        ),
        class_name="bg-white p-4 rounded-lg shadow flex flex-col items-center",
    )