import base64
import io

from apps.createjson import *
from layouts.layout_main import *

# Inicializa o app Dash
app = dash.Dash(__name__,
                suppress_callback_exceptions=True,
                external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1.0"}],)

app.title = "DWSIM Pump"

server = app.server

app.layout = layout_main()

@app.callback(Output('download-json', 'data'),
              Output('file-name-output', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              prevent_initial_call=True)
def update_dropdown(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        if 'xlsx' in filename:
            # Assume que é um arquivo Excel
            dataframe = pd.read_excel(io.BytesIO(decoded), sheet_name='Pump Data')
            createjson(dataframe, filename)
            file_dir = 'DWSIM Pump Curves/'
            partes = filename.rsplit('.', 1)
            nome_base = partes[0] if len(partes) > 1 else filename
            file_path = file_dir + nome_base + '.json'
            return dcc.send_file(file_path), filename
        else:
            return None, html.Div(['Unsupported file type.'])
    except Exception as e:
        return None, html.Div(['There was an error processing the file.'])


if __name__ == '__main__':
    app.run_server(host='127.0.0.1', port=8080, debug=False)


