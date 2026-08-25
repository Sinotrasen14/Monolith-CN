### for technical and/or system messages

## General

shell-command-success = 命令执行成功
shell-invalid-command = 无效命令
shell-invalid-command-specific = 无效 {$commandName} 命令
shell-cannot-run-command-from-server = 你不能在此服务器上运行此命令
shell-only-players-can-run-this-command = 仅有玩家可以运行此命令
shell-must-be-attached-to-entity = 你必须与某个实体建立联系才能运行此命令

## Arguments

shell-need-exactly-one-argument = 需要确切参数
shell-wrong-arguments-number-need-specific = 缺少 {$properAmount} 参数， 当前参数为 {$currentAmount}.
shell-argument-must-be-number = 参数必须是数字
shell-argument-must-be-boolean = 参数必须为布尔值
shell-wrong-arguments-number = 参数数量错误
shell-need-between-arguments = Need {$lower} to {$upper} arguments!
<<<<<<< HEAD
shell-need-minimum-arguments = 需要至少 {$minimum} 参数！
shell-need-minimum-one-argument = 需要至少一个参数！
=======
shell-need-minimum-arguments = Need at least {$minimum} arguments!
shell-need-minimum-one-argument = Need at least one argument!
shell-need-exactly-zero-arguments = This command takes zero arguments.
>>>>>>> upstream

shell-argument-uid = 实体标识符

## Guards

<<<<<<< HEAD
shell-entity-is-not-mob = 目标实体不是生物！
shell-invalid-entity-id = 无效实体ID
shell-invalid-grid-id = 无效网络ID
shell-invalid-map-id = 无效映射ID
shell-invalid-entity-uid = {$uid} 不是一个有效的实体标识符
shell-invalid-bool = 无效布尔值
shell-entity-uid-must-be-number = 实体标识符必须为数字
shell-could-not-find-entity = 无法找到实体 {$entity}
shell-could-not-find-entity-with-uid = 无法找到带有此标识符 {$uid} 的实体
shell-entity-with-uid-lacks-component = 具有 {$uid} 标识符的实体缺少 {INDEFINITE($componentName)} {$componentName} 组件
shell-invalid-color-hex = 无效颜色十六进制码！
shell-target-player-does-not-exist = 目标玩家不存在！
shell-target-entity-does-not-have-message = 目标实体缺少 {INDEFINITE($missing)} {$missing}！
=======
shell-missing-required-permission = You need {$perm} for this command!
shell-entity-is-not-mob = Target entity is not a mob!
shell-invalid-entity-id = Invalid entity ID.
shell-invalid-grid-id = Invalid grid ID.
shell-invalid-map-id = Invalid map ID.
shell-invalid-entity-uid = {$uid} is not a valid entity uid
shell-invalid-bool = Invalid boolean.
shell-entity-uid-must-be-number = EntityUid must be a number.
shell-could-not-find-entity = Could not find entity {$entity}
shell-could-not-find-entity-with-uid = Could not find entity with uid {$uid}
shell-entity-with-uid-lacks-component = Entity with uid {$uid} doesn't have {INDEFINITE($componentName)} {$componentName} component
shell-entity-target-lacks-component = Target entity doesn't have {INDEFINITE($componentName)} {$componentName} component
shell-invalid-color-hex = Invalid color hex!
shell-target-player-does-not-exist = Target player does not exist!
shell-target-entity-does-not-have-message = Target entity does not have {INDEFINITE($missing)} {$missing}!
>>>>>>> upstream
shell-timespan-minutes-must-be-correct = {$span} is not a valid minutes timespan.
shell-argument-must-be-prototype = 参数 {$index} 必须是 {LOC($prototypeName)}！
shell-argument-number-must-be-between = 参数 {$index} 必须是一个介于 {$lower} 和 {$upper} 之间的数字！
shell-argument-station-id-invalid = 参数 {$index} 必须是有效的站点ID！
shell-argument-map-id-invalid = 参数 {$index} 必须是有效的映射ID！
shell-argument-number-invalid = Argument {$index} must be a valid number!

# Hints
shell-argument-username-hint = <username>
shell-argument-username-optional-hint = [username]
