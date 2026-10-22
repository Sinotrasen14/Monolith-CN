cmd-ghostrolewhitelist-ghostrole-does-not-exist = 幽灵角色 {$ghostRole} 不存在。
cmd-ghostrolewhitelist-player-not-found = 未找到玩家 {$player}。
cmd-ghostrolewhitelist-hint-player = [player]
cmd-ghostrolewhitelist-hint-ghostrole = [ghostrole]

cmd-ghostrolewhitelistadd-desc = 允许玩家扮演白名单中的幽灵角色。
cmd-ghostrolewhitelistadd-help = 用法：ghostrolewhitelistadd <username> <ghostrole>
cmd-ghostrolewhitelistadd-already-whitelisted = {$player} 已在 {$ghostRole} .({$ghostRoleName}) 的白名单中。
cmd-ghostrolewhitelistadd-added = 已将 {$player} 添加到 {$ghostRoleId}（{$ghostRoleName}）的白名单中。

cmd-ghostrolewhitelistget-desc = 获取玩家已被列入白名单的所有幽灵角色。
cmd-ghostrolewhitelistget-help = 用法：ghostrolewhitelistget <username>
cmd-ghostrolewhitelistget-whitelisted-none = 玩家 {$player} 未被列入任何角色的白名单。
cmd-ghostrolewhitelistget-whitelisted-for = "玩家 {$player} 已被列入以下角色的白名单：
{$ghostRoles}"

cmd-ghostrolewhitelistremove-desc = 移除玩家扮演白名单幽灵角色的权限。
cmd-ghostrolewhitelistremove-help = 用法：ghostrolewhitelistremove <username> <ghostrole>
cmd-ghostrolewhitelistremove-was-not-whitelisted = {$player} 未被列入 {$ghostRoleId}（{$ghostRoleName}）的白名单。
cmd-ghostrolewhitelistremove-removed = 已将 {$player} 从 {$ghostRoleId}（{$ghostRoleName}）的白名单中移除。