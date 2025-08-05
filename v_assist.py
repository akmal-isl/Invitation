import pyttsx3
import os
import subprocess
import webbrowser
import datetime

# Инициализация движка речи
engine = pyttsx3.init()
voices = engine.getProperty('voices')

# Глобальный флаг для текущего голоса
current_voice_name = None

def set_voice_by_name(name_part):
    global current_voice_name
    for voice in voices:
        if name_part.lower() in voice.name.lower():
            engine.setProperty('voice', voice.id)
            current_voice_name = voice.name
            speak(f"Голос установлен на {voice.name}")
            return
    speak("Такой голос не найден")

# Функция для речи
def speak(text):
    print("🤖 Ответ:", text)
    engine.say(text)
    engine.runAndWait()

# Функция обработки команд
def process_command(command):
    global current_voice_name
    command = command.lower()

    if "открой хром" in command:
        speak("Открываю Chrome")
        subprocess.Popen(["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"])
    elif "закрой хром" in command:
        speak("Закрываю Chrome")
        os.system("pkill 'Google Chrome'")
    elif "открой ютуб" in command:
        speak("Открываю YouTube")
        webbrowser.open("https://www.youtube.com")
    elif "время" in command:
        now = datetime.datetime.now().strftime("%H:%M")
        speak(f"Сейчас {now}")
    elif "открой терминал" in command:
        speak("Открываю терминал")
        subprocess.Popen(["/System/Applications/Utilities/Terminal.app/Contents/MacOS/Terminal"])
    elif "открой vscode" in command or "открой код" in command:
        speak("Открываю Visual Studio Code")
        subprocess.Popen(["/Applications/Visual Studio Code.app/Contents/Resources/app/bin/code"])
    elif "выключи звук" in command:
        speak("Выключаю звук")
        os.system("osascript -e 'set volume output muted true'")
    elif "включи звук" in command:
        speak("Включаю звук")
        os.system("osascript -e 'set volume output muted false'")
    elif "громкость на" in command:
        volume_level = ''.join(filter(str.isdigit, command))
        if volume_level:
            volume_value = int(volume_level)
            os.system(f"osascript -e 'set volume output volume {volume_value}'")
            speak(f"Громкость установлена на {volume_level} процентов")
        else:
            speak("Не понял уровень громкости")

    elif "список голосов" in command:
        print("\n🎙️ Доступные голоса:")
        for idx, voice in enumerate(voices):
            print(f"{idx + 1}. {voice.name} ({voice.languages})")
        speak("Список голосов выведен в консоль. Скажи: выбери голос и название")

    elif "выбери голос" in command:
        name_part = command.replace("выбери голос", "").strip()
        if name_part:
            set_voice_by_name(name_part)
        else:
            speak("Пожалуйста, укажи часть имени голоса после команды")

    else:
        speak("Команда не распознана")

# Основной цикл
if __name__ == "__main__":
    # Установка дефолтного голоса, если не установлен
    if not current_voice_name:
        set_voice_by_name("milena")  # можно поменять на свой любимый голос
    while True:
        try:
            user_input = input("🎤 Говори...\n🗣️ Ты сказал: ")
            process_command(user_input)
        except KeyboardInterrupt:
            speak("Пока!")
            break
