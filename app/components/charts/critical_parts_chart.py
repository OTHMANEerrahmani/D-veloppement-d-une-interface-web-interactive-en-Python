import reflex as rx
from app.states.data_state import AppState


def critical_parts_chart() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "Top 10 Pièces Critiques (par Score)",
            class_name="text-lg font-semibold text-gray-700 mb-2",
        ),
        rx.recharts.bar_chart(
            rx.recharts.cartesian_grid(
                stroke_dasharray="3 3", stroke_opacity=0.5
            ),
            rx.recharts.x_axis(
                data_key="name",
                angle=-30,
                text_anchor="end",
                height=70,
                stroke="#6b7280",
            ),
            rx.recharts.y_axis(stroke="#6b7280"),
            rx.recharts.tooltip(),
            rx.recharts.bar(
                data_key="Score",
                fill="#8884d8",
                radius=[4, 4, 0, 0],
            ),
            data=AppState.top_10_critical_parts_data,
            height=300,
        ),
        class_name="bg-white p-4 rounded-lg shadow",
    )