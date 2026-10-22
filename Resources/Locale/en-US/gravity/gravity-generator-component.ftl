### Gravity Generator

## UI

gravity-generator-window-title = 重力发生器

## UI field names

gravity-generator-window-status = 状态：
gravity-generator-window-power = 功率：
gravity-generator-window-eta = 预计时间：
gravity-generator-window-charge = 充能：

## UI statuses
gravity-generator-window-status-fully-charged = 已充满
gravity-generator-window-status-off = 关闭
gravity-generator-window-status-charging = 充电中
gravity-generator-window-status-discharging = 放电中

## UI Power Buttons
gravity-generator-window-power-on = 开
gravity-generator-window-power-off = 关
gravity-generator-window-power-label = { $draw } / { $max } 瓦

## UI ETA label

gravity-generator-window-eta-none = 不适用
gravity-generator-window-eta-value = { TOSTRING($left, "m\\:ss") }

## pzn: mass limit examine
## yes i know shuttle mass is actually in kilograms but shhhhhhh dont tell anyone
gravity-generator-examine-max-mass = 它的额定承载能力为 [color=yellow]{ $mass }[/color] 吨，可使穿梭机保持悬浮。
gravity-generator-examine-load = 发生器正以其容量的 [color={ $color }]{ $percent }%[/color] 运行。
gravity-generator-examine-load-unlimited = 发生器似乎没有在运行。