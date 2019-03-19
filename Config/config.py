# ===============================GAL游戏==========================================
GAL_URL = 'localhost'
GAL_DB = 'webdata'
GAL_TABLE = 'feiyue'

WX_CRT_GAL = 'JNBQbU4t1yJZSCeyVKkCtVTPlGlxngpA9vMwsWatJDk'
WX_AGTID_GAL = '1'
# ===============================游戏评测=========================================
GAMETEST_URL = 'localhost'
GAMETEST_DB = 'webdata'
GAMETEST_TABLE = 'gamepc'

WX_CRT_GT = 'LuksPh4Au0Gw4fTP6XcxFXjBFYLnlUXPX07AAa1k730'
WX_AGTID_GT = '1000002'
# ===============================新    闻=========================================
NEWS_URL = 'localhost'
NEWS_DB = 'webdata'
NEWS_TABLE = 'news'

WX_CRT_NEWS = '4Xam8u4eDMPlM1SygIRfNfC04vSwVRzfxelGQ3sPigQ'
WX_AGTID_NEWS = '1000003'
# ===============================技    术=========================================
TECH_URL = 'localhost'
TECH_DB = 'webdata'
TECH_TABLE = 'tech'

WX_CRT_TECH = '57DGnp55ii2Oxbf86AQ5YDAWYLF8QKLjNepb1uEa3gM'
WX_AGTID_TECH = '1000004'
# ===============================工    作=========================================
WORK_URL = 'localhost'
WORK_DB = 'webdata'
WORK_TABLE = 'work'

WX_CRT_WORK = 'EYmraurMnmu5JyWd8ZyYtzBaDQMKFqORtQfKFij85So'
WX_AGTID_WORK = '1000005'

# ===============================深 圳 工 作======================================
WX_CRT_WORK_SZ = '43d6OAePJ85YxnogILBVk0qDemWH0AzAA8xnlIvgYQ4'
WX_AGTID_WORK_SZ = '1000006'

# ================================电  影==========================================
MOVIE_URL = 'localhost'
MOVIE_DB = 'webdata'
MOVIE_TABLE = 'movie'

WX_CRT_MOVIE = 'DoJT2wX9qK-xr3-dlhb1kFXRBqkp0cA1SNcZcPh6fkk'
WX_AGTID_MOVIE = '1000008'

# ================================测  试==========================================
WX_CRT_TEST = 'thYP3T_aOhmsGpTOA6b3zSiw455CbiskW41Wsm3BVNU'
WX_AGTID_TEST = '1000007'


# ================================ headers =======================================
headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                         '(KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'
}
headers_zhihu = {
    'Cookie': 'tgw_l7_route=060f637cd101836814f6c53316f73463; _zap=58ed66b8-58dd-452f-952d-5d328d423990; _xsrf=7b4ddd7d-066a-4356-a325-799c1a296c7f; d_c0="ADBqFEVcgw-PTmgYjq2vwZ9028J4JKJFBqY=|1559293486"; l_n_c=1; q_c1=461896221e6b480bb95f04f4058c6445|1559293761000|1559293761000; r_cap_id="ZDQxMDVkYmZiZmUwNDFmZmExMDcwMTI4MWY2OWFhYTc=|1559293760|0bc6fc532149d182b89638207b18f8c11b5276d9"; cap_id="NjFjNDQ2OTYwYjg0NDM5NWJlNDM1ODFjZmEyMmZhNGM=|1559293760|a613f2273a33f63f453030f529270c181f9e0116"; l_cap_id="ZDhhMGY5NDJmYTljNGUyNWEzYWM1ODE5ZTU2NzdkMGQ=|1559293760|4951f33089321b2916f5ae3ab8bb607a2581a971"; n_c=1; __utma=51854390.519149028.1559293771.1559293771.1559293771.1; __utmb=51854390.0.10.1559293771; __utmc=51854390; __utmz=51854390.1559293771.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmv=51854390.000--|3=entry_date=20190531=1; capsion_ticket="2|1:0|10:1559294136|14:capsion_ticket|44:ZmYxNTc5ZTBlN2E1NDM1ZDk4NmZiN2U5OTkzYTkzMjQ=|9f984e0aa38a9a67fef11bb5aea750cddc9e386af534e80b2dcfbf92d48b7a98"; z_c0="2|1:0|10:1559294140|4:z_c0|92:Mi4xaVZXREFnQUFBQUFBTUdvVVJWeUREeVlBQUFCZ0FsVk52RDdlWFFBQk9GMnlFbk96c1RLN0NKc3hGcElJc3dXdnJ3|2ac64c4b5a5ef8e0364f77bb68641fe60c1a32270b79ca0535e45208e32df62d"; tst=r',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                         '(KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'
}

agent = [
        'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 '
        'Safari/534.50',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safar'
        'i/534.50',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
        'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
        'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11',
        'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Sa'
        'fari/535.11',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET '
        'CLR 2.0.50727; SE 2.X MetaSr 1.0)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
]
