from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy_garden.filebrowser import FileBrowser
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from time import sleep
Window.clearcolor = (0.2, 0.2, 0.2, 0)
class FileSelector(Widget):
    def __init__(self, **kwargs):
        global img
        super(FileSelector, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.file_browser = None
        self.select_button = Button(text="Select File",
                                    background_color = [1, 2, 3, 4],
                            font_size=35,
                            size_hint_y=None,
                            height=100,
                            size_hint_x=None,
                            width=1450)
        self.select_button.bind(on_press=self.show_file_browser)
        self.add_widget(self.select_button)

    def show_file_browser(self, instance):
        if not self.file_browser:
            self.file_browser = FileBrowser(select_string='Select')

        self.popup = Popup(title='File Browser', content=self.file_browser, size_hint=(0.9, 0.9))
        self.file_browser.bind(on_success=self._fbrowser_success, on_canceled=self._fbrowser_canceled)
        self.popup.open()
    def _fbrowser_success(self, instance):
        if instance.selection:
            print(f"Selected file: {instance.selection[0]}")
            fp=instance.selection
            fp1=str(fp)
            fp2=fp1[2:-2]
            print(fp2)
            import assemblyai as aai

            aai.settings.api_key = "your api key"

# URL of the file to transcribe (replace with your audio file URL)
            FILE_URL = fp2
# Transcribe the audio
            transcriber = aai.Transcriber()
            transcript = transcriber.transcribe(FILE_URL)

# Get the transcribed text
            transcribed_text = transcript.text

# Print the transcribed text
            print("Transcription- \n")
            print(transcribed_text)
            global n
            n=transcribed_text
            print("Summary- \n")

            audio_url = fp2

            config = aai.TranscriptionConfig(
                summarization=True,
                summary_model=aai.SummarizationModel.informative,
                summary_type=aai.SummarizationType.bullets
            )

            transcript = aai.Transcriber().transcribe(audio_url, config)
            global n1
            n1=transcript.summary
            print(n1)
            import assemblyai as aai

            aai.settings.api_key = "your api key"

          
            config = aai.TranscriptionConfig(
            summarization=True,
            summary_model=aai.SummarizationModel.catchy,
            summary_type=aai.SummarizationType.gist
            )

            transcript = aai.Transcriber().transcribe(FILE_URL, config)

            s=transcript.summary
            #print(s,"\n")

            print("Youtube:-\n")
            from youtubesearchpython import VideosSearch

            videosSearch = VideosSearch(s, limit = 2)

            from urlextract import URLExtract

            extractor = URLExtract()

# Extract the relevant text from the dictionary
            video_results = videosSearch.result()
            video_links = [result['link'] for result in video_results['result']]

# Join the descriptions into a single string
            video_text = '\n'.join(video_links)

# Now pass the string to the find_urls method
            global urls
            global url
            urls = extractor.find_urls(video_text)
            print(urls,"\n")
            import webbrowser
            for url in urls:
                try:
                    #webbrowser.open(url)
                    print(f"Successfully opened {url} in the web browser.")
                except Exception as e:
                    print(f"Failed to open {url} in the web browser: {e}")
            self.select_button.text=''
            self.popup.dismiss()
            Window.size = (1000, 1200)  # Set a default window size
            self.remove_widget(self.select_button)
            FitTextApp().run()
        FileSelector().run()
    def _fbrowser_canceled(self, instance):
        print("File selection canceled")
        self.popup.dismiss()
        FileSelectorApp().run()
class FitTextLabel(Label):
    def __init__(self, **kwargs):
        super(FitTextLabel, self).__init__(**kwargs)
        self.bind(size=self._update_font_size)
        Clock.schedule_once(self._update_font_size, 0)

    def _update_font_size(self, *args):
        self.text_size = (self.width, None)
        max_height = self.height
        font_size = self.font_size

        # Reduce font size until the text fits within the Label's height
        while self.texture_size[1] > max_height and font_size > 10:
            font_size -= 1
            self.font_size = font_size
class FitTextApp(App):
    def build(self):
        global layout
        layout = BoxLayout()
        global large_text
        u=str(urls)
        large_text = ("TRANSCRIPTION:- "+n+"\nSUMMARY: "+n1+"\nYoutube Links:- "+u)
        Window.remove_widget(img)
        global label
        label = FitTextLabel(text=large_text, font_size=20)
        layout.add_widget(label)
        layout.clear=Button(text="Clear",
                            background_color = [1, 2, 3, 4],
                            font_size=15,
                            size_hint_y=None,
                            height=100,
                            size_hint_x=None,
                            width=100)
        layout.clear.bind(on_press=self.press)
        layout.add_widget(layout.clear)
        layout.link=Button(text="Open Links",
                           background_color = [1, 2, 3, 4],
                            font_size=15,
                            size_hint_y=None,
                            height=100,
                            size_hint_x=None,
                            width=100)
        layout.link.bind(on_press=self.press1)
        layout.add_widget(layout.link)
        return layout
    def press(self,instance):
        layout.remove_widget(label)
        layout.remove_widget(layout.clear)
        layout.remove_widget(layout.link)
        FileSelectorApp().run()
    def press1(self,instance):
        import webbrowser
        webbrowser.open(urls[0])
        webbrowser.open(urls[1])
class FileSelectorApp(App):
    def build(self):
        return FileSelector()

if __name__ == '__main__':
    FileSelectorApp().run()
