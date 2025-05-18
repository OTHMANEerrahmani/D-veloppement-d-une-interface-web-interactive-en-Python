import reflex as rx
from app.states.data_state import AppState


def aog_nrc_chart() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "Répartition %AOG & %NRC par Pièce (Top 10)",
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
            rx.recharts.y_axis(
                label={
                    "value": "%",
                    "angle": -90,
                    "position": "insideLeft",
                    "fill": "#6b7280",
                },
                stroke="#6b7280",
            ),
            rx.recharts.tooltip(),
            rx.recharts.legend(),
            rx.recharts.bar(
                data_key="% AOG",
                fill="#82ca9d",
                radius=[4, 4, 0, 0],
            ),
            rx.recharts.bar(
                data_key="% NRC",
                fill="#ffc658",
                radius=[4, 4, 0, 0],
            ),
            data=AppState.aog_nrc_by_part_data,
            height=300,
        ),
        class_name="bg-white p-4 rounded-lg shadow",
    )