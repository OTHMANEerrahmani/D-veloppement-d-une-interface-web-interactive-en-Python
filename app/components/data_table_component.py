import reflex as rx
from app.states.data_state import AppState, ItemData


def table_header() -> rx.Component:
    headers = [
        "PN",
        "Description",
        "Score Criticité",
        "% AOG",
        "% NRC",
        "Qté Moyenne",
        "Urgence",
    ]
    return rx.el.thead(
        rx.el.tr(
            rx.foreach(
                headers,
                lambda header: rx.el.th(
                    header,
                    class_name="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider bg-gray-50",
                ),
            )
        )
    )


def table_row(item: ItemData) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            item["pn"],
            class_name="px-4 py-2 whitespace-nowrap text-sm text-gray-700",
        ),
        rx.el.td(
            item["description"],
            class_name="px-4 py-2 whitespace-nowrap text-sm text-gray-700",
        ),
        rx.el.td(
            item["score_criticite"].to_string(),
            class_name="px-4 py-2 whitespace-nowrap text-sm text-gray-700",
        ),
        rx.el.td(
            f"{(item['percent_aog'] * 100).to_string()}%",
            class_name="px-4 py-2 whitespace-nowrap text-sm text-gray-700",
        ),
        rx.el.td(
            f"{(item['percent_nrc'] * 100).to_string()}%",
            class_name="px-4 py-2 whitespace-nowrap text-sm text-gray-700",
        ),
        rx.el.td(
            item["quantite_moyenne"].to_string(),
            class_name="px-4 py-2 whitespace-nowrap text-sm text-gray-700",
        ),
        rx.el.td(
            item["urgency"],
            class_name="px-4 py-2 whitespace-nowrap text-sm text-gray-700",
        ),
        class_name="hover:bg-gray-50",
    )


def data_table_component() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "Tableau des Données",
            class_name="text-lg font-semibold text-gray-700 mb-2",
        ),
        rx.el.div(
            rx.el.table(
                table_header(),
                rx.el.tbody(
                    rx.foreach(
                        AppState.filtered_data, table_row
                    )
                ),
                class_name="min-w-full divide-y divide-gray-200",
            ),
            rx.cond(
                AppState.filtered_data.length() == 0,
                rx.el.p(
                    "Aucune donnée à afficher.",
                    class_name="text-center py-4 text-gray-500",
                ),
            ),
            class_name="overflow-x-auto shadow border-b border-gray-200 sm:rounded-lg",
        ),
        class_name="bg-white p-4 rounded-lg shadow",
    )