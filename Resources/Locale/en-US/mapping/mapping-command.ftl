cmd-mapping-desc = 创建或加载一张地图，并将你传送到该地图。
cmd-mapping-help = 用法：mapping [MapID] [Path] [Grid]
cmd-mapping-server = 只有玩家可以使用此命令。
cmd-mapping-error = 创建新地图时发生错误。
cmd-mapping-try-grid = 无法将该文件作为地图加载。正在尝试将该文件作为网格加载……
cmd-mapping-success-load = 已从文件 {$path} 创建未初始化地图，ID 为 {$mapId}。
cmd-mapping-success-load-grid = 已从文件 {$path} 加载未初始化网格到新地图，ID 为 {$mapId}。
cmd-mapping-success = 已创建未初始化地图，ID 为 {$mapId}。
cmd-mapping-warning = 警告：服务器正在使用调试版本。你可能面临丢失更改的风险。


# duplicate text from engine load/save map commands.
# I CBF making this PR depend on that one.
cmd-mapping-failure-integer = {$arg} 不是有效的整数。
cmd-mapping-failure-float = {$arg} 不是有效的浮点数。
cmd-mapping-failure-bool = {$arg} 不是有效的布尔值。
cmd-mapping-nullspace = 你无法加载到地图 0。
cmd-hint-mapping-id = [MapID]
cmd-mapping-hint-grid = [Grid]
cmd-hint-mapping-path = [Path]
cmd-mapping-exists = 地图 {$mapId} 已存在。