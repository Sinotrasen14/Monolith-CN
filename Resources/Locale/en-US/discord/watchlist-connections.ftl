discord-watchlist-connection-header =
    { $players ->
        [one] {$players} 名观察名单中的玩家已
        *[other] {$players} 名观察名单中的玩家已
    } 连接到 {$serverName}

discord-watchlist-connection-entry = - {$playerName}，消息为“{$message}”{ $expiry ->
        [0] {""}
        *[other] {" "}（<t:{$expiry}:R> 过期）
    }{ $otherWatchlists ->
        [0] {""}
        [one] {" "}以及 {$otherWatchlists} 个其他观察名单
        *[other] {" "}以及 {$otherWatchlists} 个其他观察名单
    }