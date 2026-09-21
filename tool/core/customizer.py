import os
import io
import base64
import re
from PIL import Image
from typing import Optional

class Customizer:
    @staticmethod
    def image_to_base64_data_uri(img_path: str, max_size: int = 128) -> str:
        """读取任意图片并转为高 DPI 优化的 PNG Base64 Data URI"""
        if not os.path.exists(img_path):
            raise FileNotFoundError(f"未找到图标图片: {img_path}")

        im = Image.open(img_path).convert('RGBA')
        # 保持比例缩放
        im.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
        buf = io.BytesIO()
        im.save(buf, format='PNG', optimize=True)
        b64 = base64.b64encode(buf.getvalue()).decode('utf-8')
        return f"data:image/png;base64,{b64}"

    @staticmethod
    def update_i18n_content(
        i18n_path: str,
        title_text: Optional[str] = None,
        icon_path: Optional[str] = None,
        enable_humor: Optional[bool] = None,
        enable_token_badge: Optional[bool] = None
    ) -> bool:
        """将用户自选的标题、图标以及特性开关注入进目标 i18n.js 文件"""
        if not os.path.exists(i18n_path):
            raise FileNotFoundError(f"未找到 i18n.js 字典文件: {i18n_path}")

        with open(i18n_path, 'r', encoding='utf-8') as f:
            code = f.read()

        # 更新幽默金句开关
        if enable_humor is not None:
            humor_val = "true" if enable_humor else "false"
            if "window.__ENABLE_HUMOR_QUOTES__" in code:
                code = re.sub(r'window\.__ENABLE_HUMOR_QUOTES__\s*=\s*(true|false);', f'window.__ENABLE_HUMOR_QUOTES__ = {humor_val};', code)
            else:
                code = code.replace("window.__ENABLE_CHINESE__ = true;", f"window.__ENABLE_CHINESE__ = true;\n    window.__ENABLE_HUMOR_QUOTES__ = {humor_val};")

        # 更新 Token 徽章开关
        if enable_token_badge is not None:
            token_val = "true" if enable_token_badge else "false"
            if "window.__ENABLE_TOKEN_BADGE__" in code:
                code = re.sub(r'window\.__ENABLE_TOKEN_BADGE__\s*=\s*(true|false);', f'window.__ENABLE_TOKEN_BADGE__ = {token_val};', code)
            else:
                code = code.replace("window.__ENABLE_CHINESE__ = true;", f"window.__ENABLE_CHINESE__ = true;\n    window.__ENABLE_TOKEN_BADGE__ = {token_val};")

        # 更新标题文本
        if title_text:
            title_text = title_text.strip()
            # 替换 EXACT_DICT 里的 Antigravity 映射
            code = re.sub(r'"Antigravity":\s*"[^"]*"', f'"Antigravity": "{title_text}"', code)
            # 替换 updateTitle 正则与替换项
            code = re.sub(
                r'document\.title\.replace\(/[^/]+/g,\s*"[^"]*"\);',
                f'document.title.replace(/Antigravity|谷歌正重力|谷歌重力反/g, "{title_text}");',
                code
            )

        # 更新图标 (安全替换，使用 lambda 防转义)
        if icon_path and os.path.exists(icon_path):
            data_uri = Customizer.image_to_base64_data_uri(icon_path)
            code = re.sub(r'const LOGO_ICON_BASE64 = "[^"]+";', lambda _: f'const LOGO_ICON_BASE64 = "{data_uri}";', code)

        with open(i18n_path, 'w', encoding='utf-8') as f:
            f.write(code)

        return True
