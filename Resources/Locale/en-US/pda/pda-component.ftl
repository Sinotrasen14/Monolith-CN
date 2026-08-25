
### UI

# For the PDA screen
comp-pda-ui = ID: [color=white]{$owner}[/color], [color=yellow]{$jobTitle}[/color]

comp-pda-ui-blank = ID:

comp-pda-ui-owner = 所有者: [color=white]{$actualOwnerName}[/color]

comp-pda-ui-owner-with-company = 所有者: [color=white]{$actualOwnerName}[/color] [color={$companyColor}]({$companyName})[/color]

comp-pda-io-program-list-button = 程序

comp-pda-io-settings-button = 设置

comp-pda-io-program-fallback-title = 程序

comp-pda-io-no-programs-available = 无可用程序

pda-bound-user-interface-show-uplink-title = 打开上行链路
pda-bound-user-interface-show-uplink-description = 访问您的上行链路

pda-bound-user-interface-lock-uplink-title = 锁定上行链路
pda-bound-user-interface-lock-uplink-description = 防止任何人未经代码认证访问您的上行链路

comp-pda-ui-menu-title = PDA

comp-pda-ui-footer = 个人数字助手

<<<<<<< HEAD
comp-pda-ui-station = 站点: [color=white]{$station}[/color]

# Frontier: add "Sector"
comp-pda-ui-station-alert-level = 警报级别：[color={ $color }]{ $level }[/color]

comp-pda-ui-station-alert-level-instructions = 警报说明: [color=white]{ $instructions }[/color]
=======
# Mono
# comp-pda-ui-station = Station: [color=white]{$station}[/color]
comp-pda-ui-station = Sector Central: [color=white]{$station}[/color]

# Mono
# comp-pda-ui-station-alert-level = Sector Alert Level: [color={ $color }]{ $level }[/color]
comp-pda-ui-station-alert-level = Sector is at DEFCON [color={ $color }]{ $level }[/color]

comp-pda-ui-station-alert-level-instructions = Advise: [color=white]{ $instructions }[/color]
>>>>>>> upstream

comp-pda-ui-station-time = 站点当班时长：[color=white]{ $time }[/color]

comp-pda-ui-eject-id-button = 取出ID

comp-pda-ui-eject-pen-button = 取出笔

comp-pda-ui-ringtone-button = 铃声

comp-pda-ui-ringtone-button-description = 更改你的PDA铃声

comp-pda-ui-toggle-flashlight-button = 切换手电筒

pda-bound-user-interface-music-button = 音乐

pda-bound-user-interface-music-button-description = 在您的PDA上播放音乐

comp-pda-ui-unknown = 未知

comp-pda-ui-unassigned = 未注册

pda-notification-message = [font size=12][bold]PDA[/bold] { $header }: [/font]
    "{ $message }"

# Mono
comp-pda-ui-station-war-level-pre = WAR LEVEL: [color=cornflowerblue]COLD[/color]
comp-pda-ui-station-war-level-post = WAR LEVEL: [color=crimson]HOT[/color]
comp-pda-ui-station-war-level-unknown = WAR LEVEL: [color=white]UNKNOWN[/color]
