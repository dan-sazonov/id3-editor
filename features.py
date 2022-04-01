def get_new_filename(artist: str, title: str) -> str:
    """
    Get new filename for the track. Remove all symbols, replace spaces with underscores

    :param artist:
    :param title:
    :return:
    """

    tmp_data = []
    for data in [artist, title]:
        tmp_data.append(''.join([i.lower() if i != ' ' else '_' for i in data if i.isalnum() or i == ' ']))

    return '{0}-{1}.mp3'.format(*tmp_data)
