from you_get import common as you_get_common


if __name__ == '__main__':
    url_list = ['https://www.bilibili.com/video/BV1N7411Q7eR']
    you_get_common.download_main(
        you_get_common.any_download,
        you_get_common.any_download_playlist,
        url_list,
        None,
        output_dir='./',
        merge=True
    )
