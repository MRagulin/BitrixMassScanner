import requests
import urllib3
from tabulate import tabulate

urllib3.disable_warnings()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) OAKB/20100101 Firefox/85.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
}

schemas = ["http://", "https://"]
bitrix_domain = ["nitec.kz", "b24.kz"]

admin_urls = ["/bitrix/admin/index.php", "/bitrix/components/bitrix/desktop/admin_settings.php",
              "/bitrix/components/bitrix/map.yandex.search/settings/settings.php",
              "/bitrix/components/bitrix/player/player_playlist_edit.php", "/bitrix/tools/autosave.php",
              "/bitrix/tools/get_catalog_menu.php", "/bitrix/tools/upload.php",
              "/ololo/?SEF_APPLICATION_CUR_PAGE_URL=/bitrix/admin/", "/?USER_FIELD_MANAGER=1",
              "/bitrix/modules/main/admin/php_command_line.php", "/bitrix/services/mobileapp/jn.php",
              "/bitrix/services/main/ajax.php", "/bitrix/components/bitrix/main.numerator.edit.sequence/slider.php",
              "/bitrix/admin/php_command_line.php", "/bitrix/admin/main_controller.php",
              "/bitrix/admin/restore_export.php", "/bitrix/admin/tools_index.php", "/bitrix/bitrix.php",
              "/bitrix/modules/main/ajax_tools.php", "/bitrix/php_interface/after_connect_d7.php.",
              "/bitrix/themes/.default/.description.php", "/bitrix/components/bitrix/main.ui.selector/templates/.default/template.php",
              "/bitrix/components/bitrix/forum.user.profile.edit/templates/.default/interface.php"]
              
dangerous_urls = ["/bitrix/modules/main/include/virtual_file_system.php", "/bitrix/tools/vote/uf.php", "/bitrix/bitrix.php", 
               "/bitrix/.settings.bak", "/bitrix/error.log", "/bitrix/web.config", "/__bx_log.log", "/bitrix/authorization.config"]

print("Start checking ...")


def Scanner(schemas=['https://'], domains=['alfastrah.ru'], urls=['/bitrix/admin'], shortURL=False):
    urllib3.disable_warnings()
    buf = []
    tmp = ''
    interesting = []
    cols = ['domain']
    if domains:
        for schema in schemas:
            for domain in domains:
                if domain not in tmp: tmp = tmp + domain + '|'
                for url in urls:
                    if url not in cols:
                        if shortURL:
                            cols.append(url.split('/')[-1])
                        else:
                            cols.append(url)
                    try:
                        res = requests.get(schema + domain + url, headers=headers, verify=False, timeout=3)
                        if res.status_code in [200] or ('{' in res.text and ':' in res.text):
                            if 'bx-admin-prefix' in res.text:
                                tmp = tmp + '!admin!|'
                                interesting.append("%s !admin! %s %s " % (schema + domain + url, res.status_code, len(res.text)))
                            elif ('[Error]' in res.text and 'Bitrix\\' in res.text) or '/usr/bin/php' in res.text:
                                tmp = tmp + '!error!|'
                                interesting.append("%s !error! %s %s " % (schema + domain + url, res.status_code, len(res.text)))
                            else:
                                tmp = tmp + '+|'
                        else:
                            tmp = tmp + '- [%s]|'% res.status_code
                    except Exception as e:
                        tmp = tmp + '?|'

                buf.append(tmp.split('|')[:-1])
                tmp = ''


    print(tabulate(buf, headers=cols))
    if len(interesting) > 0:
        print('Manual handling:')
        for el in interesting:
            print(el)

Scanner(['https://'], bitrix_domain, dangerous_urls, True)