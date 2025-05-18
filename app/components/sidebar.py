import reflex as rx
from app.states.data_state import (
    AppState,
    REQUIRED_UPLOAD_COLUMNS_FR,
    COLUMN_MAPPING,
    COL_REF_PIECE,
    COL_PN_ALT,
    COL_DESC,
    COL_SCORE,
    COL_SEGMENT,
    COL_QTY_AVG,
    COL_VISITS,
    COL_FREQ_TOTAL,
    COL_FREQ_NRC,
    COL_FREQ_AOG,
    COL_PERCENT_NRC,
    COL_PERCENT_AOG,
    COL_AC_REG,
    COL_ANNEE,
    COL_URGENCY,
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
    """Displays instructions for the Excel file format."""
    required_display_names = (
        REQUIRED_UPLOAD_COLUMNS_FR.copy()
    )
    if COL_REF_PIECE in required_display_names:
        idx = required_display_names.index(COL_REF_PIECE)
        required_display_names[idx] = (
            f"{COL_REF_PIECE} (ou {COL_PN_ALT})"
        )
    optional_cols_display = [
        COL_QTY_AVG,
        COL_VISITS,
        COL_FREQ_TOTAL,
        COL_FREQ_NRC,
        COL_FREQ_AOG,
        COL_PERCENT_NRC,
        COL_PERCENT_AOG,
        COL_AC_REG,
        COL_ANNEE,
        COL_URGENCY,
    ]
    return rx.el.div(
        rx.el.p(
            "Le fichier Excel (.xlsx) doit contenir les colonnes suivantes :",
            class_name="text-xs text-gray-600 mb-1 font-semibold",
        ),
        rx.el.ul(
            rx.foreach(
                required_display_names,
                lambda col: rx.el.li(
                    f"- {col}",
                    class_name="text-xs text-gray-600",
                ),
            ),
            class_name="list-disc list-inside ml-2 mb-2",
        ),
        rx.el.p(
            "Les colonnes optionnelles incluent (entre autres) :",
            class_name="text-xs text-gray-600 mb-1 font-semibold",
        ),
        rx.el.ul(
            rx.foreach(
                optional_cols_display,
                lambda col: rx.el.li(
                    f"- {col}",
                    class_name="text-xs text-gray-600",
                ),
            ),
            class_name="list-disc list-inside ml-2 mb-2",
        ),
        rx.el.p(
            "Les noms de colonnes sont sensibles à la casse et aux accents. D'autres colonnes peuvent être présentes et seront conservées si elles correspondent à des champs attendus.",
            class_name="text-xs text-gray-500 italic",
        ),
        class_name="mt-2 p-3 bg-indigo-50 border border-indigo-200 rounded-md shadow-sm",
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
            on_click=lambda: AppState.set_selected_file_name(
                ""
            ),
            multiple=False,
            border="2px dashed #d1d5db",
            padding="1rem",
            border_radius="0.5rem",
            width="100%",
            class_name="cursor-pointer bg-gray-50 hover:bg-gray-100 hover:border-indigo-500 transition-colors duration-150 ease-in-out",
        ),
        rx.cond(
            AppState.is_loading,
            rx.el.div(
                rx.el.div(
                    class_name="animate-spin rounded-full h-4 w-4 border-2 border-gray-300 border-t-indigo-600 mr-2"
                ),
                rx.el.p(
                    "Traitement du fichier...",
                    class_name="text-xs text-gray-700",
                ),
                class_name="flex items-center mt-2",
            ),
            rx.cond(
                AppState.selected_file_name != "",
                rx.el.div(
                    rx.el.p(
                        "Fichier sélectionné: ",
                        rx.el.span(
                            AppState.selected_file_name,
                            class_name="font-medium text-indigo-700 break-all",
                        ),
                        class_name="text-xs text-gray-700 mt-2",
                    )
                ),
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
                        key=f"filter_urgency_{AppState.raw_data.length()}",
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
                        key=f"filter_ac_reg_{AppState.raw_data.length()}",
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
                        key=f"filter_annee_{AppState.raw_data.length()}",
                    ),
                ),
                class_name="px-4",
            ),
        ),
        class_name="w-full md:w-80 bg-white shadow-lg h-screen overflow-y-auto border-r border-gray-200",
    )