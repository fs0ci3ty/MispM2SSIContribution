rule Detect_Telegram_API_Key {
    meta:
        author = "@YourName"
        info = "Detects Telegram API Keys in documents"
        reference = "https://core.telegram.org/bots/api#authorizing-your-bot"

    strings:
        $a = /^[0-9]{8,10}:[a-zA-Z0-9_-]{35}$/

    condition:
        any of them
}
