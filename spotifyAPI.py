from urllib.parse import urlencode
import requests
import streamlit as st
from streamlit.components.v1 import html

import string
import random

_STKEY = 'ST_OAUTH'
_DEFAULT_SECKEY = 'oauth'

from spotipy.oauth2 import SpotifyOAuth
import webbrowser
from spotipy import Spotify

def authenticate_spotify_user(client_id, client_secret, redirect_uri, scope='playlist-modify-private'):
    """
    Autentica al usuario en Spotify y devuelve el objeto Spotify.

    Parameters:
    - client_id: str, ID de cliente de tu aplicación en Spotify.
    - client_secret: str, Secreto de cliente de tu aplicación en Spotify.
    - redirect_uri: str, URI de redirección configurado en la aplicación de Spotify.
    - scope: str, Alcance de permisos que necesitas. Por defecto, 'playlist-modify-private'.

    Returns:
    - spotipy.Spotify, Objeto Spotify autenticado.
    """
    auth_manager = SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope=scope
    )

    # Obtener el token de acceso o abrir la ventana del navegador para la autenticación.
    try:
        token_info = auth_manager.get_access_token()
    except:
        auth_url = auth_manager.get_authorize_url()
        webbrowser.open(auth_url)
        token_info = auth_manager.get_access_token()

    # Crear un objeto Spotify autenticado.
    spotify = Spotify(auth=token_info['access_token'])

    return spotify

# Uso de la función para autenticar al usuario
SPOTIFY_CLIENT_ID = st.secrets['SPOTIFY_CLIENT_ID']
SPOTIFY_CLIENT_SECRET = st.secrets['SPOTIFY_CLIENT_SECRET']
REDIRECT_URI = "http://localhost:8501/callback/"  # Asegúrate de que coincida con la configuración de tu aplicación en Spotify

spotify = authenticate_spotify_user(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, REDIRECT_URI)

@st.cache_resource(ttl=300)
def qparms_cache(key):
    return {}

def logout():
    if _STKEY in st.session_state:
        del st.session_state[_STKEY]

def string_num_generator(size):
    chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for _ in range(size))

def validate_config(config):
    required_config_options = [ 'authorization_endpoint',
                                'token_endpoint',
                                'redirect_uri',
                                'client_id',
                                'client_secret',
                                'scope' ]
    return all([k in config for k in required_config_options])

def open_page(url):
    open_script= """
        <script type="text/javascript">
            window.open('%s', '_blank').focus();
        </script>
    """ % (url)
    html(open_script)

def show_auth_link(config, label, but):
    state_parameter = string_num_generator(15)
    query_params = urlencode({'redirect_uri': config['redirect_uri'], 'client_id': config['client_id'], 'response_type': 'code', 'state': state_parameter, 'scope': config['scope']})
    request_url = f"{config['authorization_endpoint']}?{query_params}"
    if st.query_params():
        qpcache = qparms_cache(state_parameter)
        qpcache = st.query_params()
    but.button(label, on_click=open_page, args=(request_url,), type="primary")
    st.stop()

def st_oauth(config=None, label="Login via OAuth", but=None):
    if not config:
        config = _DEFAULT_SECKEY
    if isinstance(config, str):
        config = st.secrets[config]
    if _STKEY in st.session_state:
        token = st.session_state[_STKEY]
    if _STKEY not in st.session_state:
        if not validate_config(config):
            st.error("Invalid OAuth Configuration")
            st.stop()
        if 'code' not in st.query_params():
            show_auth_link(config, label, but)
        code = st.query_params()['code'][0]
        state = st.query_params()['state'][0]
        qpcache = qparms_cache(state)
        qparms = qpcache
        qpcache = {}
        st.query_params(**qparms)
        theaders = {
                        'Content-type': 'application/x-www-form-urlencoded;charset=utf-8'
                    }
        tdata = {
                    'grant_type': 'authorization_code',
                    'redirect_uri': config['redirect_uri'],
                    'client_id': config['client_id'],
                    'client_secret': config['client_secret'],
                    'scope': config['scope'],
                    'state': state,
                    'code': code,
                }
        try:
            ret = requests.post(config["token_endpoint"], headers=theaders, data=urlencode(tdata).encode("utf-8"))
            ret.raise_for_status()
        except requests.exceptions.RequestException as e:
            st.error(e)
            show_auth_link(config, label)
        token = ret.json()
        st.session_state[_STKEY] = token

    if _STKEY in st.session_state:
        st.button("Logout", on_click=logout, type="secondary")
