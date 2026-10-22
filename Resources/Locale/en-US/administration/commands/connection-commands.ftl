## Strings for the "grant_connect_bypass" command.

cmd-grant_connect_bypass-desc = 临时允许用户绕过常规连接检查。
cmd-grant_connect_bypass-help = 用法：grant_connect_bypass <user> [duration minutes]
    临时授予用户绕过常规连接限制的能力。
    该绕过仅适用于此游戏服务器，并将在（默认）1 小时后过期。
    无论白名单、恐慌地堡或玩家上限如何，他们都将能够加入。

cmd-grant_connect_bypass-arg-user = <user>
cmd-grant_connect_bypass-arg-duration = [duration minutes]

cmd-grant_connect_bypass-invalid-args = 预期 1 或 2 个参数
cmd-grant_connect_bypass-unknown-user = 无法找到用户 '{$user}'
cmd-grant_connect_bypass-invalid-duration = 无效的持续时间 '{$duration}'

cmd-grant_connect_bypass-success = 已成功为用户 '{$user}' 添加绕过