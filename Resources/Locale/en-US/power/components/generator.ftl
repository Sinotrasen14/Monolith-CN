generator-clogged = {CAPITALIZE(THE($generator))} 突然关掉!

portable-generator-verb-start = 启动发电机
portable-generator-verb-start-msg-unreliable = 启动发电机。这可能需要多尝试几次。
portable-generator-verb-start-msg-reliable = 启动发电机。
portable-generator-verb-start-msg-unanchored = 发电机必须先固定好！
portable-generator-verb-stop = 停止发电机
portable-generator-start-fail = 你拉了拉绳子，但它没启动。
portable-generator-start-success = 你拉了一下绳子，它嗡嗡作响地启动了。

portable-generator-ui-title = 便携式发电机
portable-generator-ui-status-stopped = 停止:
portable-generator-ui-status-starting = 启动:
portable-generator-ui-status-running = 运行中:
portable-generator-ui-start = 启动
portable-generator-ui-stop = 停止
portable-generator-ui-target-power-label = 输出电力 (kW):
portable-generator-ui-efficiency-label = 效率:
portable-generator-ui-fuel-use-label = 燃料消耗:
portable-generator-ui-fuel-left-label = 燃料剩余:
portable-generator-ui-clogged = 在油箱里发现了污染物!
portable-generator-ui-eject = 弹出
portable-generator-ui-eta = (~{ $minutes } min)
portable-generator-ui-unanchored = 取消固定
portable-generator-ui-current-output = 当前输出: {$voltage}
portable-generator-ui-network-stats = 网络:
portable-generator-ui-network-stats-value = { POWERWATTS($supply) } / { POWERWATTS($load) }
portable-generator-ui-network-stats-not-connected = 未连接

power-switchable-generator-examine = 功率输出设置为 {$voltage}.
power-switchable-generator-switched = 已切换输出到 {$voltage}!

power-switchable-voltage = { $voltage ->
    [HV] [color=orange]HV[/color]
    [MV] [color=yellow]MV[/color]
    *[LV] [color=green]LV[/color]
}
power-switchable-switch-voltage = 切换到 {$voltage}

fuel-generator-verb-disable-on = 先关闭发电机!
