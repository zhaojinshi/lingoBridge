import os
from PySide6.QtWidgets import (QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QPushButton,
                               QFrame, QGraphicsDropShadowEffect, QScrollArea, QWidget, QStyle)
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QColor, QIcon, QPixmap

class Ui_FloatingWindow:
    def setupUi(self, window):
        window.main_layout = QVBoxLayout()
        # 预留外边距给阴影效果
        window.main_layout.setContentsMargins(20, 20, 20, 20)
        
        window.container = QFrame()
        window.container.setObjectName("container")
        
        # 增加硬件级窗口阴影
        window.window_shadow = QGraphicsDropShadowEffect(window)
        window.window_shadow.setBlurRadius(36)
        window.window_shadow.setXOffset(0)
        window.window_shadow.setYOffset(12)
        window.window_shadow.setColor(QColor(0, 0, 0, 110))
        window.container.setGraphicsEffect(window.window_shadow)
        
        window.content_layout = QVBoxLayout()
        window.content_layout.setContentsMargins(16, 14, 16, 16)
        window.content_layout.setSpacing(14)

        # === 顶部拖拽把手与控制栏 ===
        window.header_layout = QHBoxLayout()
        window.header_layout.setContentsMargins(0, 0, 0, 0)
        
        window.brand_icon = QLabel()
        window.brand_icon.setFixedSize(22, 22)
        try:
            from core.config import ICON_PATH
            pixmap = QPixmap(str(ICON_PATH / "icon.ico"))
            window.brand_icon.setPixmap(pixmap.scaled(18, 18, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        except Exception:
            pass

        window.title_label = QLabel("lingoBridge")
        
        window.close_btn = QPushButton("×")
        window.close_btn.setFixedSize(24, 24)
        window.close_btn.setCursor(Qt.PointingHandCursor)
        window.close_btn.clicked.connect(window.hide)
        
        window.header_layout.addWidget(window.title_label)
        window.header_layout.addStretch()
        window.header_layout.addWidget(window.close_btn)

        # === 输入框 ===
        window.input_edit = QTextEdit()
        window.input_edit.setPlaceholderText("在此输入 / 双击 Ctrl+C 划词 / Alt+E 截图 / Alt+Q 唤起...")
        window.input_edit.setMaximumHeight(100)
        window.input_edit.setMinimumHeight(60)
        
        # === 快捷工具栏 (紧贴输入框下方) ===
        window.toolbar_layout = QHBoxLayout()
        window.toolbar_layout.setContentsMargins(2, 0, 2, 0)
        
        window.settings_btn = QPushButton("设置")
        window.settings_btn.setFixedSize(44, 28)
        window.settings_btn.setToolTip("设置中心")
        window.settings_btn.setCursor(Qt.PointingHandCursor)
        window.settings_btn.clicked.connect(window.show_settings)

        window.translate_btn = QPushButton("翻译  (Enter)")
        window.translate_btn.setFixedHeight(34)
        window.translate_btn.setCursor(Qt.PointingHandCursor)
        window.translate_btn.clicked.connect(window.on_translate_clicked)
        
        window.toolbar_layout.addWidget(window.settings_btn)
        window.toolbar_layout.addStretch()
        window.toolbar_layout.addWidget(window.translate_btn)

        # === 结果展示区域 ===
        from PySide6.QtWidgets import QAbstractScrollArea
        window.main_scroll = QScrollArea()
        window.main_scroll.setWidgetResizable(True)
        window.main_scroll.setFrameShape(QFrame.Shape.NoFrame)
        window.main_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        window.main_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        window.main_scroll.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        window.main_scroll.setAttribute(Qt.WA_TranslucentBackground)
        
        window.scroll_content = QFrame()
        window.scroll_content.setObjectName("scroll_content")
        window.scroll_layout = QVBoxLayout(window.scroll_content)
        window.scroll_layout.setContentsMargins(0, 2, 0, 4)
        window.scroll_layout.setSpacing(12)

        # 1. 豆包 AI 结果区域
        window.ai_title_lbl = QLabel("AI   Mimo AI")
        window.ai_result_lbl = QLabel()
        window.ai_result_lbl.setWordWrap(True)
        window.ai_result_lbl.setTextFormat(Qt.RichText)
        window.ai_result_lbl.setOpenExternalLinks(True)
        window.ai_result_lbl.setTextInteractionFlags(Qt.TextSelectableByMouse | Qt.LinksAccessibleByMouse)
        
        # 2. 谷歌翻译结果区域
        window.google_title_lbl = QLabel("G   谷歌翻译")
        window.google_result_lbl = QLabel()
        window.google_result_lbl.setWordWrap(True)
        window.google_result_lbl.setTextFormat(Qt.RichText)
        window.google_result_lbl.setOpenExternalLinks(True)
        window.google_result_lbl.setTextInteractionFlags(Qt.TextSelectableByMouse | Qt.LinksAccessibleByMouse)
        
        window.scroll_layout.addWidget(window.ai_title_lbl)
        window.scroll_layout.addWidget(window.ai_result_lbl)
        window.scroll_layout.addWidget(window.google_title_lbl)
        window.scroll_layout.addWidget(window.google_result_lbl)
        window.scroll_layout.addStretch()
        
        window.main_scroll.setWidget(window.scroll_content)

        # === 底部朗读按钮 (Status Bar) ===
        window.play_btn = QPushButton("朗读原文")
        window.play_btn.setFixedHeight(40)
        window.play_btn.setCursor(Qt.PointingHandCursor)
        window.play_btn.clicked.connect(window.play_audio)

        window.content_layout.addLayout(window.header_layout)
        window.content_layout.addWidget(window.input_edit)
        window.content_layout.addLayout(window.toolbar_layout)
        window.content_layout.addWidget(window.main_scroll)
        window.content_layout.addWidget(window.play_btn)
        
        window.container.setLayout(window.content_layout)
        window.main_layout.addWidget(window.container)
        window.setLayout(window.main_layout)

        window.hide_results()
        window.setFixedWidth(340)
        window.adjustSize()
        
        # === 弹窗淡入动画 ===
        window.fade_anim = QPropertyAnimation(window, b"windowOpacity")
        window.fade_anim.setDuration(150)
        window.fade_anim.setStartValue(0.0)
        window.fade_anim.setEndValue(1.0)
        window.fade_anim.setEasingCurve(QEasingCurve.OutQuad)

def apply_window_theme(window, theme_name):
    if theme_name == "light":
        bg_color = "rgba(247, 249, 255, 246)"
        border_color = "rgba(150, 166, 205, 105)"
        title_color = "#17233d"
        close_btn_color = "#69748c"
        input_bg = "rgba(255, 255, 255, 224)"
        input_text = "#19233a"
        input_border = "rgba(140, 158, 200, 120)"
        result_text = "#24314d"
        primary_bg = "#3157f6"
        primary_hover = "#2648db"
        selected_bg = "rgba(74, 103, 255, 22)"
        
        window.html_vars = {
            "card_bg": "rgba(74, 103, 255, 18)",
            "bubble_bg": "rgba(255,255,255,0.72)",
            "phonetic_bg": "rgba(49,87,246,0.09)",
            "phonetic_text": "#53617c",
            "divider": "rgba(85,105,150,0.13)",
            "ai_title": "#3157f6",
            "google_title": "#365fd8",
            "placeholder": "#8b95aa"
        }
        window.window_shadow.setColor(QColor(58, 77, 130, 70))
    else:
        bg_color = "rgba(14, 23, 29, 250)"
        border_color = "rgba(92, 129, 137, 105)"
        title_color = "#f2f7f6"
        close_btn_color = "#9aabad"
        input_bg = "rgba(18, 29, 35, 245)"
        input_text = "#f1f6f5"
        input_border = "rgba(111, 145, 151, 120)"
        result_text = "#e1e9e8"
        primary_bg = "#087f83"
        primary_hover = "#09979b"
        selected_bg = "rgba(28, 209, 203, 22)"
        
        window.html_vars = {
            "card_bg": "rgba(23, 193, 190, 18)",
            "bubble_bg": "rgba(18, 31, 37, 0.88)",
            "phonetic_bg": "rgba(28,209,203,0.12)",
            "phonetic_text": "#9ab7b7",
            "divider": "rgba(133,173,178,0.13)",
            "ai_title": "#20d2ce",
            "google_title": "#f0ad58",
            "placeholder": "#788b8d"
        }
        window.window_shadow.setColor(QColor(0, 0, 0, 145))

    window.container.setStyleSheet(f"""
        QFrame#container {{
            background-color: {bg_color};
            border: 1px solid {border_color};
            border-radius: 16px;
        }}
    """)
    
    window.title_label.setStyleSheet(f"color: {title_color}; font-family: 'Segoe UI', 'Microsoft YaHei'; font-size: 13px; font-weight: 600;")
    
    window.close_btn.setStyleSheet(f"""
        QPushButton {{
            background-color: transparent;
            color: {close_btn_color};
            border: none;
            font-size: 18px;
            font-weight: bold;
            padding-bottom: 2px;
        }}
        QPushButton:hover {{
            color: #ff4d4d;
        }}
    """)
    
    window.input_edit.setStyleSheet(f"""
        QTextEdit {{ 
            background-color: {input_bg}; 
            color: {input_text}; 
            border: 1px solid {input_border}; 
            border-radius: 9px; 
            font-family: 'Segoe UI', 'Microsoft YaHei'; 
            font-size: 15px; 
            padding: 12px; 
        }}
        QTextEdit:focus {{
            border: 1px solid {primary_bg};
        }}
    """)
    
    window.settings_btn.setStyleSheet(f"""
        QPushButton {{ background: transparent; color: {result_text}; border: 1px solid transparent; border-radius: 8px; padding: 5px; }}
        QPushButton:hover {{ background: {selected_bg}; border-color: {border_color}; }}
    """)
    
    window.translate_btn.setStyleSheet(f"""
        QPushButton {{
            background-color: {primary_bg};
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0 18px;
            font-family: 'Segoe UI', 'Microsoft YaHei';
            font-size: 13px;
            font-weight: bold;
        }}
        QPushButton:hover {{
            background-color: {primary_hover};
        }}
    """)

    window.ai_title_lbl.setStyleSheet(f"QLabel {{ color: {window.html_vars.get('ai_title')}; background: {selected_bg}; border-radius: 6px; font-family: 'Segoe UI', 'Microsoft YaHei'; font-size: 13px; font-weight: 650; padding: 5px 8px; }}")
    window.google_title_lbl.setStyleSheet(f"QLabel {{ color: {window.html_vars.get('google_title')}; background: {selected_bg}; border-radius: 6px; font-family: 'Segoe UI', 'Microsoft YaHei'; font-size: 13px; font-weight: 650; padding: 5px 8px; }}")
    
    bubble_bg = window.html_vars.get('bubble_bg')
    window.ai_result_lbl.setStyleSheet(f"QLabel {{ color: {result_text}; background: {bubble_bg}; border-radius: 9px; font-family: 'Segoe UI', 'Microsoft YaHei'; font-size: 14px; padding: 13px 14px; margin-bottom: 4px; line-height: 1.6; border: 1px solid {border_color}; }}")
    window.google_result_lbl.setStyleSheet(f"QLabel {{ color: {result_text}; background: {bubble_bg}; border-radius: 9px; font-family: 'Segoe UI', 'Microsoft YaHei'; font-size: 14px; padding: 13px 14px; line-height: 1.6; border: 1px solid {border_color}; }}")
    
    scroll_style = f"""
        QScrollArea {{
            background-color: transparent;
            border: none;
        }}
        QFrame#scroll_content {{
            background-color: transparent;
        }}
        QScrollBar:vertical {{
            border: none;
            background: transparent;
            width: 6px;
            margin: 0px;
        }}
        QScrollBar::handle:vertical {{
            background: rgba(120, 120, 120, 100);
            min-height: 20px;
            border-radius: 3px;
        }}
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            border: none;
            background: none;
        }}
        QScrollBar::handle:vertical:hover {{
            background: rgba(120, 120, 120, 180);
        }}
    """
    window.main_scroll.setStyleSheet(scroll_style)
    
    window.play_btn.setStyleSheet(f"""
        QPushButton {{
            background-color: {window.html_vars.get('card_bg')};
            color: {result_text};
            border: 1px solid {border_color};
            border-radius: 9px;
            font-family: 'Segoe UI', 'Microsoft YaHei';
            font-size: 13px;
            font-weight: 500;
        }}
        QPushButton:hover {{
            background-color: {bubble_bg};
        }}
    """)
