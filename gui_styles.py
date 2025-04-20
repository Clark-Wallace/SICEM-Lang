import tkinter as tk
from tkinter import ttk
from typing import Dict, Any

class ThemeConfig:
    # High contrast color palette
    COLORS = {
        'primary': '#0047AB',      # Cobalt blue - very visible
        'secondary': '#5D3FD3',    # Rich purple - distinct
        'accent': '#008B8B',       # Dark cyan - clear
        'highlight': '#CD7F32',    # Bronze - warm
        'white': '#FFFFFF',
        'background': '#F0F2F5',   # Light cool gray
        'card_bg': '#FFFFFF',      # Pure white
        'dark_gray': '#1F2937',    # Charcoal
        'success': '#2E8B57',      # Sea green
        'warning': '#CD853F',      # Peru brown
        'error': '#CD5C5C',        # Indian red
        'text_primary': '#000000', # Pure black for maximum contrast
        'text_secondary': '#1F2937' # Charcoal for secondary text
    }
    
    # Font configurations
    FONTS = {
        'title': ('SF Pro Display', 28, 'bold'),
        'subtitle': ('SF Pro Display', 20, 'bold'),
        'heading': ('SF Pro Display', 18, 'bold'),
        'body': ('SF Pro Text', 16, 'normal'),
        'small': ('SF Pro Text', 14, 'normal')
    }
    
    @classmethod
    def setup_theme(cls) -> None:
        """Configure the ttk theme with custom styles."""
        style = ttk.Style()
        
        # Configure main theme
        style.configure('.',
            background=cls.COLORS['background'],
            foreground=cls.COLORS['text_primary'],
            font=cls.FONTS['body']
        )
        
        # Custom button styles with strong contrast
        style.configure('Primary.TButton',
            background=cls.COLORS['primary'],
            foreground=cls.COLORS['white'],
            padding=(15, 8),
            font=(cls.FONTS['body'][0], cls.FONTS['body'][1], 'bold')
        )
        
        style.configure('Secondary.TButton',
            background=cls.COLORS['secondary'],
            foreground=cls.COLORS['white'],
            padding=(15, 8),
            font=(cls.FONTS['body'][0], cls.FONTS['body'][1], 'bold')
        )
        
        # Frame styles with white background
        style.configure('Card.TFrame',
            background=cls.COLORS['card_bg'],
            relief='solid',
            borderwidth=1
        )
        
        # Enhanced label styles with strong contrast
        style.configure('Title.TLabel',
            background=cls.COLORS['card_bg'],
            foreground=cls.COLORS['text_primary'],
            font=cls.FONTS['title'],
            padding=(10, 5)
        )
        
        style.configure('Subtitle.TLabel',
            background=cls.COLORS['card_bg'],
            foreground=cls.COLORS['text_primary'],
            font=cls.FONTS['subtitle'],
            padding=(8, 4)
        )
        
        # Status styles with enhanced visibility
        style.configure('Success.TLabel',
            background=cls.COLORS['card_bg'],
            foreground=cls.COLORS['success'],
            font=(cls.FONTS['body'][0], cls.FONTS['body'][1], 'bold'),
            padding=(5, 2)
        )
        
        style.configure('Warning.TLabel',
            background=cls.COLORS['card_bg'],
            foreground=cls.COLORS['warning'],
            font=(cls.FONTS['body'][0], cls.FONTS['body'][1], 'bold'),
            padding=(5, 2)
        )
        
        style.configure('Error.TLabel',
            background=cls.COLORS['card_bg'],
            foreground=cls.COLORS['error'],
            font=(cls.FONTS['body'][0], cls.FONTS['body'][1], 'bold'),
            padding=(5, 2)
        )
        
        # Configure the default theme
        style.theme_use('clam')
        
        # Enhanced button state mappings
        style.map('Primary.TButton',
            background=[
                ('active', cls.COLORS['accent']),
                ('pressed', cls.COLORS['primary'])
            ],
            foreground=[('active', cls.COLORS['white'])]
        )
        
        style.map('Secondary.TButton',
            background=[
                ('active', cls.COLORS['highlight']),
                ('pressed', cls.COLORS['secondary'])
            ],
            foreground=[('active', cls.COLORS['white'])]
        )

class StyledFrame(ttk.Frame):
    """A custom frame with enhanced styling."""
    def __init__(self, master, **kwargs):
        super().__init__(master, style='Card.TFrame', padding=10, **kwargs)
        
class StyledButton(ttk.Button):
    """A custom button with enhanced styling."""
    def __init__(self, master, text: str, style_type: str = 'Primary', **kwargs):
        super().__init__(
            master,
            text=text,
            style=f'{style_type}.TButton',
            **kwargs
        )
        
class StyledLabel(ttk.Label):
    """A custom label with enhanced styling."""
    def __init__(self, master, text: str, style_type: str = 'Title', **kwargs):
        super().__init__(
            master,
            text=text,
            style=f'{style_type}.TLabel',
            **kwargs
        )
        
class StatusLabel(ttk.Label):
    """A status label that changes color based on state."""
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.set_status('normal')
        
    def set_status(self, status: str, message: str = None) -> None:
        """Set the status and optionally update the message."""
        status_styles = {
            'success': 'Success.TLabel',
            'warning': 'Warning.TLabel',
            'error': 'Error.TLabel'
        }
        
        if message:
            self.configure(text=message)
            
        self.configure(style=status_styles.get(status, 'TLabel'))

class ScrollText(tk.Text):
    """A custom text widget with scrollbar."""
    def __init__(self, master, **kwargs):
        # Create a frame to hold the text and scrollbar
        self.frame = StyledFrame(master)
        
        # Create scrollbar
        self.scrollbar = ttk.Scrollbar(self.frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Configure text widget
        super().__init__(
            self.frame,
            yscrollcommand=self.scrollbar.set,
            wrap=tk.WORD,
            font=ThemeConfig.FONTS['body'],
            **kwargs
        )
        
        # Pack text widget
        super().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Configure scrollbar
        self.scrollbar.config(command=self.yview)
        
    def pack(self, **kwargs):
        """Pack the frame instead of the text widget."""
        self.frame.pack(**kwargs) 