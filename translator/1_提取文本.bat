@echo off
chcp 65001
echo 正在提取文本...
:: 使用 ss14_tracker.py 的 extract 命令
python ss14_tracker.py extract --target_folders Resources/Prototypes --output en.json

if %errorlevel% equ 0 (
    echo 提取完成！文件已保存为 en.json
) else (
    echo 提取失败，请检查错误信息。
)
pause
