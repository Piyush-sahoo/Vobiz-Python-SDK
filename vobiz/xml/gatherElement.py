from vobiz import exceptions
from .VobizXMLElement import VobizXMLElement
from .xmlUtils import map_type
from .speakElement import SpeakElement
from .playElement import PlayElement


class GatherElement(VobizXMLElement):
    _name = 'Gather'
    _nestable = [
        'Speak',
        'Play'
    ]

    ALLOWED_METHODS = {'GET', 'POST'}
    ALLOWED_INPUT_TYPES = {'dtmf', 'speech', 'dtmf speech'}
    ALLOWED_SPEECH_MODELS = {
        'default',
        'command_and_search',
        'phone_call',
        'telephony',
    }
    ALLOWED_LANGUAGES = {
        'en-AU', 'en-CA', 'en-GB', 'en-IE', 'en-IN', 'en-PH', 'en-SG', 'en-US',
        'en-ZA', 'de-DE', 'es-ES', 'es-MX', 'es-US', 'fr-CA', 'fr-FR', 'it-IT',
        'ja-JP', 'ko-KR', 'nl-NL', 'pt-BR', 'pt-PT', 'ru-RU', 'zh (cmn-hans-cn)',
        'zh-HK', 'zh-TW (cmn-hans-tw)', 'yue-Hant-HK', 'af-ZA'
    }

    @property
    def action(self):
        return self.__action

    @action.setter
    def action(self, value):
        if value is None or str(value).strip() == '':
            raise exceptions.ValidationError('action is required for Gather')
        value = str(value)
        if not (value.startswith('http://') or value.startswith('https://')):
            raise exceptions.ValidationError('action must be a fully qualified URL')
        self.__action = value

    def set_action(self, value):
        self.action = value
        return self

    @property
    def method(self):
        return self.__method

    @method.setter
    def method(self, value):
        if value is None:
            self.__method = None
            return
        method = str(value).upper()
        if method not in self.ALLOWED_METHODS:
            raise exceptions.ValidationError('method must be GET or POST')
        self.__method = method

    def set_method(self, value):
        self.method = value
        return self

    @property
    def input_type(self):
        return self.__input_type

    @input_type.setter
    def input_type(self, value):
        if value is None:
            self.__input_type = None
            return
        input_type = ' '.join(str(value).strip().lower().split())
        if input_type not in self.ALLOWED_INPUT_TYPES:
            raise exceptions.ValidationError('inputType must be one of: dtmf, speech, dtmf speech')
        self.__input_type = input_type

    def set_input_type(self, value):
        self.input_type = value
        return self

    @property
    def execution_timeout(self):
        return self.__execution_timeout

    @execution_timeout.setter
    def execution_timeout(self, value):
        if value is None:
            self.__execution_timeout = None
            return
        timeout = int(value)
        if timeout < 5 or timeout > 60:
            raise exceptions.ValidationError('executionTimeout must be between 5 and 60')
        self.__execution_timeout = timeout

    def set_execution_timeout(self, value):
        self.execution_timeout = value
        return self

    @staticmethod
    def _normalize_auto_or_range(value, field_name):
        if value is None:
            return None
        if isinstance(value, str) and value.strip().lower() == 'auto':
            return 'auto'
        ivalue = int(value)
        if ivalue < 2 or ivalue > 10:
            raise exceptions.ValidationError('{} must be between 2 and 10, or auto'.format(field_name))
        return ivalue

    @property
    def digit_end_timeout(self):
        return self.__digit_end_timeout

    @digit_end_timeout.setter
    def digit_end_timeout(self, value):
        self.__digit_end_timeout = self._normalize_auto_or_range(value, 'digitEndTimeout')

    def set_digit_end_timeout(self, value):
        self.digit_end_timeout = value
        return self

    @property
    def speech_end_timeout(self):
        return self.__speech_end_timeout

    @speech_end_timeout.setter
    def speech_end_timeout(self, value):
        self.__speech_end_timeout = self._normalize_auto_or_range(value, 'speechEndTimeout')

    def set_speech_end_timeout(self, value):
        self.speech_end_timeout = value
        return self

    @property
    def finish_on_key(self):
        return self.__finish_on_key

    @finish_on_key.setter
    def finish_on_key(self, value):
        if value is None:
            self.__finish_on_key = None
            return
        key = str(value)
        if key == '':
            self.__finish_on_key = ''
            return
        lowered = key.lower()
        if lowered == 'none':
            self.__finish_on_key = 'none'
            return
        if len(key) != 1 or key not in '0123456789*#':
            raise exceptions.ValidationError('finishOnKey must be one of 0-9, *, #, empty string, or none')
        self.__finish_on_key = key

    def set_finish_on_key(self, value):
        self.finish_on_key = value
        return self

    @property
    def num_digits(self):
        return self.__num_digits

    @num_digits.setter
    def num_digits(self, value):
        if value is None:
            self.__num_digits = None
            return
        digits = int(value)
        if digits < 1 or digits > 32:
            raise exceptions.ValidationError('numDigits must be between 1 and 32')
        self.__num_digits = digits

    def set_num_digits(self, value):
        self.num_digits = value
        return self

    @property
    def speech_model(self):
        return self.__speech_model

    @speech_model.setter
    def speech_model(self, value):
        if value is None:
            self.__speech_model = None
            return
        model = str(value).lower()
        if model not in self.ALLOWED_SPEECH_MODELS:
            raise exceptions.ValidationError('speechModel must be one of: default, command_and_search, phone_call, telephony')
        self.__speech_model = model

    def set_speech_model(self, value):
        self.speech_model = value
        return self

    @property
    def hints(self):
        return self.__hints

    @hints.setter
    def hints(self, value):
        if value is None:
            self.__hints = None
            return
        hint_text = str(value).strip()
        if not hint_text:
            raise exceptions.ValidationError('hints must be a non-empty comma-separated string')
        if len(hint_text) > 10000:
            raise exceptions.ValidationError('hints cannot exceed 10000 characters')
        self.__hints = hint_text

    def set_hints(self, value):
        self.hints = value
        return self

    @property
    def language(self):
        return self.__language

    @language.setter
    def language(self, value):
        if value is None:
            self.__language = None
            return
        language = str(value)
        if language not in self.ALLOWED_LANGUAGES:
            raise exceptions.ValidationError('language is not in supported Gather language list')
        self.__language = language

    def set_language(self, value):
        self.language = value
        return self

    @property
    def interim_speech_results_callback(self):
        return self.__interim_speech_results_callback

    @interim_speech_results_callback.setter
    def interim_speech_results_callback(self, value):
        if value is None:
            self.__interim_speech_results_callback = None
            return
        callback = str(value)
        if not (callback.startswith('http://') or callback.startswith('https://')):
            raise exceptions.ValidationError('interimSpeechResultsCallback must be a fully qualified URL')
        self.__interim_speech_results_callback = callback

    def set_interim_speech_results_callback(self, value):
        self.interim_speech_results_callback = value
        return self

    @property
    def interim_speech_results_callback_method(self):
        return self.__interim_speech_results_callback_method

    @interim_speech_results_callback_method.setter
    def interim_speech_results_callback_method(self, value):
        if value is None:
            self.__interim_speech_results_callback_method = None
            return
        method = str(value).upper()
        if method not in self.ALLOWED_METHODS:
            raise exceptions.ValidationError('interimSpeechResultsCallbackMethod must be GET or POST')
        self.__interim_speech_results_callback_method = method

    def set_interim_speech_results_callback_method(self, value):
        self.interim_speech_results_callback_method = value
        return self

    @property
    def log(self):
        return self.__log

    @log.setter
    def log(self, value):
        if value is None:
            self.__log = None
            return
        if not isinstance(value, bool):
            raise exceptions.ValidationError('log must be a boolean value')
        self.__log = value

    def set_log(self, value):
        self.log = value
        return self

    @property
    def redirect(self):
        return self.__redirect

    @redirect.setter
    def redirect(self, value):
        if value is None:
            self.__redirect = None
            return
        if not isinstance(value, bool):
            raise exceptions.ValidationError('redirect must be a boolean value')
        self.__redirect = value

    def set_redirect(self, value):
        self.redirect = value
        return self

    @property
    def profanity_filter(self):
        return self.__profanity_filter

    @profanity_filter.setter
    def profanity_filter(self, value):
        if value is None:
            self.__profanity_filter = None
            return
        if not isinstance(value, bool):
            raise exceptions.ValidationError('profanityFilter must be a boolean value')
        self.__profanity_filter = value

    def set_profanity_filter(self, value):
        self.profanity_filter = value
        return self

    def __init__(
            self,
            action,
            method=None,
            input_type=None,
            execution_timeout=None,
            digit_end_timeout=None,
            speech_end_timeout=None,
            finish_on_key=None,
            num_digits=None,
            speech_model=None,
            hints=None,
            language=None,
            interim_speech_results_callback=None,
            interim_speech_results_callback_method=None,
            log=None,
            redirect=None,
            profanity_filter=None,
    ):
        super(GatherElement, self).__init__()

        self.action = action
        self.method = method
        self.input_type = input_type
        self.execution_timeout = execution_timeout
        self.digit_end_timeout = digit_end_timeout
        self.speech_end_timeout = speech_end_timeout
        self.finish_on_key = finish_on_key
        self.num_digits = num_digits
        self.speech_model = speech_model
        self.hints = hints
        self.language = language
        self.interim_speech_results_callback = interim_speech_results_callback
        self.interim_speech_results_callback_method = interim_speech_results_callback_method
        self.log = log
        self.redirect = redirect
        self.profanity_filter = profanity_filter

    def to_dict(self):
        d = {
            'action': self.action,
            'method': self.method,
            'inputType': self.input_type,
            'executionTimeout': self.execution_timeout,
            'digitEndTimeout': self.digit_end_timeout,
            'speechEndTimeout': self.speech_end_timeout,
            'finishOnKey': self.finish_on_key,
            'numDigits': self.num_digits,
            'speechModel': self.speech_model,
            'hints': self.hints,
            'language': self.language,
            'interimSpeechResultsCallback': self.interim_speech_results_callback,
            'interimSpeechResultsCallbackMethod': self.interim_speech_results_callback_method,
            'log': self.log,
            'redirect': self.redirect,
            'profanityFilter': self.profanity_filter,
        }
        return {
            k: str(map_type(v))
            for k, v in d.items() if v is not None
        }

    def add_speak(
            self,
            content,
            voice=None,
            language=None,
            loop=None,
    ):
        self.add(
            SpeakElement(
                content=content,
                voice=voice,
                language=language,
                loop=loop,
            ))
        return self

    def add_play(
            self,
            content,
            loop=None,
    ):
        self.add(PlayElement(
            content=content,
            loop=loop,
        ))
        return self