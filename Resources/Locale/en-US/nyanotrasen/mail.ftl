mail-recipient-mismatch = 收件人姓名或职务不匹配。
mail-recipient-mismatch-name = 收件人姓名不匹配。
mail-invalid-access = 收件人姓名和职务匹配，但权限不符合预期。
mail-locked = 防篡改锁尚未解除。请点击收件人的身份证。
mail-desc-far = 一件邮件包裹。
mail-desc-close = 一件寄给 {CAPITALIZE($name)}，{$job} 的邮件包裹。最后已知位置：{$station}。
mail-desc-fragile = 它贴有[color=red]红色易碎标签[/color]。
mail-desc-priority = 防篡改锁的[color=yellow]黄色优先胶带[/color]已激活。
mail-desc-priority-inactive = 防篡改锁的[color=#886600]黄色优先胶带[/color]未激活。
mail-unlocked = 防篡改系统已解锁。
mail-unlocked-by-emag = 防篡改系统 *哔滋*。
mail-unlocked-reward = 防篡改系统已解锁。{$bounty} 信用点已存入 Frontier 账户。
mail-penalty-lock = 防篡改锁被破坏。空间站银行账户被扣除 {$credits} 信用点。
mail-penalty-fragile = 完整性受损。空间站银行账户被扣除 {$credits} 信用点。
mail-penalty-expired = 投递逾期。空间站银行账户被扣除 {$credits} 信用点。
mail-item-name-unaddressed = 邮件
mail-item-name-addressed = 邮件（{$recipient}）

# Frontier: reworded description, does not need to be a container.
command-mailto-description = 将一件物品排入投递给收件人的队列。用法示例：`mailto 1234 5678 false false`。如果目标实体是容器，其内容物将被转移到实际的邮件包裹中。
# Frontier: add is-large description, container<contents
command-mailto-help = 用法：{$command} <收件人 entityUid> <内容物 entityUid> [is-fragile: true|false] [is-priority: true|false] [is-large: true|false]
command-mailto-no-mailreceiver = 目标收件人实体没有 {$requiredComponent}。
command-mailto-no-blankmail = {$blankMail} 原型不存在。出了严重问题。请联系程序员。
command-mailto-bogus-mail = {$blankMail} 没有 {$requiredMailComponent}。出了严重问题。请联系程序员。
command-mailto-invalid-container = 目标容器实体没有 {$requiredContainer} 容器。
command-mailto-unable-to-receive = 目标收件人实体无法设置为接收邮件。可能缺少 ID。
command-mailto-no-teleporter-found = 目标收件人实体无法匹配到任何空间站的邮件传送器。收件人可能不在空间站上。
command-mailto-success = 成功！邮件包裹已排入队列，将在 {$timeToTeleport} 秒后的下一次传送中发出。

# Frontier: mailto command completions
command-mailto-completion-recipient = <收件人 entityUid>
command-mailto-completion-container = <内容物 entityUid>
command-mailto-completion-fragile = [is-fragile: true|false]
command-mailto-completion-priority = [is-priority: true|false]
command-mailto-completion-large = [is-large: true|false]
# End Frontier

command-mailnow = 强制所有邮件传送器尽快再投递一轮邮件。这不会绕过未投递邮件的上限。
command-mailnow-help = 用法：{$command}
command-mailnow-success = 成功！所有邮件传送器很快将再投递一轮邮件。