'''Configuration of the routes, or vocabulary of the bot'''
from bottery.conf.patterns import Pattern, DefaultPattern
from bottery.views import ping
from views import help_text, consulta_conteiner, \
    two_tokens, works, consulta_lacre, say_help, report_api


class FuncPattern(Pattern):
    '''Receives a function to preprocess the incoming message
    text before comparing it to the pattern.
    Allows use of regular expressions, selecting partial words for
    routing, etc'''
    def __init__(self, pattern, view, pre_process):
        self.pre_process = pre_process
        Pattern.__init__(self, pattern, view)

    def check(self, message):
        text, _ = self.pre_process(message.text)
        if text == self.pattern:
            return self.view
        return False


patterns = [
    Pattern('ping', ping),
    Pattern('help', help_text),
    FuncPattern('cc', consulta_conteiner, two_tokens),
    FuncPattern('ll', consulta_lacre, two_tokens),
    FuncPattern('report', report_api, two_tokens),
    Pattern('teste', works),
    DefaultPattern(say_help)
]
