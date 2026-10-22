cmd-atvrange-desc = 设置大气调试范围（以两个浮点数表示，起点 [red] 和终点 [blue]）
cmd-atvrange-help = 用法：{$command} <start> <end>
cmd-atvrange-error-start = 起始浮点数无效
cmd-atvrange-error-end = 结束浮点数无效
cmd-atvrange-error-zero = 比例不能为零，因为这会导致 AtmosDebugOverlay 中出现除以零的错误。

cmd-atvmode-desc = 设置大气调试模式。这将自动重置比例。
cmd-atvmode-help = 用法：{$command} <TotalMoles/GasMoles/Temperature> [<gas ID (for GasMoles)>]
cmd-atvmode-error-invalid = 无效模式
cmd-atvmode-error-target-gas = 此模式必须提供目标气体。
cmd-atvmode-error-out-of-range = 气体 ID 无法解析或超出范围。
cmd-atvmode-error-info = 此模式无需进一步信息。

cmd-atvcbm-desc = 从红/绿/蓝切换为灰度
cmd-atvcbm-help = 用法：{$command} <true/false>
cmd-atvcbm-error = 无效标志