'''Configuration of the routes, or vocabulary of the bot'''
from bottery.conf.patterns import Pattern, DefaultPattern
from bottery.views import ping
from views import help_text, consulta_conteiner, \
    two_tokens, works, consulta_lacre, say_help, report_api, \
    list_log, HookView


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

class HookableFuncPattern(Pattern):
    '''Receives a function to preprocess the incoming message
    text before comparing it to the pattern.
    Allows use of regular expressions, selecting partial words for
    routing, etc
    pre_process: a function to process message on check action before comparing
    with pattern
    context: string with history of messages
    conversation: HookPattern Object that will hook any next messages to this pattern
        (see ConversationPattern)'''
    def __init__(self, pattern, view, pre_process, \
                 hook_pattern=None, save_context=True):
        self.pre_process = pre_process
        self.context = ""
        self.conversation = hook_pattern
        self.save_context = save_context
        Pattern.__init__(self, pattern, view)

    def call_view(self, message):
        '''Local function to check return of view. 
        Just to treat errors if view returns only response'''
        tuple_return = self.view(message)
        if type(tuple_return) is tuple:
            response = tuple_return[0]
            hook = tuple_return[1]
        else:
            response = tuple_return
            hook = False
        return response, hook

    def check(self, message):
        ''' If a view wants to begin a conversation, it needs to return True
        Default is False.
        First we see if the context has to be set, then we run the view.
        While view returns True, the hook will remain'''
        # If hooked, go directly to view
        if (not self.conversation is None) and self.conversation.has_hook:
            if self.save_context:
                message.text = self.context + message.text
            response, hook = self.call_view(message)    
            if not hook:
                self.conversation.end_hook()
            return response
        # Else, begin normal check
        text, _ = self.pre_process(message.text)
        if text == self.pattern:
            response, hook = self.call_view(message)    
            if hook:
                self.context += text
                if (not self.conversation is None) and (not self.conversation.has_hook):
                    self.conversation.begin_hook(self)
            return response
        return False
 

class HookPattern(Pattern):
    '''FirstPattern to be checked. Allows a Pattern to "capture" and release
    the flow if it receives an incomplete messsage
    _pattern = a Pattern Object
    Usage:
    Put as first pattern
    On a view, call set_conversation(Pattern) to ensure the next message will go to this Pattern
    Also on a view, call end_conversation to release the hook'''
    def __init__(self):
        self._pattern = None
        Pattern.__init__(self, "", None)

    def check(self, message):
        if self._pattern is None:
            return False
        return self._pattern.check(message)

    def begin_hook(self, apattern):
        '''Pass the pattern that will begin a conversation'''
        self._pattern = apattern

    def end_hook(self):
        '''Releases pointer to Pattern ending a conversation'''
        self._pattern = None

    def has_hook(self):
        '''Return if hook is active'''
        return self._pattern is None


conversation = HookPattern()
patterns = [
    conversation,
    Pattern('ping', ping),
    Pattern('help', help_text),
    Pattern('log', list_log),
    FuncPattern('cc', consulta_conteiner, two_tokens),
    FuncPattern('ll', consulta_lacre, two_tokens),
    FuncPattern('report', report_api, two_tokens),
    Pattern('teste', works),
    DefaultPattern(say_help)
]
