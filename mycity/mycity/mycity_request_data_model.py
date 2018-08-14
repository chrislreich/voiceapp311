class MyCityRequestDataModel:
    """
    Represents a request from a voice platform.

    @todo: Consistent comment format that contains platform-specific terminology
    """

    def __init__(self):
        self._request_type = None
        self._request_id = None
        self._is_new_session = None
        self._session_id = None
        self._session_attributes = {}
        self._application_id = None
        self._intent_name = None
        self._intent_variables = {}
        self._api_variables = {}

    def __str__(self):
        return """\
        <MyCityRequestDataModel
            request_type={},
            request_id={},
            is_new_session={},
            session_id={},
            session_attributes={},
            application_id={},
            intent_name={},
            intent_variables={},
            api_variables={}
        >
        """.format(
            self._request_type,
            self._request_id,
            self._is_new_session,
            self._session_id,
            self._session_attributes,
            self._application_id,
            self._intent_name,
            self._intent_variables,
            self._api_variables
        )

    @property
    def request_type(self):
        """The type of this request."""
        return self._request_type

    @request_type.setter
    def request_type(self, value):
        self._request_type = value

    @property
    def request_id(self):
        """The unique identifier for this request."""
        return self._request_id

    @request_id.setter
    def request_id(self, value):
        self._request_id = value

    @property
    def is_new_session(self):
        """True if this is a new session, false otherwise.."""
        return self._is_new_session

    @is_new_session.setter
    def is_new_session(self, value):
        self._is_new_session = value

    @property
    def session_id(self):
        """Unique identifier for this session."""
        return self._session_id

    @session_id.setter
    def session_id(self, value):
        self._session_id = value

    @property
    def session_attributes(self):
        """An object containing key-value pairs of session information."""
        return self._session_attributes

    @session_attributes.setter
    def session_attributes(self, value):
        self._session_attributes = value

    @property
    def application_id(self):
        """Unique identifier for this application (a.k.a. skill id)."""
        return self._application_id

    @application_id.setter
    def application_id(self, value):
        self._application_id = value

    @property
    def intent_name(self):
        """The name of the intent being handled."""
        return self._intent_name

    @intent_name.setter
    def intent_name(self, value):
        self._intent_name = value

    @property
    def intent_variables(self):
        """
        An object containing key-value pairs representing the variables
        captured in the user's input.

        On the Alexa platform, these are called "slots".
        """
        return self._intent_variables

    @intent_variables.setter
    def intent_variables(self, value):
        self._intent_variables = value

    @property
    def api_variables(self):
        """
        Alexa API variables used primarily for progessive responses
        """
        return self._api_variables

    @api_variables.setter
    def api_variables(self, value):
        self._api_variables = value
