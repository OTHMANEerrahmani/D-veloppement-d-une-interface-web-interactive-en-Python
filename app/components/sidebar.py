import reflex as rx
from app.states.data_state import AppState


def filter_input_group(
    label: str, control: rx.Component
) -> rx.Component:
    return rx.el.div(
        rx.el.label(
            label,
            class_name="block text-sm font-medium text-gray-700 mb-1",
        ),
        control,
        class_name="mb-4",
    )


def sidebar() -> rx.Component:
    return rx.el.aside(
        rx.el.div(
            rx.el.h2(
                "Filtres",
                class_name="text-xl font-semibold text-gray-800 mb-6",
            ),
            filter_input_group(
                "PN:",
                rx.el.input(
                    placeholder="Filtrer par PN...",
                    on_change=AppState.set_filter_pn,
                    class_name="w-full p-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 text-sm",
                    default_value=AppState.filter_pn,
                ),
            ),
            filter_input_group(
                "Urgence:",
                rx.el.select(
                    rx.el.option(
                        "Toutes les urgences", value=""
                    ),
                    rx.foreach(
                        AppState.unique_urgencies,
                        lambda urgency: rx.el.option(
                            urgency, value=urgency
                        ),
                    ),
                    value=AppState.filter_urgency,
                    on_change=AppState.set_filter_urgency,
                    class_name="w-full p-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 text-sm",
                ),
            ),
            filter_input_group(
                "A/C REG:",
                rx.el.select(
                    rx.el.option(
                        "Tous les A/C REG", value=""
                    ),
                    rx.foreach(
                        AppState.unique_ac_regs,
                        lambda ac_reg: rx.el.option(
                            ac_reg, value=ac_reg
                        ),
                    ),
                    value=AppState.filter_ac_reg,
                    on_change=AppState.set_filter_ac_reg,
                    class_name="w-full p-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 text-sm",
                ),
            ),
            filter_input_group(
                "Score Criticité >",
                rx.el.input(
                    type="number",
                    placeholder="Min Score",
                    on_change=AppState.set_filter_min_score,
                    class_name="w-full p-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 text-sm",
                    default_value=AppState.filter_min_score.to_string(),
                ),
            ),
            filter_input_group(
                "Année:",
                rx.el.select(
                    rx.el.option(
                        "Toutes les années", value=""
                    ),
                    rx.foreach(
                        AppState.unique_annees,
                        lambda annee: rx.el.option(
                            annee, value=annee
                        ),
                    ),
                    value=AppState.filter_annee,
                    on_change=AppState.set_filter_annee,
                    class_name="w-full p-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 text-sm",
                ),
            ),
            class_name="p-4",
        ),
        class_name="w-full md:w-72 bg-white shadow-lg h-screen overflow-y-auto border-r border-gray-200",
    )