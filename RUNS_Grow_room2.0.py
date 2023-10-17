from PyQt5.QtWidgets import QFrame,QLabel, QApplication,  QWidget, QDesktopWidget, QVBoxLayout, QPushButton, QFileDialog,QTextEdit, QScrollArea, QMainWindow
from PyQt5.QtCore import  QPropertyAnimation,QSequentialAnimationGroup,Qt, QTimer, QThread, pyqtSignal, QRect
from PyQt5.QtGui import QPainter, QColor
from TikTokLive import TikTokLiveClient
from TikTokLive.types.events import LikeEvent, CommentEvent, ConnectEvent, JoinEvent
from PyQt5.QtGui import QFontDatabase, QFont
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import Qt, QUrl
import math 
import random
import  sys
import queue
import vlc

leaderboard = {}  # username: points

    


class BrickCrumbleWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setGeometry(300, 300, 500, 500)

        self.brick_stack = []
        y_start = 50
        for _ in range(5):
            brick = QFrame(self)
            brick.setGeometry(159, y_start, 100, 50)
            brick.setStyleSheet("background-color: red;")
            self.brick_stack.append(brick)
            y_start += 25  # Increment y-coordinate for the next brick

        self.show()

    def makeCrumble(self):
        for brick in self.brick_stack:
            # Create top-left part of the brick
            tl = QFrame(self)
            tl.setGeometry(brick.x(), brick.y(), brick.width() // 2, brick.height() // 2)
            tl.setStyleSheet("background-color: red;")

            # Create top-right part of the brick
            tr = QFrame(self)
            tr.setGeometry(brick.x() + brick.width() // 2, brick.y(), brick.width() // 2, brick.height() // 2)
            tr.setStyleSheet("background-color: red;")

            # Create bottom-left part of the brick
            bl = QFrame(self)
            bl.setGeometry(brick.x(), brick.y() + brick.height() // 2, brick.width() // 2, brick.height() // 2)
            bl.setStyleSheet("background-color: red;")

            # Create bottom-right part of the brick
            br = QFrame(self)
            br.setGeometry(brick.x() + brick.width() // 2, brick.y() + brick.height() // 2, brick.width() // 2, brick.height() // 2)
            br.setStyleSheet("background-color: red;")
            animation = QPropertyAnimation(brick, b"geometry")
           
            # Hide the original brick
            brick.hide()

            # Create animations for each part
            animation_tl = QPropertyAnimation(tl, b"geometry")
            animation_tl.setDuration(1000)
            animation_tl.setEndValue(QRect(-50, -50, tl.width(), tl.height()))

            animation_tr = QPropertyAnimation(tr, b"geometry")
            animation_tr.setDuration(1000)
            animation_tr.setEndValue(QRect(600, -50, tr.width(), tr.height()))

            animation_bl = QPropertyAnimation(bl, b"geometry")
            animation_bl.setDuration(1000)
            animation_bl.setEndValue(QRect(-50, 600, bl.width(), bl.height()))

            animation_br = QPropertyAnimation(br, b"geometry")
            animation_br.setDuration(1000)
            animation_br.setEndValue(QRect(600, 600, br.width(), br.height()))

            # Start animations
            animation_tl.start()
            animation_tr.start()
            animation_bl.start()
            animation_br.start()
    # class BrickStackWidget(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.bricks = []  # List to store all bricks
#         self.initUI()

#     def initUI(self):
#         num_rows = 50  # Number of rows of bricks (height of the stack)
#         brick_width = 50#400*(1//num_rows)  # Width of a single brick
#         brick_height = 50  # Height of a single brick

#         for row in range(num_rows):
#             brick = QWidget(self)
#             brick.setStyleSheet("background-color: green;")
#             brick.setGeometry(50, row*brick_height, brick_width, brick_height)
#             self.bricks.append(brick)

#     def makeTransparent(self):
#         if self.bricks:
#             animation_group = QSequentialAnimationGroup()

#             for idx, brick in enumerate(self.bricks):
#                 animation = QPropertyAnimation(brick, b"geometry")
#                 animation.setDuration(1000)
#                 animation.setStartValue(brick.geometry())
#                 animation.setEndValue(QRect(brick.x(), brick.y() + 50, brick.width(), brick.height()))
#                 animation_group.addAnimation(animation)

#                 if idx % 5 == 0 and idx != 0:
#                     animation_group.addPause(500)  # Adding a 500ms pause after every 5 bricks

#             animation_group.start()  # Clear the list of brick
class ScrollingWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialize a queue and populate it with some text
        self.text_queue = queue.Queue()
        for i in range(20):
            self.text_queue.put(f"Dynamic Text {i+1}")

        # Create a borderless window
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setGeometry(100, 100, 300, 300)  # Set initial dimensions

        # Create a QWidget for the central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Create a QVBoxLayout
        layout = QVBoxLayout()

        # Create 5 QTextEdit widgets and add them to the layout
        self.text_fields = []
        for i in range(5):
            text_field = QTextEdit()
            self.text_fields.append(text_field)
            layout.addWidget(text_field)

        # Create a QScrollArea and set its properties
        scroll = QScrollArea()
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll.setWidgetResizable(True)
        scroll.setWidget(central_widget)
        scroll.setFixedHeight(300)

        # Set the QVBoxLayout to the central widget
        central_widget.setLayout(layout)

        # Add QScrollArea to QMainWindow
        self.setCentralWidget(scroll)

        # Create a QTimer object for auto-scrolling
        self.timer = QTimer()
        self.timer.timeout.connect(self.auto_scroll)
        self.timer.start(5000)  # 5-second interval
        self.current_stop = 0  # Initialize current stop

    def auto_scroll(self):
        # Dequeue text and update the QTextEdit fields
        for text_field in self.text_fields:
            if not self.text_queue.empty():
                new_text = self.text_queue.get()
                text_field.setPlainText(new_text)

        # Define the 5 stops in terms of vertical scroll position
        stops = [0, 60, 120, 180, 240]
        
        # Scroll to the next stop
        self.current_stop += 1
        if self.current_stop < len(stops):
            self.centralWidget().verticalScrollBar().setValue(stops[self.current_stop])
        else:
            # Reset to the first stop after the last stop is reached
            self.current_stop = -1
            self.centralWidget().verticalScrollBar().setValue(0)

class VideoWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Create a QWidget and set its properties
        self.setWindowTitle("Video Window")
        self.setGeometry(250, 750, 512, 512)

        # Create a QVBoxLayout
        layout = QVBoxLayout()

        # Create a VLC instance
        self.vlc_instance = vlc.Instance()

        # Create a VLC media player instance
        self.media_player = self.vlc_instance.media_player_new()

        # Create a new QPushButton and connect it to the play_pause method
        self.play_button = QPushButton("Play/Pause")
        self.play_button.clicked.connect(self.play_pause)
        layout.addWidget(self.play_button)

        # Set the layout
        self.setLayout(layout)

        # Set the media
        Media = self.vlc_instance.media_new(r'https://www.tiktok.com/@dr_ear_wax/video/7267335747143912750?_d=eafdjma4b2e7mi&_r=1&preview_pb=0&share_item_id=7267335747143912750&sharer_language=en&source=h5_m&u_code=eafdjma4b2e7mi')
        Media.get_mrl()

        # Set the media to the media player instance
        self.media_player.set_media(Media)

    def play_pause(self):
        """Toggle play/pause status
        """
        if self.media_player.is_playing():
            self.media_player.pause()
        else:
            self.media_player.play()
class TikTokClientThread(QThread):
    comment_received = pyqtSignal(CommentEvent)
    join_received = pyqtSignal(JoinEvent)
    def run(self):
        client = TikTokLiveClient(unique_id="@monicaelyse")
        
        @client.on("connect")
        async def on_connect(_: ConnectEvent):
            print("Connected to Room ID:", client.room_id)

        @client.on("comment")
        async def on_comment(event: CommentEvent):
            self.comment_received.emit(event)

        @client.on("like")
        async def on_like(event: LikeEvent):
            print(f"@{event.user.unique_id} liked the stream!")
            brick_crumble_widget.makeCrumble()  

        @client.on("join")
        async def on_join(event: JoinEvent):
            #print(f"@{event.user.unique_id} joined the stream!")
            self.join_received.emit(event)
        client.run()



from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPainter, QColor, QFont
import random

class MatrixRainWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.columns = 55  # Number of text columns
        self.speeds = [random.randint(7, 12)*random.uniform(1,2) for _ in range(self.columns)]  # Random speeds for each column
        self.chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"  # Characters to use
        self.positions = [0] * self.columns  # Y-positions of text in each column
        self.char_history = [[] for _ in range(self.columns)]  # History of characters for each column
        self.max_history = 200  # Maximum length of character history
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateRain)
        self.timer.start(30)

    def updateRain(self):
        for i in range(len(self.positions)):
            self.positions[i] += self.speeds[i]
            if self.positions[i] > self.height():
                self.positions[i] = 0
                self.char_history[i].clear()

            new_char = random.choice(self.chars)
            self.char_history[i].append(new_char)
            
            if len(self.char_history[i]) > self.max_history:
                self.char_history[i].pop(0)

        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QColor(0, 255, 0))  # Green color
        painter.setFont(QFont("Courier", 20, QFont.Bold))

        for i in range(self.columns):
            x = i * 20  # X-position for this column
            y = self.positions[i]  # Y-position for this column
            for idx, char in enumerate(reversed(self.char_history[i])):
                painter.drawText(x, int(y) - idx * 20, char)


class WordArtWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.text = ""
        self.text_opacity = 0
        self.text_size = 20  # initial text size

        # Add these lines to load the custom font
        #self.font_id = QFontDatabase.addApplicationFont(r"C:\Users\mikev\Downloads\TikTokLive\new\TikTokLive\led_dot_matrix\LED Dot-Matrix.ttf")
        #self.font_family = QFontDatabase.applicationFontFamilies(self.font_id)[0]
        #self.font = QFont(self.font_family)
        #self.font.setPixelSize(self.text_size)

        self.timer = QTimer()
        self.timer.timeout.connect(self.updateText)

    def triggerText(self, text):
        self.text = text
        self.text_size = 80  # reset to initial size
        self.text_opacity = 255  # reset to initial opacity
        self.timer.start(30)

    def updateText(self):
        if self.text_opacity <= 0:
            self.timer.stop()
            self.text = ""
        else:
            self.text_size += 4  # increase size
            self.text_opacity -= 5  # reduce opacity
        self.update()

    def paintEvent(self, event):
        super(WordArtWidget, self).paintEvent(event)
        if self.text:
            painter = QPainter(self)
            #painter.setFont(self.font)  # Set custom font here
            #painter.setRenderHint(QPainter.Antialiasing, True)
            #painter.setPen(QColor(0, 255, 255, self.text_opacity))
            #self.font.setPixelSize(self.text_size)  # Update the font size
            #painter.setFont(self.font)
            painter.drawText(self.rect(), Qt.AlignCenter, self.text)
            painter.setRenderHint(QPainter.Antialiasing, True)
            painter.setPen(QColor(0, 255, 32, self.text_opacity))
            font = painter.font()
            font.setPixelSize(self.text_size)
            painter.setFont(font)
            painter.drawText(self.rect(), Qt.AlignCenter, self.text)
class ScrollingBanner(QWidget):
    def __init__(self):
        super().__init__()
        self.text_pos = self.width()  # Start from the right edge of the widget

        # Load the custom font
        self.font_id = QFontDatabase.addApplicationFont(r"C:\Users\mikev\Downloads\TikTokLive\new\TikTokLive\led_dot_matrix\LED Dot-Matrix.ttf")
        self.font_family = QFontDatabase.applicationFontFamilies(self.font_id)[0]
        self.font = QFont(self.font_family)
        self.font.setPixelSize(80)

        self.timer = QTimer()
        self.timer.timeout.connect(self.updateBanner)
        self.timer.start(100)

    def updateBanner(self):
        self.text_pos -= 9
        if self.text_pos < -self.width():
            self.text_pos = self.width()
        self.update()

    def paintEvent(self, event):
        super(ScrollingBanner, self).paintEvent(event)
        painter = QPainter(self)

        painter.fillRect(self.rect(), QColor(0,0,0,128))

        painter.setFont(self.font)
        painter.setPen(QColor(255, 0, 0))  # Text color
        painter.drawText(self.text_pos, 90, "ChatGPT Coding, Games, ask questions!")
class StaticBanner(QWidget):
    def __init__(self):
        super().__init__()

        # Load the custom font
        self.font_id = QFontDatabase.addApplicationFont(r"C:\Users\mikev\Downloads\TikTokLive\new\TikTokLive\led_dot_matrix\LED Dot-Matrix.ttf")
        self.font_family = QFontDatabase.applicationFontFamilies(self.font_id)[0]
        self.font = QFont(self.font_family)
        self.font.setPixelSize(80)

        #self.encoded_phrase = "Your Encoded Phrase Here"
    def setPhrase(self, phrase):
        self.encoded_phrase = phrase
        self.update()
    def paintEvent(self, event):
        super(StaticBanner, self).paintEvent(event)
        painter = QPainter(self)

        painter.fillRect(self.rect(), QColor(0, 0, 0, 128))

        painter.setFont(self.font)
        painter.setPen(QColor(255, 255, 255))  # Text color
        painter.drawText(self.rect(), Qt.AlignCenter, self.encoded_phrase)

class SplashWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.splashes = []  # list to store all active splashes
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateSplash)
    
    def triggerSplash(self):
        new_splash = {
            'pos': self.rect().center(),
            'radius': 0,
            'opacity': 255
        }
        self.splashes.append(new_splash)
        self.timer.start(30)

    def updateSplash(self):
        to_remove = []
        for splash in self.splashes:
            splash['radius'] += 20
            splash['opacity'] -= 10
            if splash['opacity'] <= 0:
                to_remove.append(splash)
        
        for splash in to_remove:
            self.splashes.remove(splash)
        
        self.update()

    def paintEvent(self, event):
        super(SplashWidget, self).paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setPen(Qt.NoPen)
        
        for splash in self.splashes:
            painter.setBrush(QColor(0, 0, 0, splash['opacity']))
            painter.drawEllipse(splash['pos'], splash['radius'], splash['radius'])

def initialize_game():
    pass
if __name__ == '__main__':
    app = QApplication([])
    
    
    
        # Your code for phrase selection and encoding here
        
    global chosen_phrase, encoded_phrase  # Declare them as global
        

        # Define the QWERTY keyboard layout
    qwerty_keyboard = {
            'q': 'was',
            'w': 'qase',
            'e': 'wsdr',
            'r': 'edft',
            't': 'rfgy',
            'y': 'tghu',
            'u': 'yhji',
            'i': 'ujko',
            'o': 'iklp',
            'p': 'ol',
            'a': 'qwsz',
            's': 'awedxz',
            'd': 'wersfcx',
            'f': 'ertdgcv',
            'g': 'rtyfhvb',
            'h': 'tyugjbn',
            'j': 'yuihknm',
            'k': 'ujilo,m',
            'l': 'iopk.,',
            'z': 'asx',
            'x': 'zsdc',
            'c': 'xdfv',
            'v': 'cfgb',
            'b': 'vghn',
            'n': 'bhjm',
            'm': 'njk,',
            ',': 'mkl.',
            '.': ',l/'
        }

        # The array of phrases
    phrases = ["Russia", "Russia", "Palistine"]

        # Select a random phrase
    chosen_phrase = random.choice(phrases)
        # Encode the phrase
    encoded_phrase = ""
    for char in chosen_phrase:
        if char == ' ':
            encoded_phrase += ' '
            continue
        possible_chars = qwerty_keyboard.get(char, char)
        encoded_char = random.choice(possible_chars)
        encoded_phrase += encoded_char


    window = QWidget()
    window.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
    window.setAttribute(Qt.WA_TranslucentBackground)
    #window.resize(1080,1000)  # Set initial window size to 800x600

    screen_geometry = app.desktop().screenGeometry()
    #x = (screen_geometry.width() - window.frameGeometry().width()) / 2 + 100
    #y = (screen_geometry.height() - window.frameGeometry().height()) / 2

    #window.move(int(x), int(y))
    #screen_geometry = app.desktop().screenGeometry()
    window.setGeometry(screen_geometry)
    window.show()
    
    # Create and show the static banner
    static_banner = StaticBanner()
    static_banner.setParent(window)
    static_banner.resize(800, 100)  # Set the size of the banner
    static_banner.move(170, 1700)  # Move down 1500 pixels
    static_banner.show()

    # Choose and display a random phrase
    phrases = ["hello world", "python is fun", "qwerty keyboard"]
    #initialize_game()
    static_banner.setPhrase(encoded_phrase)
    #static_banner.setPhrase(encoded)

    #Update child widget size and position
    scrolling_banner = ScrollingBanner()
    scrolling_banner.setParent(window)
    scrolling_banner.setGeometry(0, 0, window.width(), 100)  # Set the size of the banner
    scrolling_banner.move(0, 1500)
    scrolling_banner.show()

    scrolling_window = ScrollingWindow()
    scrolling_window.setParent(window)
    scrolling_window.setGeometry(0, 0, window.width(), 100)  # Set the size of the banner
    scrolling_window.move(0, 2000)
    scrolling_window.show()
    
    video_window = VideoWindow()
    video_window.setParent(window)
    video_window.setGeometry(0, 0, window.width(), 100)  # Set the size of the banner
    video_window.move(0, 750)
    video_window.show()

    # Create and show the MatrixRain widget
    matrix_rain_widget = MatrixRainWidget()
    matrix_rain_widget.setParent(window)
    matrix_rain_widget.setGeometry(0, 0, window.width(), window.height())  # Cover the entire window
    matrix_rain_widget.hide()  # Initially hide it


    splash_widget = SplashWidget()
    splash_widget.setParent(window)
    splash_widget.setGeometry(0, 0, window.width(), window.height())  # Set window as the parent of splash_widget
    splash_widget.show()  # Make sure to show the splash_widget

    instructions_label = QLabel("Try to guess the word or phrase. \nAll letters are off by one on the keyboard. \n i.e. 'Q' could be 'W, S, OR S'", window)
    instructions_label.setFont(QFont("Arial", 20))
    instructions_label.setStyleSheet("QLabel { color: rgb(255, 255, 255); }")  # Setting text color to white
    instructions_label.setGeometry(0, 1800, window.width(), 100)  # Adjust the position to be below the StaticBanner
    instructions_label.setAlignment(Qt.AlignCenter)
    instructions_label.show()

    word_art_widget = WordArtWidget()
    word_art_widget.setParent(window)
    word_art_widget.setGeometry(0, 0, window.width(), window.height())  # Set window as the parent of splash_widget
    word_art_widget.show()

    # Create and show the BrickWallWidget
    brick_crumble_widget = BrickCrumbleWidget()
    brick_crumble_widget.setParent(window)
    brick_crumble_widget.setGeometry(0, 0, 750, 750)  # Set the size and position
    brick_crumble_widget.show()

    tiktok_thread = TikTokClientThread()
    
    def handle_new_comment(event):
        global leaderboard 
        global chosen_phrase 
        print(f"{event.user.nickname} -> {event.comment}")
        window.setWindowTitle(f"New comment from {event.user.nickname}")
        
        comment = event.comment
        username = event.user.nickname
    
        if comment == chosen_phrase:
            print(f"{username} is the winner!")
            #update_leaderboard(username)
            #matrix_rain_widget.show()
            if username in leaderboard:
                leaderboard[username] += 1
            else:
                leaderboard[username] = 1
        else:
            splash_widget.triggerSplash()  # Trigger the splash effect
        print("Updated leaderboard:", leaderboard)

    def handle_new_join(event):
        username = getattr(event.user, 'nickname', getattr(event.user, 'unique_id', None))
        if username is None:
            return
        
        #print(f"{event.user.nickname} -> {event.join}")
        #window.setWindowTitle(f"New comment from {event.user.nickname}")
        #word_art_widget.triggerText(username)  # Trigger the splash effect
        #matrix_rain_widget.show()
    tiktok_thread.comment_received.connect(handle_new_comment)
    tiktok_thread.join_received.connect(handle_new_join)
    tiktok_thread.start()

    app.exec_()
    ex = BrickCrumbleWidget()
    ex.makeCrumble()
    sys.exit(app.exec_())