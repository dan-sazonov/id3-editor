from mutagen.easyid3 import EasyID3

audio = EasyID3("example.mp3")
# audio['title'] = u"Example Title"
# audio['artist'] = u"Me"
# audio['album'] = u"My album"
# audio['composer'] = u"" # clear
# audio.save()

"""
выпилить все, кроме album, title, artist, tracknumber, genre, date

audio = EasyID3("drafts/example2.mp3") - получаем словарь, идем по нему, что надо - редачим и пихаем в новый

audio['ключ'] = u"значение" - редачим

audio.save() - сохраняем

больше: https://stackoverflow.com/a/34970600/14585419"""
