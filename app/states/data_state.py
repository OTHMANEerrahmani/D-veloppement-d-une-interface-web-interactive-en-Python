import reflex as rx
import pandas as pd
from pathlib import Path
from typing import (
    TypedDict,
    List,
    Optional,
    Dict,
    Union,
    Tuple,
)
import io

COL_REF_PIECE = "Réfèrence pièce"
COL_PN_ALT = "PN"
COL_DESC = "Description"
COL_QTY_AVG = "Quantité Moyenne"
COL_VISITS = "Nombre de visites"
COL_FREQ_TOTAL = "Fréquence totale"
COL_FREQ_NRC = "Fréquence NRC"
COL_FREQ_AOG = "Fréquence AOG"
COL_PERCENT_NRC = "% NRC"
COL_PERCENT_AOG = "% AOG"
COL_SCORE = "Score de criticité"
COL_AC_REG = "A/C REG"
COL_ANNEE = "Année"
COL_URGENCY = "URGENCY"
COL_SEGMENT = "Segment"
COLUMN_MAPPING = {
    COL_REF_PIECE: "pn",
    COL_PN_ALT: "pn",
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
    COL_SEGMENT: "segment",
}
REQUIRED_INTERNAL_COLUMNS = [
    "pn",
    "description",
    "score_criticite",
    "segment",
]


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
    segment: str


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
            "segment": "Engine",
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
            "segment": "Avionics",
        },
    ]
    for i in range(3, 15):
        freq_total_val = i * 3
        freq_nrc_val = i // 2
        freq_aog_val = i // 4
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
                "segment": [
                    "Airframe",
                    "Cabin",
                    "Landing Gear",
                ][i % 3],
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
    selected_file_name: str = ""

    def _parse_and_prepare_df(
        self, df: pd.DataFrame
    ) -> Tuple[Optional[List[ItemData]], Optional[str]]:
        """
        Parses and prepares a Pandas DataFrame.
        Renames columns, validates required columns, cleans data, and converts to list of dicts.
        """
        try:
            df = df.rename(
                columns=lambda c: COLUMN_MAPPING.get(
                    c.strip(), c.strip()
                )
            )
            missing_required = [
                col
                for col in REQUIRED_INTERNAL_COLUMNS
                if col not in df.columns
            ]
            if missing_required:
                original_missing_names = []
                for internal_col_name in missing_required:
                    found_original = False
                    for (
                        original_name,
                        mapped_name,
                    ) in COLUMN_MAPPING.items():
                        if mapped_name == internal_col_name:
                            original_missing_names.append(
                                original_name
                            )
                            found_original = True
                            break
                    if not found_original:
                        original_missing_names.append(
                            internal_col_name
                        )
                return (
                    None,
                    f"Colonnes requises manquantes : {', '.join(original_missing_names)}.",
                )
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
                elif col in ItemData.__annotations__:
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
                elif col in ItemData.__annotations__:
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
            elif "annee" in ItemData.__annotations__:
                df["annee"] = None
            string_cols = [
                "pn",
                "description",
                "ac_reg",
                "urgency",
                "segment",
            ]
            for col in string_cols:
                if col in df.columns:
                    df[col] = df[col].astype(str).fillna("")
                elif col in ItemData.__annotations__:
                    df[col] = ""
            final_columns = list(
                ItemData.__annotations__.keys()
            )
            for col in final_columns:
                if col not in df.columns:
                    col_type = ItemData.__annotations__[col]
                    if col_type == str:
                        df[col] = ""
                    elif col_type == float:
                        df[col] = 0.0
                    elif col_type == int:
                        df[col] = 0
                    elif col_type == Optional[int]:
                        df[col] = None
                    else:
                        df[col] = None
            return (
                df[final_columns].to_dict(orient="records"),
                None,
            )
        except Exception as e:
            return (
                None,
                f"Erreur de traitement des données du fichier: {str(e)}",
            )

    @rx.event
    def load_data(self):
        """Loads initial data from the default Excel file or sample data if not found/error."""
        self.is_loading = True
        self.raw_data = []
        self.data_load_error_message = ""
        excel_file_path = Path(
            "assets/Tableau_Final_Items_Critiques.xlsx"
        )
        df_loaded = False
        try:
            if excel_file_path.exists():
                df = pd.read_excel(excel_file_path)
                processed_data, error = (
                    self._parse_and_prepare_df(df)
                )
                if error:
                    self.data_load_error_message = f"Erreur fichier par défaut: {error}. Chargement données exemples."
                else:
                    self.raw_data = (
                        processed_data
                        if processed_data is not None
                        else []
                    )
                    df_loaded = True
            else:
                self.data_load_error_message = f"Fichier {excel_file_path.name} introuvable. Chargement données exemples."
            if not df_loaded:
                self.raw_data = create_sample_data()
        except Exception as e:
            self.data_load_error_message = f"Erreur chargement initial: {str(e)}. Chargement données exemples."
            self.raw_data = create_sample_data()
        self.is_loading = False
        self.selected_file_name = ""

    @rx.event
    async def handle_file_upload(
        self, files: list[rx.UploadFile]
    ):
        """Handles the uploaded Excel file, processes it, and updates the app state."""
        if not files:
            yield rx.toast.error(
                "Aucun fichier sélectionné.", duration=3000
            )
            return
        uploaded_file = files[0]
        self.selected_file_name = uploaded_file.name
        if not uploaded_file.name.endswith(".xlsx"):
            self.raw_data = create_sample_data()
            self.is_loading = False
            self.selected_file_name = ""
            yield rx.toast.error(
                "Type de fichier invalide. Veuillez téléverser un fichier .xlsx.",
                duration=5000,
            )
            return
        self.is_loading = True
        yield
        try:
            file_content = await uploaded_file.read()
            df = pd.read_excel(io.BytesIO(file_content))
            processed_data, error_message = (
                self._parse_and_prepare_df(df)
            )
            if error_message:
                self.raw_data = create_sample_data()
                self.is_loading = False
                self.selected_file_name = ""
                yield rx.toast.error(
                    f"Erreur: {error_message} Données exemples chargées.",
                    duration=5000,
                )
                return
            if processed_data is not None:
                self.raw_data = processed_data
                self.data_load_error_message = ""
                yield rx.toast.success(
                    "Fichier téléversé et traité avec succès!",
                    duration=3000,
                )
            else:
                self.raw_data = create_sample_data()
                self.selected_file_name = ""
                yield rx.toast.error(
                    "Erreur inconnue lors du traitement du fichier. Données exemples chargées.",
                    duration=5000,
                )
        except ValueError as ve:
            self.raw_data = create_sample_data()
            self.selected_file_name = ""
            yield rx.toast.error(
                f"Fichier Excel corrompu ou malformé: {str(ve)}. Données exemples chargées.",
                duration=5000,
            )
        except Exception as e:
            self.raw_data = create_sample_data()
            self.selected_file_name = ""
            yield rx.toast.error(
                f"Échec du téléversement: {str(e)}. Données exemples chargées.",
                duration=5000,
            )
        finally:
            self.is_loading = False
            yield

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
                        if item.get("pn")
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
                        if item.get("urgency")
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
                        if item.get("ac_reg")
                    )
                )
            )
        )

    @rx.var
    def unique_annees(self) -> list[str]:
        if not self.raw_data:
            return []
        valid_annees: list[int] = []
        for item in self.raw_data:
            annee = item.get("annee")
            if annee is not None:
                try:
                    valid_annees.append(int(annee))
                except (ValueError, TypeError):
                    pass
        return sorted(
            list(set((str(yr) for yr in valid_annees)))
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
                if isinstance(item, dict)
                and self.filter_pn.lower()
                in str(item.get("pn", "")).lower()
            ]
        if self.filter_urgency:
            data = [
                item
                for item in data
                if isinstance(item, dict)
                and str(item.get("urgency", ""))
                == self.filter_urgency
            ]
        if self.filter_ac_reg:
            data = [
                item
                for item in data
                if isinstance(item, dict)
                and str(item.get("ac_reg", ""))
                == self.filter_ac_reg
            ]
        if self.filter_min_score > 0:
            data = [
                item
                for item in data
                if isinstance(item, dict)
                and item.get("score_criticite", 0.0)
                >= self.filter_min_score
            ]
        if self.filter_annee:
            try:
                year_int = int(self.filter_annee)
                data = [
                    item
                    for item in data
                    if isinstance(item, dict)
                    and item.get("annee") is not None
                    and (item.get("annee") == year_int)
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
            if isinstance(item, dict)
            and isinstance(
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
            if isinstance(item, dict)
            and isinstance(
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
            if isinstance(item, dict)
            and isinstance(
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
        valid_data = [
            item
            for item in self.filtered_data
            if isinstance(item, dict)
            and "score_criticite" in item
            and ("pn" in item)
        ]
        sorted_data = sorted(
            valid_data,
            key=lambda x: x.get("score_criticite", 0.0),
            reverse=True,
        )
        top_10 = sorted_data[:10]
        return [
            {
                "name": str(item.get("pn", "N/A")),
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
        valid_data_for_df = [
            item
            for item in self.filtered_data
            if isinstance(item, dict)
            and all(
                (
                    k in item
                    for k in [
                        "pn",
                        "percent_aog",
                        "percent_nrc",
                    ]
                )
            )
        ]
        if not valid_data_for_df:
            return []
        df = pd.DataFrame(valid_data_for_df)
        if df.empty:
            return []
        df["percent_aog"] = pd.to_numeric(
            df["percent_aog"], errors="coerce"
        ).fillna(0.0)
        df["percent_nrc"] = pd.to_numeric(
            df["percent_nrc"], errors="coerce"
        ).fillna(0.0)
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
        urgencies = [
            str(item.get("urgency", "Unknown"))
            for item in self.filtered_data
            if isinstance(item, dict)
        ]
        if not urgencies:
            return []
        urgency_counts = (
            pd.Series(urgencies).value_counts().to_dict()
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
            if isinstance(item, dict)
            and item.get("annee") is not None
            and all(
                (
                    k in item
                    for k in [
                        "score_criticite",
                        "quantite_moyenne",
                    ]
                )
            )
        ]
        if not data_with_year:
            return []
        df = pd.DataFrame(data_with_year)
        try:
            df["annee"] = (
                pd.to_numeric(df["annee"], errors="coerce")
                .dropna()
                .astype(int)
            )
        except Exception:
            return []
        df["score_criticite"] = pd.to_numeric(
            df["score_criticite"], errors="coerce"
        ).fillna(0.0)
        df["quantite_moyenne"] = pd.to_numeric(
            df["quantite_moyenne"], errors="coerce"
        ).fillna(0.0)
        df = df.dropna(subset=["annee"])
        if df.empty:
            return []
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
                    "name": str(int(row["annee"])),
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
        valid_data_for_df = [
            item
            for item in self.filtered_data
            if isinstance(item, dict)
        ]
        if not valid_data_for_df:
            return rx.toast(
                "Erreur: Données filtrées non valides pour le téléchargement.",
                duration=3000,
            )
        df_to_download = pd.DataFrame(valid_data_for_df)
        cols_to_download_map = {
            "pn": "PN",
            "description": "Description",
            "score_criticite": "Score criticité",
            "percent_aog": "% AOG",
            "percent_nrc": "% NRC",
            "quantite_moyenne": "Quantité Moyenne",
            "urgency": "URGENCY",
            "segment": "Segment",
        }
        download_cols_internal = [
            col_internal
            for col_internal in cols_to_download_map.keys()
            if col_internal in df_to_download.columns
        ]
        if not download_cols_internal:
            return rx.toast(
                "Aucune colonne pertinente à télécharger.",
                duration=3000,
            )
        df_to_download = df_to_download[
            download_cols_internal
        ]
        current_rename_map = {
            k: v
            for k, v in cols_to_download_map.items()
            if k in download_cols_internal
        }
        df_to_download = df_to_download.rename(
            columns=current_rename_map
        )
        csv_string = df_to_download.to_csv(
            index=False, encoding="utf-8"
        )
        return rx.download(
            data=csv_string.encode("utf-8"),
            filename="donnees_filtrees.csv",
        )