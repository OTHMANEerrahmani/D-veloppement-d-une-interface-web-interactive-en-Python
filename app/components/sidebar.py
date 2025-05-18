import reflex as rx
from app.states.data_state import (
    AppState,
    REQUIRED_INTERNAL_COLUMNS,
    COLUMN_MAPPING,
)


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


def file_upload_instructions() -> rx.Component:
    required_display_names = []
    for internal_name in REQUIRED_INTERNAL_COLUMNS:
        found = False
        for (
            display_name,
            mapped_name,
        ) in COLUMN_MAPPING.items():
            if mapped_name == internal_name:
                if (
                    internal_name == "pn"
                    and display_name == "PN"
                    and (
                        "Réfèrence pièce" in COLUMN_MAPPING
                    )
                    and (
                        COLUMN_MAPPING["Réfèrence pièce"]
                        == "pn"
                    )
                ):
                    if (
                        "Réfèrence pièce"
                        not in required_display_names
                    ):
                        required_display_names.append(
                            "Réfèrence pièce"
                        )
                    found = True
                elif (
                    display_name
                    not in required_display_names
                ):
                    required_display_names.append(
                        display_name
                    )
                    found = True
                    break
        if (
            not found
            and internal_name not in required_display_names
        ):
            required_display_names.append(internal_name)
    final_required_names = sorted(
        list(set(required_display_names))
    )
    return rx.el.div(
        rx.el.p(
            "Le fichier Excel doit contenir les colonnes suivantes (les noms peuvent varier légèrement) :",
            class_name="text-xs text-gray-600 mb-1",
        ),
        rx.el.ul(
            rx.foreach(
                final_required_names,
                lambda col: rx.el.li(
                    f"- {col}",
                    class_name="text-xs text-gray-600",
                ),
            ),
            class_name="list-disc list-inside ml-2 mb-2",
        ),
        rx.el.p(
            "Les colonnes optionnelles incluent: Quantité Moyenne, Nombre de visites, Fréquences (totale, NRC, AOG), %NRC, %AOG, A/C REG, Année, URGENCY.",
            class_name="text-xs text-gray-600",
        ),
        class_name="mt-2 p-2 bg-indigo-50 border border-indigo-200 rounded-md",
    )


def file_upload_component() -> rx.Component:
    """Component for uploading Excel files."""
    return rx.el.div(
        rx.el.h3(
            "Téléverser un Fichier Excel",
            class_name="text-md font-semibold text-gray-700 mb-2",
        ),
        rx.upload.root(
            rx.el.div(
                rx.icon(
                    tag="file_up",
                    class_name="w-8 h-8 mx-auto mb-2 text-gray-500 stroke-gray-500",
                ),
                rx.el.p(
                    rx.el.span(
                        "Cliquez pour téléverser",
                        class_name="font-semibold text-indigo-600",
                    ),
                    " ou glissez-déposez",
                    class_name="text-sm text-gray-600",
                ),
                rx.el.p(
                    "Fichier .xlsx uniquement",
                    class_name="text-xs text-gray-500 mt-1",
                ),
                class_name="flex flex-col items-center justify-center py-4",
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
            border="2px dashed #d1d5db",
            padding="1rem",
            border_radius="0.5rem",
            width="100%",
            class_name="cursor-pointer bg-gray-50 hover:bg-gray-100 hover:border-indigo-500 transition-colors duration-150 ease-in-out",
        ),
        rx.cond(
            AppState.selected_file_name != "",
            rx.el.div(
                rx.el.p(
                    "Fichier sélectionné: ",
                    rx.el.span(
                        AppState.selected_file_name,
                        class_name="font-medium text-indigo-700",
                    ),
                    class_name="text-xs text-gray-700 mt-2",
                )
            ),
        ),
        file_upload_instructions(),
        class_name="mb-6 p-4 border-b border-gray-200",
    )


def sidebar() -> rx.Component:
    return rx.el.aside(
        rx.el.div(
            file_upload_component(),
            rx.el.h2(
                "Filtres",
                class_name="text-xl font-semibold text-gray-800 mb-6 px-4 pt-4",
            ),
            rx.el.div(
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
                class_name="px-4",
            ),
        ),
        class_name="w-full md:w-80 bg-white shadow-lg h-screen overflow-y-auto border-r border-gray-200",
    )