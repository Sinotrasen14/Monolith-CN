# Displayed as initiator of vote when no user creates the vote
ui-vote-initiator-server = 服务器

## Default.Votes

ui-vote-restart-title = 重启回合
ui-vote-restart-succeeded = 重启投票成功。
ui-vote-restart-failed = 重启投票失败（需要 { TOSTRING($ratio, "P0") }）。
ui-vote-restart-fail-not-enough-ghost-players = 重启投票失败：发起重启投票至少需要 { $ghostPlayerRequirement }% 的幽灵玩家。目前幽灵玩家数量不足。
ui-vote-restart-yes = 是
ui-vote-restart-no = 否
ui-vote-restart-abstain = 弃权

ui-vote-gamemode-title = 下一个游戏模式
ui-vote-gamemode-tie = 游戏模式投票平局！正在选择…… { $picked }
ui-vote-gamemode-win = { $winner } 赢得了游戏模式投票！

ui-vote-map-title = 下一张地图
ui-vote-map-tie = 地图投票平局！正在选择…… { $picked }
ui-vote-map-win = { $winner } 赢得了地图投票！
ui-vote-map-notlobby = 地图投票仅在回合开始前的大厅中有效！
ui-vote-map-notlobby-time = 地图投票仅在回合开始前的大厅中有效，剩余 { $time }！


# Votekick votes
ui-vote-votekick-unknown-initiator = 一名玩家
ui-vote-votekick-unknown-target = 未知玩家
ui-vote-votekick-title = { $initiator } 发起了对用户 { $targetEntity } 的投票踢出。原因：{ $reason }
ui-vote-votekick-yes = 是
ui-vote-votekick-no = 否
ui-vote-votekick-abstain = 弃权
ui-vote-votekick-success = 对 { $target } 的投票踢出成功。投票踢出原因：{ $reason }
ui-vote-votekick-failure = 对 { $target } 的投票踢出失败。投票踢出原因：{ $reason }
ui-vote-votekick-not-enough-eligible = 在线合格投票者不足以发起投票踢出：{ $voters }/{ $requirement }
ui-vote-votekick-server-cancelled = 对 { $target } 的投票踢出已被服务器取消。