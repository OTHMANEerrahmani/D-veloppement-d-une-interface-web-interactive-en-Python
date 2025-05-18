import reflex as rx
import pandas as pd
from pathlib import Path
from typing import TypedDict, List, Optional, Dict, Union

COL_PN = "PN"
COL_DESC = "Description"
COL_QTY_AVG = "Quantité Moyenne"
COL_VISITS = "Nombre de visites"
COL_FREQ_TOTAL = "Fréquence totale"
COL_FREQ_NRC = "Fréquence NRC"
COL_FREQ_AOG = "Fréquence AOG"
COL_PERCENT_NRC = "% NRC"
COL_PERCENT_AOG = "% AOG"
COL_SCORE = "Score criticité"
COL_AC_REG = "A/C REG"
COL_ANNEE = "Année"
COL_URGENCY = "URGENCY"


class ItemData(TypedDict):
    pn: str
    description: str
    quantite_moyenne: float
    nombre_visites: int
    frequence_totale: int
    frequence_nrc: int
    frequence_aog: int
    percent_nrc: float
    percent_aog: float
    score_criticite: float
    ac_reg: str
    annee: Optional[int]
    urgency: str


def create_sample_data() -> list[ItemData]:
    sample_list: list[ItemData] = [
        {
            "pn": "PN001",
            "description": "Part A",
            "quantite_moyenne": 10.5,
            "nombre_visites": 5,
            "frequence_totale": 20,
            "frequence_nrc": 2,
            "frequence_aog": 1,
            "percent_nrc": 0.1,
            "percent_aog": 0.05,
            "score_criticite": 85.0,
            "ac_reg": "F-GABC",
            "annee": 2023,
            "urgency": "Critical",
        },
        {
            "pn": "PN002",
            "description": "Part B",
            "quantite_moyenne": 5.0,
            "nombre_visites": 10,
            "frequence_totale": 30,
            "frequence_nrc": 5,
            "frequence_aog": 3,
            "percent_nrc": 0.16,
            "percent_aog": 0.1,
            "score_criticite": 95.0,
            "ac_reg": "F-GDEF",
            "annee": 2023,
            "urgency": "AOG",
        },
        {
            "pn": "PN003",
            "description": "Part C",
            "quantite_moyenne": 20.0,
            "nombre_visites": 2,
            "frequence_totale": 10,
            "frequence_nrc": 1,
            "frequence_aog": 0,
            "percent_nrc": 0.1,
            "percent_aog": 0.0,
            "score_criticite": 70.0,
            "ac_reg": "F-GABC",
            "annee": 2024,
            "urgency": "Routine",
        },
        {
            "pn": "PN004",
            "description": "Part D",
            "quantite_moyenne": 8.2,
            "nombre_visites": 8,
            "frequence_totale": 15,
            "frequence_nrc": 3,
            "frequence_aog": 2,
            "percent_nrc": 0.2,
            "percent_aog": 0.13,
            "score_criticite": 90.0,
            "ac_reg": "F-GHIJ",
            "annee": 2024,
            "urgency": "Critical",
        },
        {
            "pn": "PN001",
            "description": "Part A",
            "quantite_moyenne": 12.0,
            "nombre_visites": 6,
            "frequence_totale": 22,
            "frequence_nrc": 3,
            "frequence_aog": 1,
            "percent_nrc": 0.13,
            "percent_aog": 0.04,
            "score_criticite": 88.0,
            "ac_reg": "F-GABC",
            "annee": 2024,
            "urgency": "Critical",
        },
    ]
    for i in range(5, 15):
        freq_total_val = i * 3
        freq_nrc_val = i // 3
        freq_aog_val = i // 5
        sample_list.append(
            {
                "pn": f"PN{i:03d}",
                "description": f"Part {chr(65 + i - 1)}",
                "quantite_moyenne": round(10 + i * 1.5, 1),
                "nombre_visites": i % 5 + 1,
                "frequence_totale": freq_total_val,
                "frequence_nrc": freq_nrc_val,
                "frequence_aog": freq_aog_val,
                "percent_nrc": round(
                    (
                        freq_nrc_val / freq_total_val
                        if freq_total_val > 0
                        else 0
                    ),
                    2,
                ),
                "percent_aog": round(
                    (
                        freq_aog_val / freq_total_val
                        if freq_total_val > 0
                        else 0
                    ),
                    2,
                ),
                "score_criticite": 60 + i * 2.5,
                "ac_reg": ["F-GKLM", "F-GNOP", "F-GXYZ"][
                    i % 3
                ],
                "annee": [2022, 2023, 2024][i % 3],
                "urgency": ["Routine", "Critical", "AOG"][
                    i % 3
                ],
            }
        )
    return sample_list


class AppState(rx.State):
    raw_data: list[ItemData] = []
    data_load_error_message: str = ""
    is_loading: bool = False
    filter_pn: str = ""
    filter_urgency: str = ""
    filter_ac_reg: str = ""
    filter_min_score: float = 0.0
    filter_annee: str = ""

    @rx.event
    def load_data(self):
        self.is_loading = True
        self.raw_data = []
        self.data_load_error_message = ""
        excel_file_path = Path(
            "assets/Tableau_Final_Items_Critiques.xlsx"
        )
        try:
            if not excel_file_path.exists():
                self.data_load_error_message = f"Erreur: Le fichier {excel_file_path.name} est introuvable. Chargement des données exemples."
                self.raw_data = create_sample_data()
                self.is_loading = False
                return
            df = pd.read_excel(excel_file_path)
            column_mapping = {
                COL_PN: "pn",
                COL_DESC: "description",
                COL_QTY_AVG: "quantite_moyenne",
                COL_VISITS: "nombre_visites",
                COL_FREQ_TOTAL: "frequence_totale",
                COL_FREQ_NRC: "frequence_nrc",
                COL_FREQ_AOG: "frequence_aog",
                COL_PERCENT_NRC: "percent_nrc",
                COL_PERCENT_AOG: "percent_aog",
                COL_SCORE: "score_criticite",
                COL_AC_REG: "ac_reg",
                COL_ANNEE: "annee",
                COL_URGENCY: "urgency",
            }
            actual_columns = df.columns.tolist()
            renamed_cols = {}
            missing_excel_cols = []
            for (
                excel_col,
                internal_col,
            ) in column_mapping.items():
                if excel_col in actual_columns:
                    renamed_cols[excel_col] = internal_col
                else:
                    missing_excel_cols.append(excel_col)
            if missing_excel_cols:
                self.data_load_error_message = f"Colonnes manquantes: {', '.join(missing_excel_cols)}. Chargement données exemples."
                self.raw_data = create_sample_data()
                self.is_loading = False
                return
            df = df.rename(columns=renamed_cols)
            numeric_cols_float = [
                "quantite_moyenne",
                "percent_nrc",
                "percent_aog",
                "score_criticite",
            ]
            numeric_cols_int = [
                "nombre_visites",
                "frequence_totale",
                "frequence_nrc",
                "frequence_aog",
            ]
            for col in numeric_cols_float:
                if col in df.columns:
                    df[col] = pd.to_numeric(
                        df[col], errors="coerce"
                    ).fillna(0.0)
                else:
                    df[col] = 0.0
            for col in numeric_cols_int:
                if col in df.columns:
                    df[col] = (
                        pd.to_numeric(
                            df[col], errors="coerce"
                        )
                        .fillna(0)
                        .astype(int)
                    )
                else:
                    df[col] = 0
            if "annee" in df.columns:
                df["annee"] = df["annee"].apply(
                    lambda x: (
                        int(x)
                        if pd.notnull(x)
                        and str(x)
                        .replace(".0", "")
                        .isdigit()
                        else None
                    )
                )
            else:
                df["annee"] = None
            string_cols = [
                "pn",
                "description",
                "ac_reg",
                "urgency",
            ]
            for col in string_cols:
                if col in df.columns:
                    df[col] = df[col].astype(str).fillna("")
                else:
                    df[col] = ""
            for (
                key_info
            ) in ItemData.__annotations__.items():
                key_name = key_info[0]
                if key_name not in df.columns:
                    if key_info[1] == str:
                        df[key_name] = ""
                    elif key_info[1] == float:
                        df[key_name] = 0.0
                    elif key_info[1] == int:
                        df[key_name] = 0
                    elif key_info[1] == Optional[int]:
                        df[key_name] = None
                    else:
                        df[key_name] = None
            self.raw_data = df.to_dict(orient="records")
        except Exception as e:
            self.data_load_error_message = f"Erreur: {str(e)}. Chargement des données exemples."
            self.raw_data = create_sample_data()
        self.is_loading = False

    def set_filter_pn(self, value: str):
        self.filter_pn = value

    def set_filter_urgency(self, value: str):
        self.filter_urgency = value

    def set_filter_ac_reg(self, value: str):
        self.filter_ac_reg = value

    def set_filter_min_score(self, value: str):
        try:
            self.filter_min_score = (
                float(value) if value else 0.0
            )
        except ValueError:
            self.filter_min_score = 0.0

    def set_filter_annee(self, value: str):
        self.filter_annee = value

    @rx.var
    def unique_pns(self) -> list[str]:
        if not self.raw_data:
            return []
        return sorted(
            list(
                set(
                    (
                        str(item["pn"])
                        for item in self.raw_data
                        if item["pn"]
                    )
                )
            )
        )

    @rx.var
    def unique_urgencies(self) -> list[str]:
        if not self.raw_data:
            return []
        return sorted(
            list(
                set(
                    (
                        str(item["urgency"])
                        for item in self.raw_data
                        if item["urgency"]
                    )
                )
            )
        )

    @rx.var
    def unique_ac_regs(self) -> list[str]:
        if not self.raw_data:
            return []
        return sorted(
            list(
                set(
                    (
                        str(item["ac_reg"])
                        for item in self.raw_data
                        if item["ac_reg"]
                    )
                )
            )
        )

    @rx.var
    def unique_annees(self) -> list[str]:
        if not self.raw_data:
            return []
        return sorted(
            list(
                set(
                    (
                        str(int(item["annee"]))
                        for item in self.raw_data
                        if item["annee"] is not None
                        and str(item["annee"]).isdigit()
                    )
                )
            )
        )

    @rx.var
    def filtered_data(self) -> list[ItemData]:
        data = self.raw_data
        if not data:
            return []
        if self.filter_pn:
            data = [
                item
                for item in data
                if self.filter_pn.lower()
                in str(item["pn"]).lower()
            ]
        if self.filter_urgency:
            data = [
                item
                for item in data
                if str(item["urgency"])
                == self.filter_urgency
            ]
        if self.filter_ac_reg:
            data = [
                item
                for item in data
                if str(item["ac_reg"]) == self.filter_ac_reg
            ]
        if self.filter_min_score > 0:
            data = [
                item
                for item in data
                if item["score_criticite"]
                >= self.filter_min_score
            ]
        if self.filter_annee:
            try:
                year_int = int(self.filter_annee)
                data = [
                    item
                    for item in data
                    if item["annee"] is not None
                    and item["annee"] == year_int
                ]
            except ValueError:
                pass
        return data

    @rx.var
    def total_references_tracked(self) -> int:
        return len(self.unique_pns)

    @rx.var
    def avg_score_criticite(self) -> float:
        if not self.filtered_data:
            return 0.0
        scores = [
            item["score_criticite"]
            for item in self.filtered_data
            if isinstance(
                item.get("score_criticite"), (int, float)
            )
        ]
        return (
            round(sum(scores) / len(scores), 2)
            if scores
            else 0.0
        )

    @rx.var
    def avg_percent_aog(self) -> float:
        if not self.filtered_data:
            return 0.0
        aog_percents = [
            item["percent_aog"]
            for item in self.filtered_data
            if isinstance(
                item.get("percent_aog"), (int, float)
            )
        ]
        return (
            round(
                sum(aog_percents) / len(aog_percents) * 100,
                2,
            )
            if aog_percents
            else 0.0
        )

    @rx.var
    def avg_percent_nrc(self) -> float:
        if not self.filtered_data:
            return 0.0
        nrc_percents = [
            item["percent_nrc"]
            for item in self.filtered_data
            if isinstance(
                item.get("percent_nrc"), (int, float)
            )
        ]
        return (
            round(
                sum(nrc_percents) / len(nrc_percents) * 100,
                2,
            )
            if nrc_percents
            else 0.0
        )

    @rx.var
    def top_10_critical_parts_data(
        self,
    ) -> list[dict[str, Union[str, float]]]:
        if not self.filtered_data:
            return []
        sorted_data = sorted(
            self.filtered_data,
            key=lambda x: x.get("score_criticite", 0.0),
            reverse=True,
        )
        top_10 = sorted_data[:10]
        return [
            {
                "name": str(item["pn"]),
                "Score": item.get("score_criticite", 0.0),
            }
            for item in top_10
        ]

    @rx.var
    def aog_nrc_by_part_data(
        self,
    ) -> list[dict[str, Union[str, float]]]:
        if not self.filtered_data:
            return []
        df = pd.DataFrame(self.filtered_data)
        if df.empty:
            return []
        grouped = (
            df.groupby("pn")
            .agg(
                avg_aog=("percent_aog", "mean"),
                avg_nrc=("percent_nrc", "mean"),
            )
            .reset_index()
        )
        grouped["total_aog_nrc_sum_for_sort"] = (
            grouped["avg_aog"] + grouped["avg_nrc"]
        )
        top_parts_df = grouped.sort_values(
            by=["total_aog_nrc_sum_for_sort"],
            ascending=False,
        ).head(10)
        chart_data: list[dict[str, Union[str, float]]] = []
        for _, row in top_parts_df.iterrows():
            chart_data.append(
                {
                    "name": str(row["pn"]),
                    "% AOG": round(row["avg_aog"] * 100, 2),
                    "% NRC": round(row["avg_nrc"] * 100, 2),
                }
            )
        return chart_data

    @rx.var
    def urgency_distribution_data(
        self,
    ) -> list[dict[str, Union[str, int]]]:
        if not self.filtered_data:
            return []
        urgency_counts = (
            pd.Series(
                (
                    str(item["urgency"])
                    for item in self.filtered_data
                )
            )
            .value_counts()
            .to_dict()
        )
        return [
            {"name": str(urgency), "value": count}
            for urgency, count in urgency_counts.items()
        ]

    @rx.var
    def evolution_data(
        self,
    ) -> list[dict[str, Union[str, float]]]:
        if not self.filtered_data:
            return []
        data_with_year = [
            item
            for item in self.filtered_data
            if item.get("annee") is not None
        ]
        if not data_with_year:
            return []
        df = pd.DataFrame(data_with_year)
        df["annee"] = df["annee"].astype(int)
        evolution = (
            df.groupby("annee")
            .agg(
                avg_score_criticite=(
                    "score_criticite",
                    "mean",
                ),
                total_quantite_moyenne=(
                    "quantite_moyenne",
                    "sum",
                ),
            )
            .reset_index()
        )
        evolution = evolution.sort_values(by="annee")
        result_data: list[dict[str, Union[str, float]]] = []
        for _, row in evolution.iterrows():
            result_data.append(
                {
                    "name": str(row["annee"]),
                    "Score Moyen": round(
                        row["avg_score_criticite"], 2
                    ),
                    "Quantité Totale": round(
                        row["total_quantite_moyenne"], 2
                    ),
                }
            )
        return result_data

    @rx.event
    def download_filtered_data(self):
        if not self.filtered_data:
            return rx.toast(
                "Aucune donnée filtrée à télécharger.",
                duration=3000,
            )
        df_to_download = pd.DataFrame(self.filtered_data)
        cols_to_download_map = {
            "pn": "PN",
            "description": "Description",
            "score_criticite": "Score criticité",
            "percent_aog": "% AOG",
            "percent_nrc": "% NRC",
            "quantite_moyenne": "Quantité Moyenne",
            "urgency": "URGENCY",
        }
        download_cols_internal = [
            col
            for col in cols_to_download_map.keys()
            if col in df_to_download.columns
        ]
        df_to_download = df_to_download[
            download_cols_internal
        ]
        df_to_download = df_to_download.rename(
            columns=cols_to_download_map
        )
        csv_string = df_to_download.to_csv(
            index=False, encoding="utf-8"
        )
        return rx.download(
            data=csv_string.encode("utf-8"),
            filename="donnees_filtrees.csv",
        )