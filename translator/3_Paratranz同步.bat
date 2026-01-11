@echo off
chcp 65001

:: 检查是否设定了环境变量，如果没有则尝试从 config.json 读取 (通过 python 脚本逻辑)
:: 这里为了简单交互，如果环境变量没设置，还是提示用户输入

echo ==========================================
echo      Paratranz 同步工具 (ss14_tracker)
echo ==========================================

if "%PARATRANZ_TOKEN%"=="" (
    set /p PARATRANZ_TOKEN="请输入你的 Paratranz Token (留空则从 config.json 读取): "
)

echo.
echo 请选择操作:
echo 1. 上传原文 (Upload en.json)
echo 2. 下载译文 (Download zh.json)
echo.
set /p choice="请输入数字 (1 或 2): "

if "%choice%"=="1" (
    echo 正在上传...
    python ss14_tracker.py upload --file en.json
) else if "%choice%"=="2" (
    echo 正在下载...
    python ss14_tracker.py download --file zh.json --remote en.json
) else (
    echo 无效的选择
)

pause
