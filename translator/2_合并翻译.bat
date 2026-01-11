@echo off
chcp 65001
echo 正在合并翻译...
:: 使用 ss14_tracker.py 的 merge 命令
python ss14_tracker.py merge --source Resources/Prototypes --input zh.json --output Resources/Prototypes

if %errorlevel% equ 0 (
    echo 合并完成！
) else (
    echo 合并失败，请检查错误信息。
)
pause
