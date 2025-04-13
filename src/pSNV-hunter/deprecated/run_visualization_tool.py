import ast
import base64
import glob
import json
import os
from datetime import datetime

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table
# import dash_bio as dashbio

import pandas as pd
import plotly.graph_objects as go
from dash import ctx
from dash.dash import no_update
from dash.dependencies import Input, Output, State

import _helper_functions
import _define_styles

from plots import (
    _get_deep_pileup_plots,
    # _get_patient_info_tab_plots,
    _get_gene_expression_tab_plots,
    _get_tf_expression_tab_plots,
)

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP])

path_to_csv_file = [
    "/Users/nicholasabad/Desktop/workspace/data/_DATA_FOR_PAPER_/FinalResults_long.csv"
]

data_dict = {}
print("Loading data files...")
for path in path_to_csv_file:
    dataset = "PCAWG" if "PCAWG" in path else "MASTER"
    data = pd.read_csv(path, delimiter="\t", nrows=10)
    if "interesting" not in data.columns:
        data.insert(loc=0, column="interesting", value="N/A")
    if "free_text" not in data.columns:
        data.insert(loc=len(list(data.columns)), column="free_text", value="{}")
    if "alignment" not in data.columns:
        data.insert(loc=len(list(data.columns)), column="alignment", value="{}")
    data["id"] = data.index
    data = _helper_functions._reorder_columns(data)
    data_dict[dataset] = data
print("... Done loading.")

nav_items = [dbc.NavLink("Home", href="/", active="exact")]

for idx, path in enumerate(path_to_csv_file):
    nav_items.append(
        dbc.NavItem(
            children=[
                dbc.NavLink(
                    f"{_helper_functions._get_pid(path)}",
                    href=f"/{_helper_functions._get_pid(path)}",
                    active="exact",
                ),
            ],
            style={
                "display": "flex",
                "flex-direction": "column",
                "align-items": "center",
            },
        )
    )

sidebar = html.Div(
    [
        html.H2("REMIND-Cancer"),
        html.Hr(),
        html.P("Click on a dataset to analyze.", className="lead"),
        dbc.Collapse(
            dbc.Card(dbc.CardBody("Thi content is hidden in the collapse")),
            id="collapse",
            is_open=False,
        ),
        dbc.Nav(
            nav_items,
            vertical=True,
            pills=True,
        ),
    ],
    style=_define_styles.SIDEBAR_STYLE,
)

hidden_divs_for_updating_dfs = html.Div(
    [
        html.Div(id=f"hidden-div-for-updating-df", style={"visibility": "hidden"}),
        html.Div(id="tf-summary", style={"visibility": "hidden"}),
        dash_table.DataTable(
            id="data-table",
            data=pd.DataFrame().to_dict("records"),
            filter_action="native",
            sort_action="native",
            sort_mode="multi",
            page_action="native",
            style_table={"visibility": "hidden"},
        ),
        html.Div(id="display-mutation", style={"visibility": "hidden"}),
        html.Div(id="data-table-output", style={"visibility": "hidden"}),
        dbc.Button(
            'Display Current "Free Text"',
            id="free-text-preview-button",
            n_clicks=0,
            style={"visibility": "hidden"},
        ),
        html.Div(id="free-text-preview-output", style={"visibility": "hidden"}),
        dcc.Textarea(
            id="free-text-input",
            value="Some text here...",
            style={"visibility": "hidden"},
        ),
    ]
)

hidden_divs_for_graphs = html.Div(
    [
        html.Div(id=hidden_div_name, style={"visibility": "hidden"})
        for hidden_div_name in ["ge-graph", "tf-exp-graph"]
    ]
    + [
        dbc.Tabs(
            [
                # dbc.Tab(label="Patient Information", tab_id="patient", disabled=True, label_style={"font-weight": "bold"}),
                dbc.Tab(
                    label="Important Information",
                    tab_id="info",
                    disabled=True,
                    label_style={"font-weight": "bold"},
                ),
                dbc.Tab(
                    label="Gene Expression",
                    tab_id="ge",
                    disabled=True,
                    label_style={"font-weight": "bold"},
                ),
                dbc.Tab(
                    label="Transcription Factors",
                    tab_id="tf",
                    disabled=True,
                    label_style={"font-weight": "bold"},
                ),
                dbc.Tab(
                    label="Genome Tornado Plot",
                    tab_id="tornado-plot",
                    disabled=True,
                    label_style={"font-weight": "bold"},
                ),
                dbc.Tab(
                    label="Deep Pileup",
                    tab_id="deep-pileup",
                    disabled=True,
                    label_style={"font-weight": "bold"},
                ),
                dbc.Tab(
                    label="IGV Genome Browser",
                    tab_id="igv",
                    disabled=True,
                    label_style={"font-weight": "bold"},
                ),
                dbc.Tab(
                    label="Notes / Free Text",
                    tab_id="free-text",
                    disabled=True,
                    label_style={"font-weight": "bold"},
                ),
            ],
            id="graph-tabs",
            active_tab="ge",
        ),
    ]
    + [
        html.Div(id="ge-tab-display", style={"visibility": "hidden"}),
        html.Div(id="tf-tab-display", style={"visibility": "hidden"}),
        html.Div(
            [
                dbc.Tabs(
                    [dbc.Tab(label="Unknown", tab_id="unknown", disabled=False)],
                    id="tf-tabs",
                    active_tab="unknown"
                )
            ],
            style={"visbility": "hidden"},
        ),
    ]
    + [
        dbc.Carousel(
            controls=True,
            variant="dark",
            id="chosen-tf-carousel",
            items=[],
            style={"visibility": "hidden"},
        ),
        html.Div(
            [
                html.Div(
                    id="display-original-sequence", style={"visibility": "hidden"}
                ),
                dcc.RangeSlider(
                    0,
                    20,
                    5,
                    value=[10],
                    id="display-original-sequence-slider",
                ),
                html.Div(
                    id="display-actual-tf-sequence", style={"visibility": "hidden"}
                ),
                dcc.RangeSlider(
                    0,
                    20,
                    5,
                    value=[10],
                    id="display-actual-tf-sequence-slider",
                ),
                dcc.Dropdown(
                    options={
                        "Original Sequence": "original",
                        "Reverse Complement": "reverse",
                    },
                    value="original",
                    id="display-actual-tf-sequence-dropdown",
                ),
            ],
            style={"visibility": "hidden"},
        ),
        html.Div(
            [
                dbc.Button("Submit", id="free-text-input-submit-button", n_clicks=0),
                dbc.Button(
                    "Delete Free Text",
                    id="free-text-delete-button",
                    outline=True,
                    color="danger",
                    className="me-1",
                ),
                dbc.Button(
                    "Save TF Sequence Alignment",
                    id="save-tf-sequence-alignment",
                    color="primary",
                ),
                html.Div(id="temp-display-tf-sequence-alignment"),
            ],
            style={"visibility": "hidden"},
        ),
        html.Div(
            [dbc.Accordion(id="wish-list-accordion")], style={"visibility": "hidden"}
        ),
    ],
    style={"visibility": "hidden"},
)

content = html.Div(id="page-content")

app.layout = html.Div(
    [
        dcc.Location(id="url"),
        sidebar,
        html.Div(
            [
                content,
                hidden_divs_for_updating_dfs,
                hidden_divs_for_graphs,
            ],
            style=_define_styles.CONTENT_STYLE,
        ),
        html.Div(
            [
                dash_table.DataTable(
                    data=pd.DataFrame().to_dict("records"),
                    filter_action="native",
                    sort_action="native",
                    sort_mode="multi",
                    page_action="native",
                    row_selectable="single",
                    id=f"wish-list-data-table-{pid}",
                )
                for pid in data_dict
            ]
            + [html.Div(id=f"wish-list-data-table-{pid}-output") for pid in data_dict]
            + [dcc.Download(id=f"wish-list-download-{pid}") for pid in data_dict]
            + [
                dbc.Button("Download CSV", id=f"wish-list-download-button-{pid}")
                for pid in data_dict
            ],
            style={"visibility": "hidden"},
        ),
    ]
)

for pid in data_dict:
    # Displaying the free-text comments for each wishlist dataframe.
    @app.callback(
        Output(f"wish-list-data-table-{pid}-output", "children"),
        [
            Input(f"wish-list-data-table-{pid}", "derived_virtual_selected_row_ids"),
            Input("wish-list-accordion", "active_item"),
        ],
    )
    def something(selected_rows, pid):
        if (selected_rows is not None) and (selected_rows != []) and (pid is not None):
            row = data_dict[pid].iloc[selected_rows[0]]
            free_text = ast.literal_eval(row["free_text"])
            return [
                html.H1("Saved Comments:"),
                dcc.Markdown(f"""```{json.dumps(free_text, indent = 4)[:-1]}"""),
            ]

    # Download button.
    @app.callback(
        Output(f"wish-list-download-{pid}", "data"),
        [
            Input(f"wish-list-download-button-{pid}", "n_clicks"),
            Input("wish-list-accordion", "active_item"),
        ],
        prevent_initial_call=True,
    )
    def download_button(n_clicks, active_item):
        if active_item and n_clicks is not None:
            if ctx.triggered_id == f"wish-list-download-button-{active_item}":
                data_to_export = data_dict[active_item]
                data_to_export = data_to_export[
                    (data_to_export["interesting"] == "Yes")
                    | (data_to_export["interesting"] == "Maybe")
                ]

                now = datetime.now()
                now = now.strftime("%d%b%Y_%H-%M-%S")

                return dcc.send_data_frame(
                    data_to_export.to_csv, f"{active_item}_wishlist_{now}.csv"
                )
        else:
            return


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        accordian = []
        for pid in data_dict:
            temp_data = data_dict[pid]
            data_columns = [{"name": i, "id": i} for i in temp_data.columns]
            accordian_item = dbc.AccordionItem(
                [
                    html.Div(
                        [
                            dash_table.DataTable(
                                data=temp_data[
                                    (temp_data["interesting"] == "Yes")
                                    | (temp_data["interesting"] == "Maybe")
                                ].to_dict("records"),
                                columns=data_columns,
                                filter_action="native",
                                sort_action="native",
                                sort_mode="multi",
                                page_action="native",
                                row_selectable="single",
                                css=[
                                    {
                                        "selector": ".Select-menu-outer",
                                        "rule": "display: block !important",
                                    },
                                ],
                                id=f"wish-list-data-table-{pid}",
                            ),
                            html.Div(id=f"wish-list-data-table-{pid}-output"),
                            html.Div(
                                [
                                    html.Br(),
                                    dbc.Button(
                                        f"Download Interesting Mutations for {pid}",
                                        id=f"wish-list-download-button-{pid}",
                                        color="primary",
                                    ),
                                ],
                                className="d-grid gap-2 col-6 mx-auto",
                            ),
                            dcc.Download(id=f"wish-list-download-{pid}"),
                        ],
                        style={
                            "overflow-x": "scroll",
                            "padding-bottom": "3%",
                            "overflow-y": "fixed",
                        },
                    )
                ],
                title=f"{pid}: {temp_data[(temp_data['interesting'] == 'Yes') | (temp_data['interesting'] == 'Maybe')].shape[0]}",
                item_id=pid,
            )
            accordian.append(accordian_item)
        return [
            html.H1("Home Page!"),
            html.Div(
                [
                    dash_table.DataTable(
                        id="data-table",
                        data=pd.DataFrame().to_dict("records"),
                        filter_action="native",
                        sort_action="native",
                        sort_mode="multi",
                        page_action="native",
                        style_table={"visibility": "hidden"},
                        css=[
                            {
                                "selector": ".Select-menu-outer",
                                "rule": "display: block !important",
                            },
                        ],
                    ),
                ],
                style={
                    "overflow-x": "scroll",
                    "padding-bottom": "3%",
                    "overflow-y": "fixed",
                },
            ),
            html.Div(
                dbc.Accordion(
                    accordian, start_collapsed=True, id="wish-list-accordion"
                ),
            ),
        ]

    for path in path_to_csv_file:
        pid = _helper_functions._get_pid(path)
        data = data_dict[pid]
        data_columns = [
            {"name": "interesting", "id": "interesting", "presentation": "dropdown"}
        ]
        for column in data.columns:
            if column != "interesting":
                if ("TPM" in column) or ("FPKM" in column):
                    if "Z_score" in column:
                        expression_measurement = column.split("_")[0]
                        new_colname = f"Z-Score ({expression_measurement})"

                        data_columns.append(
                            {
                                "name": new_colname,
                                "id": column,
                                "type": "numeric",
                                "format": dash_table.Format.Format(
                                    precision=2,
                                    scheme=dash_table.Format.Scheme.fixed,
                                    trim=dash_table.Format.Trim.yes,
                                ),
                            }
                        )
                elif "score" in column:
                    data_columns.append(
                        {
                            "name": column,
                            "id": column,
                            "type": "numeric",
                            "format": dash_table.Format.Format(
                                precision=3,
                            ),
                        }
                    )
                elif column in _define_styles.DATA_TABLE_COLUMN_CONVERSION:
                    data_columns.append(
                        {
                            "name": _define_styles.DATA_TABLE_COLUMN_CONVERSION[column][
                                "table_name"
                            ],
                            "id": column,
                        }
                    )

                else:
                    data_columns.append({"name": column, "id": column})

        if pathname == f"/{pid}":
            tooltip_header = {}

            for key in _define_styles.DATA_TABLE_COLUMN_CONVERSION:
                if "tooltip" in _define_styles.DATA_TABLE_COLUMN_CONVERSION[key]:
                    tooltip_description = _define_styles.DATA_TABLE_COLUMN_CONVERSION[
                        key
                    ]["tooltip"]
                    tooltip_header[key] = tooltip_description

            data_table = html.Div(
                [
                    dash_table.DataTable(
                        id="data-table",
                        data=data.to_dict("records"),
                        columns=data_columns,
                        row_selectable="single",
                        filter_action="native",
                        sort_action="native",
                        sort_mode="multi",
                        page_action="native",
                        editable=True,
                        page_size=3,
                        dropdown={
                            "interesting": {
                                "options": [
                                    {"label": i, "value": i}
                                    for i in ["N/A", "No", "Maybe", "Yes"]
                                ],
                                "clearable": False,
                            }
                        },
                        css=[
                            {
                                "selector": ".Select-menu-outer",
                                "rule": "display: block !important",
                            },
                        ],
                        tooltip_header=tooltip_header,
                        tooltip_duration=None,
                        style_data={
                            "textAlign": "center",
                        },
                        style_data_conditional=[
                            {
                                "if": {"row_index": "odd"},
                                "backgroundColor": "#f5f7f9",
                            },
                        ],
                        style_header=_define_styles.TABLE_HEADER_STYLE,
                        style_header_conditional=[
                            {
                                "if": {
                                    "column_id": [
                                        key
                                        for key in _define_styles.DATA_TABLE_COLUMN_CONVERSION
                                        if "tooltip"
                                        in _define_styles.DATA_TABLE_COLUMN_CONVERSION[
                                            key
                                        ]
                                    ]
                                },
                                "textDecoration": "underline",
                                "textDecorationStyle": "dotted",
                            },
                        ],
                    ),
                    html.Br(),
                ],
                style={
                    "overflow-x": "scroll",
                    "padding-bottom": "3%",
                    "overflow-y": "fixed",
                },
            )

            return html.Div(
                [
                    data_table,
                    html.Div(id="data-table-output"),
                    html.Br(),
                    dbc.Tabs(
                        [
                            # dbc.Tab(label="Patient Information", tab_id="patient", label_style={"font-weight": "bold"}, style = {"width": "10%"}),
                            dbc.Tab(
                                label="Important Information",
                                tab_id="info",
                                label_style={"font-weight": "bold"},
                                style={"width": "10%"},
                            ),
                            dbc.Tab(
                                label="Gene Expression",
                                tab_id="ge",
                                label_style={"font-weight": "bold"},
                                style={"width": "10%"},
                            ),
                            dbc.Tab(
                                label="Transcription Factors",
                                tab_id="tf",
                                label_style={"font-weight": "bold"},
                                style={"width": "10%"},
                            ),
                            dbc.Tab(
                                label="Genome Tornado Plot",
                                tab_id="tornado-plot",
                                label_style={"font-weight": "bold"},
                                style={"width": "10%"},
                            ),
                            dbc.Tab(
                                label="Deep Pileup",
                                tab_id="deep-pileup",
                                label_style={"font-weight": "bold"},
                                style={"width": "10%"},
                            ),
                            dbc.Tab(
                                label="IGV Genome Browser",
                                tab_id="igv",
                                label_style={"font-weight": "bold"},
                                style={"width": "10%"},
                            ),
                            dbc.Tab(
                                label="Notes / Free Text",
                                tab_id="free-text",
                                label_style={"font-weight": "bold"},
                                style={"width": "10%"},
                            ),
                        ],
                        id="graph-tabs",
                        active_tab="ge",
                    ),
                    html.Div(id="ge-tab-display"),
                ]
            )

    # If the user tries to reach a different page, return a 404 message
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    )


@app.callback(
    Output("tf-tab-display", "children"),
    [
        Input("data-table", "derived_virtual_selected_row_ids"),
        Input("tf-tabs", "active_tab"),
        Input("url", "pathname"),
    ],
)
def switch_tf_tab(
    selected_rows,
    active_tf_tab,
    pid,
):
    print(selected_rows, active_tf_tab, pid)
    if pid != "/" and selected_rows and active_tf_tab and active_tf_tab != "unknown":
        pid = pid[1:]  # Removing the initial slash.
        data = data_dict[pid].iloc[selected_rows[0]]

        # Get the graphs.
        tf_graph = go.Figure()
        try:
            tf_graph = _get_tf_expression_tab_plots.tf_expression_violin_plot(
                row=data,
                chosen_tf_name=active_tf_tab,
            )
        except:
            tf_graph = go.Figure()
        transcription_factor_dict = ast.literal_eval(data["tf_summary"])
        assert type(transcription_factor_dict) == dict

        if active_tf_tab in transcription_factor_dict:
            summary = transcription_factor_dict[active_tf_tab]["summary"]
            url = transcription_factor_dict[active_tf_tab]["url"]
        else:
            summary = ""
            url = ""

        # Get the binding affinity / created or destroyed TFBS.
        for transcription_factor_entry in data[
            "JASPAR2020_CORE_vertebrates_non_redundant(tf_name,binding_affinity,seq1,seq2,raw,zscore,log,tf_sequence_logo)"
        ].split(";"):
            tf_name, binding_affinity = transcription_factor_entry.split(",")[:2]
            if tf_name == active_tf_tab:
                break
        if float(binding_affinity) >= 11:
            created_or_destroyed = "created"
        else:
            created_or_destroyed = "destroyed"
        return [
            # NCBI Information and TF Graph
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.H1(
                                f"{active_tf_tab}",
                                style={
                                    "text-align": "center",
                                },
                            ),
                            html.H5(
                                f"Predicted to have a transcription factor binding site that is {created_or_destroyed}",
                                style={
                                    "color": "lightgrey",
                                },
                            ),
                            html.Div(f"{summary}"),
                            dcc.Link(f"Link to {active_tf_tab} description.", href=url),
                        ],
                        width=4,
                    ),
                    dbc.Col(
                        [
                            dcc.Graph(figure=tf_graph),
                        ],
                        width=8,
                    ),
                ]
            ),
            # Sequence Logo Plot
            dbc.Row(
                [
                    html.Br(),
                    html.Br(),
                    dbc.Col(
                        html.H3("Transcription Factor Logo Plot Alignment"),
                        width={"size": 6, "offset": 3},
                    ),
                    dbc.Col(
                        [
                            dbc.Carousel(
                                controls=True,
                                variant="dark",
                                id="chosen-tf-carousel",
                                items=[],
                            ),
                        ],
                        width=6,
                    ),
                    dbc.Col(
                        [
                            html.Div(id="display-mutation"),
                            dcc.RangeSlider(
                                0,
                                20,
                                5,
                                value=[10],
                                id="display-original-sequence-slider",
                            ),
                            html.Div(id="display-original-sequence"),
                            dbc.Button(
                                "Save TF Sequence Alignment",
                                id="save-tf-sequence-alignment",
                                color="primary",
                            ),
                            html.Div(id="temp-display-tf-sequence-alignment"),
                        ],
                        align="center",
                    ),
                ],
            ),
        ]


@app.callback(
    Output("temp-display-tf-sequence-alignment", "children"),
    [
        Input("save-tf-sequence-alignment", "n_clicks"),
        Input("data-table", "derived_virtual_selected_row_ids"),
        Input("tf-tabs", "active_tab"),
        Input("url", "pathname"),
        Input("display-original-sequence-slider", "value"),
        Input("chosen-tf-carousel", "active_index"),
    ],
)
def display_saved_tf_sequence_alignment(
    _,
    selected_rows,
    chosen_tf,
    pid,
    chosen_tf_value,
    chosen_tf_carousel_index,
):
    if selected_rows and chosen_tf and pid != "/":
        if ctx.triggered_id == "save-tf-sequence-alignment":
            # Get whether the TF carousel is displaying the original or revcomp sequence logo plot.
            original_or_revcomp = (
                "revcomp" if chosen_tf_carousel_index == 1 else "original"
            )

            # Update (or initialize) the 'alignment' column within the dataframe.
            pid = pid[1:]
            data = data_dict[pid]
            curr_alignment = ast.literal_eval(data.iloc[selected_rows[0]]["alignment"])

            if chosen_tf not in curr_alignment:
                curr_alignment[chosen_tf] = {}
            curr_alignment[chosen_tf] = {
                "original_or_revcomp_logo_seq": original_or_revcomp,
                "alignment": chosen_tf_value,
            }
            data_dict[pid].loc[selected_rows[0], "alignment"] = str(curr_alignment)


@app.callback(
    Output("display-mutation", "children"),
    [
        Input("data-table", "derived_virtual_selected_row_ids"),
        Input("tf-tabs", "active_tab"),
        Input("url", "pathname"),
    ],
)
def display_mutation(selected_rows, chosen_tf, pid):
    print('HERE!!!')
    if selected_rows and chosen_tf and pid != "/":
        data = data_dict[pid[1:]].iloc[selected_rows[0]]
        ref = data["REF"]
        alt = data["ALT"]

        revcomp_ref = _helper_functions._get_reverse_complement(ref)
        revcomp_alt = _helper_functions._get_reverse_complement(alt)

        jaspar_column = "JASPAR2020_CORE_vertebrates_non_redundant(tf_name,binding_affinity,seq1,seq2,raw,zscore,log,tf_sequence_logo)"

        created_or_destroyed = "<unknown>"

        if data[jaspar_column] != ".":
            for entry in data[jaspar_column].split(";"):
                tf_name = entry.split(",")[0]
                binding_affinity = float(entry.split(",")[1])
                if tf_name == chosen_tf:
                    created_or_destroyed = (
                        "created" if binding_affinity >= 11 else "destroyed"
                    )
                    break

        return [
            html.H3(f"{tf_name} was predicted to be {created_or_destroyed}."),
            html.H1(
                f"Mutation: {ref} > {alt} / Rev Comp: {revcomp_ref} > {revcomp_alt}"
            ),
            html.Br(),
        ]


@app.callback(
    Output("display-actual-tf-sequence", "children"),
    [
        Input("display-actual-tf-sequence-slider", "value"),
        Input("display-actual-tf-sequence-slider", "marks"),
    ],
)
def display_original_sequence(values, marks):
    if marks and values:
        starting_value = values[0] - 1
        ending_value = values[-1]

        color_scheme = {
            "C": "#255c99",
            "T": "#d62839",
            "G": "#f7b32b",
            "A": "#58b67f",
            ",": "#000000",
        }

        sequence = "".join([marks[letter]["label"] for letter in marks])

        return [
            html.H1(
                f"{letter}",
                style={
                    "display": "inline-block",
                    "color": f"{color_scheme[letter]}",
                    "text-align": "center",
                    "width": "30px",
                },
            )
            for letter in sequence[starting_value:ending_value]
        ]
    else:
        return no_update


@app.callback(
    [
        Output("display-actual-tf-sequence-slider", "min"),
        Output("display-actual-tf-sequence-slider", "max"),
        Output("display-actual-tf-sequence-slider", "value"),
        Output("display-actual-tf-sequence-slider", "marks"),
    ],
    [
        Input("display-actual-tf-sequence-dropdown", "value"),
        Input("data-table", "derived_virtual_selected_row_ids"),
        Input("tf-tabs", "active_tab"),
        Input("url", "pathname"),
    ],
)
def display_actual_tf_sequence_slider(dropdown_value, selected_rows, chosen_tf, pid):
    if selected_rows and chosen_tf and pid != "/":
        data = data_dict[pid[1:]].iloc[selected_rows[0]]
        jaspar_column = "JASPAR2020_CORE_vertebrates_non_redundant(tf_name,binding_affinity,seq1,seq2,raw,zscore,log,tf_sequence_logo)"
        transcription_factors = data[jaspar_column]
        for transcription_factor in transcription_factors.split(";"):
            tf_name = transcription_factor.split(",")[0]
            seq1, seq2 = transcription_factor.split(",")[2:4]
            if tf_name == chosen_tf:
                sequence = seq1 if seq1 != "." else seq2
                sequence = (
                    _helper_functions._get_reverse_complement(sequence)
                    if dropdown_value == "reverse"
                    else sequence
                )
                # Get the range slider.
                color_scheme = {
                    "C": "#255c99",
                    "T": "#d62839",
                    "G": "#f7b32b",
                    "A": "#58b67f",
                    ",": "#000000",
                }

                marks_dictionary = {}
                for value in range(1, len(sequence) + 1):
                    marks_dictionary[value] = {
                        "label": str(sequence[value - 1]),
                        "style": {
                            "color": f"{color_scheme[str(sequence[value - 1])]}",
                        },
                    }

                minimum = 1
                maximum = len(sequence)
                value = [1, int(maximum) + 1]
                marks = marks_dictionary
                return minimum, maximum, value, marks
        return no_update, no_update, no_update, no_update
    return no_update, no_update, no_update, no_update


@app.callback(
    [
        Output("display-original-sequence-slider", "min"),
        Output("display-original-sequence-slider", "max"),
        Output("display-original-sequence-slider", "value"),
        Output("display-original-sequence-slider", "marks"),
    ],
    [
        Input("data-table", "derived_virtual_selected_row_ids"),
        Input("tf-tabs", "active_tab"),
        Input("url", "pathname"),
    ],
)
def display_original_sequence_slider(selected_rows, chosen_tf, pid):
    if selected_rows and chosen_tf and pid != "/":
        pid = pid[1:]
        row_index = selected_rows[0]

        data = data_dict[pid]
        row = data.iloc[row_index]

        sequence_context = row["SEQUENCE_CONTEXT"]
        ref = row["REF"]
        index_of_mutation = sequence_context.index(",")
        sequence_context = sequence_context.replace(",", ref)

        # Get the range slider.
        color_scheme = {
            "C": "#255c99",
            "T": "#d62839",
            "G": "#f7b32b",
            "A": "#58b67f",
            ",": "#000000",
        }

        marks_dictionary = {}

        for value in range(1, len(sequence_context) + 1):
            marks_dictionary[value] = {
                "label": str(sequence_context[value - 1]),
                "style": {
                    "color": f"{color_scheme[str(sequence_context[value - 1])]}",
                    "font-size": "100%",
                },
            }
            if value == index_of_mutation + 1:
                marks_dictionary[value]["style"]["border-width"] = "3px"
                marks_dictionary[value]["style"]["border-style"] = "solid"
                marks_dictionary[value]["style"]["border-color"] = "black"

        minimum = 1
        maximum = len(sequence_context)

        saved_alignment = ast.literal_eval(row["alignment"])
        if chosen_tf in saved_alignment:
            value = saved_alignment[chosen_tf]["alignment"]
        else:
            value = [1, int(maximum) + 1]
        marks = marks_dictionary
        return minimum, maximum, value, marks
    else:
        return no_update, no_update, no_update, no_update


@app.callback(
    Output("display-original-sequence", "children"),
    [
        Input("display-original-sequence-slider", "value"),
        Input("display-original-sequence-slider", "marks"),
        Input("data-table", "derived_virtual_selected_row_ids"),
        Input("tf-tabs", "active_tab"),
        Input("url", "pathname"),
    ],
)
def display_original_sequence(values, marks, selected_rows, chosen_tf, pid):
    if marks and values and selected_rows and chosen_tf and pid != "/":
        data = data_dict[pid[1:]].iloc[selected_rows[0]]
        sequence_context = data["SEQUENCE_CONTEXT"]
        gene = data["GENE"]
        ref = data["REF"]
        index_of_mutation = sequence_context.index(",")

        starting_value = values[0] - 1
        ending_value = values[-1]

        color_scheme = {
            "C": "#255c99",
            "T": "#d62839",
            "G": "#f7b32b",
            "A": "#58b67f",
            ",": "#000000",
        }

        sequence = "".join([marks[letter]["label"] for letter in marks])
        print(f"{gene} // {sequence}")
        output = []
        for idx, letter in enumerate(sequence[starting_value:ending_value]):
            if idx != index_of_mutation - starting_value:
                output.append(
                    html.H1(
                        f"{letter}",
                        style={
                            "display": "inline-block",
                            "color": f"{color_scheme[letter]}",
                            "width": "30px",
                            "text-align": "center",
                        },
                    )
                )
            else:
                output.append(
                    html.Div(
                        [
                            html.H1(
                                f"{letter}",
                                style={
                                    "display": "inline-block",
                                    "color": f"{color_scheme[letter]}",
                                    "border-width": "3px",
                                    "border-style": "solid",
                                    "border-color": "black",
                                },
                            )
                        ],
                        style={
                            "text-align": "center",
                            "display": "inline-block",
                            "width": "30px",
                        },
                    )
                )

        return output
    else:
        return no_update


@app.callback(
    Output("chosen-tf-carousel", "items"),
    [
        Input("data-table", "derived_virtual_selected_row_ids"),
        Input("tf-tabs", "active_tab"),
        Input("url", "pathname"),
    ],
)
def display_carousel_for_chosen_tf(selected_rows, chosen_tf, pid):
    if selected_rows and chosen_tf and pid != "/":
        data = data_dict[pid[1:]].iloc[selected_rows[0]]
        transcription_factor_colname = [
            colname
            for colname in list(data.index)
            if "JASPAR2020_CORE_vertebrates_non_redundant(tf_name,binding_affinity,seq1,seq2,raw,zscore,log,tf_sequence_logo)"
            in colname
        ][0]
        transcription_factors = data[transcription_factor_colname]
        for transcription_factor in transcription_factors.split(";"):
            tf_name = transcription_factor.split(",")[0]
            tf_sequence_logo = transcription_factor.split(",")[-1]
            if tf_name == chosen_tf:
                reverse_complement_logo_seq = tf_sequence_logo.replace(
                    ".png", ".rc.png"
                )
                carousel = [
                    {
                        "key": "1",
                        "src": tf_sequence_logo,
                        "caption": "Original Logo Sequence",
                    },
                    {
                        "key": "2",
                        "src": reverse_complement_logo_seq,
                        "caption": "Reverse Complement",
                    },
                ]
                return carousel
        return []
    else:
        return []


@app.callback(
    Output("ge-tab-display", "children"),
    [
        Input("graph-tabs", "active_tab"),
        Input("data-table", "derived_virtual_selected_row_ids"),
        Input("url", "pathname"),
    ],
)
def switch_tab(active_tab, selected_rows, pid):
    if selected_rows and pid != "/":
        pid = pid[1:]  # Removing the initial slash.
        data = data_dict[pid].iloc[selected_rows[0]]

        if active_tab == "patient":
            return _helper_functions._get_patient_information(data)
        elif active_tab == "info":
            return _helper_functions._get_information_page(data)

        elif active_tab == "ge":
            fig = _get_gene_expression_tab_plots.gene_expression_violin_plot(data)
            return [
                html.Br(),
                dbc.Row(
                    [
                        dbc.Col(dcc.Graph(figure=fig), width=8),
                        dbc.Col(
                            [
                                html.H1("NCBI Gene Summary"),
                                html.Div(f"{data['ncbi_gene_summary']}"),
                                # html.Br(),
                                dcc.Link(
                                    "Link to NCBI description.", href=data["ncbi_url"]
                                ),
                            ],
                            width=4,
                        ),
                    ]
                ),
            ]

        elif active_tab == "tf":
            transcription_factor_tabs = (
                _helper_functions._get_transcription_factor_tabs(data)
            )

            return [transcription_factor_tabs, html.Br(), html.Div(id="tf-tab-display")]
        elif active_tab == "tornado-plot":
            gene = data["GENE"]
            # tornado_plot_repository = "/omics/groups/OE0436/internal/nabad/TornadoPlot_Repository"
            tornado_plot_repository = (
                "/Users/nicholasabad/Desktop/workspace/data/20June2023_tornado_plots"
            )

            path_to_potential_tornado_plot_folder = os.path.join(
                tornado_plot_repository, gene
            )
            if os.path.exists(path_to_potential_tornado_plot_folder):
                try:
                    path_to_zoomed = glob.glob(
                        os.path.join(
                            path_to_potential_tornado_plot_folder, f"{gene}_zoomed.png"
                        )
                    )[0]
                    path_to_not_zoomed = glob.glob(
                        os.path.join(
                            path_to_potential_tornado_plot_folder,
                            f"{gene}_not_zoomed.png",
                        )
                    )[0]

                    if os.path.exists(path_to_zoomed) and os.path.exists(
                        path_to_not_zoomed
                    ):
                        zoomed_encoded = base64.b64encode(
                            open(path_to_zoomed, "rb").read()
                        )
                        not_zoomed_encoded = base64.b64encode(
                            open(path_to_not_zoomed, "rb").read()
                        )
                        return [
                            html.Img(
                                src="data:image/png;base64,{}".format(
                                    zoomed_encoded.decode()
                                ),
                                style={"display": "inline-block", "width": "49%"},
                            ),
                            html.Img(
                                src="data:image/png;base64,{}".format(
                                    not_zoomed_encoded.decode()
                                ),
                                style={"display": "inline-block", "width": "49%"},
                            ),
                            html.Div(f"Path to Zoomed Graph: {path_to_zoomed}"),
                            html.Br(),
                            html.Div(f"Path to Not Zoomed Graph: {path_to_not_zoomed}"),
                        ]
                except:
                    [html.Div("No Tornado Plots of this gene")]

            return [html.Div("No Tornado Plots of this gene")]

        elif active_tab == "deep-pileup":
            gene = data["GENE"]
            pos = data["POS"]
            # deep_pileup_repository = "/omics/groups/OE0436/internal/nabad/DeepPileup_Repository3.0/master"
            deep_pileup_repository = "/Users/nicholasabad/Desktop/workspace/data/28.July.2023_dp/transfer/pcawg"
            path_to_potential_deep_pileup_folder = os.path.join(
                deep_pileup_repository, str(gene), str(pos), "plots", "base_quality_13"
            )
            if os.path.exists(path_to_potential_deep_pileup_folder):
                path_to_overview_file = glob.glob(
                    os.path.join(path_to_potential_deep_pileup_folder, "Overview*.tsv")
                )[0]
                plot_one = _get_deep_pileup_plots.af_greater_than_25_scatterplot(
                    path_to_overview_file, True
                )
                plot_two = (
                    _get_deep_pileup_plots.at_least_two_variant_alleles_scatterplot(
                        path_to_overview_file, True
                    )
                )

                plot_one_a = _get_deep_pileup_plots.af_greater_than_25_scatterplot(
                    path_to_overview_file, False
                )
                plot_two_a = (
                    _get_deep_pileup_plots.at_least_two_variant_alleles_scatterplot(
                        path_to_overview_file, False
                    )
                )

                return [
                    dcc.Graph(figure=plot_one),
                    dcc.Graph(figure=plot_two),
                    dcc.Graph(figure=plot_one_a),
                    dcc.Graph(figure=plot_two_a),
                ]

            return [html.Div("No Deep Pileup Graphs found")]

        elif active_tab == "igv":
            chromosome = str(data["#CHROM"])
            pos = int(data["POS"])

            return [
                # dashbio.Igv(
                #     id="default-igv",
                #     minimumBases=100,
                #     reference={
                #         "id": "hg19",
                #         "name": "Human (GRCh37/hg19)",
                #         "fastaURL": "https://igv.genepattern.org/genomes/seq/hg19/hg19.fasta",
                #         "indexURL": "https://igv.genepattern.org/genomes/seq/hg19/hg19.fasta.fai",
                #         "cytobandURL": "https://igv.genepattern.org/genomes/seq/hg19/cytoBand.txt",
                #         "aliasURL": "https://s3.amazonaws.com/igv.org.genomes/hg19/hg19_alias.tab",
                #         "tracks": [
                #             # NCBI Reference
                #             {
                #                 "name": "NCBI Reference",
                #                 "format": "refgene",
                #                 "id": "hg19_genes",
                #                 "url": "https://s3.amazonaws.com/igv.org.genomes/hg19/ncbiRefSeq.sorted.txt.gz",
                #                 "indexURL": "https://s3.amazonaws.com/igv.org.genomes/hg19/ncbiRefSeq.sorted.txt.gz.tbi",
                #                 "order": 1000000,
                #                 "infoURL": "https://www.ncbi.nlm.nih.gov/gene/?term=$$",
                #                 "height": 100,
                #                 "color": "rgb(176,141,87)",
                #             },
                #             # GENCODE.
                #             {
                #                 "type": "annotation",
                #                 "format": "gtf",
                #                 "url": "https://s3.amazonaws.com/igv.org.genomes/hg19/annotations/gencode.v28lift37.basic.annotation.gtf.gz",
                #                 "indexURL": "https://s3.amazonaws.com/igv.org.genomes/hg19/annotations/gencode.v28lift37.basic.annotation.gtf.gz.tbi",
                #                 "name": "GENCODE genes v28",
                #                 "visibilityWindow": 20000000,
                #             },
                #             # CpG Islands
                #             {
                #                 "name": "CpG Islands",
                #                 "type": "annotation",
                #                 "format": "cpgIslandExt",
                #                 "displayMode": "EXPANDED",
                #                 "url": "https://s3.amazonaws.com/igv.org.genomes/hg19/annotations/cpgIslandExt.txt.gz",
                #             },
                #             # sno/miRNA
                #             # {
                #             #     "name": "UCSC sno/miRNA ",
                #             #     "type": "annotation",
                #             #     "format": "wgRna",
                #             #     "displayMode": "EXPANDED",
                #             #     "url": "https://s3.amazonaws.com/igv.org.genomes/hg19/annotations/wgRna.txt.gz"
                #             # },
                #             # Common SNPs
                #             # {
                #             #     "name": "Common SNPs (150)",
                #             #     "type": "snp",
                #             #     "format": "snp",
                #             #     "visibilityWindow": 10000,
                #             #     "height": 30,
                #             #     "url": "https://s3.amazonaws.com/igv.org.genomes/hg19/snp150Common.txt.gz",
                #             #     "indexURL": "https://s3.amazonaws.com/igv.org.genomes/hg19/snp150Common.txt.gz.tbi",
                #             #     "infoURL": "https://www.ncbi.nlm.nih.gov/snp/?term=$$"
                #             # },
                #         ],
                #         "chromosomeOrder": "chr1, chr2, chr3, chr4, chr5, chr6, chr7, chr8, chr9, chr10, chr11, chr12, chr13, chr14, chr15, chr16, chr17, chr18, chr19, chr20, chr21, chr22, chrX, chrY",
                #     },
                #     locus=[f"chr{chromosome}:{pos}"],
                #     style={"width": "100%", "height": "500%"},
                # )
            ]

        elif active_tab == "free-text":
            return [
                html.Br(),
                dcc.Textarea(
                    id="free-text-input",
                    value="Some text here...",
                    style={"width": "100%", "height": 200},
                ),
                html.Div(
                    [
                        dbc.Button(
                            "Submit Comment",
                            id="free-text-preview-button",
                            n_clicks=0,
                            color="primary",
                        ),
                    ],
                    className="d-grid gap-2 col-6 mx-auto",
                ),
                html.Div(id="free-text-preview-output"),
                dbc.Button(
                    "Delete Free Text",
                    id="free-text-delete-button",
                    outline=True,
                    color="danger",
                    className="me-1",
                ),
            ]
    # Should never get here.
    else:
        return no_update


@app.callback(
    Output("free-text-preview-output", "children"),
    [
        Input("free-text-preview-button", "n_clicks"),
        Input("url", "pathname"),
        Input("free-text-delete-button", "n_clicks"),
        Input("data-table", "data"),
    ],
    [
        State("data-table", "derived_virtual_selected_row_ids"),
        State("free-text-input", "value"),
    ],
)
def display_current_free_text(
    submit_n_clicks,
    pid,
    delete_n_clicks,
    data,
    selected_rows,
    free_text_input,
):
    if (
        (pid != "/")
        and (selected_rows is not None)
        and (selected_rows != [])
        and data is not None
    ):
        pid = pid[1:]
        row_to_update = selected_rows[0]

        if ctx.triggered_id == "free-text-preview-button":
            current_value = ast.literal_eval(
                data_dict[pid].loc[row_to_update, "free_text"]
            )

            now = datetime.now()
            now = now.strftime("%d %b %Y %H:%M:%S:%f")
            current_value[now] = free_text_input
            data_dict[pid].loc[row_to_update, "free_text"] = str(current_value)

        elif ctx.triggered_id == "free-text-delete-button":
            data_dict[pid].loc[row_to_update, "free_text"] = str({})

        return [
            html.Br(),
            html.H1(f"Current Notes / Free Text: "),
            html.Div("{"),
            dcc.Markdown(
                f"""```{json.dumps(ast.literal_eval(data_dict[pid].iloc[row_to_update]["free_text"]), indent = 4)[:-1]}"""
            ),
            html.Div("}"),
            html.Br(),
        ]


@app.callback(
    Output("data-table", "data"),
    [
        Input("data-table", "data_timestamp"),
        Input("url", "pathname"),
    ],
    [State("data-table", "data")],
)
def update_columns(_, pid, data):
    if pid != "/":
        pid = pid[1:]
        data_df = pd.DataFrame(data)
        data_dict[pid] = data_df
        return data_dict[pid].to_dict("records")


if __name__ == "__main__":
    app.run_server(debug=True)
