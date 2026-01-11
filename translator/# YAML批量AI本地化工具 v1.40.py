# YAML批量AI本地化工具 v1.40 (ruamel.yaml版 - 保留注释和格式)

import os
import sys
import json
import threading
import time
import shutil
import requests
import subprocess
import webbrowser
import platform
import io
from collections import deque
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional, Dict, List, Tuple, Any, Callable
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext, Menu

# 使用 ruamel.yaml 替代 PyYAML 以保留注释和格式
try:
    from ruamel.yaml import YAML
    from ruamel.yaml.comments import CommentedMap, CommentedSeq
    from ruamel.yaml.constructor import RoundTripConstructor
    from ruamel.yaml.representer import RoundTripRepresenter
    HAS_RUAMEL = True
except ImportError:
    HAS_RUAMEL = False
    # 回退到 PyYAML
    import yaml

# ==================== 修复 Windows DPI 模糊问题 ====================
try:
    from ctypes import windll
    try:
        windll.user32.SetProcessDPIAware()
    except AttributeError:
        windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass

# ==================== 检测拖拽支持 ====================
HAS_DND = False
TkinterDnD = None
DND_FILES = None

try:
    from tkinterdnd2 import DND_FILES as _DND_FILES, TkinterDnD as _TkinterDnD
    TkinterDnD = _TkinterDnD
    DND_FILES = _DND_FILES
    HAS_DND = True
except ImportError:
    pass

VERSION = "1.40"
APP_TITLE = f"YAML批量AI本地化工具 v{VERSION}"

# ==================== 统一说明文本 ====================
APP_DESCRIPTION = """一个专业的 YAML 文件批量翻译工具

主要特性:
• 支持主流AI平台API (OpenAI, DeepSeek, Qwen, Claude等)
• 使用 ruamel.yaml 保留注释、空行和原始格式
• 批量翻译模式，减少API调用次数
• 翻译前预览，查看待翻译内容统计
• 支持双语输出模式
• 自动生成翻译对比报告"""

# ==================== 平台预设库 ====================
PLATFORM_PRESETS = {
    'openai': {
        'name': 'OpenAI',
        'url': 'https://api.openai.com/v1/chat/completions',
        'models': ['gpt-4-turbo-preview', 'gpt-4', 'gpt-3.5-turbo'],
        'default_model': 'gpt-3.5-turbo',
        'docs_url': 'https://platform.openai.com/docs'
    },
    'deepseek': {
        'name': 'DeepSeek',
        'url': 'https://api.deepseek.com/v1/chat/completions',
        'models': ['deepseek-chat', 'deepseek-coder'],
        'default_model': 'deepseek-chat',
        'docs_url': 'https://platform.deepseek.com/docs'
    },
    'qwen': {
        'name': 'Qwen',
        'url': 'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions',
        'models': ['qwen-turbo', 'qwen-plus', 'qwen-max'],
        'default_model': 'qwen-turbo',
        'docs_url': 'https://help.aliyun.com/zh/dashscope/'
    },
    'claude': {
        'name': 'Claude',
        'url': 'https://api.anthropic.com/v1/messages',
        'models': ['claude-3-opus', 'claude-3-sonnet', 'claude-3-haiku'],
        'default_model': 'claude-3-sonnet',
        'docs_url': 'https://docs.anthropic.com/claude/reference/getting-started-with-the-api'
    },
    'custom': {
        'name': 'Custom',
        'url': '',
        'models': [],
        'default_model': '',
        'docs_url': ''
    }
}

# 默认提示词
DEFAULT_PROMPT = """请将以下英文翻译为中文,如果已经为中文则不翻译。\n\n重要规则：\n1. 只返回翻译结果，不要包含其他内容\n3. 如果使用引号，用中文引号“”‘’代替\n4. 避免在翻译结果中使用英文冒号:，使用中文冒号：代替"""

# ==================== 工具函数 ====================

def open_path_in_os(path: str):
    """跨平台打开文件或文件夹"""
    try:
        if platform.system() == 'Windows':
            os.startfile(path)
        elif platform.system() == 'Darwin':  # macOS
            subprocess.call(['open', path])
        else:  # Linux
            subprocess.call(['xdg-open', path])
    except Exception as e:
        print(f"无法打开路径 {path}: {e}")

# ==================== 数据类定义 ====================

@dataclass
class FieldRule:
    """字段翻译规则"""
    field_name: str
    enabled: bool = True
    priority: int = 0
    context_fields: List[str] = field(default_factory=list)


@dataclass
class TranslationConfig:
    """翻译配置"""
    skip_chinese: bool = True
    api_timeout: int = 30
    enable_retry: bool = True
    max_retries: int = 3
    retry_delay: int = 5
    output_mode: str = 'export'
    output_folder: str = ''
    keep_structure: bool = True
    add_language_tag: bool = True
    language_tag: str = '_zh_CN'
    tag_position: str = 'end'
    enable_bilingual: bool = False
    bilingual_separator: str = ' | '
    bilingual_order: str = 'cn_first'
    # 批量翻译配置
    enable_batch_translation: bool = True
    batch_size: int = 10  # 每批翻译的文本数量
    batch_separator: str = '\n---SPLIT---\n'  # 批量翻译时的分隔符
    field_rules: List[FieldRule] = field(default_factory=lambda: [
        FieldRule('name', True, 1, ['description', 'tooltip']),
        FieldRule('description', True, 2, ['name']),
        FieldRule('tooltip', True, 3, ['name', 'description']),
        FieldRule('title', True, 4, []),
        FieldRule('label', True, 5, []),
    ])


# ==================== 优化的速率限制器 ====================

class RateLimiter:
    """优化的速率限制器 - 使用 deque 提高性能，不在锁内sleep"""
    
    def __init__(self, max_requests: int = 10, time_window: int = 60):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = deque()
        self.lock = threading.Lock()
    
    def wait_if_needed(self):
        """如果超出限制则等待"""
        sleep_time = 0
        
        with self.lock:
            now = time.time()
            
            # 移除过期的请求记录
            while self.requests and now - self.requests[0] >= self.time_window:
                self.requests.popleft()
            
            # 检查是否需要等待
            if len(self.requests) >= self.max_requests:
                sleep_time = self.time_window - (now - self.requests[0]) + 0.1
        
        # 在锁外等待
        if sleep_time > 0:
            time.sleep(sleep_time)
        
        # 重新获取锁添加记录
        with self.lock:
            now = time.time()
            while self.requests and now - self.requests[0] >= self.time_window:
                self.requests.popleft()
            self.requests.append(now)


# ==================== YAML 处理器 (ruamel.yaml 版本) ====================

class YAMLProcessor:
    """
    YAML 处理器 - 使用 ruamel.yaml 保留注释、格式和自定义标签
    如果 ruamel.yaml 不可用，则回退到 PyYAML
    """
    
    _instance = None
    _yaml = None
    
    @classmethod
    def get_instance(cls) -> 'YAMLProcessor':
        """获取单例实例"""
        if cls._instance is None:
            cls._instance = YAMLProcessor()
        return cls._instance
    
    def __init__(self):
        if HAS_RUAMEL:
            self._yaml = YAML()
            self._yaml.preserve_quotes = True  # 保留引号样式
            self._yaml.width = 4096  # 防止自动换行
            self._yaml.default_flow_style = None  # 保留原始流式样式
            # 允许重复的键（某些YAML文件可能有）
            self._yaml.allow_duplicate_keys = True
        else:
            self._yaml = None
    
    def load(self, file_path: str) -> Any:
        """
        加载 YAML 文件
        
        Args:
            file_path: 文件路径
            
        Returns:
            解析后的数据
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            if HAS_RUAMEL:
                return self._yaml.load(f)
            else:
                return yaml.load(f, Loader=yaml.SafeLoader)
    
    def load_from_string(self, content: str) -> Any:
        """从字符串加载 YAML"""
        if HAS_RUAMEL:
            return self._yaml.load(io.StringIO(content))
        else:
            return yaml.safe_load(content)
    
    def dump(self, data: Any, file_path: str) -> None:
        """
        保存 YAML 文件（保留原始格式）
        
        Args:
            data: 要保存的数据
            file_path: 文件路径
        """
        with open(file_path, 'w', encoding='utf-8') as f:
            if HAS_RUAMEL:
                self._yaml.dump(data, f)
            else:
                yaml.dump(data, f, allow_unicode=True, sort_keys=False, 
                         default_flow_style=False, indent=2)
    
    def dump_to_string(self, data: Any) -> str:
        """将数据转换为 YAML 字符串"""
        stream = io.StringIO()
        if HAS_RUAMEL:
            self._yaml.dump(data, stream)
        else:
            yaml.dump(data, stream, allow_unicode=True, sort_keys=False,
                     default_flow_style=False, indent=2)
        return stream.getvalue()
    
    @staticmethod
    def is_ruamel_available() -> bool:
        """检查 ruamel.yaml 是否可用"""
        return HAS_RUAMEL


# 为了向后兼容，保留旧的类名（但现在它们不再使用）
class TaggedValue:
    """保存带有 YAML 标签的值（兼容性保留）"""
    def __init__(self, tag: str, value):
        self.tag = tag
        self.value = value
    
    def __repr__(self):
        return f"TaggedValue({self.tag}, {self.value})"

class FlowStyleList(list):
    """标记需要使用流式格式的列表（兼容性保留）"""
    pass

# PyYAML 回退支持（当 ruamel.yaml 不可用时）
if not HAS_RUAMEL:
    class CustomYAMLLoader(yaml.SafeLoader):
        """PyYAML 回退加载器"""
        pass

    def _multi_constructor(loader, tag_suffix, node):
        full_tag = '!' + tag_suffix
        if isinstance(node, yaml.MappingNode):
            value = loader.construct_mapping(node)
            return TaggedValue(full_tag, value)
        elif isinstance(node, yaml.SequenceNode):
            value = loader.construct_sequence(node)
            return TaggedValue(full_tag, value)
        else:
            value = loader.construct_scalar(node)
            return TaggedValue(full_tag, value)

    def _construct_yaml_seq(loader, node):
        value = loader.construct_sequence(node)
        if node.flow_style:
            return FlowStyleList(value)
        return value

    CustomYAMLLoader.add_multi_constructor('!', _multi_constructor)
    CustomYAMLLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_SEQUENCE_TAG, _construct_yaml_seq)

    class CustomYAMLDumper(yaml.SafeDumper):
        """PyYAML 回退输出器"""
        pass

    def _represent_tagged_value(dumper, data):
        if isinstance(data.value, dict):
            return dumper.represent_mapping(data.tag, data.value)
        elif isinstance(data.value, list):
            return dumper.represent_sequence(data.tag, data.value)
        else:
            return dumper.represent_scalar(data.tag, str(data.value) if data.value else '')

    def _represent_flow_list(dumper, data):
        return dumper.represent_sequence('tag:yaml.org,2002:seq', data, flow_style=True)

    CustomYAMLDumper.add_representer(TaggedValue, _represent_tagged_value)
    CustomYAMLDumper.add_representer(FlowStyleList, _represent_flow_list)


# ==================== 核心翻译器 ====================

class UniversalTranslator:
    """通用翻译器 - 支持多平台API"""
    
    # 特殊字符集合
    SPECIAL_CHARS = frozenset(':{}[],&*#?|-<>=!%@`')
    
    def __init__(self, api_config: Dict[str, Any], rate_limiter: RateLimiter):
        self.config = api_config
        self.platform = api_config.get('platform', 'deepseek')
        self.api_key = api_config['api_key']
        self.model = api_config.get('model', 'deepseek-chat')
        self.base_url = api_config.get('url', PLATFORM_PRESETS.get(self.platform, {}).get('url', ''))
        self.temperature = api_config.get('temperature', 0.3)
        self.max_tokens = api_config.get('max_tokens', 1000)
        self.rate_limiter = rate_limiter
        self.lock = threading.Lock()
        self.retry_config = {
            'max_retries': api_config.get('max_retries', 3),
            'retry_delay': api_config.get('retry_delay', 5)
        }
    
    def _build_prompt(self, text: str, context_info: Optional[Dict] = None) -> str:
        """构建翻译提示词"""
        base_prompt = self.config.get('custom_prompt', DEFAULT_PROMPT)
        
        if not context_info:
            return f"{base_prompt}\n\n待翻译文本：{text}"
        
        # 构建上下文信息
        context_parts = []
        if context_info.get('field_name'):
            context_parts.append(f"字段名: {context_info['field_name']}")
        
        if context_info.get('related_fields'):
            related = context_info['related_fields']
            if related:
                context_parts.append("相关字段:")
                for field_name, field_value in related.items():
                    context_parts.append(f"  - {field_name}: {field_value}")
        
        if context_parts:
            context_str = "\n".join(context_parts)
            return f"{base_prompt}\n\n上下文信息：\n{context_str}\n\n待翻译文本：{text}"
        
        return f"{base_prompt}\n\n待翻译文本：{text}"
    
    def _make_request(self, prompt: str, timeout: int) -> Tuple[Optional[str], Optional[str]]:
        """发送API请求"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": self.temperature,
            "max_tokens": self.max_tokens
        }
        
        try:
            with self.lock:
                time.sleep(0.1)
            
            response = requests.post(self.base_url, headers=headers, json=data, timeout=timeout)
            response.raise_for_status()
            result = response.json()
            
            translated_text = result['choices'][0]['message']['content'].strip()
            return translated_text, None
            
        except requests.exceptions.Timeout:
            return None, "请求超时"
        except requests.exceptions.ConnectionError as e:
            return None, f"连接错误: {str(e)}"
        except requests.exceptions.HTTPError as e:
            return None, f"HTTP错误: {str(e)}"
        except (KeyError, IndexError) as e:
            return None, f"响应格式错误: {str(e)}"
        except Exception as e:
            return None, f"未知错误: {str(e)}"
    
    def clean_translated_text(self, text: str) -> str:
        """智能清理翻译后的文本"""
        if not text:
            return text
        
        double_quotes = text.count('"')
        single_quotes = text.count("'")
        
        if double_quotes < 2 and single_quotes < 2:
            return text
        
        quote_positions = []
        for i, char in enumerate(text):
            if char in ['"', "'"]:
                quote_positions.append(i)
                if len(quote_positions) >= 2:
                    break
        
        if len(quote_positions) >= 2:
            second_quote_pos = quote_positions[1]
            before = text[:second_quote_pos + 1]
            after = text[second_quote_pos + 1:]
            after = after.replace('"', '').replace("'", '').replace(':', '：')
            return before + after
        
        return text
    
    def translate(self, text: str, context_info: Optional[Dict] = None, 
                  timeout: int = 30) -> Tuple[str, Optional[str]]:
        """翻译文本 - 带重试机制"""
        self.rate_limiter.wait_if_needed()
        
        prompt = self._build_prompt(text, context_info)
        
        max_retries = self.retry_config['max_retries']
        retry_delay = self.retry_config['retry_delay']
        
        for attempt in range(max_retries):
            translated_text, error = self._make_request(prompt, timeout)
            
            if error is None and translated_text:
                translated_text = self.clean_translated_text(translated_text)
                return translated_text, None
            
            if attempt < max_retries - 1:
                time.sleep(retry_delay * (attempt + 1))
                continue
            
            return text, error or "翻译失败"
        
        return text, "翻译失败"
    
    def test_connection(self) -> Tuple[bool, str]:
        """测试API连接"""
        try:
            test_text = "Hello"
            start_time = time.time()
            result, error = self.translate(test_text, timeout=10)
            elapsed = time.time() - start_time
            
            if error:
                return False, f"翻译失败: {error}"
            
            if result and result != test_text:
                if elapsed > 5:
                    return True, f"测试成功但响应较慢: \"{test_text}\" → \"{result}\" (耗时 {elapsed:.2f}秒)"
                else:
                    return True, f"测试成功: \"{test_text}\" → \"{result}\" (耗时 {elapsed:.2f}秒)"
            else:
                return False, "API响应异常"
                
        except Exception as e:
            return False, f"连接失败: {str(e)}"
    
    def translate_batch(self, texts: List[str], separator: str = '\n---SPLIT---\n',
                        timeout: int = 60) -> Tuple[List[str], Optional[str]]:
        """批量翻译多条文本 - 合并为一次API调用"""
        if not texts:
            return [], None
        
        self.rate_limiter.wait_if_needed()
        
        # 构建批量翻译的提示词
        base_prompt = self.config.get('custom_prompt', DEFAULT_PROMPT)
        numbered_texts = []
        for i, text in enumerate(texts, 1):
            numbered_texts.append(f"[{i}] {text}")
        
        combined_text = '\n'.join(numbered_texts)
        
        batch_prompt = f"""{base_prompt}

请翻译以下多条文本，每条文本以编号 [数字] 开头。
请逐条翻译，返回格式保持为 [数字] 翻译内容，每条占一行。
只返回翻译结果，不要添加任何分隔符、解释或其他内容。

{combined_text}"""
        
        max_retries = self.retry_config['max_retries']
        retry_delay = self.retry_config['retry_delay']
        
        for attempt in range(max_retries):
            translated_text, error = self._make_request(batch_prompt, timeout)
            
            if error is None and translated_text:
                # 解析批量翻译结果
                results = self._parse_batch_result(translated_text, len(texts))
                if len(results) == len(texts):
                    return [self.clean_translated_text(r) for r in results], None
                else:
                    # 解析数量不匹配，返回原文
                    return texts, f"批量翻译结果解析失败 (期望{len(texts)}条，得到{len(results)}条)"
            
            if attempt < max_retries - 1:
                time.sleep(retry_delay * (attempt + 1))
                continue
            
            return texts, error or "批量翻译失败"
        
        return texts, "批量翻译失败"
    
    def _parse_batch_result(self, result: str, expected_count: int) -> List[str]:
        """解析批量翻译结果"""
        import re
        results = []
        
        # 方法1: 尝试按编号解析 [1] [2] [3] ...（逐行匹配，避免贪婪匹配问题）
        lines = result.strip().split('\n')
        numbered_results = {}
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            # 匹配 [数字] 开头的行
            match = re.match(r'^\[(\d+)\]\s*(.+)$', line)
            if match:
                num = int(match.group(1))
                content = match.group(2).strip()
                if 1 <= num <= expected_count:
                    numbered_results[num] = content
        
        # 如果成功按编号解析到足够数量的结果
        if len(numbered_results) == expected_count:
            results = [numbered_results[i] for i in range(1, expected_count + 1)]
            return results
        
        # 方法2: 尝试按非空行顺序解析（移除可能的编号前缀）
        cleaned_lines = []
        for line in lines:
            line = line.strip()
            if not line:
                continue
            # 移除 [数字] 或 数字. 或 数字) 或 数字: 等前缀
            cleaned = re.sub(r'^[\[（\(]?\d+[\]）\)\.\:：]?\s*', '', line)
            if cleaned:
                cleaned_lines.append(cleaned)
        
        if len(cleaned_lines) == expected_count:
            results = cleaned_lines
        
        return results

    @staticmethod
    def fetch_available_models(platform_id: str, api_key: str, base_url: str, 
                               timeout: int = 15) -> Tuple[Optional[List[str]], Optional[str]]:
        """从API获取可用模型列表"""
        try:
            if not api_key or not base_url:
                return None, "API Key 或 URL 不能为空"
            
            if '/chat/completions' in base_url:
                models_url = base_url.replace('/chat/completions', '/models')
            elif '/v1/' in base_url:
                base = base_url.rsplit('/v1/', 1)[0]
                models_url = f"{base}/v1/models"
            else:
                models_url = base_url.rstrip('/') + '/models'
            
            headers = {"Authorization": f"Bearer {api_key}"}
            response = requests.get(models_url, headers=headers, timeout=timeout)
            response.raise_for_status()
            
            data = response.json()
            model_objects = data.get('data', [])
            if not model_objects and isinstance(data, list):
                model_objects = data
            
            model_ids = sorted([model['id'] for model in model_objects if 'id' in model])
            
            if not model_ids:
                return None, "未能从API响应中找到模型列表"
            
            return model_ids, None
            
        except requests.exceptions.RequestException as e:
            return None, f"网络错误: {str(e)}"
        except Exception as e:
            return None, f"获取模型失败: {str(e)}"


# ==================== 字段提取器 ====================

class FieldExtractor:
    """字段提取器 - 负责从YAML数据中提取需要翻译的字段"""
    
    def __init__(self, field_rules: List[FieldRule]):
        self.field_rules = {rule.field_name: rule for rule in field_rules if rule.enabled}
        self.field_priorities = {name: rule.priority for name, rule in self.field_rules.items()}
    
    def should_translate(self, field_name: str) -> bool:
        """判断字段是否需要翻译"""
        return field_name in self.field_rules
    
    def get_context_fields(self, field_name: str) -> List[str]:
        """获取字段的上下文字段列表"""
        rule = self.field_rules.get(field_name)
        return rule.context_fields if rule else []
    
    def extract_fields(self, data: Any, path_prefix: str = '') -> List[Dict[str, Any]]:
        """提取所有需要翻译的字段
        
        支持 ruamel.yaml 的 CommentedMap/CommentedSeq 和标准 dict/list
        """
        fields = []
        
        # 检查是否是映射类型（dict 或 CommentedMap）
        if hasattr(data, 'items') and hasattr(data, '__getitem__'):
            for key, value in data.items():
                current_path = f"{path_prefix}.{key}" if path_prefix else key
                
                if self.should_translate(key) and isinstance(value, str) and value.strip():
                    fields.append({
                        'path': current_path,
                        'field_name': key,
                        'value': value,
                        'parent': data,
                        'priority': self.field_priorities.get(key, 999)
                    })
                elif hasattr(value, 'items') or isinstance(value, list):
                    fields.extend(self.extract_fields(value, current_path))
        
        # 检查是否是序列类型（list 或 CommentedSeq）
        elif isinstance(data, list):
            for i, item in enumerate(data):
                current_path = f"{path_prefix}[{i}]"
                if hasattr(item, 'items') or isinstance(item, list):
                    fields.extend(self.extract_fields(item, current_path))
        
        fields.sort(key=lambda x: x['priority'])
        return fields
    
    def build_context(self, field_info: Dict[str, Any], all_fields: List[Dict[str, Any]]) -> Dict[str, Any]:
        """为字段构建上下文信息"""
        context = {
            'field_name': field_info['field_name'],
            'related_fields': {}
        }
        
        context_field_names = self.get_context_fields(field_info['field_name'])
        if not context_field_names:
            return context
        
        parent = field_info['parent']
        if not isinstance(parent, dict):
            return context
        
        for context_field_name in context_field_names:
            if context_field_name in parent and isinstance(parent[context_field_name], str):
                value = parent[context_field_name].strip()
                if value:
                    context['related_fields'][context_field_name] = value
        
        return context


# ==================== YAML翻译核心 ====================

class YamlTranslatorCore:
    """YAML翻译核心"""
    
    def __init__(self, api_config: Dict[str, Any], translation_config: TranslationConfig,
                 max_threads: int = 4, progress_callback: Callable = None, 
                 log_callback: Callable = None, translation_callback: Callable = None):
        
        self.rate_limiter = RateLimiter(max_requests=10, time_window=60)
        self.translator = UniversalTranslator(api_config, self.rate_limiter)
        self.config = translation_config
        self.field_extractor = FieldExtractor(translation_config.field_rules)
        
        self.max_threads = max_threads
        self.progress_callback = progress_callback
        self.log_callback = log_callback
        self.translation_callback = translation_callback
        
        self.stop_flag = threading.Event()
        self.translation_records = []
        self.stats_lock = threading.Lock()
        
        self.stats = {
            'total_files': 0,
            'processed_files': 0,
            'total_translations': 0,
            'successful_translations': 0,
            'failed_translations': 0,
            'skipped_translations': 0,
            'start_time': None,
            'end_time': None
        }
    
    def log(self, message: str, level: str = "INFO"):
        """记录日志"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_msg = f"[{timestamp}] [{level}] {message}"
        if self.log_callback:
            self.log_callback(formatted_msg)
        print(formatted_msg)
    
    def update_progress(self, current: int, total: int, status: str = ""):
        """更新进度"""
        if self.progress_callback:
            self.progress_callback(current, total, status)
    
    def record_translation(self, file_path: str, field_path: str, original: str, 
                          translated: str, status: str):
        """记录翻译详情"""
        self.translation_records.append({
            'file': file_path,
            'field': field_path,
            'original': original,
            'translated': translated,
            'status': status,
            'timestamp': datetime.now().isoformat()
        })
    
    def contains_chinese(self, text: str) -> bool:
        """检查是否包含中文"""
        return any('\u4e00' <= char <= '\u9fff' for char in str(text))
    
    def find_yaml_files(self, path: str) -> List[str]:
        """查找YAML文件"""
        yaml_files = []
        
        if os.path.isfile(path):
            if path.lower().endswith(('.yml', '.yaml')):
                yaml_files.append(path)
        else:
            for root, dirs, files in os.walk(path):
                for file in files:
                    if file.lower().endswith(('.yml', '.yaml')):
                        yaml_files.append(os.path.join(root, file))
        
        return yaml_files
    
    def get_output_path(self, original_path: str, base_folder: str) -> str:
        """获取输出文件路径"""
        if self.config.output_mode == 'overwrite':
            backup_path = original_path + '.backup'
            if not os.path.exists(backup_path):
                try:
                    shutil.copy2(original_path, backup_path)
                    self.log(f"已创建备份文件: {os.path.basename(backup_path)}", "INFO")
                except Exception as e:
                    self.log(f"备份创建失败: {e}", "WARNING")
            return original_path
        
        output_folder = self.config.output_folder or os.path.join(
            os.path.dirname(original_path), 'translated'
        )
        
        if self.config.keep_structure:
            rel_path = os.path.relpath(original_path, base_folder)
            output_path = os.path.join(output_folder, rel_path)
        else:
            filename = os.path.basename(original_path)
            output_path = os.path.join(output_folder, filename)
        
        if self.config.add_language_tag and self.config.language_tag:
            dir_name = os.path.dirname(output_path)
            filename = os.path.basename(output_path)
            name, ext = os.path.splitext(filename)
            
            tag = self.config.language_tag
            if self.config.tag_position == 'before_ext':
                new_filename = f"{name}.{tag.lstrip('_')}{ext}"
            else:
                new_filename = f"{name}{tag}{ext}"
            
            output_path = os.path.join(dir_name, new_filename)
        
        try:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
        except Exception as e:
            self.log(f"输出目录创建失败: {e}", "ERROR")
        
        return output_path
    
    def translate_fields(self, fields: List[Dict[str, Any]], file_path: str) -> Tuple[int, int, int]:
        """翻译提取的字段列表 - 支持批量翻译模式"""
        successful = 0
        skipped = 0
        failed = 0
        
        # 分离需要翻译和跳过的字段
        to_translate = []
        for field_info in fields:
            if self.stop_flag.is_set():
                break
            
            original_value = field_info['value']
            
            if self.config.skip_chinese and self.contains_chinese(original_value):
                skipped += 1
                self.record_translation(file_path, field_info['path'], original_value, original_value, 'skipped')
            else:
                to_translate.append(field_info)
        
        if not to_translate:
            return successful, skipped, failed
        
        # 判断是否使用批量翻译
        enable_batch = getattr(self.config, 'enable_batch_translation', True)
        batch_size = getattr(self.config, 'batch_size', 10)
        batch_separator = getattr(self.config, 'batch_separator', '\n---SPLIT---\n')
        
        if enable_batch and len(to_translate) > 1:
            # 批量翻译模式
            successful, failed = self._translate_batch_mode(
                to_translate, file_path, batch_size, batch_separator
            )
        else:
            # 单条翻译模式
            successful, failed = self._translate_single_mode(to_translate, file_path)
        
        return successful, skipped, failed
    
    def _translate_batch_mode(self, fields: List[Dict[str, Any]], file_path: str,
                              batch_size: int, separator: str) -> Tuple[int, int]:
        """批量翻译模式"""
        successful = 0
        failed = 0
        
        # 分批处理
        for i in range(0, len(fields), batch_size):
            if self.stop_flag.is_set():
                break
            
            batch = fields[i:i + batch_size]
            texts = [f['value'] for f in batch]
            
            self.log(f"批量翻译: 第 {i//batch_size + 1} 批 ({len(batch)} 条)", "INFO")
            
            # 执行批量翻译
            translated_texts, error = self.translator.translate_batch(
                texts, separator, self.config.api_timeout * 2  # 批量翻译超时时间加倍
            )
            
            if error:
                self.log(f"批量翻译失败，回退到单条模式: {error}", "WARNING")
                # 回退到单条翻译
                s, f = self._translate_single_mode(batch, file_path)
                successful += s
                failed += f
            else:
                # 应用翻译结果
                for j, (field_info, translated) in enumerate(zip(batch, translated_texts)):
                    field_name = field_info['field_name']
                    field_path = field_info['path']
                    original_value = field_info['value']
                    parent = field_info['parent']
                    
                    if translated and translated != original_value:
                        successful += 1
                        if self.translation_callback:
                            self.translation_callback(original_value, translated)
                        
                        # 应用双语设置
                        if self.config.enable_bilingual:
                            sep = self.config.bilingual_separator
                            if self.config.bilingual_order == 'cn_first':
                                parent[field_name] = f"{translated}{sep}{original_value}"
                            else:
                                parent[field_name] = f"{original_value}{sep}{translated}"
                        else:
                            parent[field_name] = translated
                        
                        self.record_translation(file_path, field_path, original_value, parent[field_name], 'success')
                    else:
                        failed += 1
                        self.record_translation(file_path, field_path, original_value, original_value, 'failed')
        
        return successful, failed
    
    def _translate_single_mode(self, fields: List[Dict[str, Any]], file_path: str) -> Tuple[int, int]:
        """单条翻译模式"""
        successful = 0
        failed = 0
        
        for field_info in fields:
            if self.stop_flag.is_set():
                break
            
            field_name = field_info['field_name']
            field_path = field_info['path']
            original_value = field_info['value']
            parent = field_info['parent']
            
            context = self.field_extractor.build_context(field_info, fields)
            
            translated_value, error = self.translator.translate(
                original_value, context, self.config.api_timeout
            )
            
            if error:
                failed += 1
                self.log(f"翻译失败: {field_path} - {error}", "ERROR")
                self.record_translation(file_path, field_path, original_value, original_value, 'failed')
            else:
                successful += 1
                if self.translation_callback:
                    self.translation_callback(original_value, translated_value)
                
                if self.config.enable_bilingual and translated_value != original_value:
                    sep = self.config.bilingual_separator
                    if self.config.bilingual_order == 'cn_first':
                        parent[field_name] = f"{translated_value}{sep}{original_value}"
                    else:
                        parent[field_name] = f"{original_value}{sep}{translated_value}"
                else:
                    parent[field_name] = translated_value
                
                self.record_translation(file_path, field_path, original_value, parent[field_name], 'success')
        
        return successful, failed
    
    def process_yaml_file(self, file_path: str, base_folder: str):
        """处理单个YAML文件 - 使用 ruamel.yaml 保留注释和格式"""
        if self.stop_flag.is_set():
            return
        
        file_name = os.path.basename(file_path)
        self.log(f"处理文件: {file_name}")
        
        yaml_processor = YAMLProcessor.get_instance()
        
        try:
            # 使用 YAMLProcessor 加载（保留注释和格式）
            data = yaml_processor.load(file_path)
            
            if data is None:
                self.log(f"文件为空或格式不正确: {file_name}", "WARNING")
                return
            
            fields = self.field_extractor.extract_fields(data)
            
            if not fields:
                self.log(f"未找到需要翻译的字段: {file_name}", "INFO")
                return
            
            self.log(f"找到 {len(fields)} 个待翻译字段", "INFO")
            
            successful, skipped, failed = self.translate_fields(fields, file_path)
            
            output_path = self.get_output_path(file_path, base_folder)
            
            # 使用 YAMLProcessor 保存（保留原始格式）
            yaml_processor.dump(data, output_path)
            
            with self.stats_lock:
                self.stats['processed_files'] += 1
                self.stats['successful_translations'] += successful
                self.stats['skipped_translations'] += skipped
                self.stats['failed_translations'] += failed
            
            total_actions = successful + skipped + failed
            if output_path != file_path:
                self.log(f"完成: {file_name} → {os.path.basename(output_path)} (处理 {total_actions} 项)", "SUCCESS")
            else:
                self.log(f"完成: {file_name} (处理 {total_actions} 项)", "SUCCESS")
            
        except Exception as e:
            error_type = type(e).__name__
            self.log(f"处理失败 {file_name} [{error_type}]: {str(e)[:100]}", "ERROR")
    
    def translate_files(self, file_paths: List[str], base_folder: str = None) -> Dict[str, Any]:
        """翻译文件列表"""
        self.stop_flag.clear()
        self.translation_records = []
        self.stats = {
            'total_files': len(file_paths),
            'processed_files': 0,
            'total_translations': 0,
            'successful_translations': 0,
            'failed_translations': 0,
            'skipped_translations': 0,
            'start_time': datetime.now(),
            'end_time': None
        }
        
        if not base_folder:
            if len(file_paths) == 1:
                base_folder = os.path.dirname(file_paths[0])
            else:
                try:
                    base_folder = os.path.commonpath(file_paths)
                except ValueError:
                    base_folder = os.path.dirname(file_paths[0])
        
        self.log(f"开始翻译 {len(file_paths)} 个文件")
        self.log(f"线程数: {self.max_threads}")
        self.log(f"输出模式: {'覆盖源文件' if self.config.output_mode == 'overwrite' else '导出到新文件夹'}")
        
        if self.config.enable_bilingual:
            order_text = "中文在前" if self.config.bilingual_order == 'cn_first' else "原文在前"
            sep = self.config.bilingual_separator
            self.log(f"双语输出: 已启用 ({order_text}，分隔符: '{sep}')")
        
        enabled_fields = [rule.field_name for rule in self.config.field_rules if rule.enabled]
        self.log(f"翻译字段: {', '.join(enabled_fields)}")
        self.log("=" * 60)
        
        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            future_to_file = {
                executor.submit(self.process_yaml_file, fp, base_folder): fp 
                for fp in file_paths
            }
            
            completed = 0
            for future in as_completed(future_to_file):
                if self.stop_flag.is_set():
                    break
                try:
                    future.result()
                except Exception as e:
                    self.log(f"线程执行错误: {e}", "ERROR")
                completed += 1
                self.update_progress(completed, len(file_paths), f"处理中: {completed}/{len(file_paths)}")
        
        self.stats['end_time'] = datetime.now()
        elapsed = (self.stats['end_time'] - self.stats['start_time']).total_seconds()
        self.stats['duration'] = elapsed
        
        self.log("=" * 60)
        self.log(f"翻译完成！", "SUCCESS")
        self.log(f"处理文件: {self.stats['processed_files']}/{self.stats['total_files']}")
        self.log(f"翻译成功: {self.stats['successful_translations']}")
        self.log(f"跳过项: {self.stats['skipped_translations']}")
        self.log(f"翻译失败: {self.stats['failed_translations']}")
        self.log(f"耗时: {elapsed:.2f}秒")
        
        return self.stats
    
    def stop(self):
        """停止翻译"""
        self.stop_flag.set()


# ==================== 配置管理器 ====================

class ConfigManager:
    """配置管理器"""
    
    def __init__(self, config_file: str = None):
        if config_file is None:
            if getattr(sys, 'frozen', False):
                app_dir = os.path.dirname(sys.executable)
            else:
                app_dir = os.path.dirname(os.path.abspath(__file__))
            config_file = os.path.join(app_dir, "translator_config.json")
        
        self.config_file = config_file
        self.config = self.load_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """获取默认配置"""
        return {
            'api_keys': [],
            'current_key_id': None,
            'max_threads': 4,
            'skip_chinese': True,
            'api_timeout': 30,
            'enable_retry': True,
            'max_retries': 3,
            'retry_delay': 5,
            'output_mode': 'export',
            'output_folder': '',
            'keep_structure': True,
            'add_language_tag': True,
            'language_tag': '_zh_CN',
            'tag_position': 'end',
            'generate_report': True,
            'report_path': 'auto',
            'enable_bilingual': False,
            'bilingual_separator': ' | ',
            'bilingual_order': 'cn_first',
            # 批量翻译配置
            'enable_batch_translation': True,
            'batch_size': 10,
            'batch_separator': '\n---SPLIT---\n',
            'preset_tags': [
                {'tag': '_zh_CN', 'label': '简体中文'},
                {'tag': '_zh_TW', 'label': '繁体中文'},
                {'tag': '_cn', 'label': '中文简写'},
                {'tag': '_chinese', 'label': '英文标识'},
                {'tag': '_translated', 'label': '已翻译'}
            ],
            'tag_history': [],
            'max_tag_history': 10,
            'theme': 'light',
            'display_mode': 'simple',
            'sort_mode': 'add_order',
            'save_history': True,
            'max_history': 100,
            'history': [],
            'field_rules': [
                {'field_name': 'name', 'enabled': True, 'priority': 1, 
                 'context_fields': ['description', 'tooltip']},
                {'field_name': 'description', 'enabled': True, 'priority': 2, 
                 'context_fields': ['name']},
                {'field_name': 'tooltip', 'enabled': True, 'priority': 3, 
                 'context_fields': ['name', 'description']},
                {'field_name': 'title', 'enabled': True, 'priority': 4, 
                 'context_fields': []},
                {'field_name': 'label', 'enabled': True, 'priority': 5, 
                 'context_fields': []},
            ]
        }
    
    def load_config(self) -> Dict[str, Any]:
        """加载配置"""
        default_config = self._get_default_config()
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                    default_config.update(loaded)
            except Exception as e:
                print(f"配置文件加载失败，使用默认配置: {e}")
        
        return default_config
    
    def save_config(self) -> bool:
        """保存配置"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"保存配置失败: {e}")
            return False
    
    def get_translation_config(self) -> TranslationConfig:
        """获取翻译配置对象"""
        field_rules = []
        for rule_data in self.config.get('field_rules', []):
            field_rules.append(FieldRule(
                field_name=rule_data['field_name'],
                enabled=rule_data.get('enabled', True),
                priority=rule_data.get('priority', 0),
                context_fields=rule_data.get('context_fields', [])
            ))
        
        return TranslationConfig(
            skip_chinese=self.config.get('skip_chinese', True),
            api_timeout=self.config.get('api_timeout', 30),
            enable_retry=self.config.get('enable_retry', True),
            max_retries=self.config.get('max_retries', 3),
            retry_delay=self.config.get('retry_delay', 5),
            output_mode=self.config.get('output_mode', 'export'),
            output_folder=self.config.get('output_folder', ''),
            keep_structure=self.config.get('keep_structure', True),
            add_language_tag=self.config.get('add_language_tag', True),
            language_tag=self.config.get('language_tag', '_zh_CN'),
            tag_position=self.config.get('tag_position', 'end'),
            enable_bilingual=self.config.get('enable_bilingual', False),
            bilingual_separator=self.config.get('bilingual_separator', ' | '),
            bilingual_order=self.config.get('bilingual_order', 'cn_first'),
            enable_batch_translation=self.config.get('enable_batch_translation', True),
            batch_size=self.config.get('batch_size', 10),
            batch_separator=self.config.get('batch_separator', '\n---SPLIT---\n'),
            field_rules=field_rules
        )
    
    def export_config(self, export_path: str, include_api_keys: bool = False) -> Tuple[bool, str]:
        """导出配置到文件"""
        try:
            export_data = self.config.copy()
            
            # 根据选项决定是否导出API Keys
            if not include_api_keys:
                export_data['api_keys'] = []
                export_data['current_key_id'] = None
            
            # 不导出历史记录
            export_data['history'] = []
            
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            return True, f"配置已导出到: {export_path}"
        except Exception as e:
            return False, f"导出失败: {str(e)}"
    
    def import_config(self, import_path: str, merge_mode: bool = True) -> Tuple[bool, str]:
        """从文件导入配置
        
        Args:
            import_path: 导入文件路径
            merge_mode: True=合并模式(保留现有API Keys), False=覆盖模式
        """
        try:
            with open(import_path, 'r', encoding='utf-8') as f:
                imported = json.load(f)
            
            if merge_mode:
                # 合并模式：保留现有的API Keys和历史记录
                existing_keys = self.config.get('api_keys', [])
                existing_key_id = self.config.get('current_key_id')
                existing_history = self.config.get('history', [])
                
                # 更新配置
                self.config.update(imported)
                
                # 恢复API Keys（如果导入的配置中没有）
                if not imported.get('api_keys'):
                    self.config['api_keys'] = existing_keys
                    self.config['current_key_id'] = existing_key_id
                
                # 合并历史记录
                if existing_history:
                    imported_history = imported.get('history', [])
                    self.config['history'] = imported_history + existing_history
                    max_history = self.config.get('max_history', 100)
                    self.config['history'] = self.config['history'][:max_history]
            else:
                # 覆盖模式
                self.config = imported
            
            self.save_config()
            return True, "配置导入成功"
        except json.JSONDecodeError:
            return False, "导入失败: 文件格式错误，不是有效的JSON"
        except Exception as e:
            return False, f"导入失败: {str(e)}"
    
    def add_api_key(self, key_data: Dict[str, Any]) -> str:
        """添加 API Key"""
        key_id = str(int(time.time() * 1000))
        key_data['id'] = key_id
        key_data['created'] = datetime.now().isoformat()
        key_data['last_used'] = None
        key_data['use_count'] = 0
        
        self.config['api_keys'].append(key_data)
        self.save_config()
        return key_id
    
    def update_api_key(self, key_id: str, key_data: Dict[str, Any]) -> bool:
        """更新API Key"""
        for i, key in enumerate(self.config['api_keys']):
            if key['id'] == key_id:
                key_data['id'] = key_id
                key_data['created'] = key.get('created', datetime.now().isoformat())
                self.config['api_keys'][i] = key_data
                self.save_config()
                return True
        return False
    
    def remove_api_key(self, key_id: str):
        """删除API Key"""
        self.config['api_keys'] = [k for k in self.config['api_keys'] if k['id'] != key_id]
        if self.config['current_key_id'] == key_id:
            self.config['current_key_id'] = None
        self.save_config()
    
    def get_api_keys(self) -> List[Dict[str, Any]]:
        """获取所有API Keys"""
        return self.config['api_keys']
    
    def get_current_key(self) -> Optional[Dict[str, Any]]:
        """获取当前使用的Key"""
        key_id = self.config.get('current_key_id')
        if key_id:
            for key in self.config['api_keys']:
                if key['id'] == key_id:
                    return key
        return None
    
    def set_current_key(self, key_id: str):
        """设置当前使用的Key"""
        self.config['current_key_id'] = key_id
        self.save_config()
    
    def add_history(self, stats: Dict[str, Any], files: List[str]):
        """添加翻译历史"""
        if not self.config.get('save_history', True):
            return
        
        history_item = {
            'timestamp': datetime.now().isoformat(),
            'total_files': stats['total_files'],
            'processed_files': stats['processed_files'],
            'successful_translations': stats['successful_translations'],
            'failed_translations': stats['failed_translations'],
            'skipped_translations': stats.get('skipped_translations', 0),
            'duration': stats.get('duration', 0),
            'files': [os.path.basename(f) for f in files[:10]]
        }
        
        if 'history' not in self.config:
            self.config['history'] = []
        
        self.config['history'].insert(0, history_item)
        
        max_history = self.config.get('max_history', 100)
        self.config['history'] = self.config['history'][:max_history]
        
        self.save_config()


# ==================== 报告生成器 ====================

class ReportGenerator:
    """翻译报告生成器"""
    
    HTML_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>翻译对比报告</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Microsoft YaHei', sans-serif;
            background: #f5f5f5;
            padding: 20px;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        .header h1 {{ font-size: 28px; margin-bottom: 10px; }}
        .header p {{ opacity: 0.9; margin: 5px 0; }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }}
        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            text-align: center;
        }}
        .stat-number {{
            font-size: 36px;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 5px;
        }}
        .stat-label {{ color: #666; font-size: 14px; }}
        .file-section {{
            background: white;
            margin-bottom: 15px;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .file-header {{
            border-bottom: 2px solid #f0f0f0;
            padding-bottom: 10px;
            margin-bottom: 15px;
        }}
        .file-title {{ font-size: 18px; font-weight: bold; color: #333; margin-bottom: 5px; }}
        .file-info {{ color: #666; font-size: 13px; }}
        .translation-item {{
            border-left: 3px solid #4CAF50;
            padding: 12px;
            margin: 10px 0;
            background: #fafafa;
            border-radius: 4px;
        }}
        .translation-item.failed {{ border-left-color: #f44336; background: #ffebee; }}
        .translation-item.skipped {{ border-left-color: #FF9800; background: #fff3e0; }}
        .original {{ color: #666; margin-bottom: 8px; font-size: 14px; }}
        .translated {{ color: #000; font-weight: 500; font-size: 14px; }}
        .status-badge {{
            display: inline-block;
            padding: 2px 8px;
            border-radius: 3px;
            font-size: 12px;
            margin-left: 10px;
        }}
        .status-success {{ background: #4CAF50; color: white; }}
        .status-failed {{ background: #f44336; color: white; }}
        .status-skipped {{ background: #FF9800; color: white; }}
        .footer {{ text-align: center; color: #999; margin-top: 30px; padding: 20px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>YAML翻译对比报告</h1>
        <p>生成时间: {timestamp}</p>
        <p>使用平台: {platform} ({model})</p>
    </div>
    <div class="stats">
        <div class="stat-card">
            <div class="stat-number">{total_files}</div>
            <div class="stat-label">处理文件</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">{successful}</div>
            <div class="stat-label">翻译成功</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">{skipped}</div>
            <div class="stat-label">跳过项</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">{failed}</div>
            <div class="stat-label">失败项</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">{duration}</div>
            <div class="stat-label">总耗时</div>
        </div>
    </div>
    {file_sections}
    <div class="footer">
        <p>由 {app_name} 生成</p>
    </div>
</body>
</html>"""
    
    @staticmethod
    def _build_file_section(file_path: str, records: List[Dict[str, Any]]) -> str:
        """构建单个文件的HTML部分"""
        file_name = os.path.basename(file_path)
        
        success_count = len([r for r in records if r['status'] == 'success'])
        skipped_count = len([r for r in records if r['status'] == 'skipped'])
        failed_count = len([r for r in records if r['status'] == 'failed'])
        
        items_html = ""
        for record in records:
            status_class = record['status']
            status_text = {'success': '成功', 'failed': '失败', 'skipped': '跳过'}[status_class]
            status_badge = f'<span class="status-badge status-{status_class}">{status_text}</span>'
            
            items_html += f"""
            <div class="translation-item {status_class}">
                <div class="original">{record['field']}: "{record['original']}" {status_badge}</div>
                <div class="translated">→ "{record['translated']}"</div>
            </div>
            """
        
        return f"""
        <div class="file-section">
            <div class="file-header">
                <div class="file-title">{file_name}</div>
                <div class="file-info">路径: {file_path}</div>
                <div class="file-info">统计: 成功 {success_count} | 跳过 {skipped_count} | 失败 {failed_count}</div>
            </div>
            {items_html}
        </div>
        """
    
    @staticmethod
    def generate_html_report(stats: Dict[str, Any], translation_records: List[Dict[str, Any]], 
                            output_path: str, api_config: Dict[str, Any]) -> Optional[str]:
        """生成HTML对比报告"""
        files_data = {}
        for record in translation_records:
            file_path = record['file']
            if file_path not in files_data:
                files_data[file_path] = []
            files_data[file_path].append(record)
        
        file_sections_html = ""
        for file_path, records in files_data.items():
            file_sections_html += ReportGenerator._build_file_section(file_path, records)
        
        duration_str = f"{stats.get('duration', 0):.1f}秒"
        platform_name = PLATFORM_PRESETS.get(
            api_config.get('platform', 'deepseek'), {}
        ).get('name', '未知')
        
        html_content = ReportGenerator.HTML_TEMPLATE.format(
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            platform=platform_name,
            model=api_config.get('model', ''),
            total_files=stats['total_files'],
            successful=stats['successful_translations'],
            skipped=stats.get('skipped_translations', 0),
            failed=stats['failed_translations'],
            duration=duration_str,
            file_sections=file_sections_html,
            app_name=APP_TITLE
        )
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            return output_path
        except Exception as e:
            print(f"报告生成失败: {e}")
            return None


# ==================== GUI基类 ====================

class BaseDialog:
    """对话框基类"""
    
    def __init__(self, parent: tk.Tk, title: str, width: int = 600, height: int = 500):
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry(f"{width}x{height}")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        self.parent = parent
    
    def center_window(self):
        """居中显示窗口"""
        self.dialog.update_idletasks()
        width = self.dialog.winfo_width()
        height = self.dialog.winfo_height()
        x = (self.dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (height // 2)
        self.dialog.geometry(f'{width}x{height}+{x}+{y}')
    
    def destroy(self):
        """关闭对话框"""
        self.dialog.destroy()


# ==================== 字段配置对话框 ====================

class FieldConfigDialog(BaseDialog):
    """字段配置管理对话框"""
    
    def __init__(self, parent: tk.Tk, config_manager: ConfigManager, callback: Callable = None):
        super().__init__(parent, "字段配置管理", 800, 600)
        self.config_manager = config_manager
        self.callback = callback
        self.field_rules = [dict(r) for r in self.config_manager.config.get('field_rules', [])]
        
        self.setup_ui()
        self.load_field_rules()
        self.center_window()
    
    def setup_ui(self):
        """设置UI"""
        self.dialog.rowconfigure(1, weight=1)
        self.dialog.columnconfigure(0, weight=1)
        
        # 标题
        title_frame = ttk.Frame(self.dialog, padding="15")
        title_frame.grid(row=0, column=0, sticky='ew')
        ttk.Label(title_frame, text="字段配置管理", 
                 font=('Microsoft YaHei UI', 11, 'bold')).pack(side=tk.LEFT)
        ttk.Label(title_frame, text="配置需要翻译的字段及其上下文关联", 
                 font=('Microsoft YaHei UI', 9),
                 foreground='gray').pack(side=tk.LEFT, padx=(15, 0))
        
        # 主区域
        main_frame = ttk.Frame(self.dialog, padding="15")
        main_frame.grid(row=1, column=0, sticky='nsew')
        main_frame.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
        # 创建Treeview
        columns = ('enabled', 'field', 'priority', 'context')
        self.tree = ttk.Treeview(main_frame, columns=columns, show='headings', height=15)
        
        self.tree.heading('enabled', text='启用')
        self.tree.heading('field', text='字段名')
        self.tree.heading('priority', text='优先级')
        self.tree.heading('context', text='上下文字段')
        
        self.tree.column('enabled', width=60, anchor='center')
        self.tree.column('field', width=150)
        self.tree.column('priority', width=80, anchor='center')
        self.tree.column('context', width=400)
        
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky='nsew')
        scrollbar.grid(row=0, column=1, sticky='ns')
        
        self.tree.bind('<Double-1>', self.on_double_click)
        
        # 按钮区域
        btn_frame = ttk.Frame(self.dialog, padding="15")
        btn_frame.grid(row=2, column=0, sticky='ew')
        
        ttk.Button(btn_frame, text="添加字段", command=self.add_field, width=12).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="编辑", command=self.edit_field, width=12).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="删除", command=self.delete_field, width=12).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="上移", command=self.move_up, width=8).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="下移", command=self.move_down, width=8).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(btn_frame, text="保存", command=self.save_config, width=12,
                  style='Accent.TButton').pack(side=tk.RIGHT, padx=5)
        ttk.Button(btn_frame, text="取消", command=self.destroy, width=12).pack(side=tk.RIGHT)
    
    def load_field_rules(self):
        """加载字段规则到列表"""
        self.tree.delete(*self.tree.get_children())
        
        for rule in self.field_rules:
            enabled_text = '✓' if rule.get('enabled', True) else ''
            context_text = ', '.join(rule.get('context_fields', []))
            
            self.tree.insert('', tk.END, values=(
                enabled_text,
                rule['field_name'],
                rule.get('priority', 0),
                context_text
            ))
    
    def on_double_click(self, event):
        """双击编辑"""
        self.edit_field()
    
    def add_field(self):
        """添加新字段"""
        self.show_field_editor()
    
    def edit_field(self):
        """编辑字段"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("警告", "请选择要编辑的字段", parent=self.dialog)
            return
        
        item = self.tree.item(selection[0])
        field_name = item['values'][1]
        
        for rule in self.field_rules:
            if rule['field_name'] == field_name:
                self.show_field_editor(rule)
                break
    
    def delete_field(self):
        """删除字段"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("警告", "请选择要删除的字段", parent=self.dialog)
            return
        
        if not messagebox.askyesno("确认", "确定要删除选中的字段配置吗？", parent=self.dialog):
            return
        
        item = self.tree.item(selection[0])
        field_name = item['values'][1]
        
        self.field_rules = [r for r in self.field_rules if r['field_name'] != field_name]
        self.load_field_rules()
    
    def move_up(self):
        """上移"""
        selection = self.tree.selection()
        if not selection:
            return
        
        item = self.tree.item(selection[0])
        field_name = item['values'][1]
        
        for i, rule in enumerate(self.field_rules):
            if rule['field_name'] == field_name and i > 0:
                self.field_rules[i], self.field_rules[i-1] = self.field_rules[i-1], self.field_rules[i]
                self.field_rules[i]['priority'] = i
                self.field_rules[i-1]['priority'] = i - 1
                self.load_field_rules()
                break
    
    def move_down(self):
        """下移"""
        selection = self.tree.selection()
        if not selection:
            return
        
        item = self.tree.item(selection[0])
        field_name = item['values'][1]
        
        for i, rule in enumerate(self.field_rules):
            if rule['field_name'] == field_name and i < len(self.field_rules) - 1:
                self.field_rules[i], self.field_rules[i+1] = self.field_rules[i+1], self.field_rules[i]
                self.field_rules[i]['priority'] = i
                self.field_rules[i+1]['priority'] = i + 1
                self.load_field_rules()
                break
    
    def show_field_editor(self, rule_data: Dict = None):
        """显示字段编辑器"""
        is_edit = rule_data is not None
        
        editor = tk.Toplevel(self.dialog)
        editor.title("编辑字段" if is_edit else "添加字段")
        editor.geometry("500x400")
        editor.transient(self.dialog)
        editor.grab_set()
        
        editor.rowconfigure(1, weight=1)
        editor.columnconfigure(0, weight=1)
        
        ttk.Label(editor, text="编辑字段配置" if is_edit else "添加字段配置",
                 font=('Microsoft YaHei UI', 10, 'bold'),
                 padding="15").grid(row=0, column=0, sticky='ew')
        
        form = ttk.Frame(editor, padding="20")
        form.grid(row=1, column=0, sticky='nsew')
        
        # 字段名
        ttk.Label(form, text="字段名:").grid(row=0, column=0, sticky=tk.W, pady=8)
        field_name_var = tk.StringVar(value=rule_data['field_name'] if is_edit else '')
        field_entry = ttk.Entry(form, textvariable=field_name_var, width=40)
        field_entry.grid(row=0, column=1, pady=8, sticky='ew')
        if is_edit:
            field_entry.config(state='disabled')
        
        # 启用
        enabled_var = tk.BooleanVar(value=rule_data.get('enabled', True) if is_edit else True)
        ttk.Checkbutton(form, text="启用此字段", variable=enabled_var).grid(
            row=1, column=0, columnspan=2, sticky=tk.W, pady=8)
        
        # 优先级
        ttk.Label(form, text="优先级:").grid(row=2, column=0, sticky=tk.W, pady=8)
        priority_var = tk.IntVar(value=rule_data.get('priority', 0) if is_edit else len(self.field_rules))
        ttk.Spinbox(form, from_=0, to=100, textvariable=priority_var, width=10).grid(
            row=2, column=1, sticky=tk.W, pady=8)
        
        # 上下文字段
        ttk.Label(form, text="上下文字段:").grid(row=3, column=0, sticky=tk.NW, pady=8)
        
        context_frame = ttk.Frame(form)
        context_frame.grid(row=3, column=1, sticky='ew', pady=8)
        
        context_text = tk.Text(context_frame, height=6, width=40, font=('Consolas', 9))
        context_text.pack(fill=tk.BOTH, expand=True)
        
        if is_edit and rule_data.get('context_fields'):
            context_text.insert('1.0', '\n'.join(rule_data['context_fields']))
        
        ttk.Label(form, text="每行一个字段名", 
                 foreground='gray', font=('Microsoft YaHei UI', 8)).grid(
            row=4, column=1, sticky=tk.W, pady=(0, 8))
        
        form.columnconfigure(1, weight=1)
        
        # 按钮
        btn_frame = ttk.Frame(editor, padding="15")
        btn_frame.grid(row=2, column=0, sticky='ew')
        
        def save():
            field_name = field_name_var.get().strip()
            if not field_name:
                messagebox.showwarning("警告", "请输入字段名", parent=editor)
                return
            
            if not is_edit:
                for rule in self.field_rules:
                    if rule['field_name'] == field_name:
                        messagebox.showwarning("警告", "字段名已存在", parent=editor)
                        return
            
            context_fields = []
            for line in context_text.get('1.0', tk.END).strip().split('\n'):
                line = line.strip()
                if line:
                    context_fields.append(line)
            
            new_rule = {
                'field_name': field_name,
                'enabled': enabled_var.get(),
                'priority': priority_var.get(),
                'context_fields': context_fields
            }
            
            if is_edit:
                for i, rule in enumerate(self.field_rules):
                    if rule['field_name'] == field_name:
                        self.field_rules[i] = new_rule
                        break
            else:
                self.field_rules.append(new_rule)
            
            self.load_field_rules()
            editor.destroy()
        
        ttk.Button(btn_frame, text="保存", command=save, width=12).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="取消", command=editor.destroy, width=12).pack(side=tk.LEFT)
    
    def save_config(self):
        """保存配置"""
        self.config_manager.config['field_rules'] = self.field_rules
        self.config_manager.save_config()
        
        if self.callback:
            self.callback()
        
        messagebox.showinfo("成功", "字段配置已保存", parent=self.dialog)
        self.destroy()


# ==================== API Key管理对话框 ====================

class KeyManagerDialog(BaseDialog):
    """API Key管理对话框"""
    
    def __init__(self, parent: tk.Tk, config_manager: ConfigManager, callback: Callable = None):
        super().__init__(parent, "API Key 管理", 800, 500)
        self.config_manager = config_manager
        self.callback = callback
        
        self.setup_ui()
        self.refresh_tree()
        self.center_window()
    
    def setup_ui(self):
        """设置UI"""
        self.dialog.rowconfigure(1, weight=1)
        self.dialog.columnconfigure(0, weight=1)
        
        title_frame = ttk.Frame(self.dialog, padding="15 15 15 10")
        title_frame.grid(row=0, column=0, sticky='ew')
        ttk.Label(title_frame, text="API Key 管理", 
                 font=('Microsoft YaHei UI', 11, 'bold')).pack(anchor=tk.W)
        
        list_frame = ttk.Frame(self.dialog, padding="0 0 15 10")
        list_frame.grid(row=1, column=0, sticky='nsew', padx=15)
        list_frame.rowconfigure(0, weight=1)
        list_frame.columnconfigure(0, weight=1)
        
        columns = ('name', 'platform', 'model', 'status')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        self.tree.heading('name', text='名称')
        self.tree.heading('platform', text='平台')
        self.tree.heading('model', text='模型')
        self.tree.heading('status', text='状态')
        
        self.tree.column('name', width=150)
        self.tree.column('platform', width=150)
        self.tree.column('model', width=200)
        self.tree.column('status', width=100)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky='nsew')
        scrollbar.grid(row=0, column=1, sticky='ns')
        
        btn_frame = ttk.Frame(self.dialog, padding="15")
        btn_frame.grid(row=2, column=0, sticky='ew')
        
        ttk.Button(btn_frame, text="添加", command=self.add_key, width=12).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="编辑", command=self.edit_key, width=12).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="测试", command=self.test_key, width=12).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="删除", command=self.remove_key, width=12).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="关闭", command=self.on_close, width=12).pack(side=tk.RIGHT, padx=5)
    
    def refresh_tree(self):
        """刷新列表"""
        self.tree.delete(*self.tree.get_children())
        for k in self.config_manager.get_api_keys():
            platform_name = PLATFORM_PRESETS.get(k.get('platform', 'custom'), {}).get('name', '自定义')
            self.tree.insert('', tk.END, values=(
                k['name'], 
                platform_name, 
                k.get('model', 'N/A'),
                '未测试'
            ))
    
    def add_key(self):
        """添加Key"""
        KeyEditorDialog(self.dialog, self.config_manager, None, self.on_key_changed)
    
    def edit_key(self):
        """编辑Key"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("警告", "请选择要编辑的 API Key", parent=self.dialog)
            return
        
        item = self.tree.item(selection[0])
        key_name = item['values'][0]
        
        for k in self.config_manager.get_api_keys():
            if k['name'] == key_name:
                KeyEditorDialog(self.dialog, self.config_manager, k, self.on_key_changed)
                break
    
    def on_key_changed(self):
        """Key变更回调"""
        self.refresh_tree()
        if self.callback:
            self.callback()
    
    def test_key(self):
        """测试Key"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("警告", "请选择要测试的 API Key", parent=self.dialog)
            return
        
        item = self.tree.item(selection[0])
        key_name = item['values'][0]
        
        for k in self.config_manager.get_api_keys():
            if k['name'] == key_name:
                self.test_api_key(k, selection[0])
                break
    
    def test_api_key(self, key_data: Dict[str, Any], tree_item):
        """测试API Key"""
        test_window = tk.Toplevel(self.dialog)
        test_window.title("测试 API 连接")
        test_window.geometry("400x250")
        test_window.resizable(False, False)
        test_window.transient(self.dialog)
        test_window.grab_set()
        
        test_window.rowconfigure(1, weight=1)
        test_window.columnconfigure(0, weight=1)
        
        ttk.Label(test_window, text="测试 API 连接", 
                 font=('Microsoft YaHei UI', 11, 'bold'),
                 padding="20").grid(row=0, column=0)
        
        content = ttk.Frame(test_window, padding="20")
        content.grid(row=1, column=0, sticky='nsew')
        
        platform_name = PLATFORM_PRESETS.get(key_data.get('platform', 'custom'), {}).get('name', '自定义')
        ttk.Label(content, text=f"平台: {platform_name}").pack(pady=5)
        ttk.Label(content, text=f"模型: {key_data.get('model', 'N/A')}").pack(pady=5)
        
        progress = ttk.Progressbar(content, mode='indeterminate')
        progress.pack(fill=tk.X, pady=15)
        
        status_label = ttk.Label(content, text="正在测试...")
        status_label.pack(pady=10)
        
        progress.start()
        
        def do_test():
            try:
                api_config = {
                    'platform': key_data.get('platform', 'deepseek'),
                    'api_key': key_data['api_key'],
                    'model': key_data.get('model', 'deepseek-chat'),
                    'url': key_data.get('url', ''),
                    'temperature': key_data.get('temperature', 0.3),
                    'max_tokens': key_data.get('max_tokens', 1000)
                }
                
                rate_limiter = RateLimiter()
                translator = UniversalTranslator(api_config, rate_limiter)
                success, message = translator.test_connection()
                
                test_window.after(0, lambda: on_result(success, message))
                
            except Exception as e:
                test_window.after(0, lambda: on_result(False, str(e)))
        
        def on_result(success, message):
            progress.stop()
            
            if success:
                status_label.config(text="测试成功！")
                ttk.Label(content, text=message, foreground='green', wraplength=350).pack(pady=10)
                
                values = list(self.tree.item(tree_item)['values'])
                values[3] = '成功'
                self.tree.item(tree_item, values=values)
            else:
                status_label.config(text="测试失败")
                ttk.Label(content, text=message, foreground='red', wraplength=350).pack(pady=10)
            
            ttk.Button(content, text="确定", command=test_window.destroy, width=12).pack(pady=10)
        
        thread = threading.Thread(target=do_test, daemon=True)
        thread.start()
    
    def remove_key(self):
        """删除Key"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("警告", "请选择要删除的 API Key", parent=self.dialog)
            return
        
        if messagebox.askyesno("确认", "确定要删除选中的 API Key 吗？", parent=self.dialog):
            item = self.tree.item(selection[0])
            key_name = item['values'][0]
            
            for k in self.config_manager.get_api_keys():
                if k['name'] == key_name:
                    self.config_manager.remove_api_key(k['id'])
                    break
            
            self.on_key_changed()
    
    def on_close(self):
        """关闭对话框"""
        if self.callback:
            self.callback()
        self.destroy()


# ==================== API Key编辑对话框 ====================

class KeyEditorDialog(BaseDialog):
    """API Key编辑对话框"""
    
    def __init__(self, parent, config_manager: ConfigManager, 
                 key_data: Optional[Dict] = None, callback: Callable = None):
        is_edit = key_data is not None
        title = "编辑 API Key" if is_edit else "添加 API Key"
        super().__init__(parent, title, 600, 750)
        
        self.config_manager = config_manager
        self.key_data = key_data
        self.callback = callback
        self.is_edit = is_edit
        
        self.setup_ui()
        self.center_window()
    
    def setup_ui(self):
        """设置UI"""
        self.dialog.rowconfigure(1, weight=1)
        self.dialog.columnconfigure(0, weight=1)
        
        ttk.Label(self.dialog, 
                 text="编辑 API Key" if self.is_edit else "添加 API Key",
                 font=('Microsoft YaHei UI', 11, 'bold'),
                 padding="20 20 20 10").grid(row=0, column=0)
        
        canvas = tk.Canvas(self.dialog, highlightthickness=0)
        canvas.grid(row=1, column=0, sticky='nsew', padx=15, pady=10)
        
        scrollbar = ttk.Scrollbar(self.dialog, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.grid(row=1, column=1, sticky='ns')
        
        canvas.configure(yscrollcommand=scrollbar.set)
        
        form = ttk.Frame(canvas)
        canvas_window = canvas.create_window((0, 0), window=form, anchor='nw')
        
        def on_canvas_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
            canvas.itemconfig(canvas_window, width=event.width)
        
        canvas.bind('<Configure>', on_canvas_configure)
        
        row = 0
        
        # 名称
        ttk.Label(form, text="名称:").grid(row=row, column=0, sticky=tk.W, pady=8, padx=(10, 5))
        self.name_var = tk.StringVar(value=self.key_data['name'] if self.is_edit else '')
        ttk.Entry(form, textvariable=self.name_var, width=40).grid(
            row=row, column=1, columnspan=2, pady=8, sticky='ew', padx=(0, 10))
        row += 1
        
        # 平台
        ttk.Label(form, text="平台:").grid(row=row, column=0, sticky=tk.W, pady=8, padx=(10, 5))
        self.platform_combo = ttk.Combobox(form, state='readonly', width=37)
        self.platform_combo['values'] = [preset['name'] for preset in PLATFORM_PRESETS.values()]
        self.platform_combo.grid(row=row, column=1, columnspan=2, pady=8, sticky='ew', padx=(0, 10))
        self.platform_combo.bind('<<ComboboxSelected>>', self.on_platform_change)
        row += 1
        
        # API Key
        ttk.Label(form, text="API Key:").grid(row=row, column=0, sticky=tk.W, pady=8, padx=(10, 5))
        self.key_var = tk.StringVar(value=self.key_data.get('api_key', '') if self.is_edit else '')
        self.key_entry = ttk.Entry(form, textvariable=self.key_var, show='*', width=40)
        self.key_entry.grid(row=row, column=1, columnspan=2, pady=8, sticky='ew', padx=(0, 10))
        row += 1
        
        # API URL
        ttk.Label(form, text="API URL:").grid(row=row, column=0, sticky=tk.W, pady=8, padx=(10, 5))
        self.url_var = tk.StringVar(value=self.key_data.get('url', '') if self.is_edit else '')
        self.url_entry = ttk.Entry(form, textvariable=self.url_var, width=40)
        self.url_entry.grid(row=row, column=1, columnspan=2, pady=8, sticky='ew', padx=(0, 10))
        row += 1
        
        # 模型
        ttk.Label(form, text="模型:").grid(row=row, column=0, sticky=tk.W, pady=8, padx=(10, 5))
        self.model_var = tk.StringVar(value=self.key_data.get('model', '') if self.is_edit else '')
        self.model_combo = ttk.Combobox(form, textvariable=self.model_var, width=30)
        self.model_combo.grid(row=row, column=1, pady=8, sticky='ew')
        
        self.fetch_btn = ttk.Button(form, text="获取模型", width=12, command=self.fetch_models)
        self.fetch_btn.grid(row=row, column=2, pady=8, padx=(5, 10), sticky='ew')
        row += 1
        
        # 高级选项
        advanced_frame = ttk.LabelFrame(form, text="高级选项", padding="10")
        advanced_frame.grid(row=row, column=0, columnspan=3, sticky='ew', pady=10, padx=10)
        row += 1
        
        ttk.Label(advanced_frame, text="Temperature:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.temp_var = tk.DoubleVar(value=self.key_data.get('temperature', 0.3) if self.is_edit else 0.3)
        ttk.Entry(advanced_frame, textvariable=self.temp_var, width=10).grid(
            row=0, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(advanced_frame, text="Max Tokens:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.tokens_var = tk.IntVar(value=self.key_data.get('max_tokens', 1000) if self.is_edit else 1000)
        ttk.Entry(advanced_frame, textvariable=self.tokens_var, width=10).grid(
            row=1, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(advanced_frame, text="自定义提示词:", 
                 font=('Microsoft YaHei UI', 9, 'bold')).grid(
            row=2, column=0, columnspan=3, sticky=tk.W, pady=(10, 5))
        
        self.prompt_text = scrolledtext.ScrolledText(advanced_frame, height=6, 
                                                     font=('Consolas', 9), wrap=tk.WORD)
        self.prompt_text.grid(row=3, column=0, columnspan=3, sticky='ew', pady=5)
        self.prompt_text.insert('1.0', self.key_data.get('custom_prompt', DEFAULT_PROMPT) 
                               if self.is_edit else DEFAULT_PROMPT)
        
        form.columnconfigure(1, weight=1)
        
        # 初始化平台选择
        if self.is_edit:
            platform_id = self.key_data.get('platform', 'deepseek')
            name = PLATFORM_PRESETS.get(platform_id, {}).get('name', '')
            self.platform_combo.set(name)
        else:
            self.platform_combo.current(1)
        
        self.on_platform_change()
        
        # 按钮
        btn_frame = ttk.Frame(self.dialog, padding="15")
        btn_frame.grid(row=2, column=0, columnspan=2, sticky='ew')
        
        ttk.Button(btn_frame, text="保存", command=self.save, width=12).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="取消", command=self.destroy, width=12).pack(side=tk.LEFT, padx=5)
    
    def get_platform_id(self, name: str) -> Optional[str]:
        """从名称获取平台ID"""
        for pid, preset in PLATFORM_PRESETS.items():
            if preset['name'] == name:
                return pid
        return None
    
    def on_platform_change(self, event=None):
        """平台改变时更新表单"""
        platform_id = self.get_platform_id(self.platform_combo.get())
        if not platform_id:
            return
        
        preset = PLATFORM_PRESETS[platform_id]
        self.model_combo['values'] = preset['models']
        
        if not self.model_var.get() or self.model_var.get() not in preset['models']:
            self.model_var.set(preset.get('default_model', ''))
        
        self.url_var.set(preset['url'])
        
        if platform_id == 'custom':
            self.url_entry.config(state='normal')
            self.model_combo.config(state='normal')
        else:
            self.url_entry.config(state='disabled')
            self.model_combo.config(state='readonly')
    
    def fetch_models(self):
        """获取模型列表"""
        platform_id = self.get_platform_id(self.platform_combo.get())
        api_key = self.key_var.get().strip()
        base_url = self.url_var.get().strip()
        
        if not api_key:
            messagebox.showwarning("警告", "请先输入 API Key", parent=self.dialog)
            return
        
        if not base_url:
            messagebox.showwarning("警告", "请先输入 API URL", parent=self.dialog)
            return
        
        self.fetch_btn.config(state='disabled', text="获取中...")
        self.model_combo.config(state='disabled')
        
        def fetch_worker():
            try:
                models, error = UniversalTranslator.fetch_available_models(
                    platform_id, api_key, base_url, timeout=15
                )
                self.dialog.after(0, lambda: self.on_fetch_complete(models, error))
            except Exception as e:
                self.dialog.after(0, lambda: self.on_fetch_complete(None, str(e)))
        
        thread = threading.Thread(target=fetch_worker, daemon=True)
        thread.start()
    
    def on_fetch_complete(self, models: Optional[List[str]], error: Optional[str]):
        """获取模型完成"""
        self.fetch_btn.config(state='normal', text="获取模型")
        self.model_combo.config(state='normal')
        
        if error:
            messagebox.showerror("获取失败", error, parent=self.dialog)
        elif models:
            self.model_combo['values'] = models
            self.model_var.set(models[0] if models else '')
            messagebox.showinfo("成功", f"成功获取 {len(models)} 个模型！", parent=self.dialog)
    
    def save(self):
        """保存"""
        name = self.name_var.get().strip()
        api_key = self.key_var.get().strip()
        
        if not name:
            messagebox.showwarning("警告", "请输入名称", parent=self.dialog)
            return
        
        if not api_key:
            messagebox.showwarning("警告", "请输入 API Key", parent=self.dialog)
            return
        
        platform_id = self.get_platform_id(self.platform_combo.get())
        if not platform_id:
            messagebox.showwarning("警告", "请选择平台", parent=self.dialog)
            return
        
        custom_prompt = self.prompt_text.get('1.0', tk.END).strip()
        if not custom_prompt:
            custom_prompt = DEFAULT_PROMPT
        
        new_key_data = {
            'name': name,
            'platform': platform_id,
            'api_key': api_key,
            'model': self.model_var.get().strip(),
            'url': self.url_var.get().strip(),
            'temperature': self.temp_var.get(),
            'max_tokens': self.tokens_var.get(),
            'custom_prompt': custom_prompt
        }
        
        if self.is_edit:
            self.config_manager.update_api_key(self.key_data['id'], new_key_data)
        else:
            self.config_manager.add_api_key(new_key_data)
        
        messagebox.showinfo("成功", "API Key 已保存", parent=self.dialog)
        
        if self.callback:
            self.callback()
        
        self.destroy()


# ==================== 设置对话框 (完全重构支持滚动) ====================

class SettingsDialog(BaseDialog):
    """设置对话框 - 修复了嵌套滚动和鼠标滚轮支持，支持窗口大小调整"""
    
    def __init__(self, parent: tk.Tk, config_manager: ConfigManager, callback: Callable = None, initial_tab=0):
        super().__init__(parent, "设置", 720, 800)  # 增大初始高度
        self.config_manager = config_manager
        self.callback = callback
        self.initial_tab = initial_tab
        
        # 设置窗口最小尺寸，防止内容被裁剪
        self.dialog.minsize(600, 500)
        
        # 允许窗口调整大小
        self.dialog.resizable(True, True)
        
        self.setup_ui()
        self.load_settings()
        self.center_window()
    
    def setup_ui(self):
        """设置UI"""
        # 使根窗口自适应
        self.dialog.rowconfigure(1, weight=1)
        self.dialog.columnconfigure(0, weight=1)
        
        # 1. 顶部标题 (不滚动)
        title_frame = ttk.Frame(self.dialog, padding="15 15 15 10")
        title_frame.grid(row=0, column=0, sticky='ew')
        
        title_row = ttk.Frame(title_frame)
        title_row.pack(fill=tk.X)
        
        ttk.Label(title_row, text="设置中心", 
                 font=('Microsoft YaHei UI', 12, 'bold')).pack(side=tk.LEFT)
        
        # 添加提示信息
        ttk.Label(title_row, text="(可调整窗口大小，滚动查看更多选项)", 
                 font=('Microsoft YaHei UI', 8), foreground='gray').pack(side=tk.LEFT, padx=(15, 0))
        
        # 2. 中间滚动区域容器
        container = ttk.Frame(self.dialog)
        container.grid(row=1, column=0, sticky='nsew', padx=5)
        container.rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)

        # 创建 Canvas 和 Scrollbar
        self.canvas = tk.Canvas(container, highlightthickness=0, bg='#f0f0f0')
        self.scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        
        # 内容框架 (承载所有 Tab)
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        # 绑定滚动区域更新
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self._update_scroll_region()
        )

        # 在 Canvas 中创建窗口
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        # 让内部 Frame 宽度随 Canvas 变化
        self.canvas.bind('<Configure>', self._on_canvas_configure)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # 布局 Canvas 组件
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        # --- 核心修复：绑定鼠标滚轮到 Canvas ---
        self._bind_mousewheel(self.canvas)
        # 递归绑定所有子组件，确保鼠标在按钮或输入框上时也能滚动
        self._bind_mousewheel_recursive(self.scrollable_frame)

        # 3. 创建 Tab 控件 (放在滚动框架内)
        self.notebook = ttk.Notebook(self.scrollable_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.create_output_tab(self.notebook)
        self.create_translation_tab(self.notebook)
        self.create_ui_tab(self.notebook)
        
        if 0 <= self.initial_tab < len(self.notebook.tabs()):
            self.notebook.select(self.initial_tab)
            
        # 4. 底部按钮 (固定不滚动)
        btn_frame = ttk.Frame(self.dialog, padding="15")
        btn_frame.grid(row=2, column=0, sticky='ew')
        
        ttk.Button(btn_frame, text="保存设置", command=self.save_settings, 
                  width=15, style='Accent.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="取消", command=self.destroy, width=12).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="恢复默认", command=self.reset_to_defaults, width=12).pack(side=tk.RIGHT, padx=5)
    
    def _update_scroll_region(self):
        """更新滚动区域"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        # 检查是否需要显示滚动条
        content_height = self.scrollable_frame.winfo_reqheight()
        canvas_height = self.canvas.winfo_height()
        if content_height <= canvas_height:
            self.scrollbar.grid_remove()  # 内容不需要滚动时隐藏滚动条
        else:
            self.scrollbar.grid()  # 需要滚动时显示
    
    def reset_to_defaults(self):
        """恢复默认设置"""
        if not messagebox.askyesno("确认", "确定要恢复所有设置为默认值吗？\n这不会删除您的 API Key 配置。", 
                                   parent=self.dialog):
            return
        
        # 恢复默认值
        self.output_mode_var.set('export')
        self.output_folder_var.set('')
        self.keep_structure_var.set(True)
        self.add_tag_var.set(True)
        self.language_tag_var.set('_zh_CN')
        self.tag_position_var.set('end')
        self.bilingual_var.set(False)
        self.separator_var.set(' | ')
        self.bilingual_order_var.set('cn_first')
        self.skip_chinese_var.set(True)
        self.thread_var.set(4)
        self.timeout_var.set(30)
        self.retry_var.set(True)
        self.retry_count_var.set(3)
        self.retry_delay_var.set(5)
        self.generate_report_var.set(True)
        self.theme_var.set('light')
        self.save_history_var.set(True)
        self.max_history_var.set(100)
        self.display_mode_var.set('简洁模式')
        
        messagebox.showinfo("成功", "设置已恢复为默认值", parent=self.dialog)

    def _on_canvas_configure(self, event):
        """确保内部框架宽度与 Canvas 一致，防止横向滚动"""
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    def _bind_mousewheel(self, widget):
        """跨平台滚轮绑定"""
        widget.bind_all("<MouseWheel>", self._on_mousewheel) # Windows/MacOS
        widget.bind_all("<Button-4>", self._on_mousewheel)   # Linux
        widget.bind_all("<Button-5>", self._on_mousewheel)   # Linux

    def _bind_mousewheel_recursive(self, widget):
        """递归为所有子插件绑定滚轮，防止信号被拦截"""
        widget.bind("<MouseWheel>", self._on_mousewheel)
        for child in widget.winfo_children():
            self._bind_mousewheel_recursive(child)

    def _on_mousewheel(self, event):
        """处理滚轮逻辑"""
        # 仅当对话框存在且可见时处理
        if not self.dialog.winfo_exists(): return
        
        if event.num == 4 or event.delta > 0:
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5 or event.delta < 0:
            self.canvas.yview_scroll(1, "units")
    
    def create_output_tab(self, notebook):
        """创建输出设置选项卡"""
        output_tab = ttk.Frame(notebook, padding="15")
        notebook.add(output_tab, text="输出设置")
        
        # 输出模式
        mode_frame = ttk.LabelFrame(output_tab, text="输出模式", padding="10")
        mode_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.output_mode_var = tk.StringVar()
        
        ttk.Radiobutton(mode_frame, text="导出到指定文件夹（推荐）", 
                       variable=self.output_mode_var, value='export').pack(anchor=tk.W, pady=2)
        ttk.Radiobutton(mode_frame, text="覆盖原文件（危险，但会创建备份）", 
                       variable=self.output_mode_var, value='overwrite').pack(anchor=tk.W, pady=2)
        
        # 导出选项
        export_frame = ttk.LabelFrame(output_tab, text="导出选项", padding="10")
        export_frame.pack(fill=tk.X, pady=(0, 10))
        
        folder_frame = ttk.Frame(export_frame)
        folder_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(folder_frame, text="输出文件夹:").pack(side=tk.LEFT)
        self.output_folder_var = tk.StringVar()
        ttk.Entry(folder_frame, textvariable=self.output_folder_var, width=35).pack(
            side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        ttk.Button(folder_frame, text="浏览...", 
                  command=self.browse_output_folder, width=10).pack(side=tk.LEFT)
        
        self.keep_structure_var = tk.BooleanVar()
        ttk.Checkbutton(export_frame, text="保持原目录结构", 
                       variable=self.keep_structure_var).pack(anchor=tk.W, pady=5)
        
        # 语言标识
        tag_frame = ttk.LabelFrame(output_tab, text="语言标识", padding="10")
        tag_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.add_tag_var = tk.BooleanVar()
        ttk.Checkbutton(tag_frame, text="添加语言标识到文件名", 
                       variable=self.add_tag_var).pack(anchor=tk.W, pady=5)
        
        tag_input_frame = ttk.Frame(tag_frame)
        tag_input_frame.pack(fill=tk.X, pady=5, padx=(20, 0))
        
        ttk.Label(tag_input_frame, text="标识:").pack(side=tk.LEFT)
        self.language_tag_var = tk.StringVar()
        self.tag_combo = ttk.Combobox(tag_input_frame, textvariable=self.language_tag_var, width=15)
        self.tag_combo.pack(side=tk.LEFT, padx=8)
        
        position_frame = ttk.Frame(tag_frame)
        position_frame.pack(fill=tk.X, pady=5, padx=(20, 0))
        
        self.tag_position_var = tk.StringVar()
        
        ttk.Label(position_frame, text="位置:").pack(side=tk.LEFT, padx=(0, 8))
        ttk.Radiobutton(position_frame, text="末尾", 
                       variable=self.tag_position_var, value='end').pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(position_frame, text="扩展名前", 
                       variable=self.tag_position_var, value='before_ext').pack(side=tk.LEFT)
        
        # 双语输出
        bilingual_frame = ttk.LabelFrame(output_tab, text="双语输出", padding="10")
        bilingual_frame.pack(fill=tk.X)
        
        self.bilingual_var = tk.BooleanVar()
        ttk.Checkbutton(bilingual_frame, text="启用双语输出（同时显示中文和原文）", 
                       variable=self.bilingual_var).pack(anchor=tk.W, pady=5)
        
        sep_frame = ttk.Frame(bilingual_frame)
        sep_frame.pack(fill=tk.X, pady=5, padx=(20, 0))
        
        ttk.Label(sep_frame, text="分隔符:").pack(side=tk.LEFT)
        self.separator_var = tk.StringVar()
        sep_combo = ttk.Combobox(sep_frame, textvariable=self.separator_var, 
                    values=[' | ', ' / ', ' - ', ' · ', ' ', ' ⟨ ⟩ ', ' → '], width=10)
        sep_combo.pack(side=tk.LEFT, padx=8)
        
        order_frame = ttk.Frame(bilingual_frame)
        order_frame.pack(fill=tk.X, pady=5, padx=(20, 0))
        
        self.bilingual_order_var = tk.StringVar()
        
        ttk.Radiobutton(order_frame, text="中文 | 原文", 
                       variable=self.bilingual_order_var, value='cn_first').pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(order_frame, text="原文 | 中文", 
                       variable=self.bilingual_order_var, value='en_first').pack(side=tk.LEFT)
        
        # 预览框 - 增强的预览效果
        preview_outer_frame = ttk.Frame(bilingual_frame)
        preview_outer_frame.pack(fill=tk.X, padx=20, pady=(10, 5))
        
        ttk.Label(preview_outer_frame, text="效果预览:", 
                 font=('Microsoft YaHei UI', 9, 'bold')).pack(anchor=tk.W)
        
        # 使用Frame模拟预览框
        self.preview_frame = ttk.Frame(preview_outer_frame, relief='solid', borderwidth=1)
        self.preview_frame.pack(fill=tk.X, pady=5)
        
        # 预览内容 - 模拟YAML字段显示
        preview_content = ttk.Frame(self.preview_frame, padding="10")
        preview_content.pack(fill=tk.X)
        
        # 示例字段名
        ttk.Label(preview_content, text="name:", 
                 font=('Consolas', 10), foreground='#0066cc').grid(row=0, column=0, sticky='nw')
        
        # 预览值标签
        self.preview_value_label = ttk.Label(preview_content, text="", 
                                            font=('Microsoft YaHei UI', 10),
                                            wraplength=350)
        self.preview_value_label.grid(row=0, column=1, sticky='w', padx=(8, 0))
        
        # 添加第二个示例
        ttk.Label(preview_content, text="description:", 
                 font=('Consolas', 10), foreground='#0066cc').grid(row=1, column=0, sticky='nw', pady=(5, 0))
        
        self.preview_desc_label = ttk.Label(preview_content, text="", 
                                           font=('Microsoft YaHei UI', 10),
                                           wraplength=350)
        self.preview_desc_label.grid(row=1, column=1, sticky='w', padx=(8, 0), pady=(5, 0))
        
        # 状态提示
        self.preview_status_label = ttk.Label(bilingual_frame, text="", 
                                             foreground='gray', font=('Microsoft YaHei UI', 8, 'italic'))
        self.preview_status_label.pack(anchor=tk.W, padx=20, pady=(0, 5))

        # 绑定事件以更新预览
        def update_preview(*args):
            if not self.bilingual_var.get():
                self.preview_value_label.config(text="翻译后的中文内容")
                self.preview_desc_label.config(text="这是一段描述文字的翻译结果")
                self.preview_status_label.config(text="(双语输出未启用 - 仅显示翻译结果)")
                self.preview_frame.configure(style='TFrame')
                return
            
            sep = self.separator_var.get()
            order = self.bilingual_order_var.get()
            
            # 示例数据
            cn_name = "翻译后的中文名称"
            en_name = "Original English Name"
            cn_desc = "这是翻译后的描述"
            en_desc = "Original description text"
            
            if order == 'cn_first':
                name_text = f"{cn_name}{sep}{en_name}"
                desc_text = f"{cn_desc}{sep}{en_desc}"
                order_hint = "中文在前"
            else:
                name_text = f"{en_name}{sep}{cn_name}"
                desc_text = f"{en_desc}{sep}{cn_desc}"
                order_hint = "原文在前"
            
            self.preview_value_label.config(text=name_text)
            self.preview_desc_label.config(text=desc_text)
            self.preview_status_label.config(text=f"✓ 双语输出已启用 ({order_hint}，分隔符: '{sep.strip()}')")

        self.bilingual_var.trace('w', update_preview)
        self.separator_var.trace('w', update_preview)
        self.bilingual_order_var.trace('w', update_preview)
        
        # 初始化预览
        update_preview()
    
    def create_translation_tab(self, notebook):
        """创建翻译设置选项卡"""
        trans_tab = ttk.Frame(notebook, padding="15")
        notebook.add(trans_tab, text="翻译设置")
        
        # 基本设置
        basic_frame = ttk.LabelFrame(trans_tab, text="基本设置", padding="10")
        basic_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.skip_chinese_var = tk.BooleanVar()
        ttk.Checkbutton(basic_frame, text="跳过已包含中文的字段", 
                       variable=self.skip_chinese_var).pack(anchor=tk.W, pady=2)
        
        thread_frame = ttk.Frame(basic_frame)
        thread_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(thread_frame, text="默认并发线程数:").pack(side=tk.LEFT, padx=(0, 8))
        self.thread_var = tk.IntVar()
        ttk.Spinbox(thread_frame, from_=1, to=200, textvariable=self.thread_var, width=10).pack(side=tk.LEFT)
        ttk.Label(thread_frame, text="(1-200)", foreground='gray').pack(side=tk.LEFT, padx=(8, 0))
        
        timeout_frame = ttk.Frame(basic_frame)
        timeout_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(timeout_frame, text="API 请求超时:").pack(side=tk.LEFT, padx=(0, 8))
        self.timeout_var = tk.IntVar()
        ttk.Spinbox(timeout_frame, from_=5, to=300, textvariable=self.timeout_var, width=10).pack(side=tk.LEFT)
        ttk.Label(timeout_frame, text="秒", foreground='gray').pack(side=tk.LEFT, padx=(8, 0))
        
        # 批量翻译设置
        batch_frame = ttk.LabelFrame(trans_tab, text="批量翻译 (可大幅减少API调用)", padding="10")
        batch_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.batch_enabled_var = tk.BooleanVar()
        ttk.Checkbutton(batch_frame, text="启用批量翻译（推荐）", 
                       variable=self.batch_enabled_var).pack(anchor=tk.W, pady=2)
        
        batch_size_frame = ttk.Frame(batch_frame)
        batch_size_frame.pack(fill=tk.X, pady=5, padx=(20, 0))
        
        ttk.Label(batch_size_frame, text="每批数量:").pack(side=tk.LEFT, padx=(0, 8))
        self.batch_size_var = tk.IntVar()
        ttk.Spinbox(batch_size_frame, from_=2, to=50, textvariable=self.batch_size_var, width=8).pack(side=tk.LEFT)
        ttk.Label(batch_size_frame, text="条/批 (建议5-15)", foreground='gray').pack(side=tk.LEFT, padx=(8, 0))
        
        ttk.Label(batch_frame, text="💡 批量翻译将多条文本合并为一次API调用，可减少70-80%的调用次数",
                 foreground='#666', font=('Microsoft YaHei UI', 8), wraplength=400).pack(anchor=tk.W, pady=(5, 0), padx=(20, 0))
        
        # 失败重试
        retry_frame = ttk.LabelFrame(trans_tab, text="失败重试", padding="10")
        retry_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.retry_var = tk.BooleanVar()
        ttk.Checkbutton(retry_frame, text="失败自动重试", 
                       variable=self.retry_var).pack(anchor=tk.W, pady=2)
        
        retry_count_frame = ttk.Frame(retry_frame)
        retry_count_frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(retry_count_frame, text="重试次数:").pack(side=tk.LEFT, padx=(20, 8))
        self.retry_count_var = tk.IntVar()
        ttk.Spinbox(retry_count_frame, from_=1, to=10, 
                   textvariable=self.retry_count_var, width=8).pack(side=tk.LEFT)
        
        retry_delay_frame = ttk.Frame(retry_frame)
        retry_delay_frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(retry_delay_frame, text="重试延迟:").pack(side=tk.LEFT, padx=(20, 8))
        self.retry_delay_var = tk.IntVar()
        ttk.Spinbox(retry_delay_frame, from_=1, to=60, 
                   textvariable=self.retry_delay_var, width=8).pack(side=tk.LEFT)
        ttk.Label(retry_delay_frame, text="秒").pack(side=tk.LEFT, padx=(8, 0))
        
        # 报告设置
        report_frame = ttk.LabelFrame(trans_tab, text="报告设置", padding="10")
        report_frame.pack(fill=tk.X)
        
        self.generate_report_var = tk.BooleanVar()
        ttk.Checkbutton(report_frame, text="生成对比报告 (HTML)", 
                       variable=self.generate_report_var).pack(anchor=tk.W, pady=2)
    
    def create_ui_tab(self, notebook):
        """创建界面设置选项卡"""
        ui_tab = ttk.Frame(notebook, padding="15")
        notebook.add(ui_tab, text="界面设置")
        
        # 主题设置
        theme_frame = ttk.LabelFrame(ui_tab, text="主题", padding="10")
        theme_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.theme_var = tk.StringVar()
        
        ttk.Radiobutton(theme_frame, text="亮色主题", 
                       variable=self.theme_var, value='light').pack(anchor=tk.W, pady=2)
        ttk.Radiobutton(theme_frame, text="暗色主题", 
                       variable=self.theme_var, value='dark').pack(anchor=tk.W, pady=2)
        
        # 历史设置
        history_frame = ttk.LabelFrame(ui_tab, text="历史记录", padding="10")
        history_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.save_history_var = tk.BooleanVar()
        ttk.Checkbutton(history_frame, text="保存翻译历史", 
                       variable=self.save_history_var).pack(anchor=tk.W, pady=5)
        
        history_count_frame = ttk.Frame(history_frame)
        history_count_frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(history_count_frame, text="最多保存:").pack(side=tk.LEFT, padx=(20, 8))
        self.max_history_var = tk.IntVar()
        ttk.Spinbox(history_count_frame, from_=10, to=1000, 
                   textvariable=self.max_history_var, width=10).pack(side=tk.LEFT)
        ttk.Label(history_count_frame, text="条记录").pack(side=tk.LEFT, padx=(8, 0))
        
        # 显示设置
        display_frame = ttk.LabelFrame(ui_tab, text="显示设置", padding="10")
        display_frame.pack(fill=tk.X)
        
        mode_frame = ttk.Frame(display_frame)
        mode_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(mode_frame, text="文件列表显示:").pack(side=tk.LEFT, padx=(0, 8))
        self.display_mode_var = tk.StringVar()
        ttk.Combobox(mode_frame, textvariable=self.display_mode_var, width=15, state='readonly',
                    values=['简洁模式', '详细模式', '超详细模式']).pack(side=tk.LEFT)
    
    def browse_output_folder(self):
        """浏览输出文件夹"""
        folder = filedialog.askdirectory(title="选择输出文件夹", parent=self.dialog)
        if folder:
            self.output_folder_var.set(folder)
    
    def load_settings(self):
        """加载设置"""
        config = self.config_manager.config
        
        self.output_mode_var.set(config.get('output_mode', 'export'))
        self.output_folder_var.set(config.get('output_folder', ''))
        self.keep_structure_var.set(config.get('keep_structure', True))
        self.add_tag_var.set(config.get('add_language_tag', True))
        self.language_tag_var.set(config.get('language_tag', '_zh_CN'))
        self.tag_position_var.set(config.get('tag_position', 'end'))
        
        tag_values = []
        for preset in config.get('preset_tags', []):
            tag_values.append(preset['tag'])
        self.tag_combo['values'] = tag_values
        
        self.bilingual_var.set(config.get('enable_bilingual', False))
        self.separator_var.set(config.get('bilingual_separator', ' | '))
        self.bilingual_order_var.set(config.get('bilingual_order', 'cn_first'))
        
        self.skip_chinese_var.set(config.get('skip_chinese', True))
        self.thread_var.set(config.get('max_threads', 4))
        self.timeout_var.set(config.get('api_timeout', 30))
        
        # 批量翻译设置
        self.batch_enabled_var.set(config.get('enable_batch_translation', True))
        self.batch_size_var.set(config.get('batch_size', 10))
        
        self.retry_var.set(config.get('enable_retry', True))
        self.retry_count_var.set(config.get('max_retries', 3))
        self.retry_delay_var.set(config.get('retry_delay', 5))
        self.generate_report_var.set(config.get('generate_report', True))
        
        self.theme_var.set(config.get('theme', 'light'))
        self.save_history_var.set(config.get('save_history', True))
        self.max_history_var.set(config.get('max_history', 100))
        
        display_mode = config.get('display_mode', 'simple')
        mode_map = {'simple': '简洁模式', 'detail': '详细模式', 'ultra': '超详细模式'}
        self.display_mode_var.set(mode_map.get(display_mode, '简洁模式'))
    
    def save_settings(self):
        """保存设置"""
        config = self.config_manager.config
        
        config['output_mode'] = self.output_mode_var.get()
        config['output_folder'] = self.output_folder_var.get()
        config['keep_structure'] = self.keep_structure_var.get()
        config['add_language_tag'] = self.add_tag_var.get()
        config['language_tag'] = self.language_tag_var.get()
        config['tag_position'] = self.tag_position_var.get()
        config['enable_bilingual'] = self.bilingual_var.get()
        config['bilingual_separator'] = self.separator_var.get()
        config['bilingual_order'] = self.bilingual_order_var.get()
        
        config['skip_chinese'] = self.skip_chinese_var.get()
        config['max_threads'] = self.thread_var.get()
        config['api_timeout'] = self.timeout_var.get()
        
        # 批量翻译设置
        config['enable_batch_translation'] = self.batch_enabled_var.get()
        config['batch_size'] = self.batch_size_var.get()
        
        config['enable_retry'] = self.retry_var.get()
        config['max_retries'] = self.retry_count_var.get()
        config['retry_delay'] = self.retry_delay_var.get()
        config['generate_report'] = self.generate_report_var.get()
        
        config['theme'] = self.theme_var.get()
        config['save_history'] = self.save_history_var.get()
        config['max_history'] = self.max_history_var.get()
        
        mode_map = {'简洁模式': 'simple', '详细模式': 'detail', '超详细模式': 'ultra'}
        config['display_mode'] = mode_map.get(self.display_mode_var.get(), 'simple')
        
        self.config_manager.save_config()
        
        if self.callback:
            self.callback()
        
        messagebox.showinfo("成功", "设置已保存", parent=self.dialog)
        self.destroy()


# ==================== 翻译预览对话框 ====================

class TranslationPreviewDialog(BaseDialog):
    """翻译前预览对话框 - 显示待翻译内容的统计信息"""
    
    def __init__(self, parent: tk.Tk, file_paths: List[str], config_manager: ConfigManager,
                 on_confirm: Callable = None):
        super().__init__(parent, "翻译预览", 700, 550)
        self.file_paths = file_paths
        self.config_manager = config_manager
        self.on_confirm = on_confirm
        self.preview_data = None
        self.analyzing = False
        
        self.setup_ui()
        self.center_window()
        
        # 开始分析
        self.start_analysis()
    
    def setup_ui(self):
        """设置UI"""
        self.dialog.rowconfigure(1, weight=1)
        self.dialog.columnconfigure(0, weight=1)
        
        # 标题
        title_frame = ttk.Frame(self.dialog, padding="15 15 15 10")
        title_frame.grid(row=0, column=0, sticky='ew')
        
        ttk.Label(title_frame, text="📊 翻译任务预览", 
                 font=('Microsoft YaHei UI', 12, 'bold')).pack(anchor=tk.W)
        ttk.Label(title_frame, text="分析待翻译文件，预览翻译任务详情", 
                 font=('Microsoft YaHei UI', 9), foreground='gray').pack(anchor=tk.W)
        
        # 内容区域
        content_frame = ttk.Frame(self.dialog, padding="15")
        content_frame.grid(row=1, column=0, sticky='nsew')
        content_frame.rowconfigure(1, weight=1)
        content_frame.columnconfigure(0, weight=1)
        
        # 统计信息框
        stats_frame = ttk.LabelFrame(content_frame, text="统计信息", padding="10")
        stats_frame.grid(row=0, column=0, sticky='ew', pady=(0, 10))
        stats_frame.columnconfigure(1, weight=1)
        stats_frame.columnconfigure(3, weight=1)
        
        # 统计标签
        self.stats_labels = {}
        stats_items = [
            ('files', '文件数量:', 0, 0),
            ('fields', '待翻译字段:', 0, 1),
            ('skip', '将跳过:', 2, 0),
            ('chars', '总字符数:', 2, 1),
        ]
        
        for key, label, row, col in stats_items:
            ttk.Label(stats_frame, text=label).grid(row=row, column=col*2, sticky='w', padx=5, pady=3)
            self.stats_labels[key] = ttk.Label(stats_frame, text="分析中...", 
                                               font=('Microsoft YaHei UI', 9, 'bold'))
            self.stats_labels[key].grid(row=row, column=col*2+1, sticky='w', padx=(0, 20), pady=3)
        
        # 估算信息
        estimate_frame = ttk.LabelFrame(content_frame, text="预估信息", padding="10")
        estimate_frame.grid(row=1, column=0, sticky='nsew', pady=(0, 10))
        estimate_frame.columnconfigure(0, weight=1)
        
        self.estimate_text = tk.Text(estimate_frame, height=6, font=('Microsoft YaHei UI', 9),
                                     wrap=tk.WORD, state='disabled')
        self.estimate_text.pack(fill=tk.BOTH, expand=True)
        
        # 字段详情
        detail_frame = ttk.LabelFrame(content_frame, text="字段详情 (前50条)", padding="10")
        detail_frame.grid(row=2, column=0, sticky='nsew')
        detail_frame.rowconfigure(0, weight=1)
        detail_frame.columnconfigure(0, weight=1)
        
        # Treeview 显示字段
        columns = ('file', 'field', 'value')
        self.detail_tree = ttk.Treeview(detail_frame, columns=columns, show='headings', height=8)
        self.detail_tree.heading('file', text='文件')
        self.detail_tree.heading('field', text='字段')
        self.detail_tree.heading('value', text='内容预览')
        
        self.detail_tree.column('file', width=150)
        self.detail_tree.column('field', width=100)
        self.detail_tree.column('value', width=300)
        
        scrollbar = ttk.Scrollbar(detail_frame, orient=tk.VERTICAL, command=self.detail_tree.yview)
        self.detail_tree.configure(yscroll=scrollbar.set)
        
        self.detail_tree.grid(row=0, column=0, sticky='nsew')
        scrollbar.grid(row=0, column=1, sticky='ns')
        
        # 进度条
        self.progress_frame = ttk.Frame(content_frame)
        self.progress_frame.grid(row=3, column=0, sticky='ew', pady=(10, 0))
        
        self.progress_bar = ttk.Progressbar(self.progress_frame, mode='indeterminate')
        self.progress_bar.pack(fill=tk.X)
        self.progress_label = ttk.Label(self.progress_frame, text="正在分析文件...")
        self.progress_label.pack(pady=(5, 0))
        
        # 底部按钮
        btn_frame = ttk.Frame(self.dialog, padding="15")
        btn_frame.grid(row=2, column=0, sticky='ew')
        
        self.confirm_btn = ttk.Button(btn_frame, text="开始翻译", 
                                      command=self.on_confirm_click, 
                                      state=tk.DISABLED, width=15,
                                      style='Accent.TButton')
        self.confirm_btn.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(btn_frame, text="取消", command=self.destroy, width=12).pack(side=tk.LEFT, padx=5)
        
        # 批量翻译提示
        batch_enabled = self.config_manager.config.get('enable_batch_translation', True)
        batch_size = self.config_manager.config.get('batch_size', 10)
        if batch_enabled:
            ttk.Label(btn_frame, text=f"✓ 批量翻译已启用 (每批{batch_size}条)", 
                     foreground='green', font=('Microsoft YaHei UI', 8)).pack(side=tk.RIGHT, padx=5)
    
    def start_analysis(self):
        """开始分析文件"""
        self.analyzing = True
        self.progress_bar.start()
        
        def analyze():
            try:
                result = self._analyze_files()
                self.dialog.after(0, lambda: self.on_analysis_complete(result))
            except Exception as e:
                self.dialog.after(0, lambda: self.on_analysis_error(str(e)))
        
        thread = threading.Thread(target=analyze, daemon=True)
        thread.start()
    
    def _analyze_files(self) -> Dict[str, Any]:
        """分析文件内容"""
        translation_config = self.config_manager.get_translation_config()
        field_extractor = FieldExtractor(translation_config.field_rules)
        
        result = {
            'total_files': len(self.file_paths),
            'total_fields': 0,
            'skip_fields': 0,
            'total_chars': 0,
            'fields_detail': [],
            'files_detail': {}
        }
        
        yaml_processor = YAMLProcessor.get_instance()
        
        for file_path in self.file_paths:
            try:
                # 使用 YAMLProcessor 加载
                data = yaml_processor.load(file_path)
                
                if data is None:
                    continue
                
                fields = field_extractor.extract_fields(data)
                file_name = os.path.basename(file_path)
                
                file_fields = 0
                file_skip = 0
                
                for field_info in fields:
                    value = field_info['value']
                    
                    # 检查是否包含中文
                    has_chinese = any('\u4e00' <= char <= '\u9fff' for char in str(value))
                    
                    if translation_config.skip_chinese and has_chinese:
                        file_skip += 1
                        result['skip_fields'] += 1
                    else:
                        file_fields += 1
                        result['total_fields'] += 1
                        result['total_chars'] += len(value)
                        
                        # 只保存前50条详情
                        if len(result['fields_detail']) < 50:
                            result['fields_detail'].append({
                                'file': file_name,
                                'field': field_info['field_name'],
                                'path': field_info['path'],
                                'value': value[:100] + '...' if len(value) > 100 else value
                            })
                
                result['files_detail'][file_name] = {
                    'fields': file_fields,
                    'skip': file_skip
                }
                
            except Exception as e:
                result['files_detail'][os.path.basename(file_path)] = {'error': str(e)}
        
        return result
    
    def on_analysis_complete(self, result: Dict[str, Any]):
        """分析完成"""
        self.analyzing = False
        self.preview_data = result
        self.progress_bar.stop()
        self.progress_frame.grid_remove()
        
        # 更新统计信息
        self.stats_labels['files'].config(text=str(result['total_files']))
        self.stats_labels['fields'].config(text=str(result['total_fields']))
        self.stats_labels['skip'].config(text=str(result['skip_fields']))
        self.stats_labels['chars'].config(text=f"{result['total_chars']:,}")
        
        # 更新估算信息
        self.estimate_text.config(state='normal')
        self.estimate_text.delete('1.0', tk.END)
        
        batch_enabled = self.config_manager.config.get('enable_batch_translation', True)
        batch_size = self.config_manager.config.get('batch_size', 10)
        
        if batch_enabled:
            api_calls = (result['total_fields'] + batch_size - 1) // batch_size
            estimate = f"""📈 预估信息:
• 预计 API 调用次数: 约 {api_calls} 次 (批量模式，每批 {batch_size} 条)
• 待翻译字符数: {result['total_chars']:,} 字符
• 按每 1000 tokens ≈ 750 字符估算，约消耗 {result['total_chars'] * 2 // 750:,} tokens

💡 提示:
• 批量翻译模式已启用，可大幅减少 API 调用次数
• 已包含中文的字段将被跳过 ({result['skip_fields']} 个)
• 实际费用取决于所选 API 平台的定价"""
        else:
            estimate = f"""📈 预估信息:
• 预计 API 调用次数: 约 {result['total_fields']} 次 (单条模式)
• 待翻译字符数: {result['total_chars']:,} 字符
• 按每 1000 tokens ≈ 750 字符估算，约消耗 {result['total_chars'] * 2 // 750:,} tokens

💡 提示:
• 建议开启批量翻译模式以减少 API 调用次数
• 已包含中文的字段将被跳过 ({result['skip_fields']} 个)"""
        
        self.estimate_text.insert('1.0', estimate)
        self.estimate_text.config(state='disabled')
        
        # 填充字段详情
        for item in result['fields_detail']:
            self.detail_tree.insert('', tk.END, values=(
                item['file'],
                item['field'],
                item['value']
            ))
        
        # 启用确认按钮
        if result['total_fields'] > 0:
            self.confirm_btn.config(state=tk.NORMAL)
        else:
            self.confirm_btn.config(state=tk.DISABLED)
            messagebox.showinfo("提示", "未找到需要翻译的字段", parent=self.dialog)
    
    def on_analysis_error(self, error: str):
        """分析出错"""
        self.analyzing = False
        self.progress_bar.stop()
        self.progress_label.config(text=f"分析出错: {error}")
        messagebox.showerror("错误", f"分析文件时出错:\n{error}", parent=self.dialog)
    
    def on_confirm_click(self):
        """确认开始翻译"""
        if self.on_confirm:
            self.on_confirm()
        self.destroy()


# ==================== 翻译完成对话框 ====================

class TranslationCompleteDialog(BaseDialog):
    """翻译完成后显示的对话框，提供打开输出文件/文件夹的选项"""
    
    def __init__(self, parent: tk.Tk, stats: Dict[str, Any], output_folder: str, 
                 output_files: List[str] = None, report_file: str = None):
        super().__init__(parent, "翻译完成", 500, 380)
        self.stats = stats
        self.output_folder = output_folder
        self.output_files = output_files or []
        self.report_file = report_file
        
        self.setup_ui()
        self.center_window()
    
    def setup_ui(self):
        """设置UI"""
        self.dialog.rowconfigure(1, weight=1)
        self.dialog.columnconfigure(0, weight=1)
        
        # 标题
        title_frame = ttk.Frame(self.dialog, padding="20 20 20 10")
        title_frame.grid(row=0, column=0, sticky='ew')
        
        ttk.Label(title_frame, text="✓ 翻译任务完成！", 
                 font=('Microsoft YaHei UI', 14, 'bold'),
                 foreground='#2e7d32').pack(anchor=tk.W)
        
        # 统计信息
        stats_frame = ttk.LabelFrame(self.dialog, text="翻译统计", padding="15")
        stats_frame.grid(row=1, column=0, sticky='nsew', padx=20, pady=10)
        
        stats_data = [
            ("处理文件", f"{self.stats.get('processed_files', 0)}/{self.stats.get('total_files', 0)}"),
            ("翻译成功", str(self.stats.get('successful_translations', 0))),
            ("跳过项", str(self.stats.get('skipped_translations', 0))),
            ("失败项", str(self.stats.get('failed_translations', 0))),
            ("总耗时", f"{self.stats.get('duration', 0):.2f} 秒"),
        ]
        
        for i, (label, value) in enumerate(stats_data):
            ttk.Label(stats_frame, text=f"{label}:", font=('Microsoft YaHei UI', 9)).grid(
                row=i, column=0, sticky='w', pady=2)
            
            # 失败项用红色标记
            fg = '#dc143c' if label == "失败项" and int(self.stats.get('failed_translations', 0)) > 0 else None
            lbl = ttk.Label(stats_frame, text=value, font=('Microsoft YaHei UI', 9, 'bold'))
            if fg:
                lbl.configure(foreground=fg)
            lbl.grid(row=i, column=1, sticky='w', padx=(10, 0), pady=2)
        
        # 操作按钮区域
        btn_frame = ttk.Frame(self.dialog, padding="15")
        btn_frame.grid(row=2, column=0, sticky='ew')
        
        # 打开输出文件夹按钮
        open_folder_btn = ttk.Button(btn_frame, text="📂 打开输出文件夹", 
                                     command=self.open_output_folder, width=18)
        open_folder_btn.pack(side=tk.LEFT, padx=5)
        
        # 打开最近输出文件按钮（如果有输出文件）
        if self.output_files:
            open_file_btn = ttk.Button(btn_frame, text="📄 打开输出文件", 
                                       command=self.open_output_file, width=18)
            open_file_btn.pack(side=tk.LEFT, padx=5)
        
        # 打开报告按钮（如果生成了报告）
        if self.report_file and os.path.exists(self.report_file):
            report_btn = ttk.Button(btn_frame, text="📊 查看报告", 
                                   command=self.open_report, width=12)
            report_btn.pack(side=tk.LEFT, padx=5)
        
        # 关闭按钮
        ttk.Button(btn_frame, text="关闭", command=self.destroy, width=10).pack(side=tk.RIGHT, padx=5)
    
    def open_output_folder(self):
        """打开输出文件夹"""
        if self.output_folder and os.path.exists(self.output_folder):
            open_path_in_os(self.output_folder)
        else:
            messagebox.showwarning("警告", "输出文件夹不存在", parent=self.dialog)
    
    def open_output_file(self):
        """打开输出文件（弹出选择菜单如果有多个文件）"""
        if not self.output_files:
            messagebox.showwarning("警告", "没有输出文件", parent=self.dialog)
            return
        
        if len(self.output_files) == 1:
            # 只有一个文件，直接打开
            if os.path.exists(self.output_files[0]):
                open_path_in_os(self.output_files[0])
        else:
            # 多个文件，创建选择对话框
            self.show_file_selector()
    
    def show_file_selector(self):
        """显示文件选择器"""
        selector = tk.Toplevel(self.dialog)
        selector.title("选择要打开的文件")
        selector.geometry("400x300")
        selector.transient(self.dialog)
        selector.grab_set()
        
        ttk.Label(selector, text="选择要打开的输出文件:", 
                 padding="10").pack(anchor=tk.W)
        
        # 文件列表
        list_frame = ttk.Frame(selector)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        file_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, 
                                  font=('Microsoft YaHei UI', 9))
        file_listbox.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=file_listbox.yview)
        
        for f in self.output_files[:50]:  # 最多显示50个
            file_listbox.insert(tk.END, os.path.basename(f))
        
        def open_selected():
            selection = file_listbox.curselection()
            if selection:
                idx = selection[0]
                if idx < len(self.output_files):
                    path = self.output_files[idx]
                    if os.path.exists(path):
                        open_path_in_os(path)
                        selector.destroy()
        
        btn_frame = ttk.Frame(selector, padding="10")
        btn_frame.pack(fill=tk.X)
        
        ttk.Button(btn_frame, text="打开", command=open_selected, width=12).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="取消", command=selector.destroy, width=12).pack(side=tk.LEFT)
        
        file_listbox.bind('<Double-1>', lambda e: open_selected())
    
    def open_report(self):
        """打开翻译报告"""
        if self.report_file and os.path.exists(self.report_file):
            webbrowser.open(self.report_file)


# ==================== 历史记录对话框 ====================

class HistoryDialog(BaseDialog):
    """历史记录对话框"""
    
    def __init__(self, parent: tk.Tk, config_manager: ConfigManager):
        super().__init__(parent, "翻译历史记录", 900, 550)
        self.config_manager = config_manager
        
        self.setup_ui()
        self.load_history()
        self.center_window()
    
    def setup_ui(self):
        """设置UI"""
        self.dialog.rowconfigure(1, weight=1)
        self.dialog.columnconfigure(0, weight=1)
        
        title_frame = ttk.Frame(self.dialog, padding="15 15 15 5")
        title_frame.grid(row=0, column=0, sticky='ew')
        
        ttk.Label(title_frame, text="翻译历史记录", 
                 font=('Microsoft YaHei UI', 11, 'bold')).pack(side=tk.LEFT)
        
        max_history = self.config_manager.config.get('max_history', 100)
        current_count = len(self.config_manager.config.get('history', []))
        ttk.Label(title_frame, text=f"(最多保留{max_history}条，当前{current_count}条)",
                 font=('Microsoft YaHei UI', 8),
                 foreground='gray').pack(side=tk.LEFT, padx=(10, 0))
        
        list_frame = ttk.Frame(self.dialog, padding="0 0 15 10")
        list_frame.grid(row=1, column=0, sticky='nsew', padx=15)
        list_frame.rowconfigure(0, weight=1)
        list_frame.columnconfigure(0, weight=1)
        
        columns = ('time', 'files', 'success', 'skipped', 'failed', 'duration')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        self.tree.heading('time', text='时间')
        self.tree.heading('files', text='文件数')
        self.tree.heading('success', text='成功')
        self.tree.heading('skipped', text='跳过')
        self.tree.heading('failed', text='失败')
        self.tree.heading('duration', text='耗时')
        
        self.tree.column('time', width=180)
        self.tree.column('files', width=80)
        self.tree.column('success', width=80)
        self.tree.column('skipped', width=80)
        self.tree.column('failed', width=80)
        self.tree.column('duration', width=100)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky='nsew')
        scrollbar.grid(row=0, column=1, sticky='ns')
        
        btn_frame = ttk.Frame(self.dialog, padding="15")
        btn_frame.grid(row=2, column=0, sticky='ew')
        
        ttk.Button(btn_frame, text="清除全部历史", command=self.clear_history, width=15).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="关闭", command=self.destroy, width=12).pack(side=tk.RIGHT, padx=5)
    
    def load_history(self):
        """加载历史"""
        for item in self.config_manager.config.get('history', []):
            time_str = item['timestamp'][:19].replace('T', ' ')
            duration_str = f"{item.get('duration', 0):.1f}秒"
            
            self.tree.insert('', tk.END, values=(
                time_str,
                item['processed_files'],
                item['successful_translations'],
                item.get('skipped_translations', 0),
                item['failed_translations'],
                duration_str
            ))
    
    def clear_history(self):
        """清除历史"""
        if messagebox.askyesno("确认", "确定要清除所有历史记录吗？", parent=self.dialog):
            self.config_manager.config['history'] = []
            self.config_manager.save_config()
            self.tree.delete(*self.tree.get_children())
            messagebox.showinfo("成功", "历史记录已清除", parent=self.dialog)


# ==================== 主GUI类 (增强版) ====================

class TranslatorGUI:
    """主GUI类"""
    
    def __init__(self, root):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry("1200x750")
        self.root.minsize(900, 600)
        
        self.config_manager = ConfigManager()
        self.translator_core = None
        self.is_translating = False
        self.translation_lock = threading.Lock()
        self.file_queue = []
        self.current_base_folder = None
        self.last_output_folder = None
        self.last_output_files = []  # 保存最近输出的文件列表
        self.last_report_file = None  # 保存最近的报告文件路径
        self.last_stats = None  # 保存最近的统计信息
        
        self.setup_styles()
        self.create_ui()
        self.load_settings()
        self.apply_theme()
        self.bind_shortcuts()
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_styles(self):
        """配置UI样式"""
        self.style = ttk.Style()
        available_themes = self.style.theme_names()
        if 'vista' in available_themes:
            self.style.theme_use('vista')
        elif 'clam' in available_themes:
            self.style.theme_use('clam')
        
        self.style.configure('Accent.TButton', font=('Microsoft YaHei UI', 9, 'bold'))
        self.style.configure('Title.TLabel', font=('Microsoft YaHei UI', 11, 'bold'))
    
    def create_ui(self):
        """创建UI"""
        self.root.rowconfigure(2, weight=1)
        self.root.columnconfigure(0, weight=1)
        
        self.create_menu_bar()
        self.create_toolbar()
        self.create_statusbar()
        self.create_main_content()
        self.create_bottom_bar()
    
    def create_menu_bar(self):
        """创建菜单栏"""
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        
        file_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="文件(F)", menu=file_menu)
        file_menu.add_command(label="添加文件", command=self.add_files, accelerator="Ctrl+O")
        file_menu.add_command(label="添加文件夹", command=self.add_folder, accelerator="Ctrl+D")
        file_menu.add_command(label="清空列表", command=self.clear_files)
        file_menu.add_separator()
        file_menu.add_command(label="导入配置...", command=self.import_config)
        file_menu.add_command(label="导出配置...", command=self.export_config)
        file_menu.add_separator()
        file_menu.add_command(label="退出", command=self.on_closing)
        
        tools_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="工具(T)", menu=tools_menu)
        tools_menu.add_command(label="管理 API Key", command=self.show_key_manager)
        tools_menu.add_command(label="字段配置", command=self.show_field_config)
        tools_menu.add_command(label="设置...", command=self.show_settings, accelerator="Ctrl+,")
        
        help_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="帮助(H)", menu=help_menu)
        help_menu.add_command(label="翻译历史记录", command=self.show_history)
        help_menu.add_command(label="使用说明", command=self.show_help)
        help_menu.add_command(label="关于", command=self.show_about)
    
    def create_toolbar(self):
        """创建工具栏"""
        toolbar = ttk.Frame(self.root, padding="10 8")
        toolbar.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
        toolbar.columnconfigure(1, weight=1)
        
        ttk.Label(toolbar, text="API Key:", font=('Microsoft YaHei UI', 9)).grid(
            row=0, column=0, padx=(0, 8), sticky='w')
        
        self.key_combo = ttk.Combobox(toolbar, state='readonly', font=('Consolas', 9))
        self.key_combo.grid(row=0, column=1, padx=(0, 8), sticky='ew')
        self.key_combo.bind('<<ComboboxSelected>>', self.on_key_selected)
        
        ttk.Button(toolbar, text="管理", command=self.show_key_manager, width=8).grid(
            row=0, column=2, padx=(0, 15))
        
        ttk.Separator(toolbar, orient=tk.VERTICAL).grid(row=0, column=3, sticky='ns', padx=10)
        
        ttk.Label(toolbar, text="并发线程:", font=('Microsoft YaHei UI', 9)).grid(
            row=0, column=4, padx=(0, 8), sticky='w')
        
        self.thread_spin = ttk.Spinbox(toolbar, from_=1, to=200, width=8, font=('Consolas', 9))
        self.thread_spin.set(4)
        self.thread_spin.grid(row=0, column=5, padx=(0, 8))
    
    def create_statusbar(self):
        """创建状态栏"""
        statusbar = ttk.Frame(self.root, relief=tk.SUNKEN, padding="5 2")
        statusbar.grid(row=1, column=0, sticky='ew', padx=5)
        
        ttk.Label(statusbar, text=f"v{VERSION}", font=('Microsoft YaHei UI', 8)).pack(side=tk.LEFT, padx=5)
        ttk.Separator(statusbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        # YAML 引擎状态
        yaml_engine = "ruamel" if HAS_RUAMEL else "PyYAML"
        yaml_color = "#2e7d32" if HAS_RUAMEL else "#ff8c00"
        yaml_tip = "保留注释和格式" if HAS_RUAMEL else "注释可能丢失"
        yaml_label = ttk.Label(statusbar, text=f"YAML: {yaml_engine}", 
                              font=('Microsoft YaHei UI', 8), foreground=yaml_color)
        yaml_label.pack(side=tk.LEFT, padx=5)
        
        # 添加工具提示（简易实现）
        def show_yaml_tip(event):
            self.status_text.config(text=yaml_tip)
        def hide_yaml_tip(event):
            self.status_text.config(text="就绪")
        yaml_label.bind('<Enter>', show_yaml_tip)
        yaml_label.bind('<Leave>', hide_yaml_tip)
        
        ttk.Separator(statusbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        self.api_status_label = ttk.Label(statusbar, text="API未配置", font=('Microsoft YaHei UI', 8))
        self.api_status_label.pack(side=tk.LEFT, padx=5)
        
        self.file_count_status = ttk.Label(statusbar, text="文件: 0", font=('Microsoft YaHei UI', 8))
        self.file_count_status.pack(side=tk.LEFT, padx=5)
        
        self.status_text = ttk.Label(statusbar, text="就绪", font=('Microsoft YaHei UI', 8))
        self.status_text.pack(side=tk.LEFT, padx=5)
    
    def create_main_content(self):
        """创建主内容区域"""
        main_container = ttk.Frame(self.root)
        main_container.grid(row=2, column=0, sticky='nsew', padx=10, pady=5)
        
        main_container.rowconfigure(0, weight=1)
        main_container.columnconfigure(0, weight=1)
        main_container.columnconfigure(1, weight=1)
        
        self.create_file_list_panel(main_container)
        self.create_log_panel(main_container)
    
    def create_file_list_panel(self, parent):
        """创建文件列表面板 (整合 1.30 显示模式与排序)"""
        left_panel = ttk.LabelFrame(parent, text=" 待翻译文件 ", padding="8")
        left_panel.grid(row=0, column=0, sticky='nsew', padx=(0, 5))
        left_panel.rowconfigure(3, weight=1)  # 让列表区域占满剩余空间
        left_panel.columnconfigure(0, weight=1)

        # --- 搜索栏 ---
        search_frame = ttk.Frame(left_panel)
        search_frame.grid(row=0, column=0, sticky='ew', pady=(0, 5))
        
        ttk.Label(search_frame, text="🔍").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        self.search_var.trace('w', lambda *args: self.on_search_changed())
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=20)
        self.search_entry.pack(side=tk.LEFT, padx=(5, 5), fill=tk.X, expand=True)
        
        # 清除搜索按钮
        self.clear_search_btn = ttk.Button(search_frame, text="✕", width=3, 
                                           command=self.clear_search)
        self.clear_search_btn.pack(side=tk.LEFT)
        
        # 搜索结果标签
        self.search_result_label = ttk.Label(search_frame, text="", foreground='gray',
                                             font=('Microsoft YaHei UI', 8))
        self.search_result_label.pack(side=tk.LEFT, padx=(5, 0))

        # --- 控制栏：查看模式与排序 ---
        ctrl_bar = ttk.Frame(left_panel)
        ctrl_bar.grid(row=1, column=0, sticky='ew', pady=(0, 5))
        
        # 模式选择
        ttk.Label(ctrl_bar, text="模式:").pack(side=tk.LEFT)
        self.view_mode_combo = ttk.Combobox(ctrl_bar, width=8, state='readonly', 
                                           values=['简洁', '详细', '超详细'])
        self.view_mode_combo.set('简洁')
        self.view_mode_combo.bind('<<ComboboxSelected>>', lambda e: self.refresh_file_list())
        self.view_mode_combo.pack(side=tk.LEFT, padx=(2, 8))

        # 排序选择
        ttk.Label(ctrl_bar, text="排序:").pack(side=tk.LEFT)
        self.sort_mode_combo = ttk.Combobox(ctrl_bar, width=10, state='readonly',
                                           values=['添加顺序', '名称 A-Z', '大小', '修改时间'])
        self.sort_mode_combo.set('添加顺序')
        self.sort_mode_combo.bind('<<ComboboxSelected>>', lambda e: self.refresh_file_list())
        self.sort_mode_combo.pack(side=tk.LEFT, padx=2)

        # 列表容器 (带滚动条)
        list_container = ttk.Frame(left_panel)
        list_container.grid(row=3, column=0, sticky='nsew', pady=(0, 8))
        list_container.rowconfigure(0, weight=1)
        list_container.columnconfigure(0, weight=1)
        
        # 保存原始文件队列用于搜索过滤
        self._filtered_indices = None  # None 表示未过滤
        
        scrollbar = ttk.Scrollbar(list_container)
        scrollbar.grid(row=0, column=1, sticky='ns')
        
        # selectmode=tk.EXTENDED 支持 Shift 和 Ctrl 多选
        self.file_listbox = tk.Listbox(
            list_container, yscrollcommand=scrollbar.set,
            selectmode=tk.EXTENDED, font=('Microsoft YaHei UI', 9),
            relief=tk.FLAT, highlightthickness=1
        )
        self.file_listbox.grid(row=0, column=0, sticky='nsew')
        scrollbar.config(command=self.file_listbox.yview)
        
        # --- [增强] 右键上下文菜单 ---
        self.file_context_menu = Menu(self.root, tearoff=0)
        # 菜单项将在显示时动态更新
        self.file_context_menu.add_command(label="打开文件", command=self.open_selected_files)
        self.file_context_menu.add_command(label="用编辑器打开", command=self.open_with_editor)
        self.file_context_menu.add_command(label="打开所在文件夹", command=self.open_selected_folder)
        self.file_context_menu.add_separator()
        self.file_context_menu.add_command(label="复制文件路径", command=self.copy_file_path)
        self.file_context_menu.add_command(label="复制文件名", command=self.copy_file_name)
        self.file_context_menu.add_separator()
        self.file_context_menu.add_command(label="从列表移除", command=self.remove_selected_files)
        self.file_context_menu.add_command(label="仅保留选中项", command=self.keep_only_selected)
        self.file_context_menu.add_separator()
        self.file_context_menu.add_command(label="全选", command=self.select_all_files)
        
        # 绑定右键事件 (兼容多平台)
        right_click_btn = '<Button-2>' if platform.system() == 'Darwin' else '<Button-3>'
        self.file_listbox.bind(right_click_btn, self.on_listbox_right_click)
        
        # 绑定Delete键删除选中项
        self.file_listbox.bind('<Delete>', lambda e: self.remove_selected_files())
        
        # 拖拽支持 (如果环境支持)
        if HAS_DND:
            try:
                self.file_listbox.drop_target_register(DND_FILES)
                self.file_listbox.dnd_bind('<<Drop>>', self.on_drop)
            except: pass
        
        # 底部操作按钮
        btn_frame = ttk.Frame(left_panel)
        btn_frame.grid(row=4, column=0, sticky='ew')
        ttk.Button(btn_frame, text="添加文件", command=self.add_files).pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)
        ttk.Button(btn_frame, text="添加文件夹", command=self.add_folder).pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)
        ttk.Button(btn_frame, text="清空列表", command=self.clear_files).pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)
        
        # 统计标签
        self.file_count_label = ttk.Label(left_panel, text="已选择: 0 个文件", font=('Microsoft YaHei UI', 9, 'bold'))
        self.file_count_label.grid(row=5, column=0, sticky='w', pady=(8, 0))
    
    def create_log_panel(self, parent):
        """创建日志面板"""
        right_panel = ttk.Frame(parent)
        right_panel.grid(row=0, column=1, sticky='nsew', padx=(5, 0))
        right_panel.rowconfigure(1, weight=1)
        right_panel.columnconfigure(0, weight=1)
        
        progress_frame = ttk.LabelFrame(right_panel, text=" 翻译进度 ", padding="8")
        progress_frame.grid(row=0, column=0, sticky='ew', pady=(0, 8))
        progress_frame.columnconfigure(0, weight=1)
        
        self.progress_bar = ttk.Progressbar(progress_frame, mode='determinate')
        self.progress_bar.grid(row=0, column=0, sticky='ew', pady=(0, 5))
        
        self.progress_label = ttk.Label(progress_frame, text="就绪")
        self.progress_label.grid(row=1, column=0, sticky='w')
        
        log_frame = ttk.LabelFrame(right_panel, text=" 运行日志 ", padding="8")
        log_frame.grid(row=1, column=0, sticky='nsew')
        log_frame.rowconfigure(0, weight=1)
        log_frame.columnconfigure(0, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            wrap=tk.WORD,
            font=('Consolas', 9)
        )
        self.log_text.grid(row=0, column=0, sticky='nsew', pady=(0, 8))
        
        self.log_text.tag_config("INFO", foreground="#333333")
        self.log_text.tag_config("SUCCESS", foreground="#008000", font=('Consolas', 9, 'bold'))
        self.log_text.tag_config("WARNING", foreground="#FF8C00", font=('Consolas', 9, 'bold'))
        self.log_text.tag_config("ERROR", foreground="#DC143C", font=('Consolas', 9, 'bold'))
        
        ttk.Button(log_frame, text="清空日志", command=self.clear_log).grid(row=1, column=0, sticky='ew')
    
    def create_bottom_bar(self):
        """创建底部控制栏"""
        bottom_frame = ttk.Frame(self.root, padding="10")
        bottom_frame.grid(row=3, column=0, sticky='ew', padx=5, pady=5)
        
        self.start_btn = ttk.Button(
            bottom_frame,
            text="开始翻译",
            command=self.start_translation,
            style='Accent.TButton',
            width=15
        )
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_btn = ttk.Button(
            bottom_frame,
            text="停止翻译",
            command=self.stop_translation,
            state=tk.DISABLED,
            width=15
        )
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        self.open_output_btn = ttk.Button(
            bottom_frame,
            text="打开输出目录",
            command=self.open_output_folder,
            state=tk.DISABLED,
            width=15
        )
        self.open_output_btn.pack(side=tk.LEFT, padx=5)
        
        ttk.Separator(bottom_frame, orient=tk.VERTICAL).pack(side=tk.LEFT, padx=10, fill=tk.Y)
        
        ttk.Button(bottom_frame, text="输出设置", command=lambda: self.show_settings(tab=0), 
                  width=12).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(bottom_frame, text="字段配置", command=self.show_field_config, 
                  width=12).pack(side=tk.LEFT, padx=5)
    
    # ==================== 事件处理 ====================
    
    def on_listbox_right_click(self, event):
        """右键点击列表"""
        try:
            # 如果点击在选中项之外，则选中当前点击项（单选）
            # 如果点击在已选中的多选范围内，则保持选择状态
            index = self.file_listbox.nearest(event.y)
            if index not in self.file_listbox.curselection():
                self.file_listbox.selection_clear(0, tk.END)
                self.file_listbox.selection_set(index)
                self.file_listbox.activate(index)
            
            selection = self.file_listbox.curselection()
            if selection:
                # 动态更新菜单标签以显示选中数量
                count = len(selection)
                if count == 1:
                    self.file_context_menu.entryconfigure(0, label="打开文件")
                    self.file_context_menu.entryconfigure(6, label="从列表移除")
                else:
                    self.file_context_menu.entryconfigure(0, label=f"打开 {count} 个文件")
                    self.file_context_menu.entryconfigure(6, label=f"从列表移除 ({count} 项)")
                
                self.file_context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.file_context_menu.grab_release()

    def _get_real_index(self, listbox_index: int) -> int:
        """将列表框索引转换为文件队列的实际索引"""
        if self._filtered_indices is not None and listbox_index < len(self._filtered_indices):
            return self._filtered_indices[listbox_index]
        return listbox_index
    
    def remove_selected_files(self):
        """移除选中的文件"""
        selection = list(self.file_listbox.curselection())
        
        # 转换为实际索引
        real_indices = [self._get_real_index(i) for i in selection]
        real_indices.sort(reverse=True)  # 从后往前删，避免索引偏移
        
        for idx in real_indices:
            if idx < len(self.file_queue):
                del self.file_queue[idx]
        
        # 刷新列表
        self.refresh_file_list()
        self.update_file_count()
    
    def open_selected_files(self):
        """打开选中的文件"""
        selection = self.file_listbox.curselection()
        for index in selection:
            real_idx = self._get_real_index(index)
            if real_idx < len(self.file_queue):
                path = self.file_queue[real_idx]
                if os.path.exists(path):
                    open_path_in_os(path)
    
    def open_selected_folder(self):
        """打开选中文件的文件夹"""
        selection = self.file_listbox.curselection()
        if selection:
            real_idx = self._get_real_index(selection[0])
            if real_idx < len(self.file_queue):
                path = self.file_queue[real_idx]
                folder = os.path.dirname(path)
                if os.path.exists(folder):
                    open_path_in_os(folder)

    def open_with_editor(self):
        """用系统默认编辑器打开选中的文件"""
        selection = self.file_listbox.curselection()
        if not selection:
            return
        
        # 只打开前几个文件，避免一次性打开太多
        max_open = 5
        opened = 0
        for index in selection:
            if opened >= max_open:
                remaining = len(selection) - opened
                if remaining > 0:
                    self.log_message(f"[INFO] 已打开 {max_open} 个文件，剩余 {remaining} 个未打开")
                break
            real_idx = self._get_real_index(index)
            if real_idx < len(self.file_queue):
                path = self.file_queue[real_idx]
                if os.path.exists(path):
                    try:
                        if platform.system() == 'Windows':
                            os.startfile(path, 'edit')
                        elif platform.system() == 'Darwin':
                            subprocess.call(['open', '-e', path])
                        else:
                            editors = ['xdg-open', 'gedit', 'kate', 'nano', 'vim']
                            for editor in editors:
                                try:
                                    subprocess.Popen([editor, path])
                                    break
                                except FileNotFoundError:
                                    continue
                        opened += 1
                    except Exception as e:
                        self.log_message(f"[WARNING] 无法用编辑器打开 {os.path.basename(path)}: {e}")

    def copy_file_path(self):
        """复制选中文件的路径到剪贴板"""
        selection = self.file_listbox.curselection()
        if not selection:
            return
        
        paths = []
        for index in selection:
            real_idx = self._get_real_index(index)
            if real_idx < len(self.file_queue):
                paths.append(self.file_queue[real_idx])
        
        if paths:
            text = '\n'.join(paths)
            self.root.clipboard_clear()
            self.root.clipboard_append(text)
            
            count = len(paths)
            if count == 1:
                self.log_message(f"[INFO] 已复制文件路径到剪贴板")
            else:
                self.log_message(f"[INFO] 已复制 {count} 个文件路径到剪贴板")

    def copy_file_name(self):
        """复制选中文件的名称到剪贴板"""
        selection = self.file_listbox.curselection()
        if not selection:
            return
        
        names = []
        for index in selection:
            real_idx = self._get_real_index(index)
            if real_idx < len(self.file_queue):
                names.append(os.path.basename(self.file_queue[real_idx]))
        
        if names:
            text = '\n'.join(names)
            self.root.clipboard_clear()
            self.root.clipboard_append(text)
            
            count = len(names)
            if count == 1:
                self.log_message(f"[INFO] 已复制文件名到剪贴板")
            else:
                self.log_message(f"[INFO] 已复制 {count} 个文件名到剪贴板")

    def keep_only_selected(self):
        """仅保留选中的文件，移除其他所有文件"""
        selection = self.file_listbox.curselection()
        if not selection:
            return
        
        # 获取选中的文件（转换为实际索引）
        selected_files = []
        for i in selection:
            real_idx = self._get_real_index(i)
            if real_idx < len(self.file_queue):
                selected_files.append(self.file_queue[real_idx])
        
        if not selected_files:
            return
        
        # 确认操作
        remove_count = len(self.file_queue) - len(selected_files)
        if remove_count > 0:
            if not messagebox.askyesno("确认", 
                                       f"确定要移除其他 {remove_count} 个文件，仅保留选中的 {len(selected_files)} 个文件吗？"):
                return
        
        # 更新文件队列并清除搜索
        self.file_queue = selected_files
        if hasattr(self, 'search_var'):
            self.search_var.set('')
        self.refresh_file_list()
        self.update_file_count()

    def select_all_files(self):
        """全选所有文件"""
        if self.file_queue:
            self.file_listbox.selection_set(0, tk.END)

    def on_search_changed(self):
        """搜索框内容变化时触发"""
        self.refresh_file_list()
    
    def clear_search(self):
        """清除搜索"""
        self.search_var.set('')
        self.search_entry.focus_set()
    
    def refresh_file_list(self):
        """刷新文件列表显示（根据当前显示模式、排序模式和搜索过滤）"""
        # 保存当前选中状态
        selection = list(self.file_listbox.curselection())
        
        # 获取排序模式
        sort_mode = self.sort_mode_combo.get() if hasattr(self, 'sort_mode_combo') else '添加顺序'
        
        # 对文件队列进行排序
        if sort_mode == '名称 A-Z':
            self.file_queue.sort(key=lambda x: os.path.basename(x).lower())
        elif sort_mode == '大小':
            self.file_queue.sort(key=lambda x: os.path.getsize(x) if os.path.exists(x) else 0, reverse=True)
        elif sort_mode == '修改时间':
            self.file_queue.sort(key=lambda x: os.path.getmtime(x) if os.path.exists(x) else 0, reverse=True)
        # '添加顺序' 保持原有顺序
        
        # 获取搜索关键词
        search_text = self.search_var.get().strip().lower() if hasattr(self, 'search_var') else ''
        
        # 获取显示模式
        view_mode = self.view_mode_combo.get() if hasattr(self, 'view_mode_combo') else '简洁'
        
        # 清空列表
        self.file_listbox.delete(0, tk.END)
        
        # 过滤和填充列表
        self._filtered_indices = []
        filtered_count = 0
        
        for idx, path in enumerate(self.file_queue):
            file_name = os.path.basename(path).lower()
            
            # 搜索过滤
            if search_text and search_text not in file_name and search_text not in path.lower():
                continue
            
            self._filtered_indices.append(idx)
            filtered_count += 1
            
            if view_mode == '简洁':
                display_text = os.path.basename(path)
            elif view_mode == '详细':
                parent = os.path.basename(os.path.dirname(path))
                display_text = f"{os.path.basename(path)}  ({parent})"
            else:  # 超详细
                display_text = path
            
            self.file_listbox.insert(tk.END, display_text)
        
        # 更新搜索结果提示
        if hasattr(self, 'search_result_label'):
            if search_text:
                self.search_result_label.config(text=f"找到 {filtered_count}/{len(self.file_queue)}")
            else:
                self.search_result_label.config(text="")
        
        self.update_file_count()

    def open_output_folder(self):
        """打开输出目录"""
        if self.last_output_folder and os.path.exists(self.last_output_folder):
            open_path_in_os(self.last_output_folder)
        else:
            messagebox.showinfo("提示", "尚未生成输出目录或目录不存在")

    def on_key_selected(self, event=None):
        """选择API Key"""
        index = self.key_combo.current()
        if index >= 0:
            keys = self.config_manager.get_api_keys()
            if index < len(keys):
                self.config_manager.set_current_key(keys[index]['id'])
                self.api_status_label.config(text="API已连接")
    
    def on_drop(self, event):
        """处理拖拽"""
        try:
            files = self.root.tk.splitlist(event.data)
            for file_path in files:
                file_path = file_path.strip('{}')
                self.add_path(file_path)
            self.update_file_count()
        except Exception as e:
            self.log_message(f"[ERROR] 拖拽处理失败: {e}")
    
    def update_file_count(self):
        """更新文件计数"""
        count = len(self.file_queue)
        self.file_count_label.config(text=f"已选择: {count} 个文件")
        self.file_count_status.config(text=f"文件: {count}")
    
    def add_path(self, path: str):
        """添加路径"""
        if os.path.isfile(path):
            if path.lower().endswith(('.yml', '.yaml')) and path not in self.file_queue:
                self.file_queue.append(path)
                self._add_file_to_listbox(path)
        elif os.path.isdir(path):
            temp_config = TranslationConfig()
            core = YamlTranslatorCore({'api_key': '', 'platform': 'deepseek'}, temp_config, 1)
            yaml_files = core.find_yaml_files(path)
            added = 0
            for f in yaml_files:
                if f not in self.file_queue:
                    self.file_queue.append(f)
                    self._add_file_to_listbox(f)
                    added += 1
            if added > 0:
                self.log_message(f"[INFO] 从文件夹添加了 {added} 个 YAML 文件")
    
    def _add_file_to_listbox(self, path: str):
        """根据当前显示模式添加文件到列表"""
        view_mode = self.view_mode_combo.get() if hasattr(self, 'view_mode_combo') else '简洁'
        
        if view_mode == '简洁':
            display_text = os.path.basename(path)
        elif view_mode == '详细':
            parent = os.path.basename(os.path.dirname(path))
            display_text = f"{os.path.basename(path)}  ({parent})"
        else:  # 超详细
            display_text = path
        
        self.file_listbox.insert(tk.END, display_text)
    
    def add_files(self):
        """添加文件"""
        files = filedialog.askopenfilenames(
            title="选择YAML文件",
            filetypes=[("YAML文件", "*.yml *.yaml"), ("所有文件", "*.*")]
        )
        for f in files:
            self.add_path(f)
        self.update_file_count()
    
    def add_folder(self):
        """添加文件夹"""
        folder = filedialog.askdirectory(title="选择文件夹")
        if folder:
            self.current_base_folder = folder
            self.add_path(folder)
            self.update_file_count()
    
    def clear_files(self):
        """清空文件列表"""
        self.file_queue.clear()
        self.file_listbox.delete(0, tk.END)
        self.update_file_count()
    
    def clear_log(self):
        """清空日志"""
        self.log_text.delete(1.0, tk.END)
    
    def log_message(self, message: str):
        """记录日志消息"""
        level = "INFO"
        if "[SUCCESS]" in message:
            level = "SUCCESS"
        elif "[WARNING]" in message:
            level = "WARNING"
        elif "[ERROR]" in message:
            level = "ERROR"
        
        self.log_text.insert(tk.END, message + "\n", level)
        self.log_text.see(tk.END)
    
    def update_progress(self, current: int, total: int, status: str = ""):
        """更新进度"""
        if total > 0:
            progress = (current / total) * 100
            self.progress_bar['value'] = progress
            self.progress_label.config(text=f"{status} ({current}/{total})")
        self.status_text.config(text=status if status else "处理中...")
    
    def start_translation(self):
        """开始翻译 - 先显示预览对话框"""
        if not self.file_queue:
            messagebox.showwarning("警告", "请先添加要翻译的文件")
            return
        
        current_key = self.config_manager.get_current_key()
        if not current_key:
            messagebox.showwarning("警告", "请先选择或配置 API Key")
            return
        
        # 显示翻译预览对话框
        TranslationPreviewDialog(
            self.root,
            self.file_queue.copy(),
            self.config_manager,
            on_confirm=self._do_start_translation
        )
    
    def _do_start_translation(self):
        """实际执行翻译"""
        current_key = self.config_manager.get_current_key()
        if not current_key:
            return
        
        with self.translation_lock:
            self.is_translating = True
        
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.open_output_btn.config(state=tk.DISABLED)
        self.status_text.config(text="翻译中...")
        
        api_config = {
            'platform': current_key.get('platform', 'deepseek'),
            'api_key': current_key['api_key'],
            'model': current_key.get('model', 'deepseek-chat'),
            'url': current_key.get('url', ''),
            'temperature': current_key.get('temperature', 0.3),
            'max_tokens': current_key.get('max_tokens', 1000),
            'custom_prompt': current_key.get('custom_prompt', DEFAULT_PROMPT),
            'max_retries': self.config_manager.config.get('max_retries', 3),
            'retry_delay': self.config_manager.config.get('retry_delay', 5)
        }
        
        translation_config = self.config_manager.get_translation_config()
        
        try:
            max_threads = int(self.thread_spin.get())
            max_threads = max(1, min(200, max_threads))
        except ValueError:
            max_threads = 4
        
        self.translator_core = YamlTranslatorCore(
            api_config, 
            translation_config, 
            max_threads,
            progress_callback=lambda c, t, s: self.root.after(0, lambda: self.update_progress(c, t, s)),
            log_callback=lambda msg: self.root.after(0, lambda: self.log_message(msg))
        )
        
        def run_translation():
            try:
                files = self.file_queue.copy()
                base_folder = self.current_base_folder
                if not base_folder and files:
                    base_folder = os.path.dirname(files[0])
                
                # 计算并保存输出目录以便打开
                output_folder = translation_config.output_folder
                if not output_folder:
                     # 如果是覆盖模式或未指定，默认取第一个文件的目录或translated子目录
                    if translation_config.output_mode == 'overwrite':
                        output_folder = os.path.dirname(files[0])
                    else:
                        output_folder = os.path.join(os.path.dirname(files[0]), 'translated')
                
                self.last_output_folder = output_folder
                self.last_report_file = None

                stats = self.translator_core.translate_files(files, base_folder)
                self.last_stats = stats
                
                # 收集输出文件列表
                self.last_output_files = []
                for file_path in files:
                    out_path = self.translator_core.get_output_path(file_path, base_folder)
                    if os.path.exists(out_path):
                        self.last_output_files.append(out_path)
                
                self.config_manager.add_history(stats, files)
                
                if self.config_manager.config.get('generate_report', True):
                    # 报告存放在输出目录
                    report_dir = output_folder
                    if not os.path.exists(report_dir):
                        try:
                            os.makedirs(report_dir)
                        except:
                            report_dir = os.path.dirname(files[0])
                            
                    report_path = os.path.join(
                        report_dir,
                        f"translation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
                    )
                    report_file = ReportGenerator.generate_html_report(
                        stats, 
                        self.translator_core.translation_records,
                        report_path, 
                        api_config
                    )
                    if report_file:
                        self.last_report_file = report_file
                        self.root.after(0, lambda: self.log_message(f"[INFO] 报告已生成: {report_file}"))
                
                self.root.after(0, lambda: self.on_translation_complete(show_dialog=True))
                
            except Exception as e:
                import traceback
                traceback.print_exc()
                self.root.after(0, lambda: self.log_message(f"[ERROR] 翻译过程出错: {e}"))
                self.root.after(0, lambda: self.on_translation_complete(show_dialog=False))
        
        thread = threading.Thread(target=run_translation, daemon=True)
        thread.start()
    
    def stop_translation(self):
        """停止翻译"""
        if self.translator_core:
            self.translator_core.stop()
        self.log_message("[WARNING] 用户停止翻译")
        self.on_translation_complete(show_dialog=False)
    
    def on_translation_complete(self, show_dialog: bool = False):
        """翻译完成回调"""
        with self.translation_lock:
            self.is_translating = False
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        
        # 启用打开输出目录按钮
        if self.last_output_folder and os.path.exists(self.last_output_folder):
             self.open_output_btn.config(state=tk.NORMAL)
             
        self.status_text.config(text="就绪")
        self.progress_label.config(text="完成")
        
        # 显示翻译完成对话框
        if show_dialog and self.last_stats:
            TranslationCompleteDialog(
                self.root,
                self.last_stats,
                self.last_output_folder,
                self.last_output_files,
                self.last_report_file
            )
    
    def load_settings(self):
        """加载设置"""
        keys = self.config_manager.get_api_keys()
        key_names = [k['name'] for k in keys]
        self.key_combo['values'] = key_names
        
        if keys:
            current_key = self.config_manager.get_current_key()
            if current_key:
                for i, k in enumerate(keys):
                    if k['id'] == current_key['id']:
                        self.key_combo.current(i)
                        self.api_status_label.config(text="API已连接")
                        break
            else:
                self.key_combo.current(0)
                self.config_manager.set_current_key(keys[0]['id'])
        
        self.thread_spin.set(self.config_manager.config.get('max_threads', 4))
    
    def apply_theme(self):
        """应用主题"""
        theme = self.config_manager.config.get('theme', 'light')
        # 主题应用逻辑可在此扩展
    
    def bind_shortcuts(self):
        """绑定快捷键"""
        self.root.bind('<Control-o>', lambda e: self.add_files())
        self.root.bind('<Control-O>', lambda e: self.add_files())
        self.root.bind('<Control-d>', lambda e: self.add_folder())
        self.root.bind('<Control-D>', lambda e: self.add_folder())
        self.root.bind('<Control-comma>', lambda e: self.show_settings())
    
    def show_key_manager(self):
        """显示Key管理器"""
        KeyManagerDialog(self.root, self.config_manager, self.load_settings)
    
    def show_field_config(self):
        """显示字段配置"""
        FieldConfigDialog(self.root, self.config_manager)
    
    def show_settings(self, tab=0):
        """显示设置"""
        SettingsDialog(self.root, self.config_manager, self.apply_theme, initial_tab=tab)
    
    def show_history(self):
        """显示历史记录"""
        HistoryDialog(self.root, self.config_manager)
    
    def show_help(self):
        """显示帮助"""
        help_window = tk.Toplevel(self.root)
        help_window.title("使用说明")
        help_window.geometry("500x400")
        help_window.transient(self.root)
        
        text = scrolledtext.ScrolledText(help_window, wrap=tk.WORD, font=('Microsoft YaHei UI', 10))
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        text.insert('1.0', APP_DESCRIPTION)
        text.config(state=tk.DISABLED)
    
    def show_about(self):
        """显示关于"""
        about_text = f"""{APP_TITLE}

版本: {VERSION}

{APP_DESCRIPTION}

© 2024 All Rights Reserved"""
        messagebox.showinfo("关于", about_text, parent=self.root)
    
    def export_config(self):
        """导出配置"""
        # 创建导出选项对话框
        export_dialog = tk.Toplevel(self.root)
        export_dialog.title("导出配置")
        export_dialog.geometry("400x200")
        export_dialog.transient(self.root)
        export_dialog.grab_set()
        
        ttk.Label(export_dialog, text="导出配置", 
                 font=('Microsoft YaHei UI', 11, 'bold'),
                 padding="15").pack(anchor=tk.W)
        
        content = ttk.Frame(export_dialog, padding="15")
        content.pack(fill=tk.BOTH, expand=True)
        
        include_keys_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(content, text="包含 API Keys（注意：这会暴露您的密钥）",
                       variable=include_keys_var).pack(anchor=tk.W, pady=5)
        
        ttk.Label(content, text="提示：导出的配置不包含翻译历史记录",
                 foreground='gray', font=('Microsoft YaHei UI', 8)).pack(anchor=tk.W, pady=5)
        
        def do_export():
            export_path = filedialog.asksaveasfilename(
                title="导出配置",
                defaultextension=".json",
                filetypes=[("JSON 文件", "*.json"), ("所有文件", "*.*")],
                initialfilename="translator_config_export.json",
                parent=export_dialog
            )
            
            if export_path:
                success, message = self.config_manager.export_config(
                    export_path, include_keys_var.get()
                )
                if success:
                    messagebox.showinfo("成功", message, parent=export_dialog)
                    export_dialog.destroy()
                else:
                    messagebox.showerror("错误", message, parent=export_dialog)
        
        btn_frame = ttk.Frame(export_dialog, padding="15")
        btn_frame.pack(fill=tk.X)
        
        ttk.Button(btn_frame, text="导出", command=do_export, width=12).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="取消", command=export_dialog.destroy, width=12).pack(side=tk.LEFT)
    
    def import_config(self):
        """导入配置"""
        import_path = filedialog.askopenfilename(
            title="导入配置",
            filetypes=[("JSON 文件", "*.json"), ("所有文件", "*.*")]
        )
        
        if not import_path:
            return
        
        # 创建导入选项对话框
        import_dialog = tk.Toplevel(self.root)
        import_dialog.title("导入配置")
        import_dialog.geometry("450x220")
        import_dialog.transient(self.root)
        import_dialog.grab_set()
        
        ttk.Label(import_dialog, text="导入配置", 
                 font=('Microsoft YaHei UI', 11, 'bold'),
                 padding="15").pack(anchor=tk.W)
        
        content = ttk.Frame(import_dialog, padding="15")
        content.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(content, text=f"文件: {os.path.basename(import_path)}",
                 font=('Microsoft YaHei UI', 9)).pack(anchor=tk.W, pady=5)
        
        merge_var = tk.BooleanVar(value=True)
        ttk.Radiobutton(content, text="合并模式（保留现有 API Keys，合并其他设置）",
                       variable=merge_var, value=True).pack(anchor=tk.W, pady=2)
        ttk.Radiobutton(content, text="覆盖模式（完全替换现有配置）",
                       variable=merge_var, value=False).pack(anchor=tk.W, pady=2)
        
        ttk.Label(content, text="推荐使用合并模式，以保留您的 API Keys",
                 foreground='gray', font=('Microsoft YaHei UI', 8)).pack(anchor=tk.W, pady=5)
        
        def do_import():
            success, message = self.config_manager.import_config(
                import_path, merge_var.get()
            )
            if success:
                messagebox.showinfo("成功", message, parent=import_dialog)
                import_dialog.destroy()
                # 重新加载设置
                self.load_settings()
                self.apply_theme()
            else:
                messagebox.showerror("错误", message, parent=import_dialog)
        
        btn_frame = ttk.Frame(import_dialog, padding="15")
        btn_frame.pack(fill=tk.X)
        
        ttk.Button(btn_frame, text="导入", command=do_import, width=12).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="取消", command=import_dialog.destroy, width=12).pack(side=tk.LEFT)
    
    def on_closing(self):
        """窗口关闭"""
        with self.translation_lock:
            if self.is_translating:
                if not messagebox.askyesno("确认", "翻译正在进行中，确定要退出吗？"):
                    return
                self.stop_translation()
        
        self.config_manager.save_config()
        self.root.destroy()


# ==================== 程序入口 ====================

def main():
    """程序主入口"""
    try:
        if HAS_DND and TkinterDnD is not None:
            root = TkinterDnD.Tk()
        else:
            root = tk.Tk()
        
        app = TranslatorGUI(root)
        
        # 检查 ruamel.yaml 是否可用
        if not HAS_RUAMEL:
            root.after(500, lambda: messagebox.showwarning(
                "YAML引擎警告",
                "未检测到 ruamel.yaml 库，已回退到 PyYAML。\n\n"
                "PyYAML 模式下注释和空行可能会丢失。\n\n"
                "建议安装 ruamel.yaml 以保留原始格式：\n"
                "pip install ruamel.yaml",
                parent=root
            ))
        
        root.mainloop()
        
    except Exception as e:
        import traceback
        error_msg = traceback.format_exc()
        print(f"程序启动失败:\n{error_msg}")
        
        try:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("启动错误", f"程序启动失败:\n{str(e)}\n\n详细信息已打印到控制台")
            root.destroy()
        except Exception:
            pass


if __name__ == "__main__":
    main()