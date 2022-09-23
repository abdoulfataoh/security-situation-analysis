# coding: utf-8

import logging
from pathlib import Path

# [GENRAL Config]
logging.basicConfig(level=logging.INFO)
DATE_FORMAT = '%Y-%m-%dT%H:%M:%S'

# [PATH Config]
ASSETS_PATH = Path(r'assets')
DATASET_PATH = ASSETS_PATH / 'dataset'

# [LEFASO.NET Config]
LEFASO_SITE_URL = 'https://lefaso.net'
LEFASO_SECTION_PATH = 'spip.php?rubrique459&debut_articles={page}#pagination_articles'
LEFASO_ARTCILE_ATTR = {'style': 'width:100%; height:160px;margin-top:10px; margin-bottom:10px;'}
LEFASO_PAGING_STEP = 20
LEFASO_MIN_PAGING = 500
LEFASO_MAX_PAGING = 1080
LEFASO_DATE_FORMAT = '%Y-%m-%dT%H:%M:%SZ'

# [FACEBOOK Config]
FACEBOOK_SITE_URL = 'https://www.facebook.com'