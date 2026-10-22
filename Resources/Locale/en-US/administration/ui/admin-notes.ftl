# UI
admin-notes-title = {$player} 的备注
admin-notes-new-note = 新建备注
admin-notes-show-more = 显示更多
admin-notes-for = 备注对象：{$player}
admin-notes-id = Id：{$id}
admin-notes-type = 类型：{$type}
admin-notes-severity = 严重程度：{$severity}
admin-notes-secret = 机密
admin-notes-notsecret = 非机密
admin-notes-expires = 过期时间：{$expires}
admin-notes-expires-never = 永不过期
admin-notes-edited-never = 从未
admin-notes-round-id = 回合 Id：{$id}
admin-notes-round-id-unknown = 回合 Id：未知
admin-notes-created-by = 创建者：{$author}
admin-notes-created-at = 创建时间：{$date}
admin-notes-last-edited-by = 最后编辑者：{$author}
admin-notes-last-edited-at = 最后编辑时间：{$date}
admin-notes-edit = 编辑
admin-notes-delete = 删除
admin-notes-hide = 隐藏
admin-notes-delete-confirm = 确认删除
admin-notes-edited = 最后由 {$author} 于 {$date} 编辑
admin-notes-unbanned = 由 {$admin} 于 {$date} 解除封禁
admin-notes-message-desc = [color=white]自你上次在此服务器游玩以来，你收到了 { $count ->
    [1] 条管理消息
    *[other] 条管理消息
}。[/color]
admin-notes-message-admin = 来自 [bold]{ $admin }[/bold]，写于 { TOSTRING($date, "f") }：
admin-notes-message-wait = 接受按钮将在 {$time} 秒后启用。
admin-notes-message-accept = 永久忽略
admin-notes-message-dismiss = 暂时忽略
admin-notes-message-seen = 已查看
admin-notes-banned-from = 封禁来源
admin-notes-the-server = 服务器
admin-notes-permanently = 永久
admin-notes-days = {$days} 天
admin-notes-hours = {$hours} 小时
admin-notes-minutes = {$minutes} 分钟

# Note editor UI
admin-note-editor-title-new = 正在为 {$player} 创建新备注
admin-note-editor-title-existing = 正在编辑 {$player} 上由 {$author} 创建的备注 {$id}
admin-note-editor-pop-out = 弹出
admin-note-editor-secret = 机密？
admin-note-editor-secret-tooltip = 勾选此项将使玩家无法看到该备注
admin-note-editor-type-note = 备注
admin-note-editor-type-message = 消息
admin-note-editor-type-watchlist = 观察名单
admin-note-editor-type-server-ban = 服务器封禁
admin-note-editor-type-role-ban = 角色封禁
admin-note-editor-severity-select = 选择
admin-note-editor-severity-none = 无
admin-note-editor-severity-low = 低
admin-note-editor-severity-medium = 中
admin-note-editor-severity-high = 高
admin-note-editor-expiry-checkbox = 永久？
admin-note-editor-expiry-checkbox-tooltip = 勾选此项使其过期
admin-note-editor-expiry-label = 过期时间：
admin-note-editor-expiry-label-params = 过期时间：{$date}（{$expiresIn} 后）
admin-note-editor-expiry-label-expired = 已过期
admin-note-editor-expiry-placeholder = 输入过期时间（整数）。
admin-note-editor-submit = 提交
admin-note-editor-submit-confirm = 你确定吗？

# Time
admin-note-button-minutes = 分钟
admin-note-button-hours = 小时
admin-note-button-days = 天
admin-note-button-weeks = 周
admin-note-button-months = 月
admin-note-button-years = 年
admin-note-button-centuries = 世纪


# Verb
admin-notes-verb-text = 打开管理备注

# Watchlist and message login
admin-notes-watchlist = {$player} 的观察名单：{$message}
admin-notes-new-message = 你收到了来自 {$admin} 的管理消息：{$message}
admin-notes-fallback-admin-name = [System]

# Admin remarks
admin-remarks-command-description = 打开管理备注页面
admin-remarks-command-error = 管理备注已被禁用
admin-remarks-title = 管理备注

# Misc
system-user = [System]