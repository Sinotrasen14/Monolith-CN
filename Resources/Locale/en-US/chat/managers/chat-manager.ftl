### UI

chat-manager-max-message-length = 你的消息超过了 {$maxMessageLength} 个字符的限制
chat-manager-ooc-chat-enabled-message = OOC 聊天已启用。
chat-manager-ooc-chat-disabled-message = OOC 聊天已禁用。
chat-manager-looc-chat-enabled-message = LOOC 聊天已启用。
chat-manager-looc-chat-disabled-message = LOOC 聊天已禁用。
chat-manager-dead-looc-chat-enabled-message = 死亡玩家现在可以使用 LOOC。
chat-manager-dead-looc-chat-disabled-message = 死亡玩家不再可以使用 LOOC。
chat-manager-crit-looc-chat-enabled-message = 濒死玩家现在可以使用 LOOC。
chat-manager-crit-looc-chat-disabled-message = 濒死玩家不再可以使用 LOOC。
chat-manager-admin-ooc-chat-enabled-message = 管理员 OOC 聊天已启用。
chat-manager-admin-ooc-chat-disabled-message = 管理员 OOC 聊天已禁用。

chat-manager-max-message-length-exceeded-message = 你的消息超过了 {$limit} 个字符的限制
chat-manager-no-headset-on-message = 你没有佩戴耳机！
chat-manager-no-radio-key = 未指定无线电按键！
chat-manager-no-such-channel = 不存在键为“{$key}”的频道！
chat-manager-whisper-headset-on-message = 你不能通过无线电耳语！

chat-manager-server-wrap-message = [bold]{$message}[/bold]
chat-manager-sender-announcement = 中央指挥部
chat-manager-sender-announcement-wrap-message = [font size=14][bold]{$sender} 公告：[/font][font size=12]
                                                {$message}[/bold][/font]
# Einstein Engines - Language begin (changing colors for text based on language color in handler)
# For the message in double quotes, the font/color/bold/italic elements are repeated twice, outside the double quotes and inside.
# The outside elements are for formatting the double quotes, and the inside elements are for formatting the text in speech bubbles ([BubbleContent]).
chat-manager-entity-say-wrap-message = [BubbleHeader][bold][Name]{$entityName}[/Name][/bold][/BubbleHeader] {$verb}，[font={$fontType} size={$fontSize}]“[BubbleContent]{$message}[/BubbleContent]”[/font]
chat-manager-entity-say-bold-wrap-message = [BubbleHeader][bold][Name]{$entityName}[/Name][/bold][/BubbleHeader] {$verb}，[font={$fontType} size={$fontSize}]“[BubbleContent][bold]{$message}[/bold][/BubbleContent]”[/font]

chat-manager-entity-whisper-wrap-message = [font size=11][italic][BubbleHeader][Name]{$entityName}[/Name][/BubbleHeader] 低语道，“[BubbleContent]{$message}[/BubbleContent]”[/italic][/font]
chat-manager-entity-whisper-unknown-wrap-message = [font size=11][italic][BubbleHeader]某人[/BubbleHeader] 低语道，“[BubbleContent]{$message}[/BubbleContent]”[/italic][/font]
# Einstein Engines - Language end

# chat-manager-language-prefix = ({ $language }){" "} - Removed so it doesn't show up, not wanted, but part of the language system.

# THE() is not used here because the entity and its name can technically be disconnected if a nameOverride is passed...
chat-manager-entity-me-wrap-message = [italic]{ PROPER($entity) ->
    *[false] {$entityName} {$message}[/italic]
     [true] {CAPITALIZE($entityName)} {$message}[/italic]
    }

chat-manager-entity-looc-wrap-message = LOOC：[bold]{$entityName}：[/bold] {$message}
chat-manager-send-ooc-wrap-message = OOC：[bold]{$playerName}：[/bold] {$message}
chat-manager-send-ooc-patron-wrap-message = OOC：[bold][color={$patronColor}]{$playerName}[/color]：[/bold] {$message}

chat-manager-send-dead-chat-wrap-message = {$deadChannelName}：[bold][BubbleHeader]{$playerName}[/BubbleHeader]：[/bold] [BubbleContent]{$message}[/BubbleContent]
chat-manager-send-admin-dead-chat-wrap-message = {$title}：[bold]([BubbleHeader]{$userName}[/BubbleHeader])：[/bold] [BubbleContent]{$message}[/BubbleContent]
chat-manager-send-admin-chat-wrap-message = {$adminChannelName}：[bold]{$playerName}：[/bold] {$message}
chat-manager-send-admin-announcement-wrap-message = [bold]{$adminChannelName}：{$message}[/bold]

chat-manager-send-hook-ooc-wrap-message = OOC：[bold](D){$senderName}：[/bold] {$message}
chat-manager-send-hook-admin-wrap-message = ADMIN：[bold](D){$senderName}：[/bold] {$message}
chat-manager-send-hook-dead-wrap-message = ADMIN：[bold](DC) {$senderName}：[/bold] {$message}

chat-manager-dead-channel-name = 死亡
chat-manager-admin-channel-name = 管理员

chat-manager-send-collective-mind-chat-wrap-message = {$channel} 集体意识：{$message}
chat-manager-send-collective-mind-chat-wrap-message-admin = {$source}（{$channel} 集体意识）：{$message}
chat-manager-collective-mind-channel-name = 集体意识

chat-manager-rate-limited = 你发送消息的速度太快了！
chat-manager-rate-limit-admin-announcement = 速率限制警告：{ $player }

## Speech verbs for chat

chat-speech-verb-suffix-exclamation = ！
chat-speech-verb-suffix-exclamation-strong = ！！
chat-speech-verb-suffix-question = ？
chat-speech-verb-suffix-stutter = -
chat-speech-verb-suffix-mumble = 。。

chat-speech-verb-name-none = 无
chat-speech-verb-name-default = 默认
chat-speech-verb-default = 说
chat-speech-verb-name-exclamation = 惊呼
chat-speech-verb-exclamation = 惊呼道
chat-speech-verb-name-exclamation-strong = 大喊
chat-speech-verb-exclamation-strong = 大喊道
chat-speech-verb-name-question = 询问
chat-speech-verb-question = 问道
chat-speech-verb-name-stutter = 结巴
chat-speech-verb-stutter = 结巴道
chat-speech-verb-name-mumble = 嘟囔
chat-speech-verb-mumble = 嘟囔道

chat-speech-verb-name-arachnid = 蛛形
chat-speech-verb-insect-1 = 唧唧道
chat-speech-verb-insect-2 = 啾啾道
chat-speech-verb-insect-3 = 咔嗒道

chat-speech-verb-name-moth = 蛾
chat-speech-verb-winged-1 = 扑扇道
chat-speech-verb-winged-2 = 拍翼道
chat-speech-verb-winged-3 = 嗡嗡道

chat-speech-verb-name-slime = 史莱姆
chat-speech-verb-slime-1 = 咕叽道
chat-speech-verb-slime-2 = 冒泡道
chat-speech-verb-slime-3 = 渗液道

chat-speech-verb-name-plant = 迪奥娜
chat-speech-verb-plant-1 = 沙沙道
chat-speech-verb-plant-2 = 摇曳道
chat-speech-verb-plant-3 = 吱嘎道

chat-speech-verb-name-robotic = 机械
chat-speech-verb-robotic-1 = 陈述道
chat-speech-verb-robotic-2 = 哔哔道
chat-speech-verb-robotic-3 = 嘟嘟道

chat-speech-verb-name-reptilian = 爬行类
chat-speech-verb-reptilian-1 = 嘶嘶道
chat-speech-verb-reptilian-2 = 喷鼻道
chat-speech-verb-reptilian-3 = 哼气道

chat-speech-verb-name-skeleton = 骷髅
chat-speech-verb-skeleton-1 = 嘎嘎作响道
chat-speech-verb-skeleton-2 = 咔嗒道
chat-speech-verb-skeleton-3 = 咬牙道

chat-speech-verb-name-vox = 沃克斯
chat-speech-verb-vox-1 = 尖叫道
chat-speech-verb-vox-2 = 嘶叫道
chat-speech-verb-vox-3 = 呱呱道

chat-speech-verb-name-canine = 犬类
chat-speech-verb-canine-1 = 吠叫道
chat-speech-verb-canine-2 = 汪汪道
chat-speech-verb-canine-3 = 嚎叫道

chat-speech-verb-name-goat = 山羊
chat-speech-verb-goat-1 = 咩咩道
chat-speech-verb-goat-2 = 咕哝道
chat-speech-verb-goat-3 = 叫唤道

chat-speech-verb-name-small-mob = 老鼠
chat-speech-verb-small-mob-1 = 吱吱道
chat-speech-verb-small-mob-2 = 唧唧道

chat-speech-verb-name-large-mob = 鲤鱼
chat-speech-verb-large-mob-1 = 咆哮道
chat-speech-verb-large-mob-2 = 低吼道

chat-speech-verb-name-monkey = 猴子
chat-speech-verb-monkey-1 = 叽叽道
chat-speech-verb-monkey-2 = 尖叫道

chat-speech-verb-name-cluwne = 小丑

chat-speech-verb-name-parrot = 鹦鹉
chat-speech-verb-parrot-1 = 嘎嘎道
chat-speech-verb-parrot-2 = 啾啾道
chat-speech-verb-parrot-3 = 唧唧道

chat-speech-verb-cluwne-1 = 咯咯笑道
chat-speech-verb-cluwne-2 = 哈哈大笑道
chat-speech-verb-cluwne-3 = 大笑道

chat-speech-verb-name-ghost = 幽灵
chat-speech-verb-ghost-1 = 抱怨道
chat-speech-verb-ghost-2 = 呼吸道
chat-speech-verb-ghost-3 = 哼唱道
chat-speech-verb-ghost-4 = 喃喃道

chat-speech-verb-name-electricity = 电流
chat-speech-verb-electricity-1 = 噼啪道
chat-speech-verb-electricity-2 = 嗡嗡道
chat-speech-verb-electricity-3 = 尖啸道