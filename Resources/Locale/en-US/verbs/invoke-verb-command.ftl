### Localization used for the invoke verb command.
# Mostly help + error messages.

invoke-verb-command-description = 以玩家实体为使用者，对某个实体调用具有给定名称的动词
invoke-verb-command-help = invokeverb <playerUid | "self"> <targetUid> <verbName | "interaction" | "activation" | "alternative">

invoke-verb-command-invalid-args = invokeverb 接受 2 个参数。

invoke-verb-command-invalid-player-uid = 无法解析玩家 uid，或未传入 "self"。
invoke-verb-command-invalid-target-uid = 无法解析目标 uid。

invoke-verb-command-invalid-player-entity = 给定的玩家 uid 不对应有效实体。
invoke-verb-command-invalid-target-entity = 给定的目标 uid 不对应有效实体。

invoke-verb-command-success = 已以 { $player } 为使用者，对 { $target } 调用动词“{ $verb }”。

invoke-verb-command-verb-not-found = 在 { $target } 上找不到动词 { $verb }。