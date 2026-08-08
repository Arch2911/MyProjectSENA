# LOGIN
def test_login_cliente_existente_json_valido(cliente, peticiones):

    from unittest.mock import patch
    from app.services.constants import OTP_ENVIADO

    # ARRANGE
    data = {'cedula': cliente.cedula}

    with patch('app.routes.auth.routes.buscar_cliente') as mock_buscar:

        mock_buscar.return_value = OTP_ENVIADO

        # ACT
        response = peticiones.post('/auth/login', json=data)

    mock_buscar.assert_called_once_with(cliente.cedula)

    # ASSERT
    assert response.status_code == 200 # pertenece a la respuesta HTTP.

    body = response.get_json() # pertenece al contenido del JSON que se definio en endpoint con jsonify()

    assert body['status'] == 'success'


def test_login_sin_json(peticiones):

    # ARRANGE
    data = {}

    # ACT
    response = peticiones.post('/auth/login', json=data)

    assert response.status_code == 400

    body = response.get_json()

    assert body['error'] == 'json_requerido'

def test_login_cedula_no_enviada(peticiones):

    # ARRANGE
    data = {'cedula': ''}

    # ACT
    response = peticiones.post('/auth/login', json=data)

    # ASSERT
    assert response.status_code == 400

    body = response.get_json()

    assert body['error'] == 'cedula_requerida'

def test_login_cliente_inexistente(peticiones):

    # ARRANGE
    data = {'cedula': '124'}

    # ACT
    response = peticiones.post('/auth/login', json=data)

    # ASSERT
    assert response.status_code == 404

    body = response.get_json()

    assert body['error'] == 'cliente_no_existe'

def test_login_error_interno(cliente, peticiones):

    from unittest.mock import patch

    # ARRANGE
    data = {'cedula': cliente.cedula}

    with patch('app.routes.auth.routes.buscar_cliente') as mock_buscar:

        mock_buscar.return_value = None

        # ACT
        response = peticiones.post('/auth/login', json=data)

    # ASSERT
    mock_buscar.assert_called_once_with(cliente.cedula)
    assert response.status_code == 500

#VERIFY

def test_verify_valido(peticiones_autenticadas):

    from unittest.mock import patch
    from app.services.constants import CODIGO_VALIDO

    # ARRANGE
    cedula = 123
    data = {'codigo': 122457}

    with patch('app.routes.auth.routes.verificacion_cliente_otp') as mock_verificar:

        mock_verificar.return_value = CODIGO_VALIDO

        # ACT
        response = peticiones_autenticadas.post('/auth/verify', json=data)

    # ASSERT
    mock_verificar.assert_called_once_with(cedula, 122457)

    assert response.status_code == 200

    body = response.get_json()

    assert body['status'] == 'success'

def test_verify_sin_json(peticiones):

    # ARRANGE
    data = {}

    # ACT
    response = peticiones.post('/auth/verify', json=data)

    # ASSERT
    assert response.status_code == 400

    body = response.get_json()

    assert body['error'] == 'json_requerido'


def test_verify_session_invalida(peticiones):

    # ARRANGE
    data = {'codigo': 123456}


    # ACT
    response = peticiones.post('/auth/verify', json=data)

    # ASSERT
    assert response.status_code == 401

    body = response.get_json()

    assert body['error'] == 'sesion_invalida'

def test_verify_codigo_no_enviado(peticiones_autenticadas):

    # ARRANGE
    data = {'codigo': ''}

    # ACT
    response = peticiones_autenticadas.post('/auth/verify', json=data)

    # ASSERT
    assert response.status_code == 400

    body = response.get_json()

    assert body['error'] == 'codigo_requerido'

def test_verify_cliente_inexistente(peticiones):

    from unittest.mock import patch
    from app.services.constants import CLIENTE_NO_EXISTE

    # ARRANGE
    cedula_no_existente = 124
    data = {'codigo': 123456}

    with peticiones.session_transaction() as session:

        session['cedula_temporal'] = cedula_no_existente

    with patch('app.routes.auth.routes.verificacion_cliente_otp') as mock_verificar:

        mock_verificar.return_value = CLIENTE_NO_EXISTE

        # ACT
        response = peticiones.post('/auth/verify', json=data)

    # ASSERT
    mock_verificar.assert_called_once_with(cedula_no_existente, 123456)

    assert response.status_code == 404

    body = response.get_json()

    assert body['error'] == 'cliente_no_existe'

def test_verify_codigo_invalido(cliente, peticiones_autenticadas):

    from unittest.mock import patch
    from app.services.constants import CODIGO_INVALIDO

    # ARRANGE
    data = {'codigo': 123456}

    with patch('app.routes.auth.routes.verificacion_cliente_otp') as mock_verificar:

        mock_verificar.return_value = CODIGO_INVALIDO

        # ACT
        response = peticiones_autenticadas.post('/auth/verify', json=data)

    # ASSERT
    mock_verificar.assert_called_once_with(cliente.cedula, 123456)

    assert response.status_code == 401

    body = response.get_json()

    assert body['error'] == 'codigo_invalido'

def test_verify_codigo_expirado(cliente, peticiones_autenticadas):

    from unittest.mock import patch
    from app.services.constants import CODIGO_EXPIRADO

    # ARRANGE
    data = {'codigo': 123456}

    with patch('app.routes.auth.routes.verificacion_cliente_otp') as mock_verificar:

        mock_verificar.return_value = CODIGO_EXPIRADO

        # ACT
        response = peticiones_autenticadas.post('/auth/verify', json=data)

    mock_verificar.assert_called_once_with(cliente.cedula, 123456)

    assert response.status_code == 410

    body = response.get_json()

    assert body['error'] == 'codigo_expirado'

def test_verify_error_interno(cliente,peticiones_autenticadas):

    from unittest.mock import patch

    # ARRANGE
    data = {'codigo': 123456}

    with patch('app.routes.auth.routes.verificacion_cliente_otp') as mock_verificar:

        mock_verificar.return_value = None

        # ACT
        response = peticiones_autenticadas.post('/auth/verify', json=data)

    mock_verificar.assert_called_once_with(cliente.cedula, 123456)

    assert response.status_code == 500

    body = response.get_json()

    assert body['error'] == 'error_interno'