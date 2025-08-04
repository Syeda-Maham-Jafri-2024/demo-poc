import base64
import os
import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import dash_uploader as du
from pydub import AudioSegment
from code_files.audio_transcription import audio_to_text_with_openai
from code_files.improve_transcription import correct_ercp_transcription
from code_files.report_generation import generate_report_with_ai
from dash_iconify import DashIconify
from dash import no_update

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
    title="Audio Report Generator",
)
du.configure_upload(app, folder="uploads")
app.css.append_css(
    {
        "external_url": "https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css"
    }
)
navbar_custom_css = {
    "backgroundColor": "#ABCE78",
    "height": "35px",
    "display": "flex",
    "justifyContent": "center",
    "alignItems": "center",
    "fontSize": "18px",
    "fontWeight": "500",
}
card_1 = dbc.Card(
    dbc.CardBody(
        [
            html.Div(
                [
                    html.Img(
                        src="data:image/png;base64,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",
                        className="rounded-circle",
                        style={
                            "marginRight": "10px",
                            "width": "60px",
                            "height": "60px",
                        },
                    ),
                    html.Div(
                        [
                            html.H5(
                                "Sindh Institute of Advanced Endoscopy & Gastroentrology",
                                style={
                                    "margin": "0",
                                    "fontSize": "16px",
                                    "color": "#000000",
                                },
                            ),
                        ]
                    ),
                ],
                style={
                    "display": "flex",
                    "alignItems": "center",
                    "marginBottom": "20px",
                },
            ),
            html.Hr(style={"marginBottom": "10px", "marginTop": "10px"}),
            html.Div(
                [
                    html.Img(
                        src="data:image/jpeg;base64,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",
                        className="rounded-circle",
                        style={
                            "marginRight": "10px",
                            "width": "60px",
                            "height": "60px",
                        },
                    ),
                    html.Div(
                        [
                            html.H5(
                                "Doctor Name", style={"margin": "0", "fontSize": "16px"}
                            ),
                            html.P(
                                "Designation",
                                style={
                                    "margin": "0",
                                    "color": "gray",
                                    "fontSize": "12px",
                                },
                            ),
                            html.Span(
                                "● Online", style={"color": "green", "fontSize": "12px"}
                            ),
                        ]
                    ),
                ],
                style={
                    "display": "flex",
                    "alignItems": "center",
                    "marginBottom": "20px",
                },
            ),
            html.Hr(style={"marginBottom": "10px", "marginTop": "10px"}),
            html.Div(
                [
                    html.H6(
                        "Transcribe Audios",
                        style={
                            "fontWeight": "bold",
                            "fontSize": "15px",
                            "display": "inline-block",
                        },
                    ),
                    html.Button(
                        "+",
                        className="btn btn-outline-secondary btn-sm",
                        style={
                            "float": "right",
                            "padding": "0px 6px",
                            "fontSize": "12px",
                        },
                    ),
                ],
                style={"marginBottom": "10px"},
            ),
            html.H6(
                "TODAY",
                style={"fontSize": "12px", "color": "gray", "marginBottom": "10px"},
            ),
            html.Div(
                [
                    html.Div(
                        "",
                        className="rounded",
                        style={
                            "height": "33px",
                            "backgroundColor": "#f8f9fa",
                            "border": "1px solid #ABCE78",
                            "marginBottom": "10px",
                            "borderRadius": "10px",
                        },
                    ),
                    html.Div(
                        "",
                        className="rounded",
                        style={
                            "height": "33px",
                            "backgroundColor": "#f8f9fa",
                            "border": "1px solid #ABCE78",
                            "marginBottom": "10px",
                            "borderRadius": "10px",
                        },
                    ),
                    html.Div(
                        "",
                        className="rounded",
                        style={
                            "height": "33px",
                            "backgroundColor": "#f8f9fa",
                            "border": "1px solid #ABCE78",
                            "marginBottom": "10px",
                            "borderRadius": "10px",
                        },
                    ),
                ]
            ),
            html.H6(
                "LAST WEEK",
                style={
                    "fontSize": "12px",
                    "color": "gray",
                    "marginTop": "20px",
                    "marginBottom": "10px",
                },
            ),
            html.Div(
                [
                    html.Div(
                        "",
                        className="rounded",
                        style={
                            "height": "33px",
                            "backgroundColor": "#f8f9fa",
                            "border": "1px solid #ABCE78",
                            "marginBottom": "10px",
                            "borderRadius": "10px",
                        },
                    ),
                    html.Div(
                        "",
                        className="rounded",
                        style={
                            "height": "33px",
                            "backgroundColor": "#f8f9fa",
                            "border": "1px solid #ABCE78",
                            "marginBottom": "10px",
                            "borderRadius": "10px",
                        },
                    ),
                    html.Div(
                        "",
                        className="rounded",
                        style={
                            "height": "33px",
                            "backgroundColor": "#f8f9fa",
                            "border": "1px solid #ABCE78",
                            "marginBottom": "10px",
                            "borderRadius": "10px",
                        },
                    ),
                ]
            ),
            html.H6(
                "Reports",
                style={"fontWeight": "bold", "fontSize": "15px", "marginTop": "20px"},
            ),
            html.Hr(style={"marginBottom": "15px", "marginTop": "127px"}),
            html.Div(
                [
                    html.Div(
                        [
                            html.I(
                                className="fas fa-cog", style={"marginRight": "5px"}
                            ),
                            html.Span("Settings"),
                        ],
                        style={"marginBottom": "10px"},
                    ),
                    html.Div(
                        [
                            html.I(
                                className="fas fa-envelope",
                                style={"marginRight": "5px"},
                            ),
                            html.Span("Contact us"),
                        ]
                    ),
                ],
                style={"marginTop": "10px", "fontSize": "12px", "color": "gray"},
            ),
        ]
    ),
    style={"backgroundColor": "#FFFFFF", "minHeight": "75vh"},
)

card_2 = dbc.Card(
    dbc.CardBody(
        [
            html.H5("Patient Record", className="card-title"),
            dcc.Tabs(
                id="tabs",
                value="audio",
                className="custom-tab",
                children=[
                    dcc.Tab(
                        label="Audio",
                        value="audio",
                        style={
                            "padding": "5px",
                            "fontSize": "14px",
                            "backgroundColor": "#f0f0f0",
                            "marginRight": "2px",
                            "textAlign": "center",
                            "cursor": "pointer",
                            "borderRadius": "5px",
                            "boxShadow": "0px 2px 5px rgba(0, 0, 0, 0.1)",
                            "transition": "background-color 0.3s, transform 0.2s",
                        },
                        selected_style={
                            "backgroundColor": "#ABCE78",
                            "color": "white",
                            "borderRadius": "5px",
                            "transform": "scale(1.05)",
                            "boxShadow": "0px 4px 10px rgba(0, 0, 0, 0.2)",
                            "borderTop": "none",
                        },
                        children=[
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        dcc.Store(id="audio-source", data=None),
                                        html.P(
                                            "Upload your audio or click on the Start Recording button to record your Audio",
                                            className="card-text",
                                            style={
                                                "font-size": "13px",
                                                "margin": "10px 0px 10px 0px",
                                            },
                                        ),
                                        dbc.Card(
                                            [
                                                dbc.Row(
                                                    [
                                                        html.H3(
                                                            "Record your Audio",
                                                            className="text-secondary",
                                                            style={
                                                                "margin": "0px 0px 20px 0px",
                                                                "font-size": "13px",
                                                            },
                                                        ),
                                                    ],
                                                    className="justify-content-center",
                                                ),
                                                dbc.Row(
                                                    [
                                                        dbc.Col(
                                                            [
                                                                html.Div(
                                                                    du.Upload(
                                                                        id="uploader",
                                                                        text="Drag and drop or click to upload",
                                                                        max_files=1,
                                                                    ),
                                                                    style={
                                                                        "height": "100px",
                                                                        "font-size": "12px",
                                                                        "padding-bottom": "7px",
                                                                    },
                                                                    className="custom-uploader",
                                                                ),
                                                                html.Div(
                                                                    id="upload-status",
                                                                    className="mt-1",
                                                                    style={
                                                                        "font-size": "12px",
                                                                        "padding-top": "0px",
                                                                        "padding-left": "7px",
                                                                        "padding-right": "7px",
                                                                        "padding-bottom": "7px",
                                                                        "color": "#90D2E5",
                                                                    },
                                                                ),
                                                            ],
                                                            md=4,
                                                        ),
                                                        dbc.Col(
                                                            html.Div(
                                                                "Or",
                                                                style={
                                                                    "font-size": "15px",
                                                                    "font-weight": "normal",
                                                                    "color": "#6c757d",
                                                                    "text-align": "center",
                                                                },
                                                            ),
                                                            className="d-flex align-items-center justify-content-center",
                                                        ),
                                                        dbc.Col(
                                                            [
                                                                html.Div(
                                                                    [
                                                                        dbc.Row(
                                                                            [
                                                                                dbc.Col(
                                                                                    dbc.Button(
                                                                                        "Start Recording",
                                                                                        id="record-start",
                                                                                        n_clicks=0,
                                                                                        className="btn btn-outline-primary btn-lg w-100",
                                                                                        style={
                                                                                            "background-color": "#90D2E5",
                                                                                            "color": "white",
                                                                                            "font-size": "12px",
                                                                                            "font-weight": "500",
                                                                                            "padding": "10px 20px",
                                                                                            "border-radius": "25px",
                                                                                            "border": "none",
                                                                                            "box-shadow": "0px 4px 10px rgba(0, 0, 0, 0.1)",
                                                                                            "transition": "all 0.3s ease",
                                                                                        },
                                                                                    ),
                                                                                    width=6,
                                                                                ),
                                                                                dbc.Col(
                                                                                    dbc.Button(
                                                                                        "Stop Recording",
                                                                                        id="record-stop",
                                                                                        n_clicks=0,
                                                                                        className="btn btn-outline-danger btn-lg w-100",
                                                                                        style={
                                                                                            "background-color": "#A8D5BA",
                                                                                            "color": "white",
                                                                                            "font-size": "12px",
                                                                                            "font-weight": "500",
                                                                                            "padding": "10px 20px",
                                                                                            "border-radius": "25px",
                                                                                            "border": "none",
                                                                                            "box-shadow": "0px 4px 10px rgba(0, 0, 0, 0.1)",
                                                                                            "transition": "all 0.3s ease",
                                                                                        },
                                                                                    ),
                                                                                    width=6,
                                                                                ),
                                                                            ],
                                                                            className="g-2",
                                                                        ),
                                                                        html.Div(
                                                                            id="record-status",
                                                                            children="",
                                                                            style={
                                                                                "color": "green",
                                                                                "font-size": "12px",
                                                                                "padding-top": "4px",
                                                                                "text-align": "center",
                                                                                "display": "flex",
                                                                                "align-items": "center",
                                                                                "justify-content": "center",
                                                                            },
                                                                        ),
                                                                    ],
                                                                    style={
                                                                        "border": "1px dashed black",
                                                                        "border-radius": "10px",
                                                                        "padding": "20px",
                                                                        "margin": "12px 0px 0px 0px",
                                                                        "background-color": "#f8f9fa",
                                                                    },
                                                                ),
                                                            ],
                                                            md=6,
                                                        ),
                                                    ]
                                                ),
                                            ],
                                            body=True,
                                            style={
                                                "box-shadow": "0px 4px 15px rgba(0, 0, 0, 0.2)",
                                                "border-radius": "10px",
                                                "padding": "5px 0px 10px 0px",
                                                "background-color": "#f8f9fa",
                                            },
                                        ),
                                        html.Hr(
                                            style={
                                                "msrgin": "6px 0px 6px 0px",
                                            },
                                        ),
                                        html.P(
                                            "Review your uploaded/recorded audio",
                                            className="card-text",
                                            style={
                                                "font-size": "13px",
                                                "margin": "10px 0px 10px 0px",
                                            },
                                        ),
                                        dbc.Card(
                                            [
                                                dbc.Row(
                                                    [
                                                        dbc.Col(
                                                            [
                                                                html.H3(
                                                                    "Play Uploaded Audio",
                                                                    className="text-secondary",
                                                                    style={
                                                                        "margin": "0px 0px 10px 0px",
                                                                        "font-size": "13px",
                                                                    },
                                                                ),
                                                                html.Audio(
                                                                    id="audio-player",
                                                                    controls=True,
                                                                    style={
                                                                        "width": "200%",
                                                                        "height": "30px",
                                                                    },
                                                                ),
                                                            ],
                                                            md=6,
                                                        ),
                                                    ]
                                                ),
                                            ],
                                            body=True,
                                            style={
                                                "box-shadow": "0px 4px 15px rgba(0, 0, 0, 0.2)",
                                                "border-radius": "10px",
                                                "padding": "10px 0px 10px 0px",
                                                "background-color": "#f8f9fa",
                                            },
                                        ),
                                    ]
                                ),
                                style={
                                    "backgroundColor": "#f0f0f0",
                                    "borderRadius": "5px",
                                    "padding": "15px",
                                    "minHeight": "75vh",
                                },
                            ),
                        ],
                    ),
                    dcc.Tab(
                        label="Transcribe",
                        value="transcribe",
                        style={
                            "padding": "5px",
                            "fontSize": "14px",
                            "backgroundColor": "#f0f0f0",
                            "marginRight": "2px",
                            "textAlign": "center",
                            "borderRadius": "5px",
                            "cursor": "pointer",
                            "boxShadow": "0px 2px 5px rgba(0, 0, 0, 0.1)",
                            "transition": "background-color 0.3s, transform 0.2s",
                        },
                        selected_style={
                            "backgroundColor": "#ABCE78",
                            "color": "white",
                            "borderRadius": "5px",
                            "transform": "scale(1.05)",
                            "boxShadow": "0px 4px 10px rgba(0, 0, 0, 0.2)",
                            "borderTop": "none",
                        },
                        children=[
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    [
                                                        dbc.Row(
                                                            [
                                                                dbc.Col(
                                                                    html.H3(
                                                                        "Transcribe the Audio",
                                                                        className="text-secondary",
                                                                        style={
                                                                            "margin": "0px 0px 20px 0px",
                                                                            "font-size": "13px",
                                                                        },
                                                                    ),
                                                                    md=9,
                                                                ),
                                                                dbc.Col(
                                                                    dbc.ButtonGroup(  # Groups the buttons together
                                                                        [
                                                                            dbc.Button(
                                                                                "Transcribe",
                                                                                id="transcribe-button",
                                                                                n_clicks=0,
                                                                                className="mb-2",
                                                                                style={
                                                                                    "background-color": "#90D2E5",
                                                                                    "color": "white",
                                                                                    "font-size": "12px",
                                                                                    "font-weight": "500",
                                                                                    "padding": "7px 20px",
                                                                                    "border-radius": "25px",
                                                                                    "margin-right": "5px",
                                                                                    "border": "none",
                                                                                    "box-shadow": "0px 4px 10px rgba(0, 0, 0, 0.1)",
                                                                                    "transition": "all 0.3s ease",
                                                                                },
                                                                            ),
                                                                            dbc.Button(
                                                                                DashIconify(
                                                                                    icon="mdi:magic-wand",
                                                                                    width=18,
                                                                                ),
                                                                                id="magic-btn",
                                                                                n_clicks=0,
                                                                                className="mb-2",
                                                                                style={
                                                                                    "background-color": "#A8D5BA",
                                                                                    "color": "white",
                                                                                    "font-size": "12px",
                                                                                    "font-weight": "500",
                                                                                    "padding": "7px 15px",
                                                                                    "border-radius": "25px",
                                                                                    "border": "none",
                                                                                    "box-shadow": "0px 4px 10px rgba(0, 0, 0, 0.1)",
                                                                                    "transition": "all 0.3s ease",
                                                                                },
                                                                            ),
                                                                        ],
                                                                        className="d-flex",
                                                                    ),
                                                                    width="auto",
                                                                ),
                                                            ],
                                                            justify="between",
                                                        ),
                                                        html.P(
                                                            "View the transcription of your audio here",
                                                            className="card-text",
                                                            style={
                                                                "font-size": "13px",
                                                                "margin": "20px 0px 5px 0px",
                                                            },
                                                        ),
                                                        dbc.Spinner(
                                                            html.Div(
                                                                id="transcription-output",
                                                                contentEditable=True,
                                                                style={
                                                                    "white-space": "pre-wrap",
                                                                    "border": "1px solid #ccc",
                                                                    "padding": "10px",
                                                                    "border-radius": "5px",
                                                                    "background-color": "#f9f9f9",
                                                                    "font-size": "11px",
                                                                    "height": "150px",
                                                                    "overflow": "auto",
                                                                },
                                                            ),
                                                            size="md",
                                                            color="primary",
                                                            spinner_style={
                                                                "margin": "10px 0px 0px 0px"
                                                            },
                                                            id="transcribe-spinner",
                                                        ),
                                                    ],
                                                    md=12,
                                                ),
                                            ]
                                        ),
                                        html.Hr(),
                                        html.P(
                                            "Add any additional comments/information",
                                            className="card-text",
                                            style={
                                                "font-size": "13px",
                                                "margin": "20px 0px 5px 0px",
                                            },
                                        ),
                                        dbc.Card(
                                            [
                                                dbc.Row(
                                                    [
                                                        dbc.Col(
                                                            [
                                                                html.H3(
                                                                    "Add Additional Comments",
                                                                    className="text-secondary",
                                                                    style={
                                                                        "margin": "0px 0px 20px 0px",
                                                                        "font-size": "13px",
                                                                    },
                                                                ),
                                                                dcc.Textarea(
                                                                    id="additional-comments",
                                                                    placeholder="  Add comments here...",
                                                                    style={
                                                                        "width": "100%",
                                                                        "height": "60px",
                                                                        "margin": "0px 0px 5px 0px",
                                                                        "border-radius": "5px",
                                                                        "font-size": "11px",
                                                                    },
                                                                ),
                                                            ],
                                                            md=12,
                                                        ),
                                                    ]
                                                ),
                                            ],
                                            body=True,
                                            style={
                                                "box-shadow": "0px 4px 15px rgba(0, 0, 0, 0.2)",
                                                "border-radius": "10px",
                                                "padding": "20px",
                                                "padding-top": "5px",
                                                "background-color": "#f8f9fa",
                                            },
                                        ),
                                    ]
                                ),
                                style={
                                    "backgroundColor": "#f0f0f0",
                                    "borderRadius": "5px",
                                    "padding": "15px",
                                    "minHeight": "75vh",
                                },
                            ),
                        ],
                    ),
                    dcc.Tab(
                        label="Patient Report",
                        value="patient_report",
                        style={
                            "padding": "5px",
                            "fontSize": "14px",
                            "backgroundColor": "#f0f0f0",
                            "marginRight": "2px",
                            "textAlign": "center",
                            "cursor": "pointer",
                            "borderRadius": "5px",
                            "boxShadow": "0px 2px 5px rgba(0, 0, 0, 0.1)",
                            "transition": "background-color 0.3s, transform 0.2s",
                        },
                        selected_style={
                            "backgroundColor": "#ABCE78",
                            "color": "white",
                            "borderRadius": "5px",
                            "transform": "scale(1.05)",
                            "boxShadow": "0px 4px 10px rgba(0, 0, 0, 0.2)",
                            "borderTop": "none",
                        },
                        children=[
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        dbc.Form(
                                            [
                                                dbc.Row(
                                                    children=[
                                                        dbc.Col(
                                                            children=[
                                                                dbc.Row(
                                                                    [
                                                                        dbc.Label(
                                                                            "Abdominal Pain",
                                                                            style={
                                                                                "font-size": "11px",
                                                                                "font-weight": "bold",
                                                                                "margin": "0px 0px 2px 0px",
                                                                            },
                                                                        ),
                                                                        dbc.Input(
                                                                            id="abdominal-pain",
                                                                            type="text",
                                                                            value="No",
                                                                            style={
                                                                                "font-size": "11px",
                                                                                "margin": "0px 0px 7px 9px",
                                                                                "width": "60%",
                                                                                "height": "25%",
                                                                            },
                                                                        ),
                                                                    ]
                                                                ),
                                                                dbc.Row(
                                                                    [
                                                                        dbc.Label(
                                                                            "Jaundice",
                                                                            style={
                                                                                "font-size": "11px",
                                                                                "font-weight": "bold",
                                                                                "margin": "0px 0px 2px 0px",
                                                                            },
                                                                        ),
                                                                        dbc.Input(
                                                                            id="juandice",
                                                                            type="text",
                                                                            value="No",
                                                                            style={
                                                                                "font-size": "11px",
                                                                                "margin": "0px 0px 7px 9px",
                                                                                "width": "60%",
                                                                                "height": "25%",
                                                                            },
                                                                        ),
                                                                    ]
                                                                ),
                                                                dbc.Row(
                                                                    [
                                                                        dbc.Label(
                                                                            "Bile Duct Stone",
                                                                            style={
                                                                                "font-size": "11px",
                                                                                "font-weight": "bold",
                                                                                "margin": "0px 0px 2px 0px",
                                                                            },
                                                                        ),
                                                                        dbc.Input(
                                                                            id="bile-duct-stone",
                                                                            type="text",
                                                                            value="No",
                                                                            style={
                                                                                "font-size": "11px",
                                                                                "margin": "0px 0px 7px 9px",
                                                                                "width": "60%",
                                                                                "height": "25%",
                                                                            },
                                                                        ),
                                                                    ]
                                                                ),
                                                                dbc.Row(
                                                                    [
                                                                        dbc.Label(
                                                                            "Periampullary Tumor",
                                                                            style={
                                                                                "font-size": "11px",
                                                                                "font-weight": "bold",
                                                                                "margin": "0px 0px 2px 0px",
                                                                            },
                                                                        ),
                                                                        dbc.Input(
                                                                            id="periampullary-tumor",
                                                                            type="text",
                                                                            value="No",
                                                                            style={
                                                                                "font-size": "11px",
                                                                                "margin": "0px 0px 7px 9px",
                                                                                "width": "60%",
                                                                                "height": "25%",
                                                                            },
                                                                        ),
                                                                    ]
                                                                ),
                                                            ]
                                                        ),
                                                        dbc.Col(
                                                            children=[
                                                                dbc.Row(
                                                                    [
                                                                        dbc.Label(
                                                                            "Pancreatic Biliary Tumor",
                                                                            style={
                                                                                "font-size": "11px",
                                                                                "font-weight": "bold",
                                                                                "margin": "0px 0px 2px 0px",
                                                                            },
                                                                        ),
                                                                        dbc.Input(
                                                                            id="pancreatic-biliary-tumor",
                                                                            type="text",
                                                                            value="No",
                                                                            style={
                                                                                "font-size": "11px",
                                                                                "margin": "0px 0px 7px 9px",
                                                                                "width": "60%",
                                                                                "height": "25%",
                                                                            },
                                                                        ),
                                                                    ]
                                                                ),
                                                                dbc.Row(
                                                                    [
                                                                        dbc.Label(
                                                                            "Previous Surgery",
                                                                            style={
                                                                                "font-size": "11px",
                                                                                "font-weight": "bold",
                                                                                "margin": "0px 0px 2px 0px",
                                                                            },
                                                                        ),
                                                                        dbc.Input(
                                                                            id="previous-surgery",
                                                                            type="text",
                                                                            value="None",
                                                                            style={
                                                                                "font-size": "11px",
                                                                                "margin": "0px 0px 7px 9px",
                                                                                "width": "60%",
                                                                                "height": "25%",
                                                                            },
                                                                        ),
                                                                    ]
                                                                ),
                                                                dbc.Row(
                                                                    [
                                                                        dbc.Label(
                                                                            "Cholecystectomy",
                                                                            style={
                                                                                "font-size": "11px",
                                                                                "font-weight": "bold",
                                                                                "margin": "0px 0px 2px 0px",
                                                                            },
                                                                        ),
                                                                        dbc.Input(
                                                                            id="cholecystectomy",
                                                                            type="text",
                                                                            value="No",
                                                                            style={
                                                                                "font-size": "11px",
                                                                                "margin": "0px 0px 7px 9px",
                                                                                "width": "60%",
                                                                                "height": "25%",
                                                                            },
                                                                        ),
                                                                    ]
                                                                ),
                                                            ]
                                                        ),
                                                        dbc.Col(
                                                            children=[
                                                                dbc.Row(
                                                                    children=[
                                                                        dbc.Col(
                                                                            [
                                                                                dbc.Label(
                                                                                    "A.Phosphatase)",
                                                                                    style={
                                                                                        "font-size": "11px",
                                                                                        "font-weight": "bold",
                                                                                        "margin": "0px 0px 2px 0px",
                                                                                    },
                                                                                ),
                                                                                dbc.Input(
                                                                                    id="a-phosphatese",
                                                                                    type="number",
                                                                                    value=0,
                                                                                    style={
                                                                                        "font-size": "11px",
                                                                                        "margin": "0px 0px 7px 3px",
                                                                                        "width": "50%",
                                                                                        "height": "25%",
                                                                                    },
                                                                                ),
                                                                            ]
                                                                        ),
                                                                        dbc.Col(
                                                                            [
                                                                                dbc.Label(
                                                                                    "Bilirubin",
                                                                                    style={
                                                                                        "font-size": "11px",
                                                                                        "font-weight": "bold",
                                                                                        "margin": "0px 0px 2px 0px",
                                                                                    },
                                                                                ),
                                                                                dbc.Input(
                                                                                    id="bilirubin",
                                                                                    type="number",
                                                                                    value=0,
                                                                                    style={
                                                                                        "font-size": "11px",
                                                                                        "margin": "0px 0px 7px 3px",
                                                                                        "width": "50%",
                                                                                        "height": "25%",
                                                                                    },
                                                                                ),
                                                                            ]
                                                                        ),
                                                                    ]
                                                                ),
                                                                dbc.Row(
                                                                    [
                                                                        dbc.Label(
                                                                            "Abnormal Imaging",
                                                                            style={
                                                                                "font-size": "11px",
                                                                                "font-weight": "bold",
                                                                                "margin": "0px 0px 2px 0px",
                                                                            },
                                                                        ),
                                                                        dbc.Textarea(
                                                                            id="abnormal-imaging",
                                                                            value="None",
                                                                            style={
                                                                                "font-size": "11px",
                                                                                "margin": "0px 0px 7px 9px",
                                                                                "width": "75%",
                                                                                "height": "5%",
                                                                                "resize": "both",
                                                                                "overflow": "auto",
                                                                            },
                                                                        ),
                                                                    ]
                                                                ),
                                                                dbc.Row(
                                                                    [
                                                                        dbc.Label(
                                                                            "Other",
                                                                            style={
                                                                                "font-size": "11px",
                                                                                "font-weight": "bold",
                                                                                "margin": "0px 0px 2px 0px",
                                                                            },
                                                                        ),
                                                                        dbc.Textarea(
                                                                            id="other",
                                                                            value="",
                                                                            style={
                                                                                "font-size": "11px",
                                                                                "margin": "0px 0px 5px 9px",
                                                                                "width": "75%",
                                                                                "height": "5%",
                                                                                "resize": "both",
                                                                                "overflow": "auto",
                                                                            },
                                                                        ),
                                                                    ]
                                                                ),
                                                            ]
                                                        ),
                                                    ]
                                                ),
                                                html.Hr(
                                                    style={
                                                        "margin": "7px 0px 7x 0px",
                                                    }
                                                ),
                                                dbc.Row(
                                                    children=[
                                                        dbc.Col(
                                                            [
                                                                dbc.Label(
                                                                    "Access to Papilla",
                                                                    style={
                                                                        "font-size": "11px",
                                                                        "font-weight": "bold",
                                                                        "margin": "0px 0px 2px 0px",
                                                                    },
                                                                ),
                                                                dbc.Input(
                                                                    id="access-to-papilla",
                                                                    type="text",
                                                                    value="None",
                                                                    style={
                                                                        "font-size": "11px",
                                                                        "margin": "0px 0px 7px 0px",
                                                                        "width": "60%",
                                                                    },
                                                                ),
                                                            ]
                                                        ),
                                                        dbc.Col(
                                                            [
                                                                dbc.Label(
                                                                    "Opacification",
                                                                    style={
                                                                        "font-size": "11px",
                                                                        "font-weight": "bold",
                                                                        "margin": "0px 0px 2px 0px",
                                                                    },
                                                                ),
                                                                dbc.Input(
                                                                    id="opacification",
                                                                    type="text",
                                                                    value="None",
                                                                    style={
                                                                        "font-size": "11px",
                                                                        "margin": "0px 0px 7px 0px",
                                                                        "width": "60%",
                                                                    },
                                                                ),
                                                            ]
                                                        ),
                                                        dbc.Col(
                                                            [
                                                                dbc.Label(
                                                                    "Cannulation",
                                                                    style={
                                                                        "font-size": "11px",
                                                                        "font-weight": "bold",
                                                                        "margin": "0px 0px 2px 0px",
                                                                    },
                                                                ),
                                                                dbc.Input(
                                                                    id="cannulation",
                                                                    type="text",
                                                                    value="None",
                                                                    style={
                                                                        "font-size": "11px",
                                                                        "margin": "0px 0px 7px 0px",
                                                                        "width": "60%",
                                                                    },
                                                                ),
                                                            ]
                                                        ),
                                                    ]
                                                ),
                                                html.Hr(
                                                    style={
                                                        "margin": "7px 0px 7px 0px",
                                                    }
                                                ),
                                                dbc.Row(
                                                    children=[
                                                        dbc.Col(
                                                            children=[
                                                                dbc.Row(
                                                                    [
                                                                        dbc.Label(
                                                                            "Precut",
                                                                            style={
                                                                                "font-size": "11px",
                                                                                "font-weight": "bold",
                                                                                "margin": "0px 0px 2px 0px",
                                                                            },
                                                                        ),
                                                                        dbc.Input(
                                                                            id="precut",
                                                                            type="text",
                                                                            value="No",
                                                                            style={
                                                                                "font-size": "11px",
                                                                                "margin": "0px 0px 7px 9px",
                                                                                "width": "60%",
                                                                                "height": "25%",
                                                                            },
                                                                        ),
                                                                    ]
                                                                ),
                                                                dbc.Row(
                                                                    [
                                                                        dbc.Label(
                                                                            "Stenting",
                                                                            style={
                                                                                "font-size": "11px",
                                                                                "font-weight": "bold",
                                                                                "margin": "0px 0px 2px 0px",
                                                                            },
                                                                        ),
                                                                        dbc.Input(
                                                                            id="stenting",
                                                                            type="text",
                                                                            value="No",
                                                                            style={
                                                                                "font-size": "11px",
                                                                                "margin": "0px 0px 7px 9px",
                                                                                "width": "60%",
                                                                                "height": "25%",
                                                                            },
                                                                        ),
                                                                    ]
                                                                ),
                                                                dbc.Row(
                                                                    [
                                                                        dbc.Label(
                                                                            "Sphincterotomy",
                                                                            style={
                                                                                "font-size": "11px",
                                                                                "font-weight": "bold",
                                                                                "margin": "0px 0px 2px 0px",
                                                                            },
                                                                        ),
                                                                        dbc.Input(
                                                                            id="sphincterotomy",
                                                                            type="text",
                                                                            value="No",
                                                                            style={
                                                                                "font-size": "11px",
                                                                                "margin": "0px 0px 7px 9px",
                                                                                "width": "60%",
                                                                                "height": "25%",
                                                                            },
                                                                        ),
                                                                    ]
                                                                ),
                                                            ]
                                                        ),
                                                        dbc.Col(
                                                            children=[
                                                                dbc.Row(
                                                                    [
                                                                        dbc.Label(
                                                                            "Spy Glass",
                                                                            style={
                                                                                "font-size": "11px",
                                                                                "font-weight": "bold",
                                                                                "margin": "0px 0px 2px 0px",
                                                                            },
                                                                        ),
                                                                        dbc.Input(
                                                                            id="spy-glass",
                                                                            type="text",
                                                                            value="No",
                                                                            style={
                                                                                "font-size": "11px",
                                                                                "margin": "0px 0px 7px 9px",
                                                                                "width": "60%",
                                                                                "height": "25%",
                                                                            },
                                                                        ),
                                                                    ]
                                                                ),
                                                                dbc.Row(
                                                                    [
                                                                        dbc.Label(
                                                                            "Stone Removal",
                                                                            style={
                                                                                "font-size": "11px",
                                                                                "font-weight": "bold",
                                                                                "margin": "0px 0px 2px 0px",
                                                                            },
                                                                        ),
                                                                        dbc.Input(
                                                                            id="stone-removal",
                                                                            type="text",
                                                                            value="None",
                                                                            style={
                                                                                "font-size": "11px",
                                                                                "margin": "0px 0px 7px 9px",
                                                                                "width": "60%",
                                                                                "height": "25%",
                                                                            },
                                                                        ),
                                                                    ]
                                                                ),
                                                                dbc.Row(
                                                                    [
                                                                        dbc.Label(
                                                                            "Size & Type",
                                                                            style={
                                                                                "font-size": "11px",
                                                                                "font-weight": "bold",
                                                                                "margin": "0px 0px 2px 0px",
                                                                            },
                                                                        ),
                                                                        dbc.Input(
                                                                            id="size-type",
                                                                            type="text",
                                                                            value="No",
                                                                            style={
                                                                                "font-size": "11px",
                                                                                "margin": "0px 0px 7px 9px",
                                                                                "width": "60%",
                                                                                "height": "25%",
                                                                            },
                                                                        ),
                                                                    ]
                                                                ),
                                                            ]
                                                        ),
                                                        dbc.Col(
                                                            children=[
                                                                dbc.Row(
                                                                    [
                                                                        dbc.Label(
                                                                            "Sphincteroplasty",
                                                                            style={
                                                                                "font-size": "11px",
                                                                                "font-weight": "bold",
                                                                                "margin": "0px 0px 2px 0px",
                                                                            },
                                                                        ),
                                                                        dbc.Input(
                                                                            id="sphincteroplasty",
                                                                            type="text",
                                                                            value="No",
                                                                            style={
                                                                                "font-size": "11px",
                                                                                "margin": "0px 0px 7px 9px",
                                                                                "width": "60%",
                                                                                "height": "25%",
                                                                            },
                                                                        ),
                                                                    ]
                                                                ),
                                                                dbc.Row(
                                                                    [
                                                                        dbc.Label(
                                                                            "EHL",
                                                                            style={
                                                                                "font-size": "11px",
                                                                                "font-weight": "bold",
                                                                                "margin": "0px 0px 2px 0px",
                                                                            },
                                                                        ),
                                                                        dbc.Input(
                                                                            id="ehl",
                                                                            type="text",
                                                                            value="No",
                                                                            style={
                                                                                "font-size": "11px",
                                                                                "margin": "0px 0px 7px 9px",
                                                                                "width": "60%",
                                                                                "height": "25%",
                                                                            },
                                                                        ),
                                                                    ]
                                                                ),
                                                            ]
                                                        ),
                                                    ]
                                                ),
                                                html.Hr(
                                                    style={
                                                        "margin": "7px 0px 7px 0px",
                                                    }
                                                ),
                                                dbc.Row(
                                                    [
                                                        dbc.Label(
                                                            "Conclusion",
                                                            style={
                                                                "font-size": "11px",
                                                                "font-weight": "bold",
                                                                "margin": "0px 0px 2px 0px",
                                                            },
                                                        ),
                                                        dbc.Textarea(
                                                            id="conclusion",
                                                            value="No",
                                                            style={
                                                                "font-size": "11px",
                                                                "margin": "0px 0px 3px 9px",
                                                                "width": "90%",
                                                                "height": "auto",
                                                                "resize": "both",
                                                                "overflow": "hidden",
                                                            },
                                                        ),
                                                        # dbc.Col(
                                                        #     dbc.Textarea(
                                                        #         id="conclusion",
                                                        #         value="No",
                                                        #         style={
                                                        #             "font-size": "11px",
                                                        #             "margin": "0px 0px 2px 5px",
                                                        #             "width": "90%",
                                                        #             "height": "auto",
                                                        #             "resize": "both",
                                                        #             "overflow": "hidden",
                                                        #         },
                                                        #     ),
                                                        #     width=11,
                                                        # ),
                                                        # dbc.Col(
                                                        #     dbc.Button(
                                                        #         html.I(
                                                        #             className="bi bi-mic"
                                                        #         ),  # Bootstrap Icon for Microphone
                                                        #         id="microphone-button",
                                                        #         color="primary",
                                                        #         outline=True,
                                                        #         style={
                                                        #             "padding": "2px 5px",
                                                        #             "font-size": "12px",
                                                        #             "margin-left": "-4px",
                                                        #         },
                                                        #     ),
                                                        #     width="auto",
                                                        # ),
                                                    ]
                                                ),
                                            ]
                                        ),
                                        dbc.Button(
                                            "Generate Report",
                                            id="populate-form-btn",
                                            n_clicks=0,
                                            className="btn-dark",
                                            style={
                                                "background-color": "#90D2E5",
                                                "color": "white",
                                                "font-size": "12px",
                                                "font-weight": "500",
                                                # top right bottom left
                                                "padding": "7px 20px 5px",
                                                "margin": "3px 0px 0px 450px",
                                                "border-radius": "25px",
                                                "border": "none",
                                                "box-shadow": "0px 4px 10px rgba(0, 0, 0, 0.1)",
                                                "transition": "all 0.3s ease",
                                            },
                                        ),
                                    ]
                                ),
                                style={
                                    "backgroundColor": "#f0f0f0",
                                    "borderRadius": "5px",
                                    "padding": "5px",
                                    "minHeight": "70vh",
                                },
                            ),
                        ],
                    ),
                ],
                style={
                    "borderRadius": "5px",
                    "backgroundColor": "#f8f9fa",
                    "minHeight": "7px",
                },
            ),
            html.Div(id="tabs-content", style={"marginTop": "20px"}),
        ],
        style={"height": "790px", "overflow": "auto"},
    )
)

app.layout = dbc.Container(
    [
        dcc.Store(id="json-data-store"),
        html.Div(
            "Doctor's Audio Report Generation Tool",
            style=navbar_custom_css,
            className="mb-2 text-white",
        ),
        dbc.Row([dbc.Col(card_1, width=3), dbc.Col(card_2, width=9)]),
    ],
    fluid=True,
    style={"backgroundColor": "#f0f0f0", "minHeight": "100vh"},
)


# ---------------------------------------------------------------- client side call-backs -----------------------------------------------------------------

app.clientside_callback(
    """
    function(n_clicks) {
        if (n_clicks > 0) {
            startRecording(); // Start recording
            document.getElementById("record-status").innerText = "Recording in progress..."; // Update the status
        }
        return null; // Return null to avoid modifying `n_clicks`
    }
    """,
    Output("record-start", "n_clicks"),
    Input("record-start", "n_clicks"),
)

app.clientside_callback(
    """
    function(n_clicks) {
        if (n_clicks > 0) {
            stopRecording(); // Stop recording
            document.getElementById("record-status").innerText = "Recording stopped"; // Update the status
        }
        return null; // Return null to avoid modifying `n_clicks`
    }
    """,
    Output("record-stop", "n_clicks"),
    Input("record-stop", "n_clicks"),
)


def get_latest_file_from_folder(folder_path):

    files = [
        f
        for f in os.listdir(folder_path)
        if os.path.isfile(os.path.join(folder_path, f))
    ]
    if not files:
        return None
    latest_file = max(
        files, key=lambda f: os.path.getmtime(os.path.join(folder_path, f))
    )
    return latest_file


@app.callback(
    Output("audio-source", "children"),
    Output("audio-source", "data"),
    Input("record-start", "n_clicks"),
    Input("uploader", "isCompleted"),
    State("uploader", "fileNames"),
    prevent_initial_call=True,
)
def set_audio_source(n_record_clicks, is_completed, file_names):
    ctx = dash.callback_context
    if not ctx.triggered:
        return dash.no_update

    button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if button_id == "record-start":
        return "Audio Source: recorded", ("recorded", None)

    elif is_completed and file_names:
        return f"Audio Source: uploaded, File: {file_names[0]}", (
            "uploaded",
            file_names[0],
        )

    return dash.no_update


# -------------------------------------------------- server side callbacks -----------------------------------------------------------------------
def get_latest_subfolder(directory):
    subfolders = [f.path for f in os.scandir(directory) if f.is_dir()]
    if not subfolders:
        return None
    latest_folder = max(subfolders, key=os.path.getmtime)
    return latest_folder


def convert_to_mp3(input_audio_path, output_audio_path):

    audio = AudioSegment.from_file(input_audio_path)
    audio.export(output_audio_path, format="mp3")
    print(f"Converted audio saved as: {output_audio_path}")


@app.callback(
    Output("upload-status", "children"),
    Output("audio-player", "src"),
    State("uploader", "fileNames"),
    Input("uploader", "isCompleted"),
)
def handle_upload(file_names, is_completed):
    print("Upload file slected")
    print(is_completed)
    print(file_names)

    if is_completed and file_names:
        file_name = file_names[0]
        latest_folder = get_latest_subfolder("uploads")
        if latest_folder:
            file_path = os.path.join(latest_folder, file_name)
            print(f"Audio file path: {file_path}")
            if os.path.exists(file_path):
                file_extension = os.path.splitext(file_path)[1].lower()

                if file_extension != ".mp3":
                    mp3_output_path = os.path.join(
                        latest_folder, os.path.splitext(file_name)[0] + ".mp3"
                    )
                    convert_to_mp3(file_path, mp3_output_path)
                    file_path = mp3_output_path
                    print(f"Audio file path passes to audio player: {file_path}")
            if os.path.exists(file_path):
                with open(file_path, "rb") as f:
                    audio_src = f"data:audio/{file_path.split('.')[-1]};base64,{base64.b64encode(f.read()).decode()}"
                return f"File uploaded successfully: {file_name}", audio_src
        return f"Error: File {file_name} not found in the uploads directory.", ""
    return (
        "",
        "",
    )


@app.callback(
    Output("transcription-output", "children"),
    [Input("transcribe-button", "n_clicks"), Input("magic-btn", "n_clicks")],
    State("audio-source", "data"),
    State("transcription-output", "children"),
)
def handle_transcription(transcribe_clicks, magic_clicks, audio_data, current_text):
    ctx = dash.callback_context

    if not ctx.triggered:
        return current_text

    button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if button_id == "transcribe-button":
        if not audio_data:
            return "Click the Transcribe button to transcribe the uploaded audio."

        audio_source, file_name = audio_data

        if audio_source == "recorded" and transcribe_clicks:
            latest_recorded_file = get_latest_file_from_folder(folder_path=r"uploads")
            if latest_recorded_file:
                file_path = os.path.join(r"uploads", latest_recorded_file)
                if os.path.exists(file_path):
                    return audio_to_text_with_openai(file_path)
                # NOTE: need to write down the text transcription for the recording process as well
            return "Error: Unable to locate the recorded file for transcription."

        elif audio_source == "uploaded" and transcribe_clicks and file_name:
            latest_folder = get_latest_subfolder("uploads")
            if latest_folder:
                file_path = os.path.join(latest_folder, file_name)
                if os.path.exists(file_path):
                    transcription = audio_to_text_with_openai(file_path)
                    transcript_path = os.path.join(
                        r"output_files\text_outputs\transcriptions",
                        "transcript.txt",
                    )
                    with open(transcript_path, "w") as f:
                        f.write(transcription)
                    return transcription
            return "Error: Unable to locate the uploaded file for transcription."

    elif button_id == "magic-btn":
        if magic_clicks and current_text:
            corrected_transcription = correct_ercp_transcription(current_text)

            # Save corrected transcription to a file
            corrected_transcript_path = os.path.join(
                r"output_files\text_outputs\transcriptions",
                "corrected_transcript.txt",
            )
            with open(corrected_transcript_path, "w") as f:
                f.write(corrected_transcription)

            return corrected_transcription

        return "No transcription available to improve."

    return current_text


# @app.callback(
#     Output("transcription-output", "children"),
#     Input("transcribe-button", "n_clicks"),
#     State("audio-source", "data"),
# )
# def transcribe_audio(n_clicks, audio_data):
#     # print("hello")
#     # print("Audio Data:", audio_data)
#     if not audio_data:
#         return "Click the Transcribe button to transcribe the uploaded audio."

#     audio_source, file_name = audio_data
#     if audio_source == "recorded":
#         if n_clicks > 0:
#             latest_recorded_file = get_latest_file_from_folder(folder_path=r"uploads")
#             print("Latest Recorded File:", latest_recorded_file)

#             if latest_recorded_file:
#                 file_path = os.path.join(r"uploads", latest_recorded_file)
#                 if os.path.exists(file_path):
#                     transcription = audio_to_text_with_openai(file_path)
#                     return transcription
#             return "Error: Unable to locate the recorded file for transcription."
#         return "Click the Transcribe button to transcribe the recorded audio."

#     elif audio_source == "uploaded":
#         if n_clicks > 0 and file_name:
#             latest_folder = get_latest_subfolder("uploads")
#             print("Latest Folder:", latest_folder)

#             if latest_folder:
#                 file_path = os.path.join(latest_folder, file_name)
#                 if os.path.exists(file_path):
#                     transcription = audio_to_text_with_openai(file_path)
#                     transcript_path = os.path.join(
#                         r"output_files\text_outputs\transcriptions",
#                         "transcript.txt",
#                     )
#                     with open(transcript_path, "w") as f:
#                         f.write(transcription)
#                     return transcription
#             return "Error: Unable to locate the uploaded file for transcription."
#         return "Click the Transcribe button to transcribe the uploaded audio."


# # @app.callback(
# #     Output("transcription-output", "children"),
# #     Input("magic-btn", "n_clicks"),
# #     State("transcription-output", "children"),
# # )
# # def update_transcription(n_clicks, current_text):
# #     if n_clicks is None or n_clicks == 0:
# #         return current_text
# #     if current_text:
# #         return correct_ercp_transcription(current_text)
# #     return "No transcription available to improve."


@app.callback(
    [
        Output("abdominal-pain", "value"),
        Output("juandice", "value"),
        Output("bile-duct-stone", "value"),
        Output("periampullary-tumor", "value"),
        Output("pancreatic-biliary-tumor", "value"),
        Output("previous-surgery", "value"),
        Output("cholecystectomy", "value"),
        Output("a-phosphatese", "value"),
        Output("bilirubin", "value"),
        Output("abnormal-imaging", "value"),
        Output("other", "value"),
        Output("access-to-papilla", "value"),
        Output("opacification", "value"),
        Output("cannulation", "value"),
        Output("precut", "value"),
        Output("stenting", "value"),
        Output("sphincterotomy", "value"),
        Output("spy-glass", "value"),
        Output("stone-removal", "value"),
        Output("size-type", "value"),
        Output("sphincteroplasty", "value"),
        Output("ehl", "value"),
        Output("conclusion", "value"),
    ],
    Input("populate-form-btn", "n_clicks"),
    State("transcription-output", "children"),
    State("additional-comments", "value"),
)
def generate_uploaded_audio_report(n_clicks, transcription, additional_comments):
    default_values = [""] * 23
    if not n_clicks:
        return no_update
    if n_clicks > 0:
        if (
            not transcription
            or transcription
            == "Click the Transcribe button to transcribe the uploaded audio."
        ):
            return (
                "Error: No transcription available. Please transcribe the audio first."
            )
        if not additional_comments:
            additional_comments = "No additional comments provided."
        try:
            report = generate_report_with_ai(transcription, additional_comments)
            print(report)
            return [
                getattr(report, "abdominal_pain", ""),
                getattr(report, "juandice", ""),
                getattr(report, "bile_duct_stone", ""),
                getattr(report, "periampullary_tumor", ""),
                getattr(report, "pancreatic_billary_tumor", ""),
                getattr(report, "previous_surgery", ""),
                getattr(report, "cholecystectomy", ""),
                getattr(report, "a_phosphatase", ""),
                getattr(report, "bilirubin", ""),
                getattr(report, "abnormal_imaging", ""),
                getattr(report, "other", ""),
                getattr(report, "access_to_papilla", ""),
                getattr(report, "opacification", ""),
                getattr(report, "cannulation", ""),
                getattr(report, "precut", ""),
                getattr(report, "stenting", ""),
                getattr(report, "sphincterotomy", ""),
                getattr(report, "spy_glass", ""),
                getattr(report, "stone_removal", ""),
                getattr(report, "size_and_type", ""),
                getattr(report, "sphincteroplasty", ""),
                getattr(report, "ehl", ""),
                getattr(report, "conclusion", ""),
            ]

        except Exception as e:
            print(f"Error: {e}")
            return default_values


if __name__ == "__main__":
    app.run_server()
