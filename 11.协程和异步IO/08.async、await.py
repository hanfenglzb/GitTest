async def downloader(url):
    return url


async def download_url(url):
    html = await downloader(url)
    return html


if __name__ == '__main__':
    coroutine = download_url("https://www.baidu.com")
    try:
        coroutine.send(None)
    except StopIteration as e:
        print(e.value)
