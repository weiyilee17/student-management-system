from PyQt6.QtWidgets import QMessageBox


class AboutMessageBox(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('About')

        about_message = f"""Warning message TSMSendMessageToUIServer seems to be related to new M1 chips for the new \
MacBooks.

TSM AdjustCapsLockLEDForKeyTransitionHandling - _ISSetPhysicalKeyboardCapsLockLED Inhibit seems to be related \
to other languages that can be switched by Caps lock. 

Stackoverflow's suggestions says that the user should either remove the language or cancel the Caps lock \
switch language binding, which neither is a good solution. I would currently leave it as it is since it \
doesn't seem to harm, but would get back into it in the future if I make further PyQt6 applications and \
this warning is causing actual problems.
        """

        self.setText(about_message)
