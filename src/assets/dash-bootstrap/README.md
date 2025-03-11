# Dash Bootstrap Components

* The primary external layout and it's documentation can be found here (`https://dash-bootstrap-components.opensource.faculty.ai`) and was downloaded on 19 January 2025 with dash-bootstrap-components v.1.5.0.
* However, pSNV Hunter does not render properly offline
* Therefore, to solve this problem, the dbc css was downloaded from https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css and replaced within the code
  * Previous version that does not work offline:
    * ```
      app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP], title="pSNV Hunter")

      ```
  * Version that does now work offline:
    * ```
      app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=["./assets/dash-bootstrap/bootstrap.min.css"], title="pSNV Hunter")
      ```
