anomaly-component-contact-damage = 异常烧灼你的皮肤！

anomaly-vessel-component-anomaly-assigned = 异常分配给船舶
anomaly-vessel-component-not-assigned = 这艘船没有被分配到任何异常。试着用扫描仪扫描一下。
anomaly-vessel-component-assigned = 这艘船当前已分配到一个异常。
anomaly-vessel-component-upgrade-output = 点数输出

anomaly-particles-delta = Delta 粒子
anomaly-particles-epsilon = Epsilon 粒子
anomaly-particles-zeta = Zeta 粒子
anomaly-particles-omega = Omega 粒子
anomaly-particles-sigma = Sigma 粒子

anomaly-scanner-component-scan-complete = 扫描完成！

anomaly-scanner-ui-title = 异常扫描仪
anomaly-scanner-no-anomaly = 当前未扫描到异常。
anomaly-scanner-severity-percentage = 当前严重程度：[color=gray]{$percent}[/color]
anomaly-scanner-severity-percentage-unknown = 当前严重程度：[color=red]错误[/color]
anomaly-scanner-stability-low = 当前异常状态：[color=gold]衰减中[/color]
anomaly-scanner-stability-medium = 当前异常状态：[color=forestgreen]稳定[/color]
anomaly-scanner-stability-high = 当前异常状态：[color=crimson]增长中[/color]
anomaly-scanner-stability-unknown = 当前异常状态：[color=red]错误[/color]
anomaly-scanner-point-output = 点数输出：[color=gray]{$point}[/color]
anomaly-scanner-point-output-unknown = 点数输出：[color=red]错误[/color]
anomaly-scanner-particle-readout = 粒子反应分析：
anomaly-scanner-particle-danger = - [color=crimson]危险类型：[/color] {$type}
anomaly-scanner-particle-unstable = - [color=plum]不稳定类型：[/color] {$type}
anomaly-scanner-particle-containment = - [color=goldenrod]收容类型：[/color] {$type}
anomaly-scanner-particle-transformation = - [color=#6b75fa]转化类型：[/color] {$type}
anomaly-scanner-particle-danger-unknown = - [color=crimson]危险类型：[/color] [color=red]错误[/color]
anomaly-scanner-particle-unstable-unknown = - [color=plum]不稳定类型：[/color] [color=red]错误[/color]
anomaly-scanner-particle-containment-unknown = - [color=goldenrod]收容类型：[/color] [color=red]错误[/color]
anomaly-scanner-particle-transformation-unknown = - [color=#6b75fa]转化类型：[/color] [color=red]错误[/color]
anomaly-scanner-pulse-timer = 距离下次脉冲的时间：[color=gray]{$time}[/color]

anomaly-gorilla-core-slot-name = 异常核心
anomaly-gorilla-charge-none = 它内部没有[bold]异常核心[/bold]。
anomaly-gorilla-charge-limit = 它还剩 [color={$count ->
    [3]green
    [2]yellow
    [1]orange
    [0]red
    *[other]purple
}]{$count} {$count ->
    [one]次充能
    *[other]次充能
}[/color]。
anomaly-gorilla-charge-infinite = 它拥有[color=gold]无限充能[/color]。[italic]暂时……[/italic]

anomaly-sync-connected = 异常已成功连接
anomaly-sync-disconnected = 与异常的连接已丢失！
anomaly-sync-no-anomaly = 范围内没有异常。
anomaly-sync-examine-connected = 它已[color=darkgreen]连接[/color]到一个异常。
anomaly-sync-examine-not-connected = 它[color=darkred]未连接[/color]到任何异常。
anomaly-sync-connect-verb-text = 连接异常
anomaly-sync-connect-verb-message = 将附近的异常连接到 {THE($machine)}。

anomaly-generator-ui-title = 异常发生器
anomaly-generator-fuel-display = 燃料：
anomaly-generator-cooldown = 冷却：[color=gray]{$time}[/color]
anomaly-generator-no-cooldown = 冷却：[color=gray]完成[/color]
anomaly-generator-yes-fire = 状态：[color=forestgreen]就绪[/color]
anomaly-generator-no-fire = 状态：[color=crimson]未就绪[/color]
anomaly-generator-generate = 生成异常
anomaly-generator-charges = {$charges ->
    [one] {$charges} 次充能
    *[other] {$charges} 次充能
}
anomaly-generator-announcement = 一个异常已被生成！

anomaly-command-pulse = 脉冲一个目标异常
anomaly-command-supercritical = 使目标异常进入超临界状态

# Flavor text on the footer
anomaly-generator-flavor-left = 异常可能会在操作员体内生成。
anomaly-generator-flavor-right = v1.1

anomaly-behavior-unknown = [color=red]错误。无法读取。[/color]

anomaly-behavior-title = 行为偏差分析：
anomaly-behavior-point =[color=gold]异常产生 {$mod}% 的点数[/color] 

anomaly-behavior-safe = [color=forestgreen]异常极其稳定。脉冲极其罕见。[/color]
anomaly-behavior-slow = [color=forestgreen]脉冲频率大幅降低。[/color]
anomaly-behavior-light = [color=forestgreen]脉冲功率显著降低。[/color]
anomaly-behavior-balanced = 未检测到行为偏差。
anomaly-behavior-delayed-force = 脉冲频率大幅降低，但功率增加。
anomaly-behavior-rapid = 脉冲频率大幅提高，但强度减弱。
anomaly-behavior-reflect = 检测到保护涂层。
anomaly-behavior-nonsensivity = 检测到对粒子的微弱反应。
anomaly-behavior-sensivity = 检测到对粒子的放大反应。
anomaly-behavior-invisibility = 检测到光波畸变。
anomaly-behavior-secret = 检测到干扰。部分数据无法读取
anomaly-behavior-inconstancy = [color=crimson]检测到不稳定性。粒子类型可能随时间变化。[/color]
anomaly-behavior-fast = [color=crimson]脉冲频率强烈增加。[/color]
anomaly-behavior-strenght = [color=crimson]脉冲功率显著增加。[/color]
anomaly-behavior-moving = [color=crimson]检测到坐标不稳定。[/color]