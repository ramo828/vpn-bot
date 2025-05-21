info_router = {
    "az":{
        """
Router’ın Shadowsocks Desteğini Yoxlayın:
Əksər standart routerlər Shadowsocks-u birbaşa dəstəkləmir. Buna görə də, routerınızın OpenWrt və ya DD-WRT kimi xüsusi proqram təminatı (firmware) dəstəkləyib-dəstəkləmədiyini yoxlayın.

OpenWrt İstifadəsi: OpenWrt, Shadowsocks müştərisini dəstəkləyir və Outline ilə uyğundur. OpenWrt-ni routerınıza yükləmək üçün cihazınızın modelinə uyğun proqram təminatını endirin.

OpenWrt ilə Shadowsocks Quraşdırılması:
- OpenWrt-ni Yükləyin: Routerınıza OpenWrt proqram təminatını quraşdırın. Bu proses cihaz modelinizə görə dəyişir; istehsalçı təlimatlarına əməl edin.
- Shadowsocks Paketini Yükləyin:
  - OpenWrt interfeysinə (LuCI) daxil olun.
  - Sistem > Proqram Təminatı menyusundan `shadowsocks-libev` və `luci-app-shadowsocks` paketlərini yükləyin.
- Outline Giriş Açarını Konfiqurasiya Edin:
  - Giriş açarınızdan (məsələn, `ss://Z2h6JKdfdFdR34eYdh5E=@1.2.3.4:25683/?outline=1`) aşağıdakı məlumatları çıxarın:
    - Server IP/Domen Adı: 1.2.3.4
    - Port: 25683
    - Şifrələmə Metodu və Şifrə: Base64 kodlu hissəni (məsələn, `Z2h6JKdfdFdR34eYdh5E=`) bir Base64 dekoderi ilə açın. Bu, adətən `şifrələmə_metodu:şifrə` formatında olur (məsələn, `chacha20-ietf-poly1305:56gsef6zr5`).
  - LuCI interfeysində Shadowsocks sekmesine keçin, yeni bir server profili yaradın və bu məlumatları daxil edin:
    - Server: Server IP/domen adı
    - Server Portu: Port nömrəsi
    - Şifrə: Açılmış şifrə
    - Metod: Şifrələmə metodu (məsələn, `chacha20-ietf-poly1305`)
- Şəbəkə Trafikini Yönləndirin: OpenWrt-də VPN trafikini bütün cihazlar üçün yönləndirmək üçün `VPN Policy-Based Routing` paketindən istifadə edə bilərsiniz. Bu, müəyyən cihazların və ya tətbiqlərin VPN üzərindən işləməsini təmin edir.
        """
    },

     "tr":{
        """
Router’ınızın Shadowsocks Desteğini Kontrol Edin:
Çoğu standart router Shadowsocks’u doğrudan desteklemez. Bu nedenle, router’ınızın OpenWrt veya DD-WRT gibi özel bir firmware destekleyip desteklemediğini kontrol edin.

OpenWrt Kullanımı: OpenWrt, Shadowsocks istemcisini destekler ve Outline ile uyumludur. OpenWrt’yi router’ınıza yüklemek için cihazınızın modeline uygun bir firmware indirin.

OpenWrt ile Shadowsocks Kurulumu:
- OpenWrt’yi Yükleyin: Router’ınıza OpenWrt firmware’ini kurun. Bu işlem, cihaz modelinize göre değişir; üretici talimatlarını takip edin.
- Shadowsocks Paketini Yükleyin:
  - OpenWrt arayüzüne (LuCI) erişin.
  - Sistem > Yazılım menüsünden `shadowsocks-libev` ve `luci-app-shadowsocks` paketlerini yükleyin.
- Outline Erişim Anahtarını Yapılandır:
  - Erişim anahtarınızdan (örn. `ss://Z2h6JKdfdFdR34eYdh5E=@1.2.3.4:25683/?outline=1`) aşağıdaki bilgileri çıkarın:
    - Sunucu IP/Alan Adı: 1.2.3.4
    - Port: 25683
    - Şifreleme Yöntemi ve Şifre: Base64 kodlu kısmı (örn. `Z2h6JKdfdFdR34eYdh5E=`) bir Base64 çözücü ile çözün. Bu, genellikle `şifreleme_yöntemi:şifre` formatında olur (örn. `chacha20-ietf-poly1305:56gsef6zr5`).
  - LuCI arayüzünde Shadowsocks sekmesine gidin, yeni bir sunucu profili oluşturun ve bu bilgileri girin:
    - Sunucu: Sunucu IP/alan adı
    - Sunucu Portu: Port numarası
    - Şifre: Çözülen şifre
    - Yöntem: Şifreleme yöntemi (örn. `chacha20-ietf-poly1305`)
- Ağ Trafiğini Yönlendirin: OpenWrt’de VPN trafiğini tüm cihazlar için yönlendirmek için `VPN Policy-Based Routing` paketini kullanabilirsiniz. Bu, belirli cihazların veya uygulamaların VPN üzerinden gitmesini sağlar.
        """
    },
     "ru":{
        """
Проверьте поддержку Shadowsocks вашим роутером:
Большинство стандартных роутеров не поддерживают Shadowsocks напрямую. Поэтому проверьте, поддерживает ли ваш роутер пользовательские прошивки, такие как OpenWrt или DD-WRT.

Использование OpenWrt: OpenWrt поддерживает клиент Shadowsocks и совместим с Outline. Чтобы установить OpenWrt на ваш роутер, загрузите прошивку, подходящую для модели вашего устройства.

Установка Shadowsocks с OpenWrt:
- Установите OpenWrt: Прошейте ваш роутер прошивкой OpenWrt. Этот процесс зависит от модели устройства; следуйте инструкциям производителя.
- Установите пакет Shadowsocks:
  - Получите доступ к интерфейсу OpenWrt (LuCI).
  - Перейдите в меню Система > Программное обеспечение и установите пакеты `shadowsocks-libev` и `luci-app-shadowsocks`.
- Настройте ключ доступа Outline:
  - Извлеките следующую информацию из вашего ключа доступа (например, `ss://Z2h6JKdfdFdR34eYdh5E=@1.2.3.4:25683/?outline=1`):
    - IP-адрес сервера/доменное имя: 1.2.3.4
    - Порт: 25683
    - Метод шифрования и пароль: Декодируйте Base64-кодированную часть (например, `Z2h6JKdfdFdR34eYdh5E=`) с помощью декодера Base64. Обычно это формат `метод_шифрования:пароль` (например, `chacha20-ietf-poly1305:56gsef6zr5`).
  - В интерфейсе LuCI перейдите на вкладку Shadowsocks, создайте новый профиль сервера и введите следующие данные:
    - Сервер: IP-адрес сервера/доменное имя
    - Порт сервера: Номер порта
    - Пароль: Декодированный пароль
    - Метод: Метод шифрования (например, `chacha20-ietf-poly1305`)
- Направление сетевого трафика: Для направления трафика VPN для всех устройств в OpenWrt вы можете использовать пакет `VPN Policy-Based Routing`. Это позволяет определенным устройствам или приложениям использовать VPN.
        """
    },
     "en":{
        """
Check Your Router’s Shadowsocks Support:
Most standard routers do not natively support Shadowsocks. Therefore, check whether your router supports custom firmware such as OpenWrt or DD-WRT.

Using OpenWrt: OpenWrt supports the Shadowsocks client and is compatible with Outline. To install OpenWrt on your router, download the firmware appropriate for your device model.

Installing Shadowsocks with OpenWrt:
- Install OpenWrt: Flash your router with the OpenWrt firmware. This process varies depending on your device model; follow the manufacturer’s instructions.
- Install the Shadowsocks Package:
  - Access the OpenWrt interface (LuCI).
  - Navigate to System > Software and install the `shadowsocks-libev` and `luci-app-shadowsocks` packages.
- Configure the Outline Access Key:
  - Extract the following information from your access key (e.g., `ss://Z2h6JKdfdFdR34eYdh5E=@1.2.3.4:25683/?outline=1`):
    - Server IP/Domain Name: 1.2.3.4
    - Port: 25683
    - Encryption Method and Password: Decode the Base64-encoded part (e.g., `Z2h6JKdfdFdR34eYdh5E=`) using a Base64 decoder. This is typically in the format `encryption_method:password` (e.g., `chacha20-ietf-poly1305:56gsef6zr5`).
  - In the LuCI interface, go to the Shadowsocks tab, create a new server profile, and enter the following details:
    - Server: Server IP/domain name
    - Server Port: Port number
    - Password: Decoded password
    - Method: Encryption method (e.g., `chacha20-ietf-poly1305`)
- Route Network Traffic: To route VPN traffic for all devices in OpenWrt, you can use the `VPN Policy-Based Routing` package. This allows specific devices or applications to go through the VPN.
        """
    },
}

info_tv = {
    "az": """
2. Shadowsocks Tətbiqini Android TV-yə Yükləyin
- **Endirmə**: Play Store'dan "Shadowsocks"u yükləyin. Yoxdursa, 4pda.to kimi etibarlı mənbədən APK endirin.
- **Quraşdırma**: APK-nı USB/şəbəkə ilə TV-yə köçürün. Fayl meneceri (məsələn, "File Manager" və ya Kodi) ilə quraşdırın.
  - **Qeyd**: "Naməlum mənbələrdən tətbiq quraşdırma"nı aktivləşdirin (Parametrlər > Təhlükəsizlik).

3. Giriş Açarını JSON Formatına Çevirin
Shadowsocks tətbiqi ss:// formatını birbaşa qəbul etməyə bilər; JSON konfiqurasiyası yaradın.
- **Açardan Məlumat Çıxarın**:
  - Nümunə: `ss://Z2h6JKdfdFdR34eYdh5E=@1.2.3.4:25683/?outline=1`
  - Məlumatlar: Server IP/Domen (`1.2.3.4`), Port (`25683`), Şifrələmə Metodu və Şifrə (Base64 kodlu hissəni dekoderlə açın: `chacha20-ietf-poly1305:56gsef6zr5`).
- **JSON Faylı Yaradın**:
  - Mətn redaktorunda `outline.json` yaradın:
    ```json
    {
      "server": "1.2.3.4",
      "server_port": 25683,
      "local_port": 1080,
      "password": "56gsef6zr5",
      "method": "chacha20-ietf-poly1305",
      "remarks": "Outline Server"
    }
Faylı USB/şəbəkə ilə TV-yə köçürün. Kodi kimi tətbiqlər fayl meneceri kimi istifadə edilə bilər.
Shadowsocks Tətbiqini Konfiqurasiya Edin
Açın: Shadowsocks tətbiqini işə salın.
JSON Yükləyin:
"Replace from file" seçin.
outline.json faylını seçin.
Qeyd: "No application can handle this action" xətası alsanız, fayl meneceri quraşdırın.
Bağlantını Başlatın: Serveri seçin və "Connect" düyməsinə basın.
Bağlantını Test Edin
Yoxlama: Bağlantı uğurlu olarsa, TV Outline serverinə qoşulacaq. YouTube, Netflix kimi tətbiqlərlə interneti test edin.
IP Yoxlaması: Brauzerdə whatismyipaddress.com ilə IP-nizi yoxlayın. IP Outline serverinin yerləşdiyi yerə aid olmalıdır.
Sürət Testi: Sürət testi tətbiqi ilə bağlantı sürətini yoxlayın.
Problemlərin Həlli
Xəta: "Libsslocal exists too fast (Exit code: 78)":
Səbəb: Yanlış JSON konfiqurasiyası. method və password sahələrinin düzgünlüyünü, Base64 kodunun düzgün açıldığını yoxlayın.
Həll: JSON faylını yenidən yaradın, dırnaq işarələrini yoxlayın. Bəzən dırnaqları silmək kömək edə bilər.
Bağlantı Kəsilir: Giriş açarının etibarlı olduğundan və serverin işlədiyindən əmin olun. Server IP/portunu yoxlayın (bəzi portlar bloklana bilər).
YouTube Problemləri: Server konfiqurasiyası/şəbəkə filtrləməsi səbəb ola bilər. Fərqli server yeri sınayın və ya yeni giriş açarı yaradın.
Fayl Meneceri Problemləri: Fayl köçürməsi üçün fayl meneceri vacibdir. "File Manager", Kodi, "ES File Explorer" tövsiyə olunur.
Vacib Qeydlər
Dəstəklənən Cihazlar: Xiaomi Mi Box S, Ugoos X4, NVIDIA Shield TV uyğundur. Chromecast with Google TV-də fayl meneceri tələb oluna bilər.
Alternativ Tətbiq: VPN_Outline_TV kimi xüsusi Android TV tətbiqini sınayın (beta ola bilər).
Təhlükəsizlik: Giriş açarınızı paylaşmayın. Outline Manager ilə açarları asanlıqla ləğv edə/yeni açarlar yarada bilərsiniz.
Performans: Aşağı gecikmə üçün coğrafi olaraq yaxın server yeri seçin (məsələn, Türkiyə üçün Avropa). DigitalOcean/AWS kimi təchizatçıların 5 USD/ay planları kifayətdir.
Dəstək Resursları: getoutline.org və ya Reddit r/outlinevpn icmasından yardım alın.
Nümunə JSON Konfiqurasiyası Giriş açarınız ss://Z2h6JKdfdFdR34eYdh5E=@1.2.3.4:25683/?outline=1 olarsa, JSON faylı belə olacaq:
json

Kopyala
{
  "server": "1.2.3.4",
  "server_port": 25683,
  "local_port": 1080,
  "password": "56gsef6zr5",
  "method": "chacha20-ietf-poly1305",
  "remarks": "Outline Server"
}
Qeyd: password və method üçün Base64 kodunu (məsələn, Z2h6JKdfdFdR34eYdh5E=) Base64 dekoderi ilə düzgün açın. Nümunə çıxış: chacha20-ietf-poly1305:56gsef6zr5.
""",
"ru": """
2. Загрузите приложение Shadowsocks на Android TV

Скачивание: Загрузите "Shadowsocks" из Play Store. Если его нет, скачайте APK с надежного источника, например, 4pda.to.
Установка: Перенесите APK на телевизор через USB/сеть. Установите с помощью файлового менеджера (например, "File Manager" или Kodi).
Примечание: Включите "Установка приложений из неизвестных источников" (Настройки > Безопасность).
Преобразуйте ключ доступа в формат JSON Приложение Shadowsocks может не принимать формат ss:// напрямую; создайте конфигурацию JSON.
Извлеките данные из ключа:
Пример: ss://Z2h6JKdfdFdR34eYdh5E=@1.2.3.4:25683/?outline=1
Данные: IP/домен сервера (1.2.3.4), порт (25683), метод шифрования и пароль (декодируйте Base64 часть: chacha20-ietf-poly1305:56gsef6zr5).
Создайте файл JSON:
Создайте outline.json в текстовом редакторе:
json

Kopyala
{
  "server": "1.2.3.4",
  "server_port": 25683,
  "local_port": 1080,
  "password": "56gsef6zr5",
  "method": "chacha20-ietf-poly1305",
  "remarks": "Outline Server"
}
Перенесите файл на телевизор через USB/сеть. Приложения вроде Kodi можно использовать как файловый менеджер.
Настройте приложение Shadowsocks
Откройте: Запустите приложение Shadowsocks.
Загрузите JSON:
Выберите "Replace from file".
Выберите файл outline.json.
Примечание: Если появляется ошибка "No application can handle this action", установите файловый менеджер.
Запустите соединение: Выберите сервер и нажмите "Connect".
Протестируйте соединение
Проверка: При успешном подключении телевизор подключится к серверу Outline. Протестируйте интернет с помощью YouTube, Netflix и т.д.
Проверка IP: В браузере зайдите на whatismyipaddress.com. IP должен соответствовать местоположению сервера Outline.
Тест скорости: Используйте приложение для проверки скорости соединения.
Решение проблем
Ошибка: "Libsslocal exists too fast (Exit code: 78)":
Причина: Неправильная конфигурация JSON. Проверьте правильность полей method и password, а также декодирование Base64.
Решение: Пересоздайте файл JSON, проверьте кавычки. Иногда удаление кавычек может помочь.
Разрывы соединения: Убедитесь, что ключ доступа действителен и сервер работает. Проверьте IP/порт сервера (некоторые порты могут быть заблокированы).
Проблемы с YouTube: Могут быть связаны с конфигурацией сервера или фильтрацией сети. Попробуйте другое местоположение сервера или создайте новый ключ.
Проблемы с файловым менеджером: Для переноса файлов необходим файловый менеджер. Рекомендуются "File Manager", Kodi, "ES File Explorer".
Важные замечания
Поддерживаемые устройства: Xiaomi Mi Box S, Ugoos X4, NVIDIA Shield TV подходят. Для Chromecast with Google TV может потребоваться файловый менеджер.
Альтернативное приложение: Попробуйте специальное приложение для Android TV, например VPN_Outline_TV (может быть в бета-версии).
Безопасность: Не делитесь ключом доступа. С помощью Outline Manager можно легко отозвать/создать новые ключи.
Производительность: Для низкой задержки выберите географически близкое местоположение сервера (например, Европа для Турции). Планы DigitalOcean/AWS за 5 USD/месяц достаточны.
Ресурсы поддержки: Обратитесь за помощью на getoutline.org или в сообществе Reddit r/outlinevpn.
Пример конфигурации JSON Если ваш ключ доступа ss://Z2h6JKdfdFdR34eYdh5E=@1.2.3.4:25683/?outline=1, файл JSON будет таким:
json

Kopyala
{
  "server": "1.2.3.4",
  "server_port": 25683,
  "local_port": 1080,
  "password": "56gsef6zr5",
  "method": "chacha20-ietf-poly1305",
  "remarks": "Outline Server"
}
Примечание: Для password и method правильно декодируйте Base64 код (например, Z2h6JKdfdFdR34eYdh5E=). Пример вывода: chacha20-ietf-poly1305:56gsef6zr5.
""",
"en": """
2. Download the Shadowsocks App on Android TV

Download: Install "Shadowsocks" from the Play Store. If unavailable, download the APK from a trusted source like 4pda.to.
Installation: Transfer the APK to the TV via USB/network. Install using a file manager (e.g., "File Manager" or Kodi).
Note: Enable "Install apps from unknown sources" (Settings > Security).
Convert the Access Key to JSON Format The Shadowsocks app may not directly accept the ss:// format; create a Winners configuration.
Extract Data from the Key:
Example: ss://Z2h6JKdfdFdR34eYdh5E=@1.2.3.4:25683/?outline=1
Details: Server IP/Domain (1.2.3.4), Port (25683), Encryption Method and Password (decode the Base64 part: chacha20-ietf-poly1305:56gsef6zr5).
Create a JSON File:
Create outline.json in a text editor:
json

Kopyala
{
  "server": "1.2.3.4",
  "server_port": 25683,
  "local_port": 1080,
  "password": "56gsef6zr5",
  "method": "chacha20-ietf-poly1305",
  "remarks": "Outline Server"
}
Transfer the file to the TV via USB/network. Apps like Kodi can be used as a file manager.
Configure the Shadowsocks App
Open: Launch the Shadowsocks app.
Load JSON:
Select "Replace from file".
Choose the outline.json file.
Note: If you get "No application can handle this action", install a file manager.
Start Connection: Select the server and press "Connect".
Test the Connection
Verification: If successful, the TV will connect to the Outline server. Test internet with apps like YouTube, Netflix.
IP Check: Use a browser to visit whatismyipaddress.com. The IP should match the Outline server's location.
Speed Test: Use a speed test app to check connection speed.
Troubleshooting
Error: "Libsslocal exists too fast (Exit code: 78)":
Cause: Incorrect JSON configuration. Verify method and password fields, and ensure Base64 is decoded correctly.
Solution: Recreate the JSON file, check for quotation marks. Sometimes removing quotes can help.
Connection Drops: Ensure the access key is valid and the server is running. Check server IP/port (some ports may be blocked).
YouTube Issues: May be due to server configuration or network filtering. Try a different server location or create a new access key.
File Manager Issues: A file manager is essential for transferring files. Recommended: "File Manager", Kodi, "ES File Explorer".
Important Notes
Supported Devices: Xiaomi Mi Box S, Ugoos X4, NVIDIA Shield TV are compatible. Chromecast with Google TV may require a file manager.
Alternative App: Try a dedicated Android TV app like VPN_Outline_TV (may be in beta).
Security: Do not share your access key. Use Outline Manager to easily revoke/create new keys.
Performance: For low latency, choose a geographically close server location (e.g., Europe for Turkey). Providers like DigitalOcean/AWS offer sufficient plans at 5 USD/month.
Support Resources: Seek help from getoutline.org or the Reddit community r/outlinevpn.
Sample JSON Configuration If your access key is ss://Z2h6JKdfdFdR34eYdh5E=@1.2.3.4:25683/?outline=1, the JSON file will be:
json

Kopyala
{
  "server": "1.2.3.4",
  "server_port": 25683,
  "local_port": 1080,
  "password": "56gsef6zr5",
  "method": "chacha20-ietf-poly1305",
  "remarks": "Outline Server"
}
Note: For password and method, correctly decode the Base64 code (e.g., Z2h6JKdfdFdR34eYdh5E=). Sample output: chacha20-ietf-poly1305:56gsef6zr5.
""",
"tr": """
2. Shadowsocks Uygulamasını Android TV'ye İndirin

İndirme: Play Store'dan "Shadowsocks"u indirin. Yoksa, 4pda.to gibi güvenilir bir kaynaktan APK indirin.
Kurulum: APK'yı USB/ağ yoluyla TV'ye aktarın. Dosya yöneticisi (örneğin, "File Manager" veya Kodi) ile kurun.
Not: "Bilinmeyen kaynaklardan uygulama kurulumunu" etkinleştirin (Ayarlar > Güvenlik).
Erişim Anahtarını JSON Formatına Dönüştürün Shadowsocks uygulaması ss:// formatını doğrudan kabul etmeyebilir; JSON yapılandırması oluşturun.
Anahtardan Veri Çıkarın:
Örnek: ss://Z2h6JKdfdFdR34eYdh5E=@1.2.3.4:25683/?outline=1
Veriler: Sunucu IP/Domain (1.2.3.4), Port (25683), Şifreleme Yöntemi ve Parola (Base64 kodlu kısmı dekoder ile açın: chacha20-ietf-poly1305:56gsef6zr5).
JSON Dosyası Oluşturun:
Metin editöründe outline.json oluşturun:
json

Kopyala
{
  "server": "1.2.3.4",
  "server_port": 25683,
  "local_port": 1080,
  "password": "56gsef6zr5",
  "method": "chacha20-ietf-poly1305",
  "remarks": "Outline Server"
}
Dosyayı USB/ağ yoluyla TV'ye aktarın. Kodi gibi uygulamalar dosya yöneticisi olarak kullanılabilir.
Shadowsocks Uygulamasını Yapılandırın
Açın: Shadowsocks uygulamasını başlatın.
JSON Yükleyin:
"Replace from file" seçeneğini seçin.
outline.json dosyasını seçin.
Not: "No application can handle this action" hatası alırsanız, dosya yöneticisi kurun.
Bağlantıyı Başlatın: Sunucuyu seçin ve "Connect" düğmesine basın.
Bağlantıyı Test Edin
Doğrulama: Başarılı olursa, TV Outline sunucusuna bağlanacak. YouTube, Netflix gibi uygulamalarla interneti test edin.
IP Kontrolü: Tarayıcıda whatismyipaddress.com ile IP'nizi kontrol edin. IP, Outline sunucusunun konumuna ait olmalıdır.
Hız Testi: Hız testi uygulaması ile bağlantı hızını kontrol edin.
Sorun Giderme
Hata: "Libsslocal exists too fast (Exit code: 78)":
Neden: Yanlış JSON yapılandırması. method ve password alanlarının doğruluğunu, Base64 kodunun doğru açıldığını kontrol edin.
Çözüm: JSON dosyasını yeniden oluşturun, tırnak işaretlerini kontrol edin. Bazen tırnakları kaldırmak yardımcı olabilir.
Bağlantı Kesintileri: Erişim anahtarının geçerli olduğundan ve sunucunun çalıştığından emin olun. Sunucu IP/portunu kontrol edin (bazı portlar engellenebilir).
YouTube Sorunları: Sunucu yapılandırması/ağ filtrelemesi nedeniyle olabilir. Farklı bir sunucu konumu deneyin veya yeni bir erişim anahtarı oluşturun.
Dosya Yöneticisi Sorunları: Dosya aktarımı için dosya yöneticisi gereklidir. Önerilen: "File Manager", Kodi, "ES File Explorer".
Önemli Notlar
Desteklenen Cihazlar: Xiaomi Mi Box S, Ugoos X4, NVIDIA Shield TV uyumludur. Chromecast with Google TV için dosya yöneticisi gerekebilir.
Alternatif Uygulama: VPN_Outline_TV gibi özel Android TV uygulamasını deneyin (beta olabilir).
Güvenlik: Erişim anahtarınızı paylaşmayın. Outline Manager ile anahtarları kolayca iptal edebilir/yeni anahtarlar oluşturabilirsiniz.
Performans: Düşük gecikme için coğrafi olarak yakın bir sunucu konumu seçin (örneğin, Türkiye için Avrupa). DigitalOcean/AWS gibi sağlayıcıların 5 USD/ay planları yeterlidir.
Destek Kaynakları: getoutline.org veya Reddit r/outlinevpn topluluğundan yardım alın.
Örnek JSON Yapılandırması Erişim anahtarınız ss://Z2h6JKdfdFdR34eYdh5E=@1.2.3.4:25683/?outline=1 ise, JSON dosyası şöyle olacaktır:
json

Kopyala
{
  "server": "1.2.3.4",
  "server_port": 25683,
  "local_port": 1080,
  "password": "56gsef6zr5",
  "method": "chacha20-ietf-poly1305",
  "remarks": "Outline Server"
}
Not: password ve method için Base64 kodunu (örneğin, Z2h6JKdfdFdR34eYdh5E=) Base64 dekoderi ile doğru şekilde açın. Örnek çıktı: chacha20-ietf-poly1305:56gsef6zr5.
"""
}