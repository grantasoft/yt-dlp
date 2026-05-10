from .common import InfoExtractor



class RTPAIE(InfoExtractor):
    _VALID_URL = r'https?://(?:www\.)?rtpa\.es/video:(?P<slug>[^_]+)_(?P<id>\d+)\.html'
    IE_NAME = 'rtpa'
    IE_DESC = 'Radiotelevisión del Principado de Asturias (TPA)'

    _TESTS = [{
        'url': 'https://www.rtpa.es/video:Xuntanza-.--T.2-Cap.-12_551777848815.html',
        'info_dict': {
            'id': '551777848815',
            'ext': 'mp4',
            'title': 'TPA a la carta: Xuntanza , del domingo 03 de mayo de 2026',
            'description': '=Xuntanza  :  T.2 Cap. 12, capítulo del domingo 03 de mayo de 2026',
            'thumbnail': r're:^https?://.*\.png',
        },
        'params': {'skip_download': 'm3u8'},
    }, {
        'url': 'https://www.rtpa.es/video:Pueblos.-Santianes_551777936431.html',
        'info_dict': {
            'id': '551777936431',
            'ext': 'mp4',
            'title': 'TPA a la carta: Pueblos, del lunes 04 de mayo de 2026',
            'description': '=Pueblos : Santianes, capítulo del lunes 04 de mayo de 2026',
            'thumbnail': r're:^https?://.*\.png',
        },
        'params': {'skip_download': 'm3u8'},
    }]

    def _real_extract(self, url):
        video_id = self._match_id(url)
        webpage = self._download_webpage(url, video_id)

        hls_url = self._search_regex(
            r'<source\s+[^>]*src=(["\'])(?P<url>(?:(?!\1).)+\.m3u8)\1',
            webpage, 'HLS URL', group='url')

        formats, subtitles = self._extract_m3u8_formats_and_subtitles(
            hls_url, video_id, m3u8_id='hls', headers={'Referer': 'https://www.rtpa.es/'})

        for f in formats:
            f.setdefault('http_headers', {}).setdefault('Referer', 'https://www.rtpa.es/')

        title = (
            self._html_search_meta(['og:title', 'twitter:title'], webpage, default=None)
            or self._html_extract_title(webpage, default=None)
        )

        description = self._html_search_meta(
            ['og:description', 'twitter:description'], webpage, default=None)

        thumbnail = (
            self._search_regex(
                r'<video[^>]+poster=(["\'])(?P<url>(?:(?!\1).)+)\1',
                webpage, 'thumbnail', default=None, group='url')
            or self._html_search_meta(['og:image', 'twitter:image'], webpage, default=None)
        )

        subtitle_url = self._search_regex(
            r'<track\s+kind=[\'"]captions[\'"][^>]+src=(["\'])(?P<url>(?:(?!\1).)+\.vtt)\1',
            webpage, 'subtitle URL', default=None, group='url')

        if subtitle_url:
            subtitles.setdefault('es', []).append({
                'url': subtitle_url,
                'name': 'Español',
            })

        return {
            'id': video_id,
            'title': title,
            'description': description,
            'thumbnail': thumbnail,
            'formats': formats,
            'subtitles': subtitles,
        }
