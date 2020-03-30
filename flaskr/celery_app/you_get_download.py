from you_get import common as you_get_common


if __name__ == '__main__':
    url = ''
    you_get_common.download_main(
        you_get_common.any_download,
        you_get_common.any_download_playlist,
        url_list,
        play_list,
        output_dir=''
    )
