# FTLdiskburner
cmd-ftldisk-desc = 创建一个FTL坐标磁盘，用于航行到给定EntityID所在的地图
cmd-ftldisk-help = ftldisk [EntityID]

cmd-ftldisk-no-transform = 实体 {$destination} 没有Transform组件！
cmd-ftldisk-no-map = 实体 {$destination} 不在任何地图上！
cmd-ftldisk-no-map-comp = 实体 {$destination} 不知为何在地图 {$map} 上，但没有地图组件。
cmd-ftldisk-map-not-init = 实体 {$destination} 在地图 {$map} 上，该地图尚未初始化！请检查是否可以安全初始化，然后先初始化地图，否则玩家将卡在原地！
cmd-ftldisk-map-paused = 实体 {$desintation} 在地图 {$map} 上，该地图已暂停！请先取消暂停地图，否则玩家将卡在原地。
cmd-ftldisk-planet = 实体 {$desintation} 在行星地图 {$map} 上，需要一个FTL点。该点可能已存在。
cmd-ftldisk-already-dest-not-enabled = 实体 {$destination} 在地图 {$map} 上，该地图已有FTLDestinationComponent，但未启用！为安全起见，请手动设置。
cmd-ftldisk-requires-ftl-point = 实体 {$destination} 在地图 {$map} 上，前往该地图需要一个FTL点！该点可能已存在。

cmd-ftldisk-hint = 地图 netID