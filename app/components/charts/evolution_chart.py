import reflex as rx
from app.states.data_state import AppState


def evolution_chart() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "Évolution Score Moyen & Qté Totale par Année",
            class_name="text-lg font-semibold text-gray-700 mb-2",
        ),
        rx.recharts.line_chart(
            rx.recharts.cartesian_grid(
                stroke_dasharray="3 3", stroke_opacity=0.5
            ),
            rx.recharts.x_axis(
                data_key="name", stroke="#6b7280"
            ),
            rx.recharts.y_axis(
                y_axis_id="left",
                orientation="left",
                stroke="#8884d8",
                label={
                    "value": "Score Moyen",
                    "angle": -90,
                    "position": "insideLeft",
                    "fill": "#8884d8",
                },
            ),
            rx.recharts.y_axis(
                y_axis_id="right",
                orientation="right",
                stroke="#82ca9d",
                label={
                    "value": "Quantité Totale",
                    "angle": -90,
                    "position": "insideRight",
                    "fill": "#82ca9d",
                },
            ),
            rx.recharts.tooltip(),
            rx.recharts.legend(),
            rx.recharts.line(
                type="monotone",
                data_key="Score Moyen",
                stroke="#8884d8",
                y_axis_id="left",
                active_dot={"r": 8},
            ),
            rx.recharts.line(
                type="monotone",
                data_key="Quantité Totale",
                stroke="#82ca9d",
                y_axis_id="right",
                active_dot={"r": 8},
            ),
            data=AppState.evolution_data,
            height=300,
        ),
        class_name="bg-white p-4 rounded-lg shadow",
    )