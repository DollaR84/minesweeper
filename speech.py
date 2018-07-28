"""
The speak module.

Created on 26.11.2016

@author: Ruslan Dolovanyuk

"""

import ctypes

import win32com.client


class Speech:
    """The speak class for speak voice."""

    def __init__(self, config):
        """Initialize speech class."""
        self.config = config

        self.speaker = win32com.client.Dispatch("Sapi.SpVoice")
        self.voices = self.speaker.GetVoices()
        self.voices_ids = [voice.Id for voice in self.voices]
        self.voices_names = [voice.GetDescription() for voice in self.voices]

        self.set_voice(self.config.getint('speech', 'voice'))
        self.speaker.Rate = self.config.getint('speech', 'rate')
        self.speaker.Volume = self.config.getint('speech', 'volume')

        self.nvda = self.config.getboolean('speech', 'nvda')
        self.nvda_error = False
        self.sLib = ctypes.windll.LoadLibrary('./nvdaControllerClient32.dll')
        nvda_error = self.sLib.nvdaController_testIfRunning()
        errorMessage = str(ctypes.WinError(nvda_error))
        if 0 != nvda_error:
            print('NVDA error: ' + errorMessage)
            self.nvda_error = True

        self.set_speak_out()

    def set_voice(self, index):
        """Set voice for speak."""
        try:
            self.speaker.Voice = self.voices[index]
            self.speak_sapi(self.voices_names[index])
        except:
            print('error: do not set voice')

    def set_speak_out(self):
        """Set speak out: nvda or sapi."""
        if self.nvda and not self.nvda_error:
            self.speak = self.speak_nvda
        else:
            self.speak = self.speak_sapi

    def speak_nvda(self, phrase):
        """Speak phrase in nvda screen reader."""
        self.sLib.nvdaController_speakText(phrase)

    def speak_sapi(self, phrase):
        """Speak phrase in sapi voice."""
        self.speaker.Speak(phrase)
