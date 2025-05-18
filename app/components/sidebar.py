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


def file_upload_component() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "Téléverser un Fichier Excel",
            class_name="text-md font-semibold text-gray-700 mb-2",
        ),
        rx.upload.root(
            rx.el.div(
                rx.icon(
                    tag="cloud_upload",
                    class_name="w-8 h-8 mx-auto mb-2 text-gray-500 stroke-gray-500",
                ),
                rx.el.p(
                    rx.el.span(
                        "Cliquez pour téléverser",
                        class_name="font-semibold text-indigo-600",
                    ),
                    " ou glissez-déposez",
                    class_name="text-xs text-gray-600",
                ),
                rx.el.p(
                    "Fichier .xlsx uniquement",
                    class_name="text-xs text-gray-500",
                ),
                class_name="flex flex-col items-center justify-center py-3",
            ),
            id="excel_upload",
            accept={
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": [
                    ".xlsx"
                ]
            },
            on_drop=AppState.handle_file_upload(
                rx.upload_files(upload_id="excel_upload")
            ),
            multiple=False,
            class_name="w-full border-2 border-dashed border-gray-300 rounded-lg cursor-pointer bg-gray-50 hover:bg-gray-100 hover:border-indigo-500 transition-colors duration-150 ease-in-out",
        ),
        class_name="mb-6 p-4 border-b border-gray-200",
    )


def sidebar() -> rx.Component:
    return rx.el.aside(
        rx.el.div(
            file_upload_component(),
            rx.el.h2(
                "Filtres",
                class_name="text-xl font-semibold text-gray-800 mb-6 px-4",
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
            class_name="p-4 md:p-0",
        ),
        class_name="w-full md:w-72 bg-white shadow-lg h-screen overflow-y-auto border-r border-gray-200",
    )